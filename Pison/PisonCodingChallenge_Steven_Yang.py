import json
with open('boggle.json', 'r') as f:
    data = json.load(f)

# jason parser

start = -(3//2)
end = 3//2+1
deltas = []
for i in range(start, end):
    for j in range(start, end):
        deltas.append((i, j))

# possible moves is a 3x3 focusing and deltas of +-1 from 0,0 as the middle


def neighbors(x, y, board):
    length = len(board)
    valid = []
    for i, j in deltas:
        if i == 0 and j == 0:
            continue
        if x+i > length-1 or y+j > length-1 or x+i < 0 or y+j < 0:
            continue
        else:
            valid.append((x+i, y+j))

    return valid

# makes sure we only consider indices in the board


initial = {"valid": False}

# initialize trie as a nested dictionary


def make_trie(word, trie):
    if not word:
        return None

    if word[0] not in trie:
        trie[word[0]] = {"valid": len(word) == 1}

    return make_trie(word[1:], trie[word[0]])

# make trie recursively, once we hit the end of a word, flag it is a valid word in the dictionary given


def gen_trie(words):
    for word in words:
        make_trie(word, initial)
    return initial

# generate trie for all words in dictionary


def dfs(x, y, visited, current, trie, board):
    if (x, y) in visited:
        return None

    letter = board[x][y]
    visited.add((x, y))

    if letter in trie:
        current += letter
        if trie[letter]["valid"]:
            print("Valid word: ", current)

        for new_x, new_y in neighbors(x, y, board):
            dfs(new_x, new_y, visited.copy(), current, trie[letter], board)


# DFS to check on the trie to save time, run on every letter on the board and see if prefixes match


def solution(trie, board):
    length = len(board)
    for i in range(length):
        for j in range(length):
            dfs(i, j, set(), '', trie, board)


if __name__ == '__main__':
    words = data["dictionary"]
    board = data["board"]
    solution(gen_trie(words), board)





