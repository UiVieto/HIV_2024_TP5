import importlib
import random
import string
import inspect
import re

import matplotlib.pyplot as plt

import google.generativeai as genai

from common.llm_test_generator import LLMTestGenerator
from common.prompt_generator import PromptGenerator
from common.abstract_executor import AbstractExecutor

from to_test.number_to_words import number_to_words
from to_test.strong_password_checker import strong_password_checker


KEY = "AIzaSyDTcdlS7_IdLM_0miPUP4EmAgqKLD3ZrTA"
BUDGET = 99


def generate_inital_tests_with_llm(model, function_to_test):
    # Create an LLMTestGenerator object with the generative model and the function to test
    llm_generator = LLMTestGenerator(model, function=function_to_test)

    # Create a PromptGenerator object with the function to test
    prompt_generator = PromptGenerator(function_to_test)

    # Generate a prompt for the function
    prompt = prompt_generator.generate_prompt()

    # Print the prompt
    #print(prompt)

    # Create a test function using the LLMTestGenerator
    test, test_name = llm_generator.create_test_function(prompt)

    print("Tests produced by LLM:")

    print(test)

    # Define the filename for the generated test file
    filename = f"test_{function_to_test.__name__}.py"

    # Write the test function to the file
    llm_generator.write_test_to_file(test, filename=filename)

    # Get the module name and function name from the filename
    module_name = filename.split(".")[0]
    function_name = test_name

    # Import the module dynamically
    module = importlib.import_module(module_name)

    # Get the function from the module
    function = getattr(module, function_name)

    executor = AbstractExecutor(function)

    # Execute the input function and get the coverage date
    coverage_data = executor._execute_input(input=function_to_test)

    # Print the coverage date
    return function, coverage_data

def parse_test(test_function, input_type: str=None) -> list:
    lines = inspect.getsourcelines(test_function)[0]
    lines = [line.rstrip('\n') for line in lines]
    
    inputs = []

    for line in lines:
        if 'assert' in line:
            value = re.search(r'\((.*?)\)', line).group(1)
            
            if input_type == 'int':
                try:
                    inputs.append(int(value))
                except Exception:
                    print(f"Warning: invalid test value, '{value}' given")
            else:
                try:
                    value = value.replace("'", '')
                    value = value.replace('"', '')
                    inputs.append(value)
                except Exception:
                    print(f"Warning: invalid test value, '{value}' given")
    
    return inputs

def get_score(inputs: list[int], coverage: dict) -> tuple[int, int]:
    return coverage['covered_lines'] + coverage['covered_branches'], -len(inputs)

def generate_number() -> int:
    return random.randint(1, 100) * random.randint(1, 100)

def generate_password() -> str:
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits

    return ''.join(random.choice(chars) for _ in range(random.randint(4, 40)))

def greedy_search(inputs: list, executor: AbstractExecutor, key=None) -> tuple[list, dict, int]:
    temp_inputs = inputs.copy()
    temp_inputs.sort(key=key)

    input = [temp_inputs.pop()]
    coverage = executor._execute_input(input_list=input)
    score = get_score(input, coverage['coverage'])

    best_inputs = input, coverage, score

    n = 1
    while len(temp_inputs) > 0:
        if n >= BUDGET:
            break

        input = best_inputs[0] + [temp_inputs.pop()]
        coverage = executor._execute_input(input_list=input)
        score = get_score(input, coverage['coverage'])

        if score > best_inputs[2]:
            best_inputs = input, coverage, score

        n += 1

    return best_inputs, n

def local_search(best: tuple, executor: AbstractExecutor, generator, budget: int):
    best_inputs, best_coverage, best_score = best
    
    for _ in range(budget):
        if random.randint(0, 1) == 0:
            input: list = best_inputs.copy()
            input[random.randint(0, len(input) - 1)] = generator()
            coverage = executor._execute_input(input_list=input)
            score = get_score(input, coverage['coverage'])

            if score >= best_score:
                best_inputs = input
                best_coverage = coverage
                best_score = score
        else:
            input: list = best_inputs.copy()
            removed_value = input.pop(random.randint(0, len(input) - 1))
            coverage = executor._execute_input(input_list=input)
            score = get_score(input, coverage['coverage'])

            if score >= best_score:
                best_inputs = input
                best_coverage = coverage
                best_score = score
            else:
                input.append(removed_value)

    return best_inputs, best_coverage


def number_optimize(initial_inputs: list[int], initial_coverage: dict, executor: AbstractExecutor) -> list[int]:
    (inputs, coverage, score), n = greedy_search(initial_inputs, executor)

    if score > get_score(initial_inputs, initial_coverage['coverage']):
        best_inputs = inputs, coverage
    else:
        best_inputs = initial_inputs, initial_coverage['coverage']

    best_inputs = local_search((inputs, coverage, score), executor, generate_number, BUDGET - n)

    return best_inputs

