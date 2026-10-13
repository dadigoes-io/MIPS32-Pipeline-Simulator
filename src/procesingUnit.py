class ProcessingUnit:

    def __init__(self, program_counter, instruction_mem, data_mem, register_file, alu, pipeline):
        self.pc = program_counter
        self.instruction_mem = instruction_mem
        self.data_mem = data_mem
        self.register_file = register_file
        self.alu = alu
        self.pipeline = pipeline

    