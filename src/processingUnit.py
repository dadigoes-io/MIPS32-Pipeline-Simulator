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

        if not self.instruction_mem.dir_out_of_bonds(pc):

            self.pipeline.get_if_id_pr().upload_reg(
                self.pc.add_four(),
                self.instruction_mem.read(pc),
            )

        else:
            self.pipeline.get_if_id_pr().set_empty(True)

        # For printing
        self.pipeline.get_if_id_pr().set_instr_pc(pc)
        #if_id_reg.set_next_pc(pc)

    def instruction_decode(self):

        if self.pipeline.get_if_id_pr().is_empty():
            self.pipeline.get_id_ex_pr().set_empty(True)
            alu_type_op = None
            control_signals = None
            
        else:
            instr = self.pipeline.get_if_id_pr().get_instr()
            instr = instr.split()

            opcode = instr[0]

            match opcode:
                case "lw":
                    # lw $dest, offset($base)
                    offset, base = instr[2].split("(")

                    alu_type_op = ALUOperation.ADD
                    reg_dst = instr[1].split(",")   # $dest
                    op_1 = base.rstrip(")")          # $base
                    op_2 = None
                    address_value = offset          # offset

                    control_signals = {
                        # ID_EX
                        "ALUSrc" : True,
                        "Jump" : False,
                        # EX_MEM
                        "Branch" : False,
                        "MemWrite": False,
                        "MemRead": True,
                        "Zero": False,
                        # MEM_WB
                        "MemtoReg" : True,
                        "RegWrite": True,
                        "RegDst" : True
                    }

                case "sw":
                    # sw $source, offset($base)
                    offset, base = instr[2].split("(")

                    alu_type_op = ALUOperation.ADD
                    reg_dst = None
                    op_1 = base.rstrip(")")          # $base
                    op_2 = instr[1]                  # $source
                    address_value = offset          # offset

                    control_signals = {
                        # ID_EX
                        "ALUSrc" : True,
                        "Jump" : False,
                        # EX_MEM
                        "Branch" : False,
                        "MemWrite": True,
                        "MemRead": False,
                        "Zero": False,
                        # MEM_WB
                        "MemtoReg" : False,
                        "RegWrite": True,
                        "RegDst" : True
                    }
            
                case "beq" | "bne":
                    # beq  $op1, $op2, address_value
                    alu_type_op = ALUOperation.SUB 

                    reg_dst = None
                    op_1 = instr[1].rstrip(",")
                    op_2 = instr[2].rstrip(",")
                    address_value = instr[3]

                    control_signals = {
                        # ID_EX
                        "ALUSrc" : False,
                        # EX_MEM
                        "Branch" : True,
                        "BranchN" : False,
                        "MemWrite": False,
                        "MemRead": False,
                        "Zero": False,  # Upload in ex()
                    }
                    if opcode == "bne":
                        control_signals["BranchN"] = True

                case ("addi"| "subi" | "slti"):
                    # addi $dest, $op1, i

                    match opcode:
                        case "addi":
                            alu_type_op = ALUOperation.ADD
                        case "subi":
                            alu_type_op = ALUOperation.SUB
                        case "slti":
                            alu_type_op = ALUOperation.SLT
                    
                    reg_dst = instr[1].rstrip(",")
                    op_1 = instr[2].rstrip(",")
                    op_2 = None
                    address_value = instr[3]

                    control_signals = {
                        # ID_EX
                        "ALUSrc" : True,
                        "Jump" : False,
                        # EX_MEM
                        "Branch" : False,
                        "MemWrite": True,
                        "MemRead": False,
                        "Zero": False,
                        # MEM_WB
                        "MemtoReg" : False,
                        "RegWrite": True,
                        "RegDst" : True
                    }

                case ("add" | "sub" | "and" | "or" | "xor" | "slt"):
                    # and $dest, $op1, op2

                    match opcode:
                        case "add":
                            alu_type_op = ALUOperation.ADD
                        case "sub":
                            alu_type_op = ALUOperation.SUB
                        case "and":
                            alu_type_op = ALUOperation.AND
                        case "or":
                            alu_type_op = ALUOperation.OR
                        case "xor":
                            alu_type_op = ALUOperation.OR
                        case "slt":
                            alu_type_op = ALUOperation.OR

                    reg_dst = instr[1].rstrip(",")
                    op_1 = instr[2].rstrip(",")
                    op_2 = instr[3]
                    address_value = None

                    control_signals = {
                        # ID_EX
                        "ALUSrc" : False,
                        "Jump" : False,
                        # EX_MEM
                        "Branch" : False,
                        "MemWrite": True,
                        "MemRead": False,
                        "Zero": False,
                        # MEM_WB
                        "MemtoReg" : False,
                        "RegWrite": True,
                        "RegDst" : True
                    }

                case "j":
                    # j address_value
                    alu_type_op = None 

                    reg_dst = None
                    op_1 = None
                    op_2 = None
                    address_value = instr[1]

                    control_signals = {
                        # ID_EX
                        "ALUSrc" : False,
                        "Jump" : True
                    }

            # Update ID_EX Register
            self.pipeline.get_id_ex_pr().upload_reg(reg_dst, op_1, op_2, address_value)

        # For printing
        self.pipeline.get_id_ex_pr().set_instr_pc(
            self.pipeline.get_if_id_pr().get_instr_pc()
        )

        return (alu_type_op, control_signals)
        
    def execute(self):
        if self.pipeline.get_id_ex_pr().is_empty():
            ex_mem_copy = {
                "alu_result": None,
                "store_data": None,
                "reg_dst": None,
                "empty": True,
                "instr_pc": self.pipeline.get_id_ex_pr().get_instr_pc()
            }
            control_signals = None

        else:
            ex_mem_copy = {
                "alu_result": None,
                "store_data": None,
                "reg_dst": None,
                "empty": False,
                "instr_pc": self.pipeline.get_id_ex_pr().get_instr_pc()
            }
            control_signals = None

        return (ex_mem_copy, control_signals)
     
    def memory_access(self):
        if self.pipeline.get_ex_mem_pr().is_empty():
            self.pipeline.get_mem_wb_pr().set_empty(True)

        else:
            self.pipeline.get_mem_wb_pr().set_empty(False)

        # For printing
        self.pipeline.get_mem_wb_pr().set_instr_pc(
            self.pipeline.get_ex_mem_pr().get_instr_pc()
        )

    def write_back(self):
        if not self.pipeline.get_mem_wb_pr().is_empty():
            print("")

    def is_finished(self):
        # Check PC in bounds 
        return (
            self.instruction_mem.dir_out_of_bonds(self.pc.get_value()) &
            self.pipeline.get_if_id_pr().is_empty() &
            self.pipeline.get_id_ex_pr().is_empty() &
            self.pipeline.get_ex_mem_pr().is_empty() &
            self.pipeline.get_mem_wb_pr().is_empty()
        )

    def upload_ex_mem_reg(self, ex_mem_copy):
        self.pipeline.get_ex_mem_pr().upload_reg(
            ex_mem_copy["reg_dst"],
            ex_mem_copy["alu_result"],
            ex_mem_copy["store_data"],
            ex_mem_copy["empty"]
        )
        # For printing
        self.pipeline.get_ex_mem_pr().set_instr_pc(
            self.pipeline.get_id_ex_pr().get_instr_pc()
        )

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