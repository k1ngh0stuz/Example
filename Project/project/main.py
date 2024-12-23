def find_min_word(crossword):

    R, C = len(crossword), len(crossword[0])

    def extract_words(line):
        return [word for word in line.split('#') if len(word) >= 2]

    words = []

    for row in crossword:
        words.extend(extract_words(row))

    for col in range(C):
        column = ''.join(crossword[row][col] for row in range(R))
        words.extend(extract_words(column))

    return min(words)

R, C = map(int, input().split())
crossword = [input().strip() for _ in range(R)]

print(find_min_word(crossword))

