# Question: Develop a collection of different rules for generating the
#  terms of a sequence and a program for randomly selecting
#  one of these rules and the particular sequence generated
#  using these rules. Make this part of an interactive program
#  that prompts for the next term of the sequence and determines whether the response is the intended next term.

# input:
# output:

# rules:
# 1. fib numbers
# 2. Q27 of ex 2.4
# 3. Q28 of ex 2.4
# 4. ulam numbers
# 5. Q30 of supp exercises
# 6. Q31 of supp exercises

import random
import math

def prompt(n = 20):
    random_number = random.randint(0, 5)
    seq = []
    if (random_number % 6 == 0):
        gen_seq(fibonacci_sequence, seq, n)
    elif (random_number % 6 == 1):
        gen_seq(ex24_q27, seq, n)
    elif (random_number % 6 == 2):
        gen_seq(ex24_q28, seq, n)
    elif (random_number % 6 == 3):
        gen_seq(ulam_sequence, seq, n)
    elif (random_number % 6 == 4):
        gen_seq(supp_q30, seq, n)
    else:
        gen_seq(supp_q31, seq, n)

def gen_seq(func, seq, n):
    # generate sequence using the func
    func(seq, n)

    # print out n-1 elements
    print("The first {0} elements:".format(n-1))
    for i in range(0, n-1):
        print(seq[i], end=' ')
    print()

    # prompt for the next element
    wrong = 1
    while wrong:
        next_element = input("Enter the next element: ")
        try:
            next_element = int(next_element)
            print("The integer you entered is:", next_element)
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
        if next_element == seq[n - 1]:
            wrong = 0
            print("Correct!")
        else:
            wrong = 1
            print("Wrong!")

    print("This sequence is {0}".format(func.__name__))

def fibonacci_sequence(seq, n):
    seq.append(1)
    seq.append(1)
    for i in range(2, n):
        seq.append(seq[i-1]+seq[i-2])

def ex24_q27(seq, n):
    for i in range(0, n):
        seq.append(int(i+1+round(math.sqrt(i+1))))

def ex24_q28(seq, n):
    for i in range(0, n):
        seq.append(int(math.floor(math.sqrt(2*(i+1)) + 0.5)))

def ulam_sequence(seq, n):
    seq.append(1)
    seq.append(2)
    target_n = 3
    while len(seq) < n:
        count = 0
        for i in range(len(seq)):
            for j in range(i+1, len(seq)):
                if (seq[i] + seq[j]) == target_n:
                    count+=1
                if (count > 1):
                    break
            if (count > 1):
                break
        if count == 1:
            seq.append(target_n)
        target_n+=1

def supp_q30(seq, n):
    seq.append(1)
    seq.append(3)
    seq.append(4)
    for i in range(3, n):
        seq.append(seq[i-1]+seq[i-2]+seq[i-3])

def supp_q31(seq, n):
    seq.append(2)
    for i in range(1,n):
        if ((i+1) % 2):
            seq.append(int(seq[i-1]*i/2))
        else:
            seq.append(int(seq[i-1]+(i+1)/2))


if __name__ == "__main__":
    prompt()


