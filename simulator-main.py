# Add and Shift helper function
import math
from typing import List, Literal
time = 0

'''
------------ NOTES ------------
'''

# TODO: Create a way to keep track of how much time the methods take

"""
Could use a global variable that XOR, AND, NAND, OR, and SHIFTAQ functions can access.
Everytime one of those functions are called, we add to the global variable. Clear when starting new simulation.
I.E. global_time += xDT
"""

'''
------------ END NOTES ------------
'''


"""
-------- BASIC LOGIC GATE & F.A. OPERATIONS --------
"""


# AND Operation
# Input: Two Bits
# Output: 1 or 0
def AND(bitOne: int, bitTwo: int) -> Literal[0, 1]:
    global time
    time += 1
    if bitOne == 1 and bitTwo == 1:
        return 1
    else:
        return 0


# NAND Operation
# Input: Two Bits
# Output: 1 or 0
def NAND(bitOne: int, bitTwo: int) -> Literal[0, 1]:
    global time
    time += 1
    if bitOne == 1 and bitTwo == 1:
        return 0
    else:
        return 1


# OR Operation
# Input: Two Bits
# Output: 1 or 0
def OR(bitOne: int, bitTwo: int) -> Literal[0, 1]:
    global time
    time += 1
    if bitOne or bitTwo:
        return 1
    else:
        return 0


# XOR Operation
# Input: Two Bits
# Output: 1 or 0
def XOR(bitOne: int, bitTwo: int) -> Literal[0, 1]:
    global time
    time += 2
    return AND(OR(bitOne, bitTwo), NAND(bitOne, bitTwo))

# Four bit full adder implementation
# Using logic gates to generate results
# for the sum and carry
# INPUT: Two 4-bit binary numbers and CarryIn
# Output: Sum of 4-bit binary addition, carryOut
def FourBitFullAdder(A_bits, B_bits, carryIn):
    sum_one = XOR(XOR(A_bits[3], B_bits[3]), carryIn)
    carry_one = OR(AND(XOR(A_bits[3], B_bits[3]), carryIn), AND(A_bits[3], B_bits[3]))
    sum_two = XOR(XOR(A_bits[2], B_bits[2]), carry_one)
    carry_two = OR(AND(XOR(A_bits[2], B_bits[2]), carry_one), AND(A_bits[2], B_bits[2]))
    sum_three = XOR(XOR(A_bits[1], B_bits[1]), carry_two)
    carry_three = OR(AND(XOR(A_bits[1], B_bits[1]), carry_two), AND(A_bits[1], B_bits[1]))
    sum_four = XOR(XOR(A_bits[0], B_bits[0]), carry_three)
    carry_final = OR(AND(XOR(A_bits[0], B_bits[0]), carry_three), AND(A_bits[0], B_bits[0]))

    # Create the final representation of the F.A. summation
    sum_bits = [sum_four, sum_three, sum_two, sum_one]

    return sum_bits, carry_final