def password_optimize(initial_inputs: list[int], initial_coverage: dict, executor: AbstractExecutor) -> list[int]:
    (inputs, coverage, score), n = greedy_search(initial_inputs, executor, lambda x: (len(x), x))

    if score > get_score(initial_inputs, initial_coverage['coverage']):
        best_inputs = inputs, coverage
    else:
        best_inputs = initial_inputs, initial_coverage['coverage']

    best_inputs = local_search((inputs, coverage, score), executor, generate_password, BUDGET - n)

    return best_inputs


if __name__ == "__main__":
    # Configure the generative AI with the API key
    genai.configure(api_key=KEY)

    # Create a generative model
    model = genai.GenerativeModel('gemini-1.5-pro')

    ######Generate intial tests with LLM
    test, coverage_data = generate_inital_tests_with_llm(model, number_to_words)
    number_to_words_inputs = parse_test(test, 'int')

    test, coverage_data = generate_inital_tests_with_llm(model, strong_password_checker)
    strong_password_checker_inputs = parse_test(test)

    print(strong_password_checker_inputs)

    try:
        """
        TODO:
        -Insert your code here to improve the initial line and branch coverage
        -Use the "test" returned from the generate_inital_tests_with_llm function to start your generation
        -You can leverage the information about the datatype from the inputs in "test" generated by the LLM
        -You must use the "executor" to evaluate your tests and guide the generation process
        -Your test generator shoud return a list with new inputs to be evaluated
        -You goal is to keep the number of inputs as small as possible and the coverage as high as possible
        """
        # number_to_words test generation
        print('------------------------number_to_words---------------------------')
        scores = []

        executor = AbstractExecutor(number_to_words)
        initial_coverage = executor._execute_input(input_list=number_to_words_inputs)
        print(f"Initial coverage: {initial_coverage['coverage']}")
        print(f"Initial test values: {number_to_words_inputs}")
        print()

        best_inputs = number_to_words_inputs
        best_score = get_score(number_to_words_inputs, initial_coverage['coverage'])
        
        for i in range(5):
            print(f'------------------Run {i+1}------------------')
            result, final_coverage = number_optimize(number_to_words_inputs, initial_coverage, executor)
            print(f"Final coverage: {final_coverage['coverage']}")
            print(f"Test values: {result}")
            print()

            line_coverage_improment = final_coverage["coverage"]["percent_covered"] - initial_coverage["coverage"]["percent_covered"]
            branch_coverage_improment = final_coverage["coverage"]["covered_branches"]/final_coverage["coverage"]["num_branches"] - initial_coverage["coverage"]["covered_branches"]/initial_coverage["coverage"]["num_branches"]
            total_tests = len(result)
            final_score = (line_coverage_improment + branch_coverage_improment) / total_tests
            print(f"Final score: {final_score}")
            print()

            score = get_score(result, final_coverage['coverage'])
            if score > best_score:
                best_inputs = result
                best_score = score

            scores.append(final_score)

        print("Best inputs:", best_inputs)

        plt.boxplot(scores)
        plt.title("Distribution des scores pour number_to_words")
        plt.show()

        # strong_password_checker test generation
        print('-------------------strong_password_checker------------------------')
        scores = []
        best_inputs = strong_password_checker_inputs
        best_score = get_score(number_to_words_inputs, initial_coverage['coverage'])

        executor = AbstractExecutor(strong_password_checker)
        initial_coverage = executor._execute_input(input_list=strong_password_checker_inputs)
        print(f"Initial coverage: {initial_coverage['coverage']}")
        print(f"Initial test values: {number_to_words_inputs}")
        print()

        for i in range(5):
            print(f'------------------Run {i+1}------------------')
            result, final_coverage = password_optimize(strong_password_checker_inputs, initial_coverage, executor)
            print(f"Final coverage: {final_coverage['coverage']}")
            print(f"Test values: {result}")
            print()

            line_coverage_improment = final_coverage["coverage"]["percent_covered"] - initial_coverage["coverage"]["percent_covered"]
            branch_coverage_improment = final_coverage["coverage"]["covered_branches"]/final_coverage["coverage"]["num_branches"] - initial_coverage["coverage"]["covered_branches"]/initial_coverage["coverage"]["num_branches"]
            total_tests = len(result)
            final_score = (line_coverage_improment + branch_coverage_improment) / total_tests
            print(f"Final score: {final_score}")
            print()

            scores.append(final_score)

            score = get_score(result, final_coverage['coverage'])
            if score > best_score:
                best_inputs = result
                best_score = score

        print("Best inputs:", best_inputs)

        plt.boxplot(scores)
        plt.title("Distribution des scores pour strong_password_checker")
        plt.show()

    except Exception as e:
        print(f"Exception occured: {e}")
