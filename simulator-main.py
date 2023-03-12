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


test_multiplier = [0, 0, 1, 0]
test_multiplicand = [1, 1, 0, 0]

print(test_multiplier, "*", test_multiplicand, '=')

mult_result, numXOR, numShift = add_and_shift(test_multiplier, test_multiplicand)
# Assuming xor is 2Dt
# Assuming shift op is 3Dt


print("Result: ", mult_result)
print("Timing: ", 2 * numXOR + 3 * numShift, "DT")
