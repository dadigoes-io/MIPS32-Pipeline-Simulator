class ForwardingUnit:

        @staticmethod
        def is_raw(op_reg, forward_reg_dst, forward_control):
            if forward_control["RegWrite"] and forward_reg_dst is not None:
                return op_reg == forward_reg_dst
            else:
                return False

