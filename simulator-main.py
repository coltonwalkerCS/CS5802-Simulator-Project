# Add and Shift helper function
import math
from typing import List, Literal

# TODO: Fix IterativeMethod() - Not producing right product
# TODO: Fix FastAdderCarrySelect() - ???
# TODO: Create a way to keep track of how much time the methods take

"""
Could use a global variable that XOR, AND, NAND, OR, and SHIFTAQ functions can access.
Everytime one of those functions are called, we add to the global variable. Clear when starting new simulation.
I.E. global_time += xDT
"""

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


# NEED TO FIX:
# SHOULD WORK FOR ANY BIT SIZE 0-16
# RETURNS BIT SIZE 4,8,12,16, AND 20
# NEW IMPLEMENTATION
# FIND WHICH IS MAX, GET IT IN BITS OF 4, 8, 12 OR 16
# SET BOTH TO THE SAME SIZE
# ADD BOTH AND RETURN IN SIZE + 4 (IF CARRY)

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
        # print(binNumOne[numPointer - 4:numPointer])
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
    elif numFAOps == 4:
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
    elif numFAOps == 5:
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
        
        # Generate 1 and 0 carry options for third FA operation in parallel
        FA_binaryFourOptionOne, newCarryFourOpOne = FourBitFullAdder(binNumOne[numPointer - 20:numPointer - 16],
                                                                   binNumTwo[numPointer - 20:numPointer - 16], 1)
        FA_binaryFourOptionTwo, newCarryFourOpTwo = FourBitFullAdder(binNumOne[numPointer - 20:numPointer - 16],
                                                                   binNumTwo[numPointer - 20:numPointer - 16], 0)

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
        
        sumBin = MUX(FA_binaryFourOptionOne, FA_binaryFourOptionTwo, newCarry) + sumBin

        if newCarry:
            endCarry = newCarryFourOpOne
        else:
            endCarry = newCarryFourOpTwo
    elif numFAOps == 6:
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
        
        # Generate 1 and 0 carry options for third FA operation in parallel
        FA_binaryFourOptionOne, newCarryFourOpOne = FourBitFullAdder(binNumOne[numPointer - 20:numPointer - 16],
                                                                   binNumTwo[numPointer - 20:numPointer - 16], 1)
        FA_binaryFourOptionTwo, newCarryFourOpTwo = FourBitFullAdder(binNumOne[numPointer - 20:numPointer - 16],
                                                                   binNumTwo[numPointer - 20:numPointer - 16], 0)

        # Generate 1 and 0 carry options for third FA operation in parallel
        FA_binaryFiveOptionOne, newCarryFiveOpOne = FourBitFullAdder(binNumOne[numPointer - 24:numPointer - 20],
                                                                   binNumTwo[numPointer - 24:numPointer - 20], 1)
        FA_binaryFiveOptionTwo, newCarryFiveOpTwo = FourBitFullAdder(binNumOne[numPointer - 24:numPointer - 20],
                                                                   binNumTwo[numPointer - 24:numPointer - 20], 0)
        
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
        
        sumBin = MUX(FA_binaryFourOptionOne, FA_binaryFourOptionTwo, newCarry) + sumBin

        if newCarry:
            endCarry = newCarryFourOpOne
        else:
            endCarry = newCarryFourOpTwo
        
        sumBin = MUX(FA_binaryFiveOptionOne, FA_binaryFiveOptionTwo, newCarry) + sumBin

        if newCarry:
            endCarry = newCarryFiveOpOne
        else:
            endCarry = newCarryFiveOpTwo
    elif numFAOps == 7:
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
        
        # Generate 1 and 0 carry options for third FA operation in parallel
        FA_binaryFourOptionOne, newCarryFourOpOne = FourBitFullAdder(binNumOne[numPointer - 20:numPointer - 16],
                                                                   binNumTwo[numPointer - 20:numPointer - 16], 1)
        FA_binaryFourOptionTwo, newCarryFourOpTwo = FourBitFullAdder(binNumOne[numPointer - 20:numPointer - 16],
                                                                   binNumTwo[numPointer - 20:numPointer - 16], 0)

        # Generate 1 and 0 carry options for third FA operation in parallel
        FA_binaryFiveOptionOne, newCarryFiveOpOne = FourBitFullAdder(binNumOne[numPointer - 24:numPointer - 20],
                                                                   binNumTwo[numPointer - 24:numPointer - 20], 1)
        FA_binaryFiveOptionTwo, newCarryFiveOpTwo = FourBitFullAdder(binNumOne[numPointer - 24:numPointer - 20],
                                                                   binNumTwo[numPointer - 24:numPointer - 20], 0)
        
        # Generate 1 and 0 carry options for third FA operation in parallel
        FA_binarySixOptionOne, newCarrySixOpOne = FourBitFullAdder(binNumOne[numPointer - 28:numPointer - 24],
                                                                   binNumTwo[numPointer - 28:numPointer - 24], 1)
        FA_binarySixOptionTwo, newCarrySixOpTwo = FourBitFullAdder(binNumOne[numPointer - 28:numPointer - 24],
                                                                   binNumTwo[numPointer - 28:numPointer - 24], 0)
        
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
        
        sumBin = MUX(FA_binaryFourOptionOne, FA_binaryFourOptionTwo, newCarry) + sumBin

        if newCarry:
            endCarry = newCarryFourOpOne
        else:
            endCarry = newCarryFourOpTwo
        
        sumBin = MUX(FA_binaryFiveOptionOne, FA_binaryFiveOptionTwo, newCarry) + sumBin

        if newCarry:
            endCarry = newCarryFiveOpOne
        else:
            endCarry = newCarryFiveOpTwo

        sumBin = MUX(FA_binarySixOptionOne, FA_binarySixOptionTwo, newCarry) + sumBin

        if newCarry:
            endCarry = newCarrySixOpOne
        else:
            endCarry = newCarrySixOpTwo
    else:
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
        
        # Generate 1 and 0 carry options for third FA operation in parallel
        FA_binaryFourOptionOne, newCarryFourOpOne = FourBitFullAdder(binNumOne[numPointer - 20:numPointer - 16],
                                                                   binNumTwo[numPointer - 20:numPointer - 16], 1)
        FA_binaryFourOptionTwo, newCarryFourOpTwo = FourBitFullAdder(binNumOne[numPointer - 20:numPointer - 16],
                                                                   binNumTwo[numPointer - 20:numPointer - 16], 0)

        # Generate 1 and 0 carry options for third FA operation in parallel
        FA_binaryFiveOptionOne, newCarryFiveOpOne = FourBitFullAdder(binNumOne[numPointer - 24:numPointer - 20],
                                                                   binNumTwo[numPointer - 24:numPointer - 20], 1)
        FA_binaryFiveOptionTwo, newCarryFiveOpTwo = FourBitFullAdder(binNumOne[numPointer - 24:numPointer - 20],
                                                                   binNumTwo[numPointer - 24:numPointer - 20], 0)
        
        # Generate 1 and 0 carry options for third FA operation in parallel
        FA_binarySixOptionOne, newCarrySixOpOne = FourBitFullAdder(binNumOne[numPointer - 28:numPointer - 24],
                                                                   binNumTwo[numPointer - 28:numPointer - 24], 1)
        FA_binarySixOptionTwo, newCarrySixOpTwo = FourBitFullAdder(binNumOne[numPointer - 28:numPointer - 24],
                                                                   binNumTwo[numPointer - 28:numPointer - 24], 0)
        
        # Generate 1 and 0 carry options for third FA operation in parallel
        FA_binarySevOptionOne, newCarrySevOpOne = FourBitFullAdder(binNumOne[numPointer - 32:numPointer - 28],
                                                                   binNumTwo[numPointer - 32:numPointer - 28], 1)
        FA_binarySevOptionTwo, newCarrySevOpTwo = FourBitFullAdder(binNumOne[numPointer - 32:numPointer - 28],
                                                                   binNumTwo[numPointer - 32:numPointer - 28], 0)        
        
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
        
        sumBin = MUX(FA_binaryFourOptionOne, FA_binaryFourOptionTwo, newCarry) + sumBin

        if newCarry:
            endCarry = newCarryFourOpOne
        else:
            endCarry = newCarryFourOpTwo
        
        sumBin = MUX(FA_binaryFiveOptionOne, FA_binaryFiveOptionTwo, newCarry) + sumBin

        if newCarry:
            endCarry = newCarryFiveOpOne
        else:
            endCarry = newCarryFiveOpTwo

        sumBin = MUX(FA_binarySixOptionOne, FA_binarySixOptionTwo, newCarry) + sumBin

        if newCarry:
            endCarry = newCarrySixOpOne
        else:
            endCarry = newCarrySixOpTwo

        sumBin = MUX(FA_binarySevOptionOne, FA_binarySevOptionTwo, newCarry) + sumBin

        if newCarry:
            endCarry = newCarrySevOpOne
        else:
            endCarry = newCarrySevOpTwo

    # sumBin.insert(0, endCarry)
    return sumBin, endCarry


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
def iterativeBase(A, B):
    # 2^n (ac) operation
    ac_0 = AND(A[2], B[2])
    ac_1, carryAC1 = XOR(AND(A[3], B[2]), AND(A[2], B[3])), AND(AND(A[3], B[2]), AND(A[2], B[3]))
    ac_2, carryAC2 = XOR(AND(A[3], B[3]), carryAC1), AND(AND(A[3], B[3]), carryAC1)
    ac_3 = carryAC2

    AC = [ac_3, ac_2, ac_1, ac_0]

    # 2 ^n/2 (ad + bc)
    ad_0 = AND(A[2], B[0])
    ad_1, carryAD1 = XOR(AND(A[3], B[0]), AND(A[2], B[1])), AND(AND(A[3], B[0]), AND(A[2], B[1]))
    ad_2, carryAD2 = XOR(AND(A[3], B[1]), carryAD1), AND(AND(A[3], B[1]), carryAD1)
    ad_3 = carryAD2

    AD = [ad_3, ad_2, ad_1, ad_0]

    bc_0 = AND(A[0], B[2])
    bc_1, carryBC1 = XOR(AND(A[1], B[2]), AND(A[0], B[3])), AND(AND(A[1], B[2]), AND(A[0], B[3]))
    bc_2, carryBC2 = XOR(AND(A[1], B[3]), carryBC1), AND(AND(A[1], B[3]), carryBC1)
    bc_3 = carryBC2

    BC = [bc_3, bc_2, bc_1, bc_0]

    # + bd
    bd_0 = AND(A[0], B[0])
    bd_1, carryBD1 = XOR(AND(A[1], B[0]), AND(A[0], B[1])), AND(AND(A[1], B[0]), AND(A[0], B[1]))
    bd_2, carryBD2 = XOR(AND(A[1], B[1]), carryBD1), AND(AND(A[1], B[1]), carryBD1)
    bd_3 = carryBD2

    BD = [bd_3, bd_2, bd_1, bd_0]

    # ADD BC + AD
    # with fast addition Carry Select Adder
    BC_AD, carryBCAD = FastAdderCarrySelect(BC, AD, 0)
    # 2^n/2 (add two 00)
    BC_AD = BC_AD + [0, 0]
    BC_AD = [carryBCAD] + BC_AD
    # Fast addition Carry Select Adder
    for _ in range(8-len(BC_AD)):
        BC_AD.insert(0, 0)

    # Put AC, BD in same register
    AC_BD = AC + BD
    # Add them together and return the result
    return FastAdderCarrySelect(AC_BD, BC_AD, 0)


