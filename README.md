# LMC Simulation

‘Topic 1.1.1 The structure and function of the processor’ is the very first topic the OCR A-Level Computer Science specification. It predominantly involves the internal components of a computer system’s (main) processor - the Central Processing Unit (CPU) - and how this processor handles instructions using the Fetch-Decode-Execute (FDE) cycle. The topic also covers the factors that affect the performance of the CPU as well as the two main processor architectures (designs); ‘von Neumann’ and ‘Harvard’, and how they differ from each other.
This topic appears frequently in both AS-Level (Year 12) and A2-Level (Year 13) exam papers so it is essential for students to have a deep understanding of the topic so that they can achieve the best grade they can in the final A-Level exams.

When talking to my classmates, however, it quickly became apparent that a significant proportion of them have large gaps in their knowledge in this topic or are outright confused when it comes to how the CPU operates or how to write assembly instructions as per the OCR specification.

Additionally, it became clear that, although my classmates could define pipelining, very few of them understand well how it works within the CPU and that they struggle to visualise how three instructions can be simultaneously processed during the Fetch-Decode-Execute cycle.
To solve this problem, I will create a simulation of a Little Man Computer (LMC) system. This would involve:
-	A CPU of the Harvard architecture, meaning that data and instructions are stored in separate memory locations, which are accessed via separate buses. The system must also use a reduced instruction set – fewer, simpler instructions that are of a fixed length. This is necessary to allow pipelining to be supported as all instructions must be uniform in execution time.
-	Two separate memory modules with 50 memory locations each. One of the modules will store data and the other will store instructions. This allows for up to 50 lines of assembly code to be written by the user, which will be sufficient for any task an A-Level student would need to complete.
-	A text editor for users to write LMC assembly code which will be run by the simulated processor. 

My goal is to be able to simulate all CPU sub-components and the main memory (within the OCR A-Level specification) so that the application is genuinely useful for all A-Level Computer Science students.
