phoneNumber = '3662277'
words = ['foo', 'bar', 'baz', 'foobar', 'emo', 'cap', 'car', 'cat']

def solve(phoneNumber, words):
    map = {'abc': '2', 'def': '3', 'ghi': '4', 'jkl': '5', 'mno': '6', 'pqrs': '7', 'tuv': '8', 'wxyz': '9'}
    wordsInDigits = []
    for word in words:
        wordInDigits = []
        for letter in word:
            for key in map.keys():
                if letter in key:
                    wordInDigits.append(map[key])
                    break
        wordInDigits = ''.join(wordInDigits)
        wordsInDigits.append(wordInDigits)
    out = []
    for i, word in enumerate(wordsInDigits):
        if word in phoneNumber:
            out.append(words[i])
    return out


print(solve(phoneNumber, words))
