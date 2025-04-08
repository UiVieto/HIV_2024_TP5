def test_number_to_words(number_to_words):
    assert number_to_words(0) == "Zero"
    assert number_to_words(5) == "Five"
    assert number_to_words(13) == "Thirteen"
    assert number_to_words(18) == "Eighteen"
    assert number_to_words(20) == "Twenty"
    assert number_to_words(50) == "Fifty"
    assert number_to_words(25) == "Twenty Five"
    assert number_to_words(99) == "Ninety Nine"
    assert number_to_words(100) == "One Hundred"
    assert number_to_words(500) == "Five Hundred"
    assert number_to_words(123) == "One Hundred Twenty Three"
    assert number_to_words(999) == "Nine Hundred Ninety Nine"
    assert number_to_words(1000) == "One Thousand"
    assert number_to_words(1234) == "One Thousand Two Hundred Thirty Four"
    assert number_to_words(12345) == "Twelve Thousand Three Hundred Forty Five"  # Notice grouping
    assert number_to_words(1000000) == "One Million"
    assert number_to_words(1234567) == "One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven"
    assert number_to_words(1000000000) == "One Billion"
    assert number_to_words(123456789012) == "One Hundred Twenty Three Billion Four Hundred Fifty Six Million Seven Hundred Eighty Nine Thousand Twelve" # Example with billions and all groups
    assert number_to_words(1002003) == "One Million Two Thousand Three" # Test handling internal zeros