# Fast adder carry select implementation
# Input: Two binary numbers 4,8,12 or 16 bits long
# Output: Sum of two binary numbers
def FastAdderCarrySelect(binNumOne, binNumTwo, carryIn):
    numFAOps = len(binNumOne) / 4
    sumBin = []
    carryFA = carryIn
    numPointer = len(binNumOne)
    if numFAOps == 1:
        # Primary FA operation
        FA_result, newCarry = FourBitFullAdder(binNumOne, binNumTwo, carryFA)
        sumBin = FA_result + sumBin
        endCarry = newCarry
    elif numFAOps == 2:
        FA_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 4:numPointer],
                                               binNumTwo[numPointer - 4:numPointer], carryFA)

        FA1_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 8:numPointer - 4],
                                                binNumTwo[numPointer - 8:numPointer - 4], newCarry)

        sumBin = FA1_result + FA_result

        endCarry = newCarry
    elif numFAOps == 3:
        FA_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 4:numPointer],
                                               binNumTwo[numPointer - 4:numPointer], carryFA)

        FA1_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 8:numPointer - 4],
                                                binNumTwo[numPointer - 8:numPointer - 4], newCarry)

        FA2_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 12:numPointer - 8],
                                                binNumTwo[numPointer - 12:numPointer - 8], newCarry)

        sumBin = FA2_result + FA1_result + FA_result

        endCarry = newCarry
    elif numFAOps == 4:
        FA_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 4:numPointer],
                                               binNumTwo[numPointer - 4:numPointer], carryFA)

        FA1_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 8:numPointer - 4],
                                                binNumTwo[numPointer - 8:numPointer - 4], newCarry)

        FA2_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 12:numPointer - 8],
                                                binNumTwo[numPointer - 12:numPointer - 8], newCarry)

        FA3_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 16:numPointer - 12],
                                                binNumTwo[numPointer - 16:numPointer - 12], newCarry)

        sumBin = FA3_result + FA2_result + FA1_result + FA_result

        endCarry = newCarry
    elif numFAOps == 5:
        FA_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 4:numPointer],
                                               binNumTwo[numPointer - 4:numPointer], carryFA)

        FA1_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 8:numPointer - 4],
                                                binNumTwo[numPointer - 8:numPointer - 4], newCarry)

        FA2_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 12:numPointer - 8],
                                                binNumTwo[numPointer - 12:numPointer - 8], newCarry)

        FA3_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 16:numPointer - 12],
                                                binNumTwo[numPointer - 16:numPointer - 12], newCarry)

        FA4_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 20:numPointer - 16],
                                                binNumTwo[numPointer - 20:numPointer - 16], newCarry)

        sumBin = FA4_result + FA3_result + FA2_result + FA1_result + FA_result

        endCarry = newCarry
    elif numFAOps == 6:
        # Primary FA operation
        FA_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 4:numPointer],
                                               binNumTwo[numPointer - 4:numPointer], carryFA)

        FA1_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 8:numPointer - 4],
                                                binNumTwo[numPointer - 8:numPointer - 4], newCarry)

        FA2_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 12:numPointer - 8],
                                                binNumTwo[numPointer - 12:numPointer - 8], newCarry)

        FA3_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 16:numPointer - 12],
                                                binNumTwo[numPointer - 16:numPointer - 12], newCarry)

        FA4_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 20:numPointer - 16],
                                                binNumTwo[numPointer - 20:numPointer - 16], newCarry)

        FA5_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 24:numPointer - 20],
                                                binNumTwo[numPointer - 24:numPointer - 20], newCarry)

        sumBin = FA5_result + FA4_result + FA3_result + FA2_result + FA1_result + FA_result

        endCarry = newCarry
    elif numFAOps == 7:
        FA_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 4:numPointer],
                                               binNumTwo[numPointer - 4:numPointer], carryFA)

        FA1_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 8:numPointer - 4],
                                                binNumTwo[numPointer - 8:numPointer - 4], newCarry)

        FA2_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 12:numPointer - 8],
                                                binNumTwo[numPointer - 12:numPointer - 8], newCarry)

        FA3_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 16:numPointer - 12],
                                                binNumTwo[numPointer - 16:numPointer - 12], newCarry)

        FA4_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 20:numPointer - 16],
                                                binNumTwo[numPointer - 20:numPointer - 16], newCarry)

        FA5_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 24:numPointer - 20],
                                                binNumTwo[numPointer - 24:numPointer - 20], newCarry)

        FA6_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 28:numPointer - 24],
                                                binNumTwo[numPointer - 28:numPointer - 24], newCarry)

        sumBin = FA6_result + FA5_result + FA4_result + FA3_result + FA2_result + FA1_result + FA_result

        endCarry = newCarry
    else:
        FA_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 4:numPointer],
                                               binNumTwo[numPointer - 4:numPointer], carryFA)

        FA1_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 8:numPointer - 4],
                                                binNumTwo[numPointer - 8:numPointer - 4], newCarry)

        FA2_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 12:numPointer - 8],
                                                binNumTwo[numPointer - 12:numPointer - 8], newCarry)

        FA3_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 16:numPointer - 12],
                                                binNumTwo[numPointer - 16:numPointer - 12], newCarry)

        FA4_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 20:numPointer - 16],
                                                binNumTwo[numPointer - 20:numPointer - 16], newCarry)

        FA5_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 24:numPointer - 20],
                                                binNumTwo[numPointer - 24:numPointer - 20], newCarry)

        FA6_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 28:numPointer - 24],
                                                binNumTwo[numPointer - 28:numPointer - 24], newCarry)

        FA7_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 32:numPointer - 28],
                                                binNumTwo[numPointer - 32:numPointer - 28], newCarry)

        sumBin = FA7_result + FA6_result + FA5_result + FA4_result + FA3_result + FA2_result + FA1_result + FA_result

        endCarry = newCarry
    return sumBin, endCarry


