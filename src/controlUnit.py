class ControlUnit:

    def __init__(self):
        self.id_ex_control = {
            "RegDst" : None,
            "ALUSrc" : None
        }
        self.ex_mem_control = {
            "Branch" : None,
            "MemWrite": None,
            "MemRead": None
        }
        self.mem_wb_control = {
            "MemtoReg" : None,
            "RegWrite": None     
        }
