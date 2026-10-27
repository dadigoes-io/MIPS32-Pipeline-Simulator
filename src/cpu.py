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
        cycle = 0

        # Print execution
        self.processing_unit.print_execution(cycle)

        while not self.processing_unit.is_finished():

            cycle+=1
            stall_signal = False
            
            # WB
            self.processing_unit.write_back(self.control_unit)

            # EX execution without store
            (ex_mem_copy, jump_address) = self.processing_unit.execute(self.control_unit)

            # MEM
            result_mem, reg_dst_mem = self.processing_unit.memory_access(self.control_unit)
            if not self.processing_unit.get_pipeline().get_mem_wb_pr().is_empty():
                self.control_unit.mem_to_wb()
            else:
                self.control_unit.flush_mem_wb()

            # EX upload Registers
            result_ex, reg_dst_ex = self.processing_unit.update_ex_mem_reg(ex_mem_copy)
            if not self.processing_unit.get_pipeline().get_ex_mem_pr().is_empty():
                self.control_unit.ex_to_mem()
            else:
                self.control_unit.flush_ex_mem()
            
            # ID
            if jump_address is not None:
                # flush instrs after active conditional jump
                self.processing_unit.get_pipeline().get_id_ex_pr().set_empty(True)
                self.control_unit.flush_id_ex()
            else:
                stall_signal = self.processing_unit.instruction_decode(self.control_unit,
                                                        result_ex,
                                                        reg_dst_ex,
                                                        result_mem,
                                                        reg_dst_mem)

            # IF
            pc_src = (jump_address is not None)
            
            self.processing_unit.instruction_fetch(pc_src, jump_address, stall_signal)

            # Print execution
            self.processing_unit.print_execution(cycle)
        
            input()

def main():
    # Control Unity creation
    control_unit = ControlUnit()

    # Processing Unity creation
    instr_mem = InstructionMemory()
    instr_mem.read_program("programs/programa_Practica2.txt")
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