Words = ["TEST", "STRUM", "BUM", "STRUT", "SUITE", "STOP"]
Board = [["I","E","K"], ["T","U","T"], ["S","R","M"]]

length = len(Board)

start = -(3//2)
end = 3//2+1
deltas = []
for i in range(start, end):
    for j in range(start, end):
        deltas.append((i, j))


def neighbors(x, y):
    valid = []
    for i, j in deltas:
        if i == 0 and j == 0:
            continue
        if x+i > length-1 or y+j > length-1 or x+i < 0 or y+j < 0:
            continue
        else:
            valid.append((x+i, y+j))

    return valid


initial = {"valid": False}


def make_trie(word, trie):
    if not word:
        return None

    if word[0] not in trie:
        trie[word[0]] = {"valid": len(word) == 1}

    return make_trie(word[1:], trie[word[0]])


def gen_trie(words):
    for word in words:
        make_trie(word, initial)
    return initial


solutions = set()


def dfs(x, y, visited, current, trie):
    if (x, y) in visited:
        return None

    letter = Board[x][y]
    visited.add((x, y))

    if letter in trie:
        current += letter
        if trie[letter]["valid"]:
            print("Valid word: ", current)
            solutions.add(current)

        for new_x, new_y in neighbors(x, y):
            dfs(new_x, new_y, visited.copy(), current, trie[letter])


def solution(trie):
    for i in range(length):
        for j in range(length):
            dfs(i, j, set(), '', trie)
    return solutions


print(solution(gen_trie(Words)))





