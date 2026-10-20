class ForwardingUnit:

        def __init__(self):
            self.reg_dst_ex = None
            self.reg_dst_mem = None
            self.ex_mem_control = None
            self.mem_wb_control = None 

        def set_ex_regs(self, reg_dst_ex, ex_mem_control):
            self.reg_dst_ex = reg_dst_ex
            self.ex_mem_control = ex_mem_control

        def set_mem_regs(self, reg_dst_mem, mem_wb_control):
                    self.reg_dst_mem = reg_dst_mem
                    self.mem_wb_control = mem_wb_control

        def is_raw_ex_op_1(self, op_1_reg):
            if (self.ex_mem_control["RegWrite"]):
                return op_1_reg == self.reg_dst_ex
            else:
                return False

        def is_raw_ex_op_2(self, op_2_reg):
            if (self.ex_mem_control["RegWrite"]):
                return op_2_reg == self.reg_dst_ex
            else:
                return False
            
        def is_raw_mem_op_1(self, op_1_reg):
            if (self.mem_wb_control["RegWrite"]):
                return op_1_reg == self.reg_dst_mem
            else:
                return False

        def is_raw_mem_op_2(self, op_2_reg):
            if (self.mem_wb_control["RegWrite"]):
                return op_2_reg == self.reg_dst_mem
            else:
                return False