# NEED TO FIX:
# ONCE FAST ADDER IS FIXED SHOULD BE WORKING WITH
# NEW FAST ADDER IMPLEMENTATION
# ITS TOO CONFUSING ATM WITH THE CARRY

# TODO: Rewrite iterativeMethod() 

# Using X * Y = 2^n(ac) + 2^(n/2)(ad + bc) + bd, we can simplify the algorithm
# 2^nX is the same as shifting a binary number, X, n spaces to the left
# Therefore, find AD, BC, BD, and AC and follow the equation 
def iterativeMethod(A, B, n):
    # Base case
    if n == 4:
        return iterativeBase(A, B)
    else:
        # Recursive call
        n_div_two = int(n / 2)
        # 2^n iter(ac, n/2)
        AC, AC_Carry = iterativeMethod(A[0:n_div_two], B[0:n_div_two], n_div_two)

        # 2^n/2 (iter(ad, n/2) + iter(bc, n/2)
        AD, AD_Carry = iterativeMethod(A[0:n_div_two], B[n_div_two:n], n_div_two)
        BC, BC_Carry = iterativeMethod(A[n_div_two:n], B[0:n_div_two], n_div_two)

        # Take care of AD and BC Carry
        AD = [0, 0, 0] + [AD_Carry] + AD
        BC = [0, 0, 0] + [BC_Carry] + BC

        AD_BC, ADBC_Carry = FastAdderCarrySelect(AD, BC, 0)
        AD_BC = AD_BC + [0, 0, 0, 0]

        # + iter(bd, n/2)
        BD, BD_Carry = iterativeMethod(A[n_div_two:n], B[n_div_two:n], n_div_two)

        # Fast adder

        AC_BD = AC + BD
        # Make sure to implement w/ carry

        return FastAdderCarrySelect(AC_BD, AD_BC, 0)

