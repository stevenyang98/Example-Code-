# Problem Set 4B
# Name: Steven Yang
# Collaborators: Mike Carolan
# Time Spent: 4:35
# Late Days Used: 1 

import string


### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, input_text):
        '''
        Initializes a Message object
                
        input_text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = input_text 
        self.valid_words = load_words(WORDLIST_FILENAME) #feed in argument into load_words()

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words[:] #shallow copy
        

    def make_shift_dicts(self, input_shifts):
        '''
        Creates a list of dictionaries; each dictionary can be used to apply a
        cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. By shifted down, we mean 
        that if 'a' is shifted down by 2, the result is 'c.'

        The dictionary should have 52 keys of all the uppercase letters and
        all the lowercase letters only.
        input_shifts (list of integer): the amount by which to shift every letter of the
        alphabet. 0 <= shift < 26

        Returns: a list of dictionaries mapping letter (string) to
                 another letter (string).
        '''
        first_dictionary = {} #first dictionary for odd letters
        second_dictionary = {} #second dictionary for even letters
        lower_case = 'abcdefghijklmnopqrstuvwxyz'
        upper_case = 'abcdefghijklmnopqrstuvwxyz'.upper()
        
        for letters in lower_case:
            index = lower_case.index(letters) #make the i into an int essentially  
            first_dictionary[letters] = lower_case[(index + input_shifts[0])%26] #the % accounts for cycling through alphabet
            second_dictionary[letters] = lower_case[(index + input_shifts[1])%26]
        for letter in upper_case:
            index = upper_case.index(letter) #make the i into an int essentially 
            first_dictionary[letter] = upper_case[(index + input_shifts[0])%26] #the % accounts for cycling through alphabet
            second_dictionary[letter] = upper_case[(index + input_shifts[1])%26]
        return [first_dictionary, second_dictionary]
        
        

    def apply_shifts(self, shift_dicts):
        '''
        Applies the Caesar Cipher to self.message_text with letter shifts 
        specified in shift_dicts. Creates a new string that is self.message_text, 
        shifted down the alphabet by some number of characters, determined by 
        the shift value that shift_dicts was built with.       
        
        shift_dicts: list of dictionaries; each dictionary with 52 keys, mapping
            lowercase and uppercase letters to their new letters
            (as built by make_shift_dicts)

        Returns: the message text (string) with every letter shifted using the
            input shift_dicts 

        '''
        lower_case = 'abcdefghijklmnopqrstuvwxyz'
        upper_case = 'abcdefghijklmnopqrstuvwxyz'.upper()
        shifted_string =""
        for char in range(len(self.message_text)):
            letter = self.message_text[char] #just calling the value at the index
            if letter in lower_case or letter in upper_case: #no spaces
                if char % 2 == 0: #if it's an even index, odd letter
                    if letter in shift_dicts[0]:
                        shifted_string +=shift_dicts[0][letter]#get value from the key in shift dicts
                else:
                    if letter in shift_dicts[1]:
                        shifted_string +=shift_dicts[1][letter]
            else:
                letter = self.message_text[char]
                shifted_string += letter #essentially do nothing
        return shifted_string
                    
                    
                
       
                


class PlaintextMessage(Message):
    def __init__(self, input_text, input_shifts):
        '''
        Initializes a PlaintextMessage object.       
        
        input_text (string): the message's text
        input_shifts (list of integers): the list of shifts associated with this message

        A PlaintextMessage object inherits from Message. It has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shifts (list of integers, determined by input shifts)
            self.encryption_dicts (list of dictionaries, built using shifts)
            self.encrypted_message_text (string, encrypted using self.encryption_dict)

        '''
        Message.__init__(self, input_text) #call message constructor
        self.shifts = input_shifts #unique to subclass
        self.encryption_dicts = self.make_shift_dicts(input_shifts) #call previous method
        self.encrypted_message_text = self.apply_shifts(self.encryption_dicts) #call previous method

    def get_shifts(self):
        '''
        Used to safely access self.shifts outside of the class
        
        Returns: self.shifts
        '''
        return self.shifts 

    def get_encryption_dicts(self):
        '''
        Used to safely access a copy self.encryption_dicts outside of the class
        
        Returns: a COPY of self.encryption_dicts
        '''
        empty_list = [] #new list to append to 
        for i in self.encryption_dicts: #iterate through the original list:
            empty_list.append(i.copy()) #make copy of each dictionary
        return empty_list

    def get_encrypted_message_text(self):
        '''
        Used to safely access self.encrypted_message_text outside of the class
        
        Returns: self.encrypted_message_text
        '''
        return self.encrypted_message_text 

    def modify_shifts(self, input_shifts):
        '''
        Changes self.shifts of the PlaintextMessage, and updates any other 
        attributes that are determined by the shift list.        
        
        input_shifts (list of length 2): the new shift that should be associated with this message.
        [0 <= shift < 26]

        Returns: nothing
        '''
        self.shifts = input_shifts
        self.encryption_dicts = self.make_shift_dicts(input_shifts) #call previous method
        self.encrypted_message_text = self.apply_shifts(self.encryption_dicts) #call previous method


class CiphertextMessage(Message):
    def __init__(self, input_text):
        '''
        Initializes a CiphertextMessage object
                
        input_text (string): the message's text
        
        a CiphertextMessage object inherits from Message. It has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, input_text) #both are inherited from message constructor

    def decrypt_message(self):
        '''
        Decrypts self.message_text by trying every possible combination of shift
        values and finding the "best" one. 
        We will define "best" as the list of shifts that creates the maximum number
        of valid English words when we use apply_shifts(shifts)on the message text. 
        If [a, b] are the original shift values used to encrypt the message, then we 
        would expect [(26 - a), (26 - b)] to be the best shift values for
        decrypting it.

        Note: if multiple lists of shifts are equally good, such that they all create 
        the maximum number of valid words, you may choose any of those lists
        (and their corresponding decrypted messages) to return.

        Returns: a tuple of the best shift value list used to decrypt the message
        and the decrypted message text using that shift value
        '''
        maximum = 0 #what I want
        count= 0
        best = [0,0] #placeholder
        for a in range(26):
            for b in range(26): #find 26^2 combinations
                count = 0 #reinitialize after going thru
                dicts = self.make_shift_dicts([26-a,26-b]) #call previous method
                decrypted = self.apply_shifts(dicts)
                decrypted_list = decrypted.split() #make the string into a list
                for word in decrypted_list:
                    if is_word(self.valid_words, word): #if this is true
                        count +=1
                if count > maximum: 
                    maximum = count #new count, loop again and again
                    best = [26-a,26-b] #the values that return the most words
        new_dict = self.make_shift_dicts(best)
        return(best, self.apply_shifts(new_dict))
                


