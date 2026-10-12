from enum import Enum

class InstructionType(Enum):
    ARITHMETIC_LOGIC = 1
    LOAD = 2
    STORE = 3
    BRANCH = 4
    JUMP = 5


class ALUOperation(Enum):
    ADD = 1
    SUB = 2
    AND = 3
    OR = 4
    XOR = 5
    SLT = 6