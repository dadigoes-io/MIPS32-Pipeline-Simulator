from programCounter import ProgramCounter
from memory import *
from registerFile import RegisterFile
from alu import ALU
from pipeline import *
from enums import *
from controlUnit import ControlUnit
from forwardingUnit import ForwardingUnit
from hazardDetectionUnit import HazardDetectionUnit

class ProcessingUnit:

    def __init__(self, program_counter: ProgramCounter, instruction_mem: InstructionMemory, data_mem: DataMemory, register_file: RegisterFile, alu: ALU, pipeline: Pipeline):
        self.pc = program_counter
        self.instruction_mem = instruction_mem
        self.data_mem = data_mem
        self.register_file = register_file
        self.alu = alu
        self.pipeline = pipeline
        self.raw_list = []

    def instruction_fetch(self, pc_src, jump_address, stall_signal):

        if not stall_signal:
            # Load pc from IF_ID Register
            pc_aux =  jump_address if pc_src else self.pc.get_value()

            if pc_src:
                self.pc.set_value(pc_aux)
            
            if not self.instruction_mem.is_out_of_bounds(pc_aux):

                self.pipeline.get_if_id_pr().update_reg(
                    self.pc.add_four(),
                    self.instruction_mem.read(pc_aux)
                )
                # For printing
                self.pipeline.get_if_id_pr().set_instr_pc(pc_aux)
                #if_id_reg.set_next_pc(pc)

            else:
                self.pipeline.get_if_id_pr().set_empty(True)

        

    def instruction_decode(self, control_unit: ControlUnit, result_ex, reg_dst_ex, result_mem, reg_dst_mem):

        if self.pipeline.get_if_id_pr().is_empty():
            self.pipeline.get_id_ex_pr().set_empty(True)
            control_unit.flush_id_ex()
            return False

        else:
            instr = self.pipeline.get_if_id_pr().get_instr()
            instr = instr.split()

            opcode = instr[0]

            match opcode:
                case "lw":
                    # lw $dest, offset($base)
                    offset, base = instr[2].split("(")

                    # For Forwarding Unit
                    op_1_reg = base.rstrip(")")
                    op_2_reg = None

                    # Load registers from Register File
                    alu_type_op = ALUOperation.ADD
                    reg_dst = instr[1].rstrip(",")   # $dest
                    op_1_val = self.register_file.load_value(op_1_reg)         # $base
                    op_2_val = None
                    address_value = int(offset)          # offset

                    control_signals = {
                        # ID_EX
                        "ALUSrc" : True,
                        # EX_MEM
                        "Jump" : False,
                        "Branch" : False,
                        "BranchN" : False,
                        "MemWrite": False,
                        "MemRead": True,
                        # MEM_WB
                        "MemtoReg" : True,
                        "RegWrite": True,
                        "RegDst" : True
                    }

                case "sw":
                    # sw $source, offset($base)
                    offset, base = instr[2].split("(")

                    # For Forwarding Unit
                    op_1_reg = base.rstrip(")")
                    op_2_reg = instr[1].rstrip(",")
                    
                    alu_type_op = ALUOperation.ADD
                    reg_dst = None
                    op_1_val = self.register_file.load_value(op_1_reg)          # $base
                    op_2_val = self.register_file.load_value(op_2_reg)                 # $source
                    address_value = int(offset)          # offset

                    

                    control_signals = {
                        # ID_EX
                        "ALUSrc" : True,
                        # EX_MEM
                        "Jump" : False,
                        "Branch" : False,
                        "BranchN" : False,
                        "MemWrite": True,
                        "MemRead": False,
                        # MEM_WB
                        "MemtoReg" : False,
                        "RegWrite": False,
                        "RegDst" : True
                    }
            
                case "beq" | "bne":
                    # beq  $op1, $op2, address_value
                    alu_type_op = ALUOperation.SUB

                    # For Forwarding Unit
                    op_1_reg = instr[1].rstrip(",")
                    op_2_reg = instr[2].rstrip(",")

                    reg_dst = None
                    op_1_val = self.register_file.load_value(op_1_reg)
                    op_2_val = self.register_file.load_value(op_2_reg)
                    address_value = int(instr[3])

                    control_signals = {
                        # ID_EX
                        "ALUSrc" : False,
                        # EX_MEM
                        "Jump" : False,
                        "Branch" : True,
                        "BranchN" : False,
                        "MemWrite": False,
                        "MemRead": False,
                        # MEM_WB
                        "MemtoReg" : False,
                        "RegWrite": False,
                        "RegDst" : False
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

                    # For Forwarding Unit
                    op_1_reg = instr[2].rstrip(",")
                    op_2_reg = None

                    # Load registers from Register File
                    reg_dst = instr[1].rstrip(",")
                    op_1_val = self.register_file.load_value(op_1_reg)
                    op_2_val = None
                    address_value = int(instr[3])

                    control_signals = {
                        # ID_EX
                        "ALUSrc" : True,
                        # EX_MEM
                        "Jump" : False,
                        "Branch" : False,
                        "BranchN" : False,
                        "MemWrite": False,
                        "MemRead": False,
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
                            alu_type_op = ALUOperation.XOR
                        case "slt":
                            alu_type_op = ALUOperation.SLT

                    # For Forwarding Unit
                    op_1_reg = instr[2].rstrip(",")
                    op_2_reg = instr[3]

                    # Load registers from Register File
                    reg_dst = instr[1].rstrip(",")
                    op_1_val = self.register_file.load_value(op_1_reg)
                    op_2_val = self.register_file.load_value(op_2_reg)
                    address_value = None

                    control_signals = {
                        # ID_EX
                        "ALUSrc" : False,
                        # EX_MEM
                        "Jump" : False,
                        "Branch" : False,
                        "BranchN" : False,
                        "MemWrite": False,
                        "MemRead": False,
                        # MEM_WB
                        "MemtoReg" : False,
                        "RegWrite": True,
                        "RegDst" : True
                    }

                case "j":
                    # j address_value
                    alu_type_op = ALUOperation.ADD 

                    # For Forwarding Unit
                    op_1_reg = None
                    op_2_reg = None

                    reg_dst = None
                    op_1_val = None
                    op_2_val = None
                    address_value = int(instr[1])

                    control_signals = {
                        # ID_EX
                        "ALUSrc" : False,
                        # EX_MEM
                        "Jump" : True,
                        "Branch" : False,
                        "BranchN" : False,
                        "MemWrite": False,
                        "MemRead": False,
                        # MEM_WB
                        "MemtoReg" : False,
                        "RegWrite": False,
                        "RegDst" : False 
                    }

            # Hazard detection
            is_raw_ex, is_load_raw = HazardDetectionUnit.is_raw_ex(op_1_reg, op_2_reg, reg_dst_ex, control_unit.get_ex_mem_control())
            if is_raw_ex:
                self.raw_list.append((self.pipeline.get_if_id_pr().get_instr_pc(),
                                      self.pipeline.get_ex_mem_pr().get_instr_pc()))    # Corresponds to executed ex 

            if HazardDetectionUnit.is_raw_mem(op_1_reg, op_2_reg, reg_dst_mem, control_unit.get_mem_wb_control()):
                self.raw_list.append((self.pipeline.get_if_id_pr().get_instr_pc(),
                                      self.pipeline.get_mem_wb_pr().get_instr_pc()))    # Corresponds to executed mem

            if is_load_raw:
                self.pipeline.get_id_ex_pr().set_empty(True)
                control_unit.flush_id_ex()
                # For printing
                self.pipeline.get_id_ex_pr().set_instr_pc(
                    self.pipeline.get_if_id_pr().get_instr_pc()
                )
                return True

            # Forwarding
            if ForwardingUnit.is_raw(op_1_reg, reg_dst_ex, control_unit.get_ex_mem_control()): 
                op_1_val = result_ex
            elif ForwardingUnit.is_raw(op_1_reg, reg_dst_mem, control_unit.get_mem_wb_control()):
                op_1_val = result_mem

            if ForwardingUnit.is_raw(op_2_reg, reg_dst_ex, control_unit.get_ex_mem_control()):
                op_2_val = result_ex
            elif ForwardingUnit.is_raw(op_2_reg, reg_dst_mem, control_unit.get_mem_wb_control()):
                op_2_val = result_mem         
            
            # Update ID_EX Register
            self.pipeline.get_id_ex_pr().update_reg(reg_dst, op_1_val, op_2_val, address_value)

            # For printing
            self.pipeline.get_id_ex_pr().set_instr_pc(
                self.pipeline.get_if_id_pr().get_instr_pc()
            )

            control_unit.id_to_ex(control_signals, alu_type_op)

            return False        

    def execute(self, control_unit: ControlUnit):

        ex_mem_copy = {
            "alu_result": None,
            "store_data": None,
            "reg_dst": None,
            "empty": True,
            "instr_pc": self.pipeline.get_id_ex_pr().get_instr_pc()
        }

        if self.pipeline.get_id_ex_pr().is_empty():
            return  ex_mem_copy, None
        
        else:

            control = control_unit.get_id_ex_control()
            id_ex_reg = self.pipeline.get_id_ex_pr()

            if control["Jump"]:
                jump_address = self.alu.operation(int(id_ex_reg.get_address_value()),
                                                  int(id_ex_reg.get_instr_pc()),
                                                  ALUOperation.ADD)

            elif control["Branch"]:
                # Comprobar en eq o ne y cargar posible salto

                alu_result = int(self.alu.operation(int(id_ex_reg.get_op_1_val()),
                                                int(id_ex_reg.get_op_2_val()),
                                                ALUOperation.SUB))
                
                signal_zero = (alu_result == 0)

                if control_unit.get_id_ex_control()["BranchN"] ^ signal_zero:
                    jump_address = self.alu.operation(
                        int(id_ex_reg.get_address_value()),
                        int(id_ex_reg.get_instr_pc()),
                        ALUOperation.ADD
                    )
                else:
                    jump_address = None
                    
            else:
                alu_result = self.alu.operation(id_ex_reg.get_op_1_val(),
                                                id_ex_reg.get_address_value() if control["ALUSrc"] else id_ex_reg.get_op_2_val(),
                                                control_unit.get_alu_operation())
                
                jump_address = None
                
                ex_mem_copy = {
                    "alu_result": alu_result,
                    "store_data": id_ex_reg.get_op_2_val(),
                    "reg_dst": id_ex_reg.get_reg_dst(),
                    "empty": False,
                    "instr_pc": self.pipeline.get_id_ex_pr().get_instr_pc()
                }

            return (ex_mem_copy, jump_address)
     
    def memory_access(self, control_unit: ControlUnit):
        # For printing
        self.pipeline.get_mem_wb_pr().set_instr_pc(
            self.pipeline.get_ex_mem_pr().get_instr_pc()
        )

        if self.pipeline.get_ex_mem_pr().is_empty():
            self.pipeline.get_mem_wb_pr().set_empty(True)
            self.pipeline.get_mem_wb_pr().set_instr_pc(None)
            return None, None
        else:
            address = self.get_pipeline().get_ex_mem_pr().get_alu_result()
            if control_unit.get_ex_mem_control()["MemWrite"]:
                self.data_mem.write(address, self.get_pipeline().get_ex_mem_pr().get_store_data())
                alu_data = None
                mem_data = None
            else:
                if control_unit.get_ex_mem_control()["MemRead"]:
                    alu_data = None
                    mem_data = self.data_mem.read(address)
                else:
                    alu_data = self.get_pipeline().get_ex_mem_pr().get_alu_result()
                    mem_data = None

            reg_dst = self.get_pipeline().get_ex_mem_pr().get_reg_dst()
            self.pipeline.get_mem_wb_pr().update_reg(alu_data, mem_data, reg_dst)

            mem_to_reg_data = mem_data if control_unit.get_ex_mem_control()["MemtoReg"] else alu_data
            
            return mem_to_reg_data, reg_dst       

    def write_back(self, control_unit: ControlUnit):
        if not self.get_pipeline().get_mem_wb_pr().is_empty():
            # MemtoReg
            write_data = (self.get_pipeline().get_mem_wb_pr().get_mem_data()
            if control_unit.get_mem_wb_control()["MemtoReg"]
            else self.get_pipeline().get_mem_wb_pr().get_alu_data())

            # RegWrite
            reg_dst = self.get_pipeline().get_mem_wb_pr().get_reg_dst()
            if control_unit.get_mem_wb_control()["RegWrite"]:
                self.register_file.store_value(reg_dst, write_data)

    def is_finished(self):
        # Check PC in bounds 
        return (
            self.instruction_mem.is_out_of_bounds(self.pc.get_value()) and
            self.pipeline.get_if_id_pr().is_empty() and
            self.pipeline.get_id_ex_pr().is_empty() and
            self.pipeline.get_ex_mem_pr().is_empty() and
            self.pipeline.get_mem_wb_pr().is_empty()
        )

    def update_ex_mem_reg(self, ex_mem_copy):

        # For printing
        self.pipeline.get_ex_mem_pr().set_instr_pc(
            self.pipeline.get_id_ex_pr().get_instr_pc()
        )

        self.pipeline.get_ex_mem_pr().update_reg(
            ex_mem_copy["reg_dst"],
            ex_mem_copy["alu_result"],
            ex_mem_copy["store_data"],
            ex_mem_copy["empty"]
        )

        return ex_mem_copy["alu_result"], ex_mem_copy["reg_dst"]   

    def print_execution(self, cycle):
        
        YELLOW = "\033[93m"
        RED = "\033[91m"
        GREEN = "\033[32m"
        CYAN = "\033[96m"
        RESET = "\033[0m"

        print(f"\n============== CYCLE {cycle} ==============")
        pc = (self.pipeline.get_if_id_pr().get_instr_pc()
              if not self.pipeline.get_if_id_pr().is_empty()
              else None)
        if pc is None:
            print(f"{GREEN}IF_ID:\n\tBUBBLE{RESET}")
        else:
            print(f"{GREEN}IF_ID:\n\t{pc} : {self.instruction_mem.read(pc)}{RESET}")

        pc = (self.pipeline.get_id_ex_pr().get_instr_pc()
              if not self.pipeline.get_id_ex_pr().is_empty()
              else None)
        if pc is None:
            print(f"{YELLOW}ID_EX:\n\tBUBBLE{RESET}")
        else:
            print(f"{YELLOW}ID_EX:\n\t{pc} : {self.instruction_mem.read(pc)}{RESET}")

        pc = (self.pipeline.get_ex_mem_pr().get_instr_pc()
              if not self.pipeline.get_ex_mem_pr().is_empty()
              else None)
        if pc is None:
            print(f"{CYAN}EX_MEM:\n\tBUBBLE{RESET}")
        else:
            print(f"{CYAN}EX_MEM:\n\t{pc} : {self.instruction_mem.read(pc)}{RESET}")

        pc = (self.pipeline.get_mem_wb_pr().get_instr_pc()
              if not self.pipeline.get_mem_wb_pr().is_empty()
              else None)
        if pc is None:
            print(f"{RED}MEM_WB:\n\tBUBBLE{RESET}")
        else:
            print(f"{RED}MEM_WB:\n\t{pc} : {self.instruction_mem.read(pc)}{RESET}")

        print("_______________ Register File _______________\n")
        self.register_file.print_register_file()

        print("________________ Data Memory ________________\n")
        self.data_mem.print_data_mem()

        print("_______________ Detected RAWs _______________\n")
        for pc_1,pc_2 in self.raw_list:
            print(f"{pc_1} : {self.instruction_mem.read(pc_1)}\n")
            print(f"{pc_2} : {self.instruction_mem.read(pc_2)}\n\n")

        self.raw_list.clear()

    def get_pipeline(self):
        return self.pipeline
    