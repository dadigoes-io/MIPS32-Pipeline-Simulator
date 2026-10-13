from enums import ALUOperation

class ALU:

    @staticmethod
    def operation(op1, op2, operation):

        match operation:
            case ALUOperation.ADD:
                result = op1 + op2

            case ALUOperation.SUB:
                result = op1 - op2

            case ALUOperation.AND:
                result = op1 & op2

            case ALUOperation.OR:
                result = op1 | op2

            case ALUOperation.XOR:
                result = op1 ^ op2

            case ALUOperation.SLT:
                result = int(op1 < op2)
            
        return (result, result == 0)