class ForwardingUnit:

        @staticmethod
        def is_raw(op_reg, reg_dst_ex, ex_mem_control):
            if ex_mem_control["RegWrite"] and op_reg is not None:
                return op_reg == reg_dst_ex
            else:
                return False

