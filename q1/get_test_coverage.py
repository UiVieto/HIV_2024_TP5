import sys
sys.path.append('..')

import google.generativeai as genai
from common.llm_test_generator import LLMTestGenerator
from common.prompt_generator import PromptGenerator
from common.abstract_executor import AbstractExecutor
from file_name_check import file_name_check
import importlib

function_to_test = file_name_check

# Define the filename for the generated test file
filename = "test_generated.py"

# Get the module name and function name from the filename
module_name = filename.split(".")[0]
function_name = 'test_file_name_check'

# Import the module dynamically
module = importlib.import_module(module_name)

# Get the function from the module
function = getattr(module, function_name)


executor2 = AbstractExecutor(function)

# Execute the input function and get the coverage date
coverage_data = executor2._execute_input(function_to_test)

# Print the coverage date
print("Coverage data:")
print(coverage_data)
