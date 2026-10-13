class ProgramCounter:

    def __init__(self):
        self.value = 0

    def getValue(self):
        return self.value

    def putValue(self, val):
        self.value = val