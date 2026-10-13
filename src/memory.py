class Memory:

    def __init__(self):
        self.mem = {}

    def read(self, dir):
        return self.mem.get(dir)

class InstructionMemory (Memory):

    def __init__(self):
        super().__init__()
        self.labels = {}

    def read_program(self, programFile):
        file = open(programFile, "r")
        line = file.readline()
        i = 0
        while line:
            # Remove comments and leftover spaces
            line = line.split('#')[0].strip()

            if self.isLabel(line):
                self.labels[line[:-1]] = i

            if self.isInstruction(line):
                self.mem[i] = line
                i += 4            
                
            line = file.readline()
        file.close()
        self.replaceLabels()

    def replaceLabels(self):

        for instr_dir in self.mem.keys():
            aux_label = self.mem[instr_dir].split()[-1]
            if aux_label in self.labels.keys():            
                new_line = self.mem[instr_dir].replace(aux_label, str(self.labels[aux_label]))
                self.mem[instr_dir] = new_line

    def printMem(self):
        for k in self.mem.keys():
            print(f"{k} : {self.mem.get(k)}")
    
    def isInstruction(self, line):
        return '$' in line or "j " in line

    def isLabel(self, line):
        return line.endswith(':')
    
    
class DataMemory (Memory):

    def __init__(self):
        super().__init__()

    def write(self, dir, value):
        self.mem[dir] = value
