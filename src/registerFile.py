class RegisterFile:

    def __init__(self):
        self.mem = {
            "$zero": 0,
            "$at": None,
            "$v0": None,
            "$v1": None,
            "$a0": None,
            "$a1": None,
            "$a2": None,
            "$a3": None,
            "$t0": None,
            "$t1": None,
            "$t2": None,
            "$t3": None,
            "$t4": None,
            "$t5": None,
            "$t6": None,
            "$t7": None,
            "$s0": None,
            "$s1": None,
            "$s2": None,
            "$s3": None,
            "$s4": None,
            "$s5": None,
            "$s6": None,
            "$s7": None,
            "$t8": None,
            "$t9": None,
            "$k0": None,
            "$k1": None,
            "$gp": None,
            "$sp": 512,
            "$fp": None,
            "$ra": None,
        }   
    
    def store_value(self, k, v):
        if k != "$zero":
           self.mem[k] = v

    def load_value(self, k):
        return self.mem[k]

    def print_register_file(self):
        for k in self.mem.keys():
            if self.mem[k] is not None:
                print(f"{k}: {self.mem[k]}")