"""
-------- ADD-AND-SHIFT ALGORITHM --------
"""


# Shift AQ
def shiftAQ(AQ: List[int]) -> List[int]:
    for i in range(len(AQ) - 1, 0, -1):
        AQ[i] = AQ[i - 1]
    AQ[0] = 0

    global time
    time += 3
    return AQ


# Add and Shift helper function
# Add B to AQ Function
def add_B_to_AQ(AQ, B):
    sizeAQ = len(AQ) - 1
    sizeB = len(B)

    NEW_AQ = AQ[:]

    # Carry Bit
    carryBit = 0
    XOR_Num = 0
    for i in range(sizeB):
        bitAQ = NEW_AQ[sizeAQ - sizeB - i]
        bitB = B[sizeB - i - 1]

        # Result bit will be carryBit + bitAQ + bitB
        resultBit = XOR(bitAQ, bitB)
        carry = AND(bitAQ, bitB)

        resultBitFinal = XOR(resultBit, carryBit)
        carryTwo = AND(resultBit, carryBit)

        XOR_Num += 2

        # Set result into AQ
        NEW_AQ[sizeAQ - sizeB - i] = resultBitFinal

        # Need to reset carry with new carry
        # One will be 0 the other 1 if there
        # exist a carry
        carryBit = carry
        carryBit += carryTwo

    NEW_AQ[0] = carryBit

    return NEW_AQ, XOR_Num


# Add and shift function
# Input: Multiplier and Multiplicand
# (using a list and in binary representation)
# Output: Result of multiplying the two
# inputs together
def add_and_shift(multiplier, multiplicand):
    # Finds the size AQ will be (+1 for carry bit)
    size_AQ = (2 * max(len(multiplier), len(multiplicand))) + 1

    # Create empty list to hold carry bit and AQ
    AQ = [0] * size_AQ

    # Set B to the multiplicand
    B = multiplicand

    # Initialize AQ
    for i in range(len(multiplier)):
        AQ[size_AQ - len(multiplier) + i] = multiplier[i]
    num_XOR = 0
    num_Shift = 0
    for i in range(len(B)):
        # Check Q0 if 1 or 0
        if AQ[size_AQ - 1]:
            AQ, XOR_OPS = add_B_to_AQ(AQ, B)
            num_XOR += XOR_OPS
            AQ = shiftAQ(AQ)
            num_Shift += 1
        else:
            AQ = shiftAQ(AQ)
            num_Shift += 1

    return AQ, num_XOR, num_Shift


"""
-------- ITERATIVE METHOD ALGORITHM --------
"""

