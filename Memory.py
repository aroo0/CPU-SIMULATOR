
# Abstract Memory class, from which three basic memories are inherited with specific acces_time: Main Memory (30 ns), Cache (0.5 ns), Register (0.1).

class Memory:
    def __init__(self, name, access_time):
        self.name = name
        self.access_time = access_time
        self.execute_time = 0

    # Generalized dummy reader/writer to specify what is happening in the terminal.
    # All read/write functions in Cache, Main Memory or Register are triggered by the ISA or CPU class.
    def read(self, address, data):
        print(f'---> Reading {data} from tag {address} in {self.name}')
        self.execute_time += self.access_time

    def write(self, address, data):
        print(f'---> Writing {data} to tag {address} in {self.name} ')
        self.execute_time += self.access_time

    def get_time(self):
        return self.execute_time


class MainMemory(Memory):
    # Main memory with infinite storage space, all commands from the .txt file, as well as input data are stored in Memory.blocks here before execution in format: [Register: Data]. The CPU always queries the registry.
    def __init__(self):
        Memory.__init__(self, name='Main Memory', access_time=30)

        self.blocks = {}

    def read(self, address):
        if address in self.blocks.keys():
            data = self.blocks[address]
            super().read(address, data)
            return data

    def write(self, address, data):
        self.blocks[address] = data
        super().write(address, data)