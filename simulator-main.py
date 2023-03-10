# Add and Shift helper function
import math


# Need to implement
def FourBitFullAdder(Abits, Bbits, carryIn):
    return


# Need to implement
def CarrySelect(binaryNumOne, binaryNumTwo):
    return


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
# Output: Result bit and carry
def XOR(bitOne, bitTwo):
    # return AND(OR(bitOne, bitTwo), NAND(bitOne, bitTwo))
    # 1 1 or 0 0
    if bitOne == bitTwo:
        # If 1 1 else 0 0
        if bitOne == 1:
            result = 0
            carry = 1
        else:
            result = 0
            carry = 0
    # If 1 0 or 0 1
    else:
        result = 1
        carry = 0

    return result, carry


# Shift AQ
def shiftAQ(AQ):
    for i in range(len(AQ)-1, 0, -1):
        AQ[i] = AQ[i-1]
    AQ[0] = 0
    return AQ


# Add and Shift helper function
# Add B to AQ Function
def add_B_to_AQ(AQ, B):
    sizeAQ = len(AQ)-1
    sizeB = len(B)

    NEW_AQ = AQ[:]

    # Carry Bit
    carryBit = 0
    XOR_Num = 0
    for i in range(sizeB):
        bitAQ = NEW_AQ[sizeAQ - sizeB - i]
        bitB = B[sizeB - i - 1]

        # Result bit will be carryBit + bitAQ + bitB
        resultBit, carry = XOR(bitAQ, bitB)
        resultBitFinal, carryTwo = XOR(resultBit, carryBit)
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
        AQ[size_AQ-len(multiplier)+i] = multiplier[i]
    num_XOR = 0
    num_Shift = 0
    for i in range(len(B)):
        # Check Q0 if 1 or 0
        if AQ[size_AQ-1]:
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

print(test_multiplier, "*", test_multiplicand, '=')

mult_result, numXOR, numShift = add_and_shift(test_multiplier, test_multiplicand)
# Assuming xor is 2Dt
# Assuming shift op is 3Dt


print("Result: ", mult_result)
print("Timing: ", 2 * numXOR + 3 * numShift, "DT")


print("Iterative Method Testing")
A_Test = [0, 0, 1, 1, 0, 1]
B_Test = [0, 0, 1, 1, 1, 1]
print(iterativeMethod(iterativeMethodPrep(A_Test, B_Test)))
