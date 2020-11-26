import argparse
from functools import cmp_to_key
from functools import reduce

class operand:
    contents = ""
    size = 0
    negative = False

    def __init__(self, contents):
        self.contents = contents
        self.size = len(contents)
        self.negative = (self.contents[0] == "-")
        
        if (self.negative):
            self.contents = self.contents[1:]
            self.size -= 1
    
    def print_contents(self):

        if self.negative:
            print("(-" + self.contents + ")", end = " ")
        else: print(self.contents, end = " ")

def print_list(input_list):

    for x in input_list:
        x.print_contents()

def same_sign(sign_tuple):
    return True if (sign_tuple == (0,0)) else False

def cmp_pure_value(op1, op2):

    sign1 = 0 if (op1.negative == False) else 1
    sign2 = 0 if (op2.negative == False) else 1
    sign_tuple = (sign1, sign2)

    if sign_tuple == (0,1): # + > - vs - < + 
        return 1
    elif sign_tuple == (1,0):
        return -1
 
    if op1.size > op2.size: #return the opposite if negatives
        return 1 if same_sign(sign_tuple) else -1
    elif op1.size < op2.size:
        return -1 if same_sign(sign_tuple) else 1

    for x,y in zip(op1.contents, op2.contents):

        if ord(x) > ord(y):
            return 1 if same_sign(sign_tuple) else -1
        elif ord(x) < ord(y):
            return -1 if same_sign(sign_tuple) else 1
    
    return 0

def add(num1, num2):

    len_list = sorted([num1, num2], key= lambda operand : operand.size)
    shorter_len = len_list[0]
    longer_len = len_list[1]

    shorter_len_str = shorter_len.contents[::-1]
    longer_len_str = longer_len.contents[::-1]

    signs_booleans = (num1.negative, num2.negative)

    carry_on = 0
    result = []

    for x,y in zip(shorter_len_str, longer_len_str):
        digit = int(x) + int(y) + carry_on
        carry_on = digit // 10
        result.append(str(digit%10))

    for x in range(shorter_len.size, longer_len.size): #adding rest of unused operands
        result.append(longer_len_str[x])

    if carry_on == 1: #dealing with excess carry on

        if shorter_len.size != longer_len.size:

            for x in range(shorter_len.size, longer_len.size):

                if result[x] == "9":
                    result[x] = "0"
                else:
                    result[x] = str(int(result[x])+1)
                    carry_on = 0
                    break
            if carry_on != 0:
                result.append("1")

        else: result.append("1")

    if signs_booleans == (True, True) or signs_booleans == (True, False): #if two negatives => negative version of their positive sums
        result.append("-")

    whole_result = "".join(result[::-1])

    whole_result_obj = operand(whole_result)

    return whole_result_obj


def subtract(num1, num2):

    negative = False

    if num1.contents == num2.contents:
        return operand("0")

    if num1.size > num2.size:
        mightier = num1
        tinier = num2
    elif num1.size < num2.size:
        mightier = num2
        tinier = num1
        negative = True
    else:
        for x,y in zip(num1.contents, num2.contents):
            if x > y:
                mightier = num1
                tinier = num2
                break
            elif x < y:
                mightier = num2
                tinier = num1
                negative = True

    mightier_str = mightier.contents[::-1]
    tinier_str = tinier.contents[::-1]

    borrow = 0
    result = []

    for x,y in zip(mightier_str, tinier_str):

        op1 = int(x) + borrow
        op2 = int(y)

        if op1 < op2:
            op1 += 10
            borrow = -1

        digit = op1 - op2

        result.append(str(digit))

    for x in range(tinier.size, mightier.size):
        result.append(mightier_str[x])

    if borrow == -1 and tinier.size != mightier.size:
        
        for x in range(tinier.size, mightier.size):

            if result[x] != "0":
                result[x] = str(int(result[x])-1)
                break
            else: result[x] = "9"

    whole_result = "".join(result[::-1])

    while whole_result[0] == "0":
        whole_result = whole_result[1:]

    if negative:
        whole_result = "-" + whole_result

    return operand(whole_result)

def switch(num1, num2, operation):

    sign_booleans = (num1.negative, num2.negative)

    if operation == "a": 

        if sign_booleans == (False, False) or sign_booleans == (True, True):
            return add(num1, num2)
        elif sign_booleans == (False, True):
            return subtract(num1, num2)
        else: return subtract(num2, num1)
    elif operation == "s":

        if sign_booleans == (False, False):
            return subtract(num1, num2)
        elif sign_booleans == (False, True) or sign_booleans == (True, False):
            return add(num1, num2)
        else: return(subtract(num2, num1))

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--operation', '-o', dest = 'operation', type = str)
    args = parser.parse_args()

    print("Enter any amount of positive/negative numbers separated by spaces and indicate the operation -o performed.")
    print("Operations supported are a addition or s subtraction.")

    numbers = input().split(" ")
    op_list = []

    for x in numbers:
        op_list.append(operand(x))

    print_list(op_list)

    while len(op_list) != 1:

        op_list[1] = switch(op_list[0], op_list[1], args.operation)
        op_list = op_list[1:]

    msg = "sum to" if args.operation == "a" else "differs to"

    print(msg, end = " ")
    print_list(op_list)

    return 0

if __name__ == "__main__":
    main()
    


















  
    