def first_recurring_character(string):
    seen = list()
    for character in string:
        if character in seen:
            return character
        else:
            seen.append(character)


test_string = 'MyBrainIsTheBestBrain!'
print(first_recurring_character(test_string))
