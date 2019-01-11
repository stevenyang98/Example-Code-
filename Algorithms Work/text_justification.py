def badness(width, s):
    if s > width:
        b = s-width
    else:
        b = float('inf')
    return b**3


def get_badness(words, width, S):
    w = len(width)+1
    length = [[0]*w for i in range(w)]
    bad = [[0]*w for i in range(w)]

    for i in range(1,w):  # have to index at zero if doing prefixes
        length[i][i] = width[i-1]
        bad[i][i] = badness(width[i-1],S)

    for i in range(1,w):
        for j in range(i+1,w):
            length[i][j] = length[i][j-1] + width[j-1]  # calculating word lengths
            bad[i][j] = badness(length[i][j], S)

    x = [float('inf') for i in range(w)]
    x[0] = 0
    p = [None for i in range(w)]
    for i in range(1,w):
        for j in range(i+1):
            if j == 0:
                continue
            temp = bad[j][i] + x[j-1]
            if x[i] > temp:
                x[i] = temp
                p[i] = j-1,i
    n = w-1
    p[0] = (None, 0)
    sequence = []
    while n is not None:
        sequence.append(p[n])
        n = p[n][0]

    sequence.pop()
    sequence.reverse()
    text = ''
    for i,j in sequence:
        text += ' '.join(words[i:j])+"\n"
    return text


Words = ["Steven","Yang","likes","to","code"]
Width = [6,4,5,2,4]
S = 14
print(get_badness(Words, Width, S))
