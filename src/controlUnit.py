class ControlUnit:

    def __init__(self):

        self.id_ex_control = {
            # ID_EX
            "ALUSrc" : False, "Jump" : False, "Branch" : False, "BranchN" : False,
            # EX_MEM
            "MemWrite": False, "MemRead": False,
            # MEM_WB
            "MemtoReg" : False, "RegWrite": False,
        }

        self.ex_mem_control = {
            # EX_MEM
            "MemWrite": False, "MemRead": False,
            # MEM_WB
            "MemtoReg" : False, "RegWrite": False, 
        }

        self.mem_wb_control = {
            # MEM_WB
            "MemtoReg" : False, "RegWrite": False,
        }

        self.alu_operation = None

    def id_to_ex(self, control_signals, alu_operation):
        for k in self.id_ex_control.keys():
            self.id_ex_control[k] = control_signals[k]
        self.alu_operation = alu_operation

    def flush_id_ex(self):
        for k in self.id_ex_control.keys():
            self.id_ex_control[k] = False

    def ex_to_mem(self):
        for k in self.ex_mem_control.keys():
            self.ex_mem_control[k] = self.id_ex_control[k]

    def flush_ex_mem(self):
        for k in self.ex_mem_control.keys():
            self.ex_mem_control[k] = False

    def mem_to_wb(self):
        for k in self.mem_wb_control.keys():
            self.mem_wb_control[k] = self.ex_mem_control[k]

    def flush_mem_wb(self):
        for k in self.mem_wb_control.keys():
            self.mem_wb_control[k] = False

    def get_id_ex_control(self):
        return self.id_ex_control

    def get_ex_mem_control(self):
        return self.ex_mem_control

    def get_mem_wb_control(self):
        return self.mem_wb_control

    def get_alu_operation(self):
        return self.alu_operation
        