
class Pipeline:

    def __init__(self):
        self.if_id_pr = IF_ID_PipelineRegister()
        self.id_ex_pr = ID_EX_PipelineRegister()
        self.ex_mem_pr = EX_MEM_PipelineRegister()
        self.mem_wb_pr = MEM_WB_PipelineRegister()

    # ID_ID Register

    def get_if_id_pr(self):
        return self.if_id_pr
    
    def set_if_id_pr(self, if_id_pr):
        self.if_id_pr = if_id_pr

    # ID_EX Register

    def get_id_ex_pr(self):
            return self.id_ex_pr
    
    def set_id_ex_pr(self, id_ex_pr):
        self.id_ex_pr = id_ex_pr

    # EX_MEM Register

    def get_ex_mem_pr(self):
        return self.ex_mem_pr
      
    def set_ex_mem_pr(self, ex_mem_pr ):
        self.ex_mem_pr = ex_mem_pr 

    # MEM_WB

    def get_mem_wb_pr(self):
            return self.mem_wb_pr
          
    def set_mem_wb_pr(self, mem_wb_pr ):
        self.mem_wb_pr = mem_wb_pr 

class IF_ID_PipelineRegister:

    def __init__(self):
        self.next_pc = None
        self.instr = None
        self.empty = True
        # For printing
        self.instr_pc = None 

    def is_empty(self):
        return self.empty

    def set_empty(self, bool):
        self.empty = bool
        
    def set_next_pc(self, pc):
        self.next_pc = pc

    def get_next_pc(self):
        return self.next_pc

    def set_instr(self, instr):
        self.instr = instr

    def get_instr(self):
        return self.instr

    # For printing
    def get_instr_pc(self):
        return self.instr_pc
    
    def set_instr_pc(self, pc):
        self.instr_pc = pc

class ID_EX_PipelineRegister:

    def __init__(self):
        self.op_1 = None
        self.op_2 = None
        self.reg_dst = None
        self.address_value = None
        self.empty = True
        # For printing
        self.instr_pc = None 

    def is_empty(self):
            return self.empty

    def set_empty(self, bool):
        self.empty = bool

    # For printing
    def get_instr_pc(self):
        return self.instr_pc
    
    def set_instr_pc(self, pc):
        self.instr_pc = pc

    

class EX_MEM_PipelineRegister:

    def __init__(self):
        self.alu_result = None
        self.store_data = None
        self.reg_dst = None
        self.empty = True
        # For printing
        self.instr_pc = None

    def is_empty(self):
            return self.empty

    def set_empty(self, bool):
        self.empty = bool

    # For printing
    def get_instr_pc(self):
        return self.instr_pc
    
    def set_instr_pc(self, pc):
        self.instr_pc = pc

class MEM_WB_PipelineRegister:

    def __init__(self):
        self.write_data = None
        self.reg_dst = None
        self.empty = True
        # For printing
        self.instr_pc = None 

    def is_empty(self):
            return self.empty

    def set_empty(self, bool):
        self.empty = bool

    # For printing
    def get_instr_pc(self):
        return self.instr_pc
    
    def set_instr_pc(self, pc):
        self.instr_pc = pc
