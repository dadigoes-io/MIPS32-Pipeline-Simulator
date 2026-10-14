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

    processing_unit = ProcessingUnit(
        ProgramCounter(),
        instr_mem,
        DataMemory(),
        RegisterFile(),
        ALU(),
        Pipeline()
    )

    # Central Processing Unity creation
    cpu = CPU(processing_unit, control_unit)

    alu_type_op = None

    while not processing_unit.is_finished():

        # WB
        processing_unit.write_back()

        # EX execution without store
        (ex_mem_copy, control_signals_ex, jump_address) = processing_unit.execute(control_unit)

        # MEM
        processing_unit.memory_access()
        control_unit.mem_to_wb()

        # EX upload Registers
        processing_unit.upload_ex_mem_reg(ex_mem_copy)
        control_unit.ex_to_mem()
        
        # ID
        (alu_type_op, control_signals_id) = processing_unit.instruction_decode()
        control_unit.id_to_ex(control_signals_id, alu_type_op)

        # IF
        processing_unit.instruction_fetch(control_unit.get_id_ex_control()["Jump"], jump_address)
        
        # Print execution
        processing_unit.print_execution()
        
        input()

main()