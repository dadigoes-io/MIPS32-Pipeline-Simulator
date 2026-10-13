from alu import ALU
from enums import ALUOperation

class CPU:

    def __init__(self, up, uc, cycles):
        self.up = up
        self.uc = uc
        cycles = 0


def main():

    print(f"5 sub 10 = {ALU.operation(5, 10, ALUOperation.SUB)}")
    print(f"-2 slt 1 = {ALU.operation(-2, 1, ALUOperation.SLT)}")


main()