def test_strong_password_checker(strong_password_checker):
    assert strong_password_checker("a") == 5
    assert strong_password_checker("aA1") == 3
    assert strong_password_checker("1337C0d3") == 0
    assert strong_password_checker("aaaB1") == 3  # Needs uppercase and repeating chars fixed
    assert strong_password_checker("bbaaaaaaaaaaaaaaacccccc") == 8 # Long with repeats
    assert strong_password_checker("A1234567890aaabbbbccccc") == 3 # Needs one more type and repeating chars fixed
    assert strong_password_checker("") == 6
    assert strong_password_checker("ABABABABABABABABABAB1") == 2  # Long, needs lowercase
    assert strong_password_checker("abcdefghijklmnopqrstuvwxyz") == 3  # Needs digit and uppercase and is too long
    assert strong_password_checker("aaaaaaaaaa") == 6  # Short and repeating
    assert strong_password_checker("aaaaaaaaaaaaaaaaaaaaa") == 7 # Long and repeating
    assert strong_password_checker("aaaaaa") == 2 # Repeating
    assert strong_password_checker("aaaa") == 2 # Short and repeating
    assert strong_password_checker("111111") == 2 # Needs lowercase and uppercase
    assert strong_password_checker("aaaaaaaa") == 2 # Needs uppercase and digit
    assert strong_password_checker("AAAAAAAA") == 2 # Needs lowercase and digit
    assert strong_password_checker("12345") == 1 # Too short
    assert strong_password_checker("123456789012345678901") == 1  # Too long
    assert strong_password_checker("1Aa") == 3
    assert strong_password_checker("1111111aA") == 3
