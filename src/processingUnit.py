from programCounter import ProgramCounter
from memory import *
from registerFile import RegisterFile
from alu import ALU
from pipeline import *

class ProcessingUnit:

    def __init__(self, program_counter: ProgramCounter, instruction_mem: InstructionMemory, data_mem: DataMemory, register_file: RegisterFile, alu: ALU, pipeline: Pipeline):
        self.pc = program_counter
        self.instruction_mem = instruction_mem
        self.data_mem = data_mem
        self.register_file = register_file
        self.alu = alu
        self.pipeline = pipeline

    def instruction_fetch(self, pc_src, jump_dir):

        if pc_src:
            pc = self.pc.get_value()
        else:
            pc = jump_dir   # Not implemented yet

        # Store Instruction in IF_ID_Register
        self.pipeline.get_if_id_pr().set_instr(
            self.instruction_mem.read(self.pc.get_value())
        )

        # Add PC + 4 AND store in IF_ID_Register
        self.pipeline.get_if_id_pr().set_next_pc(
            self.pc.add_four()
        )
        

    def instruction_decode(self):
        print()

    def execute(self):
        print("hola")

    def memory_access(self):
        print("hola")

    def write_back(self):
        print("hola")