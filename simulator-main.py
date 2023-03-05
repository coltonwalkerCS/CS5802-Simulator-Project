# Add and Shift helper function
# XOR Operation
# Input: Two Bits
# Output: Result bit and carry
def XOR(bitOne, bitTwo):
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


# Add B to AQ Function
def add_B_to_AQ(AQ, B):
    sizeAQ = len(AQ)-1
    sizeB = len(B)

    NEW_AQ = AQ[:]

    # Carry Bit
    carryBit = 0

    for i in range(sizeB):
        bitAQ = NEW_AQ[sizeAQ - sizeB - i]
        bitB = B[sizeB - i - 1]

        # Result bit will be carryBit + bitAQ + bitB
        resultBit, carry = XOR(bitAQ, bitB)
        resultBitFinal, carryTwo = XOR(resultBit, carryBit)

        # Set result into AQ
        NEW_AQ[sizeAQ - sizeB - i] = resultBitFinal

        # Need to reset carry with new carry
        # One will be 0 the other 1 if there
        # exist a carry
        carryBit = carry
        carryBit += carryTwo

    NEW_AQ[0] = carryBit

    return NEW_AQ


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

    for i in range(len(B)):
        # Check Q0 if 1 or 0
        if AQ[size_AQ-1]:
            AQ = add_B_to_AQ(AQ, B)
            AQ = shiftAQ(AQ)
        else:
            AQ = shiftAQ(AQ)

    return AQ


test_multiplier = [0, 1, 1, 0]
test_multiplicand = [1, 1, 0, 0]

print(test_multiplier, "*", test_multiplicand, '=')
print(add_and_shift(test_multiplier, test_multiplicand))
