class ISA:
    # The ISA protocol class reads and writes instructions and data from a .txt file.

    def __init__(self):

        self.instructions = {

            'ADD': '.add',
            'ADDI': '.addi',
            'SUB': '.sub',
            'SLT': '.slt',
            'BNE': '.bne',
            'J': '.j',
            'JAL': '.jal',
            'LW': '.lw',
            'SW': '.sw',
            'CACHE': '.cache',
            'HALT': '.halt'

        }

    # Instructions:

    def read_file(self, input):

        with open(input) as data:
            data = data.readlines()
            data_to_parse = [x.strip().split(',') for x in data]
        return data_to_parse

    def store_instructions_to_memory(self, cpu, input):
        print('\n// STORING INSTRUCTIONS //\n')
        instruction_register = 100
        for instruction in self.read_file(input):
            register = f'R{instruction_register}'
            cpu.main_memory.write(register, instruction)
            instruction_register += 1
        print('---> Done!')
        return

    def store_data(self, cpu, input):
        print('\n// STORING DATA //\n')
        for pair in self.read_file(input):
            register = f'R{int(pair[0], 2)}'
            data = int(pair[1])
            cpu.main_memory.write(register, data)
        print('---> Done!')
        print('\n-------------------\n')
        return

    def read_instruction(self, instruction):
        inst = instruction[0]
        return self.instructions[inst]  # returning command to CPU e.g. add