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

    def run(self):
        alu_type_op = None

        while not self.processing_unit.is_finished():

            # WB
            self.processing_unit.write_back()

            # EX execution without store
            (ex_mem_copy, jump_address) = self.processing_unit.execute(self.control_unit)

            # MEM
            self.processing_unit.memory_access()
            if not self.processing_unit.get_pipeline().get_mem_wb_pr().is_empty():
                self.control_unit.mem_to_wb()
            else:
                self.control_unit.flush_mem_wb()

            # EX upload Registers
            self.processing_unit.update_ex_mem_reg(ex_mem_copy)
            if not self.processing_unit.get_pipeline().get_ex_mem_pr().is_empty():
                self.control_unit.ex_to_mem()
            else:
                self.control_unit.flush_ex_mem()
            
            # ID
            (alu_type_op, control_signals_id) = self.processing_unit.instruction_decode()
            if not self.processing_unit.get_pipeline().get_id_ex_pr().is_empty():
                self.control_unit.id_to_ex(control_signals_id, alu_type_op)
            else:
                self.control_unit.flush_id_ex()

            # IF
            pc_src = (self.control_unit.get_ex_mem_control()["Jump"] or
                     (self.control_unit.get_ex_mem_control()["Branch"] and jump_address != None))
            
            self.processing_unit.instruction_fetch(pc_src, jump_address)
            
            # Print execution
            self.processing_unit.print_execution()
            
            input()

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

    cpu.run()

main()