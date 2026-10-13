from controlUnit import ControlUnit
from processingUnit import ProcessingUnit
from programCounter import ProgramCounter
from memory import InstructionMemory
from memory import DataMemory
from registerFile import RegisterFile
from alu import ALU
from pipeline import Pipeline

class CPU:

    def __init__(self, processing_unit, control_unit):
        self.processing_unit = processing_unit
        self.control_unit = control_unit
        self.cycles = 0


def main():
    # Control Unity creation
    control_unit = ControlUnit()

    # Processing Unity creation
    instr_mem = InstructionMemory()
    instr_mem.read_program("programs/programa_prueba.txt")
    instr_mem.print_mem()

    processing_unit = ProcessingUnit(ProgramCounter(),
                        instr_mem,
                        DataMemory(),
                        RegisterFile(),
                        ALU(),
                        Pipeline())

    # Central Processing Unity creation
    cpu = CPU(processing_unit, control_unit)

    i = 0
    while processing_unit.pc.get_value() is not None: # cambiar a wb (esta en if)
        
        processing_unit.write_back()
        (ex_mem_copy, control_signals_ex) = processing_unit.execute()
        processing_unit.memory_access()
        processing_unit.upload_ex_mem_reg(ex_mem_copy)
        (alu_type_op, control_signals_id) = processing_unit.instruction_decode()
        processing_unit.instruction_fetch(True, None)
        
        
        processing_unit.print_execution()

        
        input()

main()