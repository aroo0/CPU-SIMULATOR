# CPU Simulator

CPU Simulator is a simplified model of processor design based on three classes: CPU, Memory, and ISA. The project is implemented in Python and provides an interactive environment to simulate the fetch, decode, and execute cycle of a basic processor.

## Features

- Three types of memory with different access speed (Main Memory, Cache, Register).
- Cache memory with LRU (Least Recently Used block) replacement and write-back policy.
- Data and command list for the processor are read from an external .txt file.
- The processor executes a few basic commands.
- Simplified processor-memory communication in {register:data} scheme.

## Getting Started

To use CPU Simulator, simply clone the repository and run the `program.py` file. An example of the commands in the cycle are in `instruction_input.txt`.

