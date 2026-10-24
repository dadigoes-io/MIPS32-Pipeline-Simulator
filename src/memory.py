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

            if ":" in line:
                label, line = line.split(":")
                self.labels[label.strip()] = i
                line = line.strip()

            if self._is_instruction(line):
                self.mem[i] = line
                i += 4            
                
            line = file.readline()
        file.close()
        self._replace_labels()

    def _replace_labels(self):

        for instr_address in self.mem.keys():
            aux_label = self.mem[instr_address].replace(",", " ").split()[-1]

            if aux_label in self.labels.keys():            
                new_line = self.mem[instr_address].rsplit(aux_label, 1)[0] + str(self.labels[aux_label] - instr_address)
                self.mem[instr_address] = new_line

    def print_mem(self):
        for k in self.mem.keys():
            print(f"{k} : {self.mem.get(k)}")

    def is_out_of_bounds(self, address):
        return address > max(self.mem.keys())
    
    def _is_instruction(self, line):
        if not line:
            return False    # Case line was a comment
        
        return ('$' in line) or (line.split()[0] == "j")
    
    
class DataMemory (Memory):

    def __init__(self):
        super().__init__()

    def write(self, address, value):
        self.mem[address] = value
    
    def print_data_mem(self):
        for k in self.mem.keys():
            print(f"{k}: {self.mem[k]}")
