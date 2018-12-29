def decode_message(A):
    """
    Return the first half of the longest palindrome subsequence of string A
    """
    a = len(A)
    x = [[0 for letter in A] for char in A]
    for i in range(a):
        x[i][i] = A[i] #covers base case where i = j, palindrome of string length one is one no matter what
    #variable character length (char_len)
    for char_len in range(2,a+1): #choosing different character length
        for i in range(a-char_len+1):
            j = i+char_len-1
            if A[i] == A[j] and char_len == 2:
                x[i][j] = A[i]+A[j]
            elif A[i] == A[j]:
                x[i][j] = A[i]+x[i+1][j-1]#+A[j]
            else:
                x[i][j] = max(x[i][j-1],x[i+1][j],key=len)
    longest = x[0][a-1]
    #l = len(longest)
    return longest#[:l//2+1]






