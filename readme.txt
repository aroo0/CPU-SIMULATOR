CPU SIMULATOR. 



Simplified model of processor design based on three classes: CPU, Memory, ISA.

program.py is starting file.

- implemented three types of memory with different access speed (Main Memory, Cache, Register).
- Cache memory with LRU (Least recently used block) replacement and write-back policy.
- Simulation of fetch, decode, execute cycle. 
- Data and command list for the processor are read from an external .txt file.
- The processor executes a few basic commands. 
- Simplified processor-memory communication in {register:data} scheme.