# Base case for iterative function
# Spliting terms until the length is two
# We then can do trivial multiplication (0 * 1 = 0 or 1 * 1 = 1)
# Returning 2^n*(ac) + 2^(n/2)(adbc) + bd
def base(A: List[int], B: List[int], n: int) -> List[int]:
    a: int = A[0]
    b: int = A[1]
    c: int = B[0]
    d: int = B[1]
    carry_one: int = 0
    carry_two: int = 0
    adbc_carry: int = 0

    ac: List[int] = []
    ad: List[int] = []
    bc: List[int] = []
    adbc: List[int] = []
    bd: List[int] = []

    to_return: List[int] = []

    ac.append(0)
    ac.append(AND(a, c)) #
    ac = SHIFTL(ac, n) #

    ad.append(0)
    ad.append(AND(a, d))

    bc.append(0)
    bc.append(AND(b, c))

    adbc_carry = AND(ad[1], bc[1]) #

    adbc.append(0)
    adbc.append(adbc_carry)
    adbc.append(XOR(ad[1], bc[1])) #

    adbc = SHIFTL(adbc, n // 2)

    bd.append(0)
    bd.append(0)
    bd.append(0)
    bd.append(AND(b, d))

    to_return, carry_one = FastAdderCarrySelect(ac, adbc, 0)
    to_return, carry_two = FastAdderCarrySelect(to_return, bd, carry_one)

    return to_return, carry_two


# Wrapper function for itMain
# It makes sure the length of the binary number is a power of two
# Trims the zeros at beginning of result as well
def iterative(A: List[int], B: List[int], n: int) -> List[int]:
    while not math.log(n, 2).is_integer():
        A.insert(0, 0)
        B.insert(0, 0)
        n += 1
    
    result = itMain(A, B, n)

    while result[0][0] == 0:
        result[0].pop(0)
    
    return result

def itMain(A: List[int], B: List[int], n: int) -> List[int]:
    if n == 2:
        return base(A, B, n)
    
    # Recursive call
    n_div_two = n // 2

    # 2^n iter(ac, n/2)
    AC, AC_Carry = itMain(A[0:n_div_two], B[0:n_div_two], n_div_two)
    AC = SHIFTL(AC, n)

    # 2^n/2 (iter(ad, n/2) + iter(bc, n/2)
    AD, AD_Carry = itMain(A[0:n_div_two], B[n_div_two:n], n_div_two)
    BC, BC_Carry = itMain(A[n_div_two:n], B[0:n_div_two], n_div_two)

    AD_BC, ADBC_Carry = FastAdderCarrySelect(AD, BC, 0)
    AD_BC.insert(0, ADBC_Carry)
    AD_BC = SHIFTL(AD_BC, n // 2) # Shift

    while len(AD_BC) < len(AC):
        AD_BC.insert(0, 0)

    # + iter(bd, n/2)
    BD, BD_Carry = itMain(A[n_div_two:n], B[n_div_two:n], n_div_two)

    while len(BD) < len(AC):
        BD.insert(0, 0)

    # Fast adder

    AC_BD, ACBD_Carry = FastAdderCarrySelect(AC, BD, 0)
    # Make sure to implement w/ carry

    return FastAdderCarrySelect(AC_BD, AD_BC, ACBD_Carry)

# Shift Left
# Input: Binary number and number of shifts
# Output: Binary number shifted num_shifts to the left
def SHIFTL(binary_number: List[int], num_shifts: int) -> List[int]:
    # IDK if Python does pass-by-reference or if the inputted list is copied, so
    to_return: List[int] = binary_number
    for _ in range(num_shifts):
        to_return.append(0)
    
    global time
    time += 3
    return to_return


if __name__ == "__main__":

    testData = [([1, 1, 1, 0], [1, 1, 1, 1]), ([0, 1, 0, 1], [0, 1, 0, 1]),
                ([1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]),
                ([1, 0, 1, 1, 1, 0], [1, 1, 0, 1, 1, 1]),
                ([1, 1, 1, 0, 1, 1], [1, 0, 0, 0, 1, 1]),
                ([0, 0, 0, 1, 1, 1, 1, 1], [0, 1, 0, 1, 0, 1, 0, 1]),
                ([1, 1, 0, 1, 0, 1, 1, 1], [0, 1, 0, 1, 0, 1, 0, 1]),
                ([0, 1, 0, 1, 0, 1, 0, 1], [1, 1, 0, 1, 0, 1, 1, 1]),
                ([0, 1, 1, 1, 0, 1, 1, 1], [0, 0, 1, 1, 0, 0, 1, 1]),
                ([0, 1, 1, 1, 1, 0, 0, 0], [0, 1, 1, 1, 0, 1, 1, 1]),
                ([0, 1, 0, 1, 0, 1, 0, 1, 0, 1], [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]),
                ([1, 1, 0, 0, 1, 1, 1, 0, 1, 1], [1, 0, 0, 1, 1, 1, 0, 0, 0, 0]),
                ([1, 0, 0, 1, 1, 0, 1, 1, 1, 0], [0, 1, 0, 1, 1, 1, 1, 0, 1, 0]),
                ([0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1], [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]),
                ([0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1], [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]),
                ([1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]),
                ([1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]),
                ([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0], [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]),
                ([1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0], [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1]),
                ([0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0], [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0]),
                ([1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0], [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0])]

    test_multiplier = [0, 1, 0, 1]
    test_multiplicand = [1, 1, 0, 1]

    for multPair in testData:
        time = 0
        print(multPair[0], '+', multPair[1], '=', add_and_shift(multPair[0], multPair[1]))
        print('time of operation: ', time, end='\n')

    print("\nIterative")
    for multPair in testData:
        time = 0
        # print(multPair[0], '+', multPair[1], '=', iterative(multPair[0], multPair[1]))
        print(multPair[0], '+', multPair[1], '=', iterative(multPair[0], multPair[1], len(multPair[0])))
        print('time of operation: ', time, end='\n')