def summandMatrix(A: List[int], B: List[int]) -> List[List[int]]:
    num_length = len(A)
    columns = (2 * num_length) - 1
    append = []
    summand_matrix = []

    for i in range(num_length):
        if B[num_length - (1 + i)] == 0:
            append = [0] * columns
        else:
            append = [0] * ((num_length - 1) - i)
            for j in range(num_length):
                append.append(A[j])
            
            for j in range(i):
                append.append(0)
        
        summand_matrix.append(append)
        append = []

    return summand_matrix

def iterative(A: List[int], B: List[int]) -> List[int]:
    summand_matrix: List[List[int]] = []
    n: int = len(A)
    temp_int: int = 0

    # A * B = 2^n(ac) + 2^(n/2)(ad + bc) + bd
    ad: List[List[int]] = []
    bd: List[List[int]] = []
    ac: List[List[int]] = []
    bc: List[List[int]] = []

    ad_bin: List[int] = []
    bd_bin: List[int] = []
    ac_bin: List[int] = []
    bc_bin: List[int] = []
    adbc_bin: List[int] = []
    temp_bin: List[int] = []
    return_bin: List[int] = []

    # Helps populate summand_matrix
    append: List[int] = []

    ac_shift: List[int] = []
    adbc_shift: List[int] = []

    # Length of the numbers needs to be divisible by 2
    # If a number is not divisible by 2, adding 1 will ALWAYS make it divisible by 2
    # Adding 0 to beginning of binary number does not change its value
    if n % 2 != 0:
        A.insert(0, 0)
        B.insert(0, 0)
        n += 1
    
    # Create summand matrix from input
    summand_matrix = summandMatrix(A, B)

    # Filling ad, bd, ac, bc from summand_matrix
    for i in range((n // 2)):
        append = [0] * ((n // 2) - i - 1)

        for j in range((n // 2)):
            append.append(summand_matrix[i][((n - 1) + ((n // 2) + j - i))])

        for j in range(i):
            append.append(0)

        bd.append(append)
        append = []

    for i in range((n // 2)):
        append = [0] * ((n // 2) - i - 1)

        for j in range((n // 2)):
            append.append(summand_matrix[i][((n - 1) - i + j)])

        for j in range(i):
            append.append(0)

        ad.append(append)
        append = []

    for i in range((n // 2)):
        append = [0] * ((n // 2) - i - 1)

        for j in range((n // 2)):
            append.append(summand_matrix[(i + (n // 2))][((n - (n // 2) - 1) - i + j)])

        for j in range(i):
            append.append(0)

        ac.append(append)
        append = []

    for i in range((n // 2)):
        append = [0] * ((n // 2) - i - 1)

        for j in range((n // 2)):
            append.append(summand_matrix[(i + (n // 2))][((n - 1) + (j - i))])

        for j in range(i):
            append.append(0)

        bc.append(append)
        append = []
        
    
    if len(ad[0]) % 4 != 0:
        for i in range(len(ad)):
            for _ in range(4 - (len(ad[i]) % 4)):
                ad[i].insert(0, 0)
                ac[i].insert(0, 0)
                bc[i].insert(0, 0)
                bd[i].insert(0, 0)
    
    temp_bin = ad[0]
    for i in range(len(ad) - 1):
        temp_bin, temp_int = FastAdderCarrySelect(temp_bin, ad[i + 1], temp_int)
    ad_bin = temp_bin
    
    if temp_int == 1:
        ad.insert(0, 1)
        temp_int = 0

    temp_bin = ac[0]
    for i in range(len(ad) - 1):
        temp_bin, temp_int = FastAdderCarrySelect(temp_bin, ac[i + 1], temp_int)
    ac_bin = temp_bin

    if temp_int == 1:
        ac.insert(0, 1)
        temp_int = 0

    temp_bin = bd[0]
    for i in range(len(ad) - 1):
        temp_bin, temp_int = FastAdderCarrySelect(temp_bin, bd[i + 1], temp_int)
    bd_bin = temp_bin

    if temp_int == 1:
        bd.insert(0, 1)
        temp_int = 0

    temp_bin = bc[0]
    for i in range(len(ad) - 1):
        temp_bin, temp_int = FastAdderCarrySelect(temp_bin, bc[i + 1], temp_int)
    bc_bin = temp_bin

    if temp_int == 1:
        bc.insert(0, 1)
        temp_int = 0

    adbc_bin, temp_int = FastAdderCarrySelect(ad_bin, bc_bin, 0)

    if temp_int == 1:
        adbc_bin.insert(0, 1)
        temp_int = 0

    ac_shift = SHIFTL(ac_bin, n)
    adbc_shift = SHIFTL(adbc_bin, (n // 2))

    if len(ac_shift) % 4 != 0:
        for _ in range(4 - (len(ac_shift) % 4)):
            ac_shift.insert(0, 0)
    
    while len(adbc_shift) != len(ac_shift):
        adbc_shift.insert(0, 0)

    while len(bd_bin) != len(ac_shift):
        bd_bin.insert(0, 0)
    
    temp_bin = []
    temp_bin, temp_int = FastAdderCarrySelect(ac_shift, adbc_shift, 0)
    return_bin, temp_int = FastAdderCarrySelect(temp_bin, bd_bin, temp_int)

    if temp_int == 1:
        return_bin.insert(0, 1)
    
    # Test
    # print("AD")
    # for list in ad:
    #     print(list)
    # print("BD")
    # for list in bd:
    #     print(list)
    # print("AC")
    # for list in ac:
    #     print(list)
    # print("BC")
    # for list in bc:
    #     print(list)

    # print("\nBIN AD")
    # print(ad_bin)
    # print("\nBIN BD")
    # print(bd_bin)
    # print("\nBIN AC")
    # print(ac_bin)
    # print("\nBIN BC")
    # print(bc_bin)
    # print("AC_SHIFT")
    # print(ac_shift)

    return return_bin


# AND Operation
# Input: Two Bits
# Output: 1 or 0
def AND(bitOne: int, bitTwo: int) -> Literal[0, 1]:
    if bitOne == 1 and bitTwo == 1:
        return 1
    else:
        return 0
    

# NAND Operation
# Input: Two Bits
# Output: 1 or 0
def NAND(bitOne: int, bitTwo: int) -> Literal[0, 1]:
    if bitOne == 1 and bitTwo == 1:
        return 0
    else:
        return 1


# OR Operation
# Input: Two Bits
# Output: 1 or 0
def OR(bitOne: int, bitTwo: int) -> Literal[0, 1]:
    if bitOne or bitTwo:
        return 1
    else:
        return 0


# XOR Operation
# Input: Two Bits
# Output: 1 or 0
def XOR(bitOne: int, bitTwo: int) -> Literal[0, 1]:
    return AND(OR(bitOne, bitTwo), NAND(bitOne, bitTwo))


# Shift AQ
def shiftAQ(AQ: List[int]) -> List[int]:
    for i in range(len(AQ) - 1, 0, -1):
        AQ[i] = AQ[i - 1]
    AQ[0] = 0
    return AQ

# Shift Left
# Input: Binary number and number of shifts
# Output: Binary number shifted num_shifts to the left
def SHIFTL(binary_number: List[int], num_shifts: int) -> List[int]:
    # IDK if Python does pass-by-reference or if the inputted list is copied, so
    to_return: List[int] = binary_number
    for _ in range(num_shifts):
        to_return.append(0)
    
    return to_return

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

if __name__ == "__main__":
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
    #
    # print(test_add_one, '+', test_add_two, '=')
    # print(FastAdderCarrySelect(test_add_one, test_add_two, 0))
    #
    #
    # print(test_add_three, '+', test_add_four, '=')
    # print(FastAdderCarrySelect(test_add_three, test_add_four, 0))
    #
    # print(test_add_five, '+', test_add_six, '=')
    # print(FastAdderCarrySelect(test_add_five, test_add_six, 0))
    #
    # print(test_add_seven, '+', test_add_eight, '=')
    # print(FastAdderCarrySelect(test_add_seven, test_add_eight, 0))

    # Testing Add and Shift and Iterative Method correctness with two 12-bit numbers
    # print(test_add_seven, '*', test_add_eight, '=')
    # print("Add and Shift    -", add_and_shift(test_add_seven, test_add_eight))
    # print("Iterative Method -", iterativeMethod(test_add_seven, test_add_eight, 16))

    # Testing matrix of summands
    print("Matrix of summands:", test_add_one, "*", test_add_two)
    print(iterative(test_add_one, test_add_two))
    print(add_and_shift(test_add_one, test_add_two))

    print("\nMatrix of summands:", test_add_three, "*", test_add_four)
    print(iterative(test_add_three, test_add_four))
    print(add_and_shift(test_add_three, test_add_four))

    print("\nMatrix of summands:", test_add_five, "*", test_add_six)
    print(iterative(test_add_five, test_add_six))
    print(add_and_shift(test_add_five, test_add_six))

    print("\nMatrix of summands:", test_add_seven, "*", test_add_eight)
    print(iterative(test_add_seven, test_add_eight))
    print(add_and_shift(test_add_seven, test_add_eight))