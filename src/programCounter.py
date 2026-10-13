class ProgramCounter:

    def __init__(self):
        self.value = 0

    def get_value(self):
        return self.value

    def put_value(self, val):
        self.value = val

    def add_four(self):
        self.value += 4
        return self.value