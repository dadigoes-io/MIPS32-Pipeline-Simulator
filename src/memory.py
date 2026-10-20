class Memory:

    def __init__(self):
        self.mem = {}

    def read(self, address):
        return self.mem.get(address)

class InstructionMemory (Memory):

    def __init__(self):
        super().__init__()
        self.labels = {}

    def read_program(self, program_file):
        file = open(program_file, "r")
        line = file.readline()
        i = 0
        while line:
            # Remove comments and leftover spaces
            line = line.split('#')[0].strip()

            if self._is_label(line):
                self.labels[line[:-1]] = i

            if self._is_instruction(line):
                self.mem[i] = line
                i += 4            
                
            line = file.readline()
        file.close()
        self._replace_labels()

    def _replace_labels(self):

        for instr_address in self.mem.keys():
            aux_label = self.mem[instr_address].split()[-1]

            if aux_label in self.labels.keys():            
                new_line = self.mem[instr_address].replace(aux_label, str(self.labels[aux_label] - instr_address))
                self.mem[instr_address] = new_line

    def print_mem(self):
        for k in self.mem.keys():
            print(f"{k} : {self.mem.get(k)}")

    def is_out_of_bounds(self, address):
        return address > max(self.mem.keys())
    
    def _is_instruction(self, line):
        return '$' in line or "j " in line

    def _is_label(self, line):
        return line.endswith(':')
    
    
class DataMemory (Memory):

    def __init__(self):
        super().__init__()

    def write(self, address, value):
        self.mem[address] = value
    
    def print_data_mem(self):
        for k in self.mem.keys():
            print(f"{k}: {self.mem[k]}")
