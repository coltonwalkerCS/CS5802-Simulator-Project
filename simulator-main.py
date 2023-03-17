# Add and Shift helper function
import math


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


# Given two binary numbers with carry 1 and 0
# choose the binary option which corresponds
# to the carry
def MUX(binOptionCarryOne, binOptionCarryZero, carryOut):
    if carryOut:
        return binOptionCarryOne
    else:
        return binOptionCarryZero


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
        # Primary FA operation
        FA_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 4:numPointer],
                                               binNumTwo[numPointer - 4:numPointer], carryFA)

        # Generate 1 and 0 carry options for next FA operation in parallel
        FA_binaryOptionOne, newCarryOpOne = FourBitFullAdder(binNumOne[numPointer - 8:numPointer - 4],
                                                             binNumTwo[numPointer - 8:numPointer - 4], 1)
        FA_binaryOptionTwo, newCarryOpTwo = FourBitFullAdder(binNumOne[numPointer - 8:numPointer - 4],
                                                             binNumTwo[numPointer - 8:numPointer - 4], 0)

        sumBin = FA_result + sumBin
        sumBin = MUX(FA_binaryOptionOne, FA_binaryOptionTwo, newCarry) + sumBin

        if newCarry:
            endCarry = newCarryOpOne
        else:
            endCarry = newCarryOpTwo

    elif numFAOps == 3:
        # Primary FA operation
        FA_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 4:numPointer],
                                               binNumTwo[numPointer - 4:numPointer], carryFA)

        # Generate 1 and 0 carry options for first FA operation in parallel
        FA_binaryFirOptionOne, newCarryFirOpOne = FourBitFullAdder(binNumOne[numPointer - 8:numPointer - 4],
                                                                   binNumTwo[numPointer - 8:numPointer - 4], 1)
        FA_binaryFirOptionTwo, newCarryFirOpTwo = FourBitFullAdder(binNumOne[numPointer - 8:numPointer - 4],
                                                                   binNumTwo[numPointer - 8:numPointer - 4], 0)

        # Generate 1 and 0 carry options for second FA operation in parallel
        FA_binarySecOptionOne, newCarrySecOpOne = FourBitFullAdder(binNumOne[numPointer - 12:numPointer - 8],
                                                                   binNumTwo[numPointer - 12:numPointer - 8], 1)
        FA_binarySecOptionTwo, newCarrySecOpTwo = FourBitFullAdder(binNumOne[numPointer - 12:numPointer - 8],
                                                                   binNumTwo[numPointer - 12:numPointer - 8], 0)

        sumBin = FA_result + sumBin
        sumBin = MUX(FA_binaryFirOptionOne, FA_binaryFirOptionTwo, newCarry) + sumBin

        if newCarry:
            newCarry = newCarryFirOpOne
        else:
            newCarry = newCarryFirOpTwo

        sumBin = MUX(FA_binarySecOptionOne, FA_binarySecOptionTwo, newCarry) + sumBin

        if newCarry:
            endCarry = newCarrySecOpOne
        else:
            endCarry = newCarrySecOpTwo
    else:
        # Primary FA operation
        FA_result, newCarry = FourBitFullAdder(binNumOne[numPointer - 4:numPointer],
                                               binNumTwo[numPointer - 4:numPointer], carryFA)

        # Generate 1 and 0 carry options for first FA operation in parallel
        FA_binaryFirOptionOne, newCarryFirOpOne = FourBitFullAdder(binNumOne[numPointer - 8:numPointer - 4],
                                                                   binNumTwo[numPointer - 8:numPointer - 4], 1)
        FA_binaryFirOptionTwo, newCarryFirOpTwo = FourBitFullAdder(binNumOne[numPointer - 8:numPointer - 4],
                                                                   binNumTwo[numPointer - 8:numPointer - 4], 0)

        # Generate 1 and 0 carry options for second FA operation in parallel
        FA_binarySecOptionOne, newCarrySecOpOne = FourBitFullAdder(binNumOne[numPointer - 12:numPointer - 8],
                                                                   binNumTwo[numPointer - 12:numPointer - 8], 1)
        FA_binarySecOptionTwo, newCarrySecOpTwo = FourBitFullAdder(binNumOne[numPointer - 12:numPointer - 8],
                                                                   binNumTwo[numPointer - 12:numPointer - 8], 0)

        # Generate 1 and 0 carry options for third FA operation in parallel
        FA_binaryThrOptionOne, newCarryThrOpOne = FourBitFullAdder(binNumOne[numPointer - 16:numPointer - 12],
                                                                   binNumTwo[numPointer - 16:numPointer - 12], 1)
        FA_binaryThrOptionTwo, newCarryThrOpTwo = FourBitFullAdder(binNumOne[numPointer - 16:numPointer - 12],
                                                                   binNumTwo[numPointer - 16:numPointer - 12], 0)

        sumBin = FA_result + sumBin
        sumBin = MUX(FA_binaryFirOptionOne, FA_binaryFirOptionTwo, newCarry) + sumBin

        if newCarry:
            newCarry = newCarryFirOpOne
        else:
            newCarry = newCarryFirOpTwo

        sumBin = MUX(FA_binarySecOptionOne, FA_binarySecOptionTwo, newCarry) + sumBin

        if newCarry:
            newCarry = newCarrySecOpOne
        else:
            newCarry = newCarrySecOpTwo

        sumBin = MUX(FA_binaryThrOptionOne, FA_binaryThrOptionTwo, newCarry) + sumBin

        if newCarry:
            endCarry = newCarryThrOpOne
        else:
            endCarry = newCarryThrOpTwo

    sumBin.insert(0, endCarry)
    return sumBin


