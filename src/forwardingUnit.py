class ForwardingUnit:

        @staticmethod
        def is_raw(op_reg, forward_reg_dst, forward_control):
            if forward_control["RegWrite"] and forward_reg_dst not in (None,"$zero"):
                return op_reg == forward_reg_dst
            else:
                return False

