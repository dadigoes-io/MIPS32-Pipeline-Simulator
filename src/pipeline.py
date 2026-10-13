
class Pipeline:

    def __init__(self):
        self.if_id_pr = IF_ID_PipelineRegister()
        self.id_ex_pr = ID_EX_PipelineRegister()
        self.ex_mem_pr = EX_MEM_PipelineRegister()
        self.mem_wb_pr = MEM_WB_PipelineRegister()


class IF_ID_PipelineRegister:

    def __init__(self):
        self.next_pc = None
        self.instr = None

class ID_EX_PipelineRegister:

    def __init__(self):
        self.type_op = None
        self.op_1 = None
        self.op_2 = None
        self.reg_dst = None
        self.address_value = None

class EX_MEM_PipelineRegister:

    def __init__(self):
        self.type_op = None
        self.alu_result = None
        self.store_data = None
        self.reg_dst = None

class MEM_WB_PipelineRegister:

    def __init__(self):
        self.type_op = None
        self.write_data = None
        self.reg_dst = None