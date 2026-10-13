from programCounter import ProgramCounter
from memory import *
from registerFile import RegisterFile
from alu import ALU
from pipeline import *
from enums import *

class ProcessingUnit:

    def __init__(self, program_counter: ProgramCounter, instruction_mem: InstructionMemory, data_mem: DataMemory, register_file: RegisterFile, alu: ALU, pipeline: Pipeline):
        self.pc = program_counter
        self.instruction_mem = instruction_mem
        self.data_mem = data_mem
        self.register_file = register_file
        self.alu = alu
        self.pipeline = pipeline

    def instruction_fetch(self, pc_src, jump_dir):
        # Note: jump_dir not implemented yet
        
        # Load pc and IF_ID Register
        pc = self.pc.get_value() if pc_src else jump_dir
        
        if_id_reg = self.pipeline.get_if_id_pr()

        # For printing
        self.pipeline.get_if_id_pr().set_instr_pc(pc)
        #if_id_reg.set_next_pc(pc)


        if pc is not None:
            
            # Store Instruction in IF_ID_Register
            if_id_reg.set_instr(
                self.instruction_mem.read(pc)
            )

            # Add PC + 4 AND store in IF_ID_Register
            if_id_reg.set_next_pc(
                self.pc.add_four()
            )

            # Check PC in bounds 
            if self.instruction_mem.dir_out_of_bonds(self.pc.get_value()):
                self.pc.set_value(None)

    def instruction_decode(self):
        instr = self.pipeline.get_if_id_pr().get_instr()

        alu_type_op = None
        control_signals = None

        if instr is not None:
            instr = instr.split()
            opcode = instr[0]

            match opcode:
                case "lw":
                    alu_type_op = ALUOperation.ADD
                    op1 = None
                    op2 = instr[2]
                    reg_dest = instr[1][:-1]
                    address_value = None

                case "sw":
                    alu_type_op = ALUOperation.ADD

                case "beq" | "bne":
                    alu_type_op = ALUOperation.SUB    

                case ("add" | "addi"):
                    alu_type_op = ALUOperation.ADD

                case ("sub" | "subi"):
                    alu_type_op = ALUOperation.SUB

                case "and":
                    alu_type_op = ALUOperation.AND

                case "or":
                    alu_type_op = ALUOperation.OR

                case "xor":
                    alu_type_op = ALUOperation.XOR

                case ("slt" | "slti"):
                    alu_type_op = ALUOperation.SLT

                case "j":
                    alu_type_op = None
                

            # For printing
            self.pipeline.get_id_ex_pr().set_instr_pc(
                self.pipeline.get_if_id_pr().get_instr_pc()
            )

        return (alu_type_op, control_signals)
        
    def execute(self):

        ex_mem_copy = {
            "alu_result": None,
            "store_data": None,
            "reg_dst": None,
            "instr_pc": self.pipeline.get_id_ex_pr().get_instr_pc()
        }

        control_signals = None

        return (ex_mem_copy, control_signals)
     

    def memory_access(self):


        # For printing
        self.pipeline.get_mem_wb_pr().set_instr_pc(
            self.pipeline.get_ex_mem_pr().get_instr_pc()
        )

    def write_back(self):
        print("")

    def upload_ex_mem_reg(self, ex_mem_copy):
        self.pipeline.get_ex_mem_pr().set_instr_pc(ex_mem_copy["instr_pc"])


    def print_execution(self):
        print("====================")
        pc = self.pipeline.get_if_id_pr().get_instr_pc()
        print(f"IF_ID:\n\t{pc} : {self.instruction_mem.read(pc)}")

        pc = self.pipeline.get_id_ex_pr().get_instr_pc()
        print(f"ID_EX:\n\t{pc} : {self.instruction_mem.read(pc)}")

        pc = self.pipeline.get_ex_mem_pr().get_instr_pc()
        print(f"EX_MEM:\n\t{pc} : {self.instruction_mem.read(pc)}")

        pc = self.pipeline.get_mem_wb_pr().get_instr_pc()
        print(f"MEM_WB:\n\t{pc} : {self.instruction_mem.read(pc)}")