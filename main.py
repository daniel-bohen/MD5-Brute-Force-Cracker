import hashlib, time, itertools, string
from collections import deque
from multiprocessing import *

#get the array of potential characters, initialize global variables
cs = string.ascii_lowercase + string.digits + string.ascii_uppercase
start_time = time.time() 
real = []

def getHash(guess):
    #pass in the global variables
    global start_time, real

    #guess is a tuple of characters, this line converts it to a single string
    guess = ''.join(guess)

    #converts the string to the md5 hashed value 
    guess_hash = hashlib.md5(guess.encode()).hexdigest()

    #if the guess_hash is in the read-in array of hashes, print the guess as a string, and compute the time it took to compute
    if guess_hash in real:
        print('{}   {}'.format(guess, time.time()-start_time))

def main():
    #pass in the global variables
    global start_time, real, cs

    #read in from the file 'hashes.txt' 
    text_file = open("hashes.txt", "r")
    lines = text_file.readlines()

    #remove the newline character from each line that was read in, retaining just the hash 
    for line in lines:
        real.append(line.rstrip('\n'))
    
    #set the start time after you have read in from the file
    start_time = time.time()

    #set the multiprocess pool, with processes equal to the number of cpu cores you have
    p = Pool(processes=cpu_count())

    #compute all the combinations for each password of length 1 to 8 
    for password_length in range(1, 9):
        #uses a deque and imap to ensure that computed strings are not stored in memory -- otherwise fills up all ram and crashes program
        #components of p.imap_unordered, the multiprocessing function: 
            # getHash: calls the getHash function for each element in the result of itertools.product
            # itertools.product(cs, repeat=password_length): the set of all possible combinations the inputset (cs) that are of length password_length
            # chunksize=2500: the number of jobs sent to each cpu at a time, needs to be balanced to save on data I/O for each cpu
            # 0: the max length of the deque, means items are popped immediatelly after they are pushed, means nothing is stored
        deque(p.imap_unordered(getHash, itertools.product(cs, repeat=password_length), chunksize=2500), 0)
           

#this is necessary for multiprocessing, per the documentation
if __name__=="__main__":
    main()