# Initialize the starting registers to be 2^n
def iterativeMethodPrep(A, B):
    # Set n (should be of 2^x)
    n = math.ceil(math.log(max(len(A), len(B)), 2))
    lenIter = int(math.pow(2, n))

    # Convert A and B into n bit list
    A_Init = [0] * (lenIter - len(A)) + A[:]
    B_Init = [0] * (lenIter - len(B)) + B[:]

    return A_Init, B_Init, n


# Base case for iterative method (4-bits)
def iterativeBase(A, B, n):
    # 2^n (ac) operation
    ac_0 = AND(A[2], B[2])
    ac_1, carryAC1 = XOR(AND(A[3], B[2]), AND(A[2], B[3]))
    ac_2, carryAC2 = XOR(AND(A[3], B[3]), carryAC1)
    ac_3 = carryAC2

    AC = [ac_3, ac_2, ac_1, ac_0]

    # 2 ^n/2 (ad + bc)
    ad_0 = AND(A[2], B[0])
    ad_1, carryAD1 = XOR(AND(A[3], B[0]), AND(A[2], B[1]))
    ad_2, carryAD2 = XOR(AND(A[3], B[1]), carryAD1)
    ad_3 = carryAD2

    bc_0 = AND(A[0], B[2])
    bc_1, carryBC1 = XOR(AND(A[1], B[2]), AND(A[0], B[3]))
    bc_2, carryBC2 = XOR(AND(A[1], B[3]), carryBC1)
    bc_3 = carryBC2

    # + bd
    bd_0 = AND(A[0], B[0])
    bd_1, carryBD1 = XOR(AND(A[1], B[0]), AND(A[0], B[1]))
    bd_2, carryBD2 = XOR(AND(A[1], B[1]), carryBD1)
    bd_3 = carryBD2

    BD = [bd_3, bd_2, bd_1, bd_0] + [0] * 4

    # ADD BC + AD
    # Fast addition Carry Select Adder

    # Put AC, BD in same register
    AC_BD = AC + BD

    return


def iterativeMethod(A, B, n):
    # Base case
    if n == 4:
        return iterativeBase(A, B, n)
    else:
        # Recursive call
        # 2^n iter(ac, n/2)

        # 2^n/2 (iter(ad, n/2) + iter(bc, n/2)

        # + iter(bd, n/2)
        return


# AND Operation
# Input: Two Bits
# Output: 1 or 0
def AND(bitOne, bitTwo):
    if bitOne == 1 and bitTwo == 1:
        return 1
    else:
        return 0


# NAND Operation
# Input: Two Bits
# Output: 1 or 0
def NAND(bitOne, bitTwo):
    if bitOne == 1 and bitTwo == 1:
        return 0
    else:
        return 1


# OR Operation
# Input: Two Bits
# Output: 1 or 0
def OR(bitOne, bitTwo):
    if bitOne or bitTwo:
        return 1
    else:
        return 0


# XOR Operation
# Input: Two Bits
# Output: 1 or 0
def XOR(bitOne, bitTwo):
    return AND(OR(bitOne, bitTwo), NAND(bitOne, bitTwo))


# Shift AQ
def shiftAQ(AQ):
    for i in range(len(AQ) - 1, 0, -1):
        AQ[i] = AQ[i - 1]
    AQ[0] = 0
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


test_multiplier = [0, 1, 0, 1]
test_multiplicand = [1, 1, 0, 1]

# print(test_multiplier, "*", test_multiplicand, '=')
#
# mult_result, numXOR, numShift = add_and_shift(test_multiplier, test_multiplicand)
# # Assuming xor is 2Dt
# # Assuming shift op is 3Dt
#
#
# print("Result: ", mult_result)
# print("Timing: ", 2 * numXOR + 3 * numShift, "DT")
#
#
# print("Iterative Method Testing")
# A_Test = [0, 0, 1, 1, 0, 1]
# B_Test = [0, 0, 1, 1, 1, 1]
# print(iterativeMethod(iterativeMethodPrep(A_Test, B_Test)))

# FULL ADDER TESTING
# test_add_one = [1, 1, 1, 1]
# test_add_two = [1, 1, 1, 1]
#
# result, carry = FourBitFullAdder(test_add_one, test_add_two, 0)
# print(test_add_one, "+", test_add_two, "=", result)
# print("with carry: ", carry)


# Carry Select fast adder testing
test_add_one = [1, 0, 1, 1]
test_add_two = [1, 1, 0, 1]

test_add_three = [1, 1, 0, 0, 0, 0, 1, 1]
test_add_four = [1, 0, 1, 1, 1, 1, 0, 0]

test_add_five = [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0]
test_add_six = [1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1]

test_add_seven = [1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1]
test_add_eight = [0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1]

print(test_add_one, '+', test_add_two, '=')
print(FastAdderCarrySelect(test_add_one, test_add_two, 0))


print(test_add_three, '+', test_add_four, '=')
print(FastAdderCarrySelect(test_add_three, test_add_four, 0))
#
# print(test_add_five, '+', test_add_six, '=')
# print(FastAdderCarrySelect(test_add_five, test_add_six, 0))
#
# print(test_add_seven, '+', test_add_eight, '=')
# print(FastAdderCarrySelect(test_add_seven, test_add_eight, 0))
