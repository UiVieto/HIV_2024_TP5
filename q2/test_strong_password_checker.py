def test_strong_password_checker(strong_password_checker):
    assert strong_password_checker("a") == 5
    assert strong_password_checker("aA1") == 3
    assert strong_password_checker("1337C0d3") == 0
    assert strong_password_checker("aaaB1") == 1  # Needs one uppercase or digit
    assert strong_password_checker("bbaaaaaaaaaaaaaaacccccc") == 8  # Needs uppercase, digit, and repeating chars fixed
    assert strong_password_checker("..................!!!") == 7  # Needs lowercase, uppercase, and digit
    assert strong_password_checker("") == 6
    assert strong_password_checker("ABABABABABABABABABAB1") == 2  # Too long, needs repeating chars fixed
    assert strong_password_checker("abcdefghijklmnopqrstuvwxyz") == 3  # Needs digit, uppercase, and is too long.
    assert strong_password_checker("aaaa") == 2  # Replace 1 'a'
    assert strong_password_checker("aaaaa") == 2  # Replace 1 'a'
    assert strong_password_checker("aaaaaa") == 2  # Replace 2 'a's
    assert strong_password_checker("aaaaaaa") == 3  # Replace 2 'a's
    assert strong_password_checker("aaaaaaaa") == 3 # Replace 2 'a's
    assert strong_password_checker("aaaaaaaaa") == 3  # Replace 3 'a's
    assert strong_password_checker("A1") == 4  # Too short, missing lowercase
    assert strong_password_checker("aA12345678901234567890") == 6 # Too long
    assert strong_password_checker("1111111111") == 3 # Repeating characters and missing alpha
    assert strong_password_checker("aaaaaaaaaa1") == 3 # Repeating characters and missing uppercase
    assert strong_password_checker("AAAAAaaaaa") == 2 # Missing digit
    assert strong_password_checker("AAAAA11111") == 2 # Missing lowercase
