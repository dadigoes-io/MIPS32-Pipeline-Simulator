from controlUnit import ControlUnit
from processingUnit import ProcessingUnit
from programCounter import ProgramCounter
from memory import InstructionMemory
from memory import DataMemory
from registerFile import RegisterFile
from alu import ALU
from pipeline import Pipeline

class CPU:

    def __init__(self, up, uc):
        self.up = up
        self.uc = uc
        self.cycles = 0


def main():
    # Unidad de control
    uc = ControlUnit()

    # Unidad de procesamiento
    instr_mem = InstructionMemory()
    instr_mem.read_program("programs/programa_Practica2.txt")
    instr_mem.printMem()

    up = ProcessingUnit(ProgramCounter(),
                        instr_mem,
                        DataMemory(),
                        RegisterFile(),
                        ALU(),
                        Pipeline())

    # Unidad Central de Procesamiento
    cpu = CPU(up, uc)

main()