def test_plaintext_message():
    '''
    Write two test cases for the PlaintextMessage class here. 
    Each one should handle different cases (see handout for
    more details.) Write a comment above each test explaining what 
    case(s) it is testing. 
    '''

#    #### Example test case (PlaintextMessage) ##### 

#    # This test is checking encoding a lowercase string with punctuation in it. 
#    plaintext = PlaintextMessage('hello!', [2,3])
#    print('Expected Output: jhnoq!')
#    print('Actual Output:', plaintext.get_encrypted_message_text())

    #This test checks a proper noun string
    plaintext = PlaintextMessage('George', [1,2])
    print('Expected Output: Hgpthg')
    print('Actual Output: ', plaintext.get_encrypted_message_text())
    
    #This test checks a word with a space in it and alternating cases
    plaintext = PlaintextMessage('hOt DoG', [2,1])
    print('Expected Output: jPv FpI')
    print('Actual Output: ', plaintext.get_encrypted_message_text())
    

def test_ciphertext_message():
    '''
    Write two test cases for the CiphertextMessage class here. 
    Each one should handle different cases (see handout for
    more details.) Write a comment above each test explaining what 
    case(s) it is testing. 
    '''

#    #### Example test case (CiphertextMessage) ##### 
    
#   # This test is checking decoding a lowercase string with punctuation in it.
#    ciphertext = CiphertextMessage('fbjim!')
#    print('Expected Output:', ([2, 3], 'hello!'))
#    print('Actual Output:', ciphertext.decrypt_message())

    #This test checks a word with a space in it
    ciphertext = CiphertextMessage('gczjsfx cmfq')
    print('Expected Output:', ([1,2], 'healthy dogs'))
    print('Actual Output:' , ciphertext.decrypt_message())
    
    #This test checks a word with alternating cases and punctuation
    ciphertext = CiphertextMessage('BnJoFhL')
    print('Expected Output:', ([2,1], 'DoLpHiN'))
    print('Actual Output:' , ciphertext.decrypt_message())

def decode_story():
    '''
    Write your code here to decode the story contained in the file story.txt.
    Hint: use the helper function get_story_string and your CiphertextMessage class.

    Returns: a tuple containing (best_shift, decoded_story)

    '''
    Cipher = CiphertextMessage(get_story_string())
    return Cipher.decrypt_message()

if __name__ == '__main__':

#    # Uncomment these lines to try running your test cases 
#     test_plaintext_message()
#     test_ciphertext_message()
#
#    # Uncomment these lines to try running decode_story_string()
#     best_shift, story = decode_story()
#     print("Best shift:", best_shift)
#     print("Decoded story: ", story)
    pass 
