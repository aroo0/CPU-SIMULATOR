from Memory import Memory 
from ISA import ISA
from Cache import Cache



class Register(Memory):
    # A specific fast-acting class inherited from Memory. 
    # Correlates strongly with the processor and holds a queue of consecutive tasks in fetch_decode_execute_cycle. 
    def __init__(self):
        Memory.__init__(self, name="Register", access_time=0.1)
        self.registers = {

            'PC': None,
            'Memory address register': None,
            'Memory data register': None,
            'Instruction register': None,
            'Accumulator': None

        }

    def read(self, address):
        data = self.registers[address]
        print(f'---> REGISTER: Reading {data} to {address}')
        self.execute_time += self.execute_time
        return data

    def write(self, address, data):
        print(f'---> REGISTER: Writing {data} to {address}')
        self.execute_time += self.execute_time
        self.registers[address] = data


class CPU:
    # Processor class with fetch_decode_execute_cycle implementation. 
    # Intepretes operations thanks to the ISA protocol (ISA class),
    # executes them, and returns the result to the currently connected memory.
    def __init__(self, memory):
        self.register = Register()
        self.main_memory = memory
        self.dir_memory = memory
        self.isa = ISA()
        self.memory_mode = 0
        self.program_counter = 100 
        self.CU = None  # Control Unit
        self.halt_signal = False
        self.exec_time = 0

    def fetch(self):
        # The position of the PC (program_counter) from the registry is very important, 
        # because it allows the processor to comprehend at what stage of the task list execution it is.
        self.register.write('PC', self.program_counter)

        # Reading memory address of instruction
        memory_address_register = self.program_counter  # 100
        self.register.write('Memory address register', memory_address_register)
        # Reading instruction from address
        memory_data_register = self.dir_memory.read(f'R{memory_address_register}')
        self.register.write('Memory data register', memory_data_register)
        self.register.write('Instruction register', memory_data_register)
        self.register.write('Accumulator', memory_data_register[1:])
        # After each fetch, self.program_counter (PC) adds 1 to its number to proceeds to the next instructions.
        self.program_counter += 1
        self.register.write('PC', self.program_counter)
        return

    def decode(self):
        # Ineterpts the code of a given instruction based on the protocol in the ISA class.
        current_instruction = self.register.read('Memory data register')
        encode_inststruction = self.isa.read_instruction(current_instruction)
        data = self.register.read('Accumulator')
        command = f'self{encode_inststruction}(*{data})'
        print(f'---> Name of instruction: {encode_inststruction}')
        return command

    def alu_execute(self, command):
        return exec(command)

    def fetch_decode_execute_cycle(self):
        # The function that brings together the fetch, decode and execute functions into one cycle.
        index = 1
        while self.halt_signal == False:
            print(
                f'\n------------------- // Instruction {index} // -------------------\n'.upper())
            print('\n-----> Fetching instruction:\n'.upper())
            self.fetch()
            print('\n-----> Decoding instruction:\n'.upper())
            command = self.decode()
            print('\n-----> Executiong instruction: \n'.upper())
            self.alu_execute(command)
            index += 1


    # Impementation of CPU commands:

    def add(self, rd, rs, rt):
        # adds numbers from two registers to a given register
        r1 = self.main_memory.read(rs)
        r2 = self.main_memory.read(rt)
        data = r1 + r2
        print(f'---> Executing: {r1} + {r2} = {data}')
        self.main_memory.write(rd, data)
        return

    def addi(self, rt, rs, immd):
        # adds a number from a register and some number to a given register
        r1 = self.main_memory.read(rs)
        data = r1 + int(immd)
        print(f'---> Executing: {r1} + {immd} = {data}')
        self.main_memory.write(rt, data)
        return

    def sub(self, rd, rs, rt):
        # analogous to add but subtracting
        r1 = self.main_memory.read(rs)
        r2 = self.main_memory.read(rt)
        data = r1 - r2
        print(f'---> Executing: {r1} - {r2} = {data}')
        self.main_memory.write(rd, data)
        return

    def slt(self, rd, rs, rt):
        # returns 1 if the number in the second register greater than the first, otherwise 0 
        r1 = self.main_memory.read(rs)
        r2 = self.main_memory.read(rt)
        print(
            f'---> Checking larger value: if {r1} < {r2} stored value = 1, else value = 0')
        if r1 < r2:
            data = 1
        else:
            data = 0

        self.main_memory.write(rd, data)
        return

    def bne(self, rt, rs):
        # Increases the counter porgram if the numbers of the given registers are not equal. 
        r1 = self.main_memory.read(rs)
        r2 = self.main_memory.read(rt)
        print(f'---> Checking for equality {r1} == {r2}')
        if r1 != r2:
            print('---> False!')
            self.program_counter += 4
            print(f'---> Jumping PC to {self.program_counter}')
            return
        else:
            print('---> True!')
            print('---> PC preserved.')

    def j(self, target):
        print(f'----> Jumping PC to {target}')
        self.program_counter = int(target)

    def jal(self, target):
        data = self.program_counter + 4
        self.main_memory.write('R7', data)
        self.program_counter = target

    def halt(self, arg=False):
        # termination of PCU 
        if arg == ';':
            if self.memory_mode == 1:
                self.cache(0)
            self.halt_signal = True
            print('Program will terminate. \n')
            print(
                '--------------------------------------------------------------------\n')

    def cache(self, code):
        # Enabling Memory Cache if code=1
        code = int(code)
        if code == 0:
            self.exec_time += self.main_memory.get_time()
            self.main_memory = self.dir_memory
            self.memory_mode = 0
            print('Cache Memory off.')

        elif code == 1:
            self.main_memory = Cache(self.dir_memory)
            self.memory_mode = 1
            print('Working with Cache Memory.')

        elif (code == 2) & (self.memory_mode == 1):
            self.main_memory.flush_memory()

        return


    def set_memory(self, memory):
        self.main_memory = memory

    def get_exec_time(self):
        # Sums the access_time of individual memories, varying depending on whether the query ended in Cache or routed to Main Memory.
        self.exec_time += self.dir_memory.get_time()
        self.exec_time += self.register.get_time()
        print(f"-----> Execution time: {self.exec_time:.2f} nanoseconds")

    def run(self, cpu, instruction_input, data_input):
        # The function that initiates the program. It requires a prior invocation of the class instance,
        # as well as specifying the source of the .txt files. 
        # That is, the contents of the main memory register and the list of operations to be performed.
    
        print('\n------------------- // CPU SIMULATOR // -------------------\n')

        print(f'\n----> Loading instruction from file {instruction_input}\n')
        self.isa.store_instructions_to_memory(cpu, instruction_input)
        print('~~')
        print(f'\n----> Loading data from file {data_input}\n')
        self.isa.store_data(cpu, data_input)
        print(f'\n -----> Runing fetch_decode_execute cycle \n')
        self.fetch_decode_execute_cycle()
        print('-----> Program done!')
        self.get_exec_time()