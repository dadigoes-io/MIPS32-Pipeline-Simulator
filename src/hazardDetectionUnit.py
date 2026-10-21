class HazardDetectionUnit:

    @staticmethod
    def is_raw_ex(op_1_reg, op_2_reg, ex_reg_dst, ex_control):
        if ex_control["RegWrite"] and ex_reg_dst != None:
            raw = op_1_reg == ex_reg_dst or op_2_reg == ex_reg_dst
            return (raw,    # if raw
                    raw and ex_control["MemRead"])                             # if load raw
        else:
            return False, False

    @staticmethod
    def is_raw_mem(op_1_reg, op_2_reg, mem_reg_dst, mem_control):    
        if mem_control["RegWrite"]  and mem_reg_dst != None:
            return op_1_reg == mem_reg_dst or op_2_reg == mem_reg_dst
        else:
            return False 
