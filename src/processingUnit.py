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
        # For printing
        self.operations = {
            "IF": None,
            "ID": None,
            "EX": None,
            "MEM": None,
            "WB": None
        }
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
                self.operations["IF"] = f"Instruction fetched at PC {pc_aux}" 

            else:
                self.pipeline.get_if_id_pr().set_empty(True)
    
        else:
            self.operations["IF"] = "STALL (PC and IF_ID unchanged)" 

    def instruction_decode(self, control_unit: ControlUnit, result_ex, reg_dst_ex, result_mem, reg_dst_mem):

        if self.pipeline.get_if_id_pr().is_empty():
            self.pipeline.get_id_ex_pr().set_empty(True)
            control_unit.flush_id_ex()
            return False

        else:
            instr = self.pipeline.get_if_id_pr().get_instr()
            instr = instr.replace(","," ").split()

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
                    reg_dst = instr[1]   # $dest
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
                    }

                case "sw":
                    # sw $source, offset($base)
                    offset, base = instr[2].split("(")

                    # For Forwarding Unit
                    op_1_reg = base.rstrip(")")
                    op_2_reg = instr[1]
                    
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
                    }
            
                case "beq" | "bne":
                    # beq  $op1, $op2, address_value
                    alu_type_op = ALUOperation.SUB

                    # For Forwarding Unit
                    op_1_reg = instr[1]
                    op_2_reg = instr[2]

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
                    op_1_reg = instr[2]
                    op_2_reg = None

                    # Load registers from Register File
                    reg_dst = instr[1]
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
                    op_1_reg = instr[2]
                    op_2_reg = instr[3]

                    # Load registers from Register File
                    reg_dst = instr[1]
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
                    }

            # Hazard detection
            is_load_raw = HazardDetectionUnit.is_load_raw(op_1_reg, op_2_reg, reg_dst_ex, control_unit.get_ex_mem_control())

            # For printing
            raw_case_ex = {
                "load_raw": is_load_raw,
                "pc_orig" : self.pipeline.get_ex_mem_pr().get_instr_pc() ,
                "pc_dest" : self.pipeline.get_if_id_pr().get_instr_pc(),
                "addr_reg" : reg_dst_ex,
                "operands" : [],
                "stage" :  "EX",
                "forwarded_value" : result_ex,
                "forwarding_disabled" : False
            }

            # Load RAW Hazard
            if is_load_raw:
                self.pipeline.get_id_ex_pr().set_empty(True)
                control_unit.flush_id_ex()

                if op_1_reg == reg_dst_ex:
                    raw_case_ex["operands"].append(1)

                if op_2_reg == reg_dst_ex:
                    raw_case_ex["operands"].append(2)

                raw_case_ex["forwarded_value"] = None

                self.raw_list.append(raw_case_ex)

                # For printing
                self.pipeline.get_id_ex_pr().set_instr_pc(
                    self.pipeline.get_if_id_pr().get_instr_pc()
                )
                self.operations["ID"] = "STALL (load-use hazard)"
                return True

            # For printing
            raw_case_mem = {
                "load_raw": False,
                "pc_orig" : self.pipeline.get_mem_wb_pr().get_instr_pc() ,
                "pc_dest" : self.pipeline.get_if_id_pr().get_instr_pc(),
                "addr_reg" : reg_dst_mem,
                "operands" : [],
                "stage" :  "MEM",
                "forwarded_value" : result_mem,
                "forwarding_disabled" : False
            }

            # Forwarding EX
            if ForwardingUnit.is_raw(op_1_reg, reg_dst_ex, control_unit.get_ex_mem_control()): 
                op_1_val = result_ex
                raw_case_ex["addr_reg"] = op_1_reg
                raw_case_ex["operands"].append(1)

            if ForwardingUnit.is_raw(op_2_reg, reg_dst_ex, control_unit.get_ex_mem_control()):
                op_2_val = result_ex
                raw_case_ex["addr_reg"] = op_2_reg
                raw_case_ex["operands"].append(2)

            # Forwarding MEM
            if not raw_case_mem["forwarding_disabled"]:
                if ForwardingUnit.is_raw(op_1_reg, reg_dst_mem, control_unit.get_mem_wb_control()):
                    raw_case_mem["operands"].append(1)

                    if 1 in raw_case_ex["operands"]:
                        raw_case_mem["forwarding_disabled"] = True
                    else:
                        op_1_val = result_mem

                if ForwardingUnit.is_raw(op_2_reg, reg_dst_mem, control_unit.get_mem_wb_control()):
                    raw_case_mem["operands"].append(2)

                    if 2 in raw_case_ex["operands"]:
                        raw_case_mem["forwarding_disabled"] = True
                    else:
                        op_2_val = result_mem

            # Save raws
            if raw_case_mem["operands"]:
                            self.raw_list.append(raw_case_mem)

            if raw_case_ex["operands"]:
                self.raw_list.append(raw_case_ex)
            
            # Update ID_EX Register
            self.pipeline.get_id_ex_pr().update_reg(reg_dst, op_1_val, op_2_val, address_value)

            # For printing
            values = ""

            if op_1_reg is not None:
                values += f"{op_1_reg}={op_1_val} "

            if op_2_reg is not None:
                values += f"{op_2_reg}={op_2_val} "

            if address_value is not None:
                values += f"immediate={address_value}"

            if values:
                self.operations["ID"] = values.strip()
            else:
                self.operations["ID"] = "Jump decoded"                

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

            str_operation = "None"

            if control["Jump"]:
                jump_address = self.alu.operation(int(id_ex_reg.get_address_value()),
                                                  int(id_ex_reg.get_instr_pc()),
                                                  ALUOperation.ADD)
                self.operations["EX"] = f"JUMP -> PC {jump_address}"

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

                # For printing operations
                decision = f"TAKEN -> PC {jump_address}" if jump_address is not None else "NOT TAKEN"
                self.operations["EX"] = f"BRANCH ({alu_result} = 0) -> {decision}"
                    
            else:
                alu_result = self.alu.operation(id_ex_reg.get_op_1_val(),
                                                id_ex_reg.get_address_value() if control["ALUSrc"] else id_ex_reg.get_op_2_val(),
                                                control_unit.get_alu_operation())

                str_operation = control_unit.get_alu_operation().name                
                
                jump_address = None
                
                ex_mem_copy = {
                    "alu_result": alu_result,
                    "store_data": id_ex_reg.get_op_2_val(),
                    "reg_dst": id_ex_reg.get_reg_dst(),
                    "empty": False,
                    "instr_pc": self.pipeline.get_id_ex_pr().get_instr_pc()
                }

                op_2 = id_ex_reg.get_address_value() if control["ALUSrc"] else id_ex_reg.get_op_2_val()
                self.operations["EX"] = f"{id_ex_reg.get_op_1_val()} {str_operation} {op_2} = {alu_result}"

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
                # For printing operations
                self.operations["MEM"] = f"WRITE [{address}] <- {self.pipeline.get_ex_mem_pr().get_store_data()}"
            else:
                if control_unit.get_ex_mem_control()["MemRead"]:
                    alu_data = None
                    mem_data = self.data_mem.read(address)
                    # For printing operations
                    self.operations["MEM"] = f"READ [{address}] -> {mem_data}"
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
                # For printing operations
                self.operations["WB"] = f"{reg_dst} <- {write_data}"

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

        print(f"\n=============== CYCLE {cycle} ===============")
        
        print(f"PC: {self.pc.get_value()}")

        pc = (self.pipeline.get_if_id_pr().get_instr_pc()
              if not self.pipeline.get_if_id_pr().is_empty()
              else None)
        if pc is None:
            print(f"{GREEN}IF_ID:\n\tEMPTY{RESET}")
        else:
            print(f"{GREEN}IF_ID:\n\t{pc} : {self.instruction_mem.read(pc)}{RESET}")

        pc = (self.pipeline.get_id_ex_pr().get_instr_pc()
              if not self.pipeline.get_id_ex_pr().is_empty()
              else None)
        if pc is None:
            print(f"{YELLOW}ID_EX:\n\tEMPTY{RESET}")
        else:
            print(f"{YELLOW}ID_EX:\n\t{pc} : {self.instruction_mem.read(pc)}{RESET}")

        pc = (self.pipeline.get_ex_mem_pr().get_instr_pc()
              if not self.pipeline.get_ex_mem_pr().is_empty()
              else None)
        if pc is None:
            print(f"{CYAN}EX_MEM:\n\tEMPTY{RESET}")
        else:
            print(f"{CYAN}EX_MEM:\n\t{pc} : {self.instruction_mem.read(pc)}{RESET}")

        pc = (self.pipeline.get_mem_wb_pr().get_instr_pc()
              if not self.pipeline.get_mem_wb_pr().is_empty()
              else None)
        if pc is None:
            print(f"{RED}MEM_WB:\n\tEMPTY{RESET}")
        else:
            print(f"{RED}MEM_WB:\n\t{pc} : {self.instruction_mem.read(pc)}{RESET}")

        print("____________ Operations performed ____________")

        for stage in self.operations:
            if self.operations[stage] is not None:
                print(f"{stage}: {self.operations[stage]}")
            self.operations[stage] = None

        print("_______________ Register File _______________\n")
        self.register_file.print_register_file()

        print("________________ Data Memory ________________\n")
        self.data_mem.print_data_mem()

        print("_______________ Detected RAWs _______________\n")
        for raw in self.raw_list:
            pc_orig = raw["pc_orig"]
            pc_dest = raw["pc_dest"]
            stage = raw["stage"]

            print(f"{pc_orig} : {self.instruction_mem.read(pc_orig)}\t({stage})")
            print(f"{pc_dest} : {self.instruction_mem.read(pc_dest)}\t(ID)")

            print(f"Register: {raw["addr_reg"]}")
            print(f"Operands: {raw["operands"]}")

            if raw["load_raw"]:
                print("Stall applied in PC and IF_ID pipeline register")
            else:
                if raw["forwarding_disabled"]:
                    print("Forwarding disabled due to EX priority")
                else:
                    print(f"Forwarding: {stage} -> ID")
                    print(f"Transferred value: {raw['forwarded_value']}")
            print("\n")

        self.raw_list.clear()

    def get_pipeline(self):
        return self.pipeline
    