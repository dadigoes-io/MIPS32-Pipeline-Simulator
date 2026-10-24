class HazardDetectionUnit:

    @staticmethod
    def is_load_raw(op_1_reg, op_2_reg, ex_reg_dst, ex_control):
        if ex_control["RegWrite"] and ex_reg_dst not in (None, "$zero"):
            raw = op_1_reg == ex_reg_dst or op_2_reg == ex_reg_dst
            return raw and ex_control["MemRead"]                            # if load raw
        else:
            return False
