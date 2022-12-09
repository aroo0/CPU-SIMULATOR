from CPU_core import CPU
from Memory import MainMemory



hard_memory = MainMemory()
cpu = CPU(hard_memory)
cpu.run(cpu, 'CPU SIMULATOR/instruction_input.txt', 'CPU SIMULATOR/data_input.txt')
