from collections import OrderedDict
from Memory import Memory

class Cache(Memory):
    # Implemetation of 4 blocks cache memory with LRU (Least recently used block) replacement and write-back policy.
    def __init__(self, main_memory):
        Memory.__init__(self, name='Cache', access_time=0.5)
        self.main_memory = main_memory

        self.blocks = OrderedDict()
        self.size = 3

    def read(self, address):
        # LUR replacement build with OrderedDict. In the read function, when triggered, each block is tracked 
        # and moved to the front of the queue at the time of use. 
        # If the register number the CPU asks for is in the Cache (Cache Hit), it is returned immediately,
        # otherwise the Cache queries Main Memory(Cache Miss). 
        # If the Cache memory is full, and the register number from the processor query is not in the Cache, 
        # the write function is triggered, which sent the register number and its data to Main Memory, 
        # making place for its overwriting.
        for block in self.blocks.keys():
            if address == block:
                data = self.blocks[address]
                print('---> Cache Hit!')
                self.blocks.move_to_end(address)
                super().read(address, data)
                return data

        else:
            print('---> Cache Miss!')
            data = self.main_memory.read(address)
            self.write(address, data)
            return data

    def write(self, address, data):
        # Data from a given block is transferred to main memory when there is a need to overwrite that block. 
        if len(self.blocks) > self.size:
            print('---> Cache full! Storing LUR value to Main Memory')
            last = self.blocks.popitem(last=False)
            self.main_memory.write(last[0], last[1])

        self.blocks[address] = data
        super().write(address, data)

    def flush_memory(self):
        # Clears what is currently in memory.
        self.blocks.clear()
        print('Cache Memory flushed!')
        return