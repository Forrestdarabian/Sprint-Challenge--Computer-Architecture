"""CPU functionality."""

import sys


lesstf = 0b100
greatertf = 0b010
equaltf = 0b001
SP = 7
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
ADD = 0b10100000
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110


# greater gtf == > flag, ltf == < flag, etf == = flag


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = True
        self.flags = 0b00000001
        self.commands = {
            HLT: self.HLT,
            LDI: self.LDI,
            PRN: self.PRN,
            ADD: self.ADD,
            MUL: self.MUL,
            PUSH: self.PUSH,
            POP: self.POP,
            CALL: self.CALL,
            RET: self.RET,
            CMP: self.CMP,
            JMP: self.JMP,
            JEQ: self.JEQ,
            JNE: self.JNE
        }

    def HLT(self, oper_a, oper_b):
        self.running = False

    def LDI(self, oper_a, oper_b):
        self.reg[oper_a] = oper_b
        self.pc += 3

    def PRN(self, oper_a, oper_b):
        print(self.reg[oper_a])
        self.pc += 2

    def ADD(self, oper_a, oper_b):
        self.alu('ADD', oper_a, oper_b)
        self.pc += 3

    def MUL(self, oper_a, oper_b):
        self.alu('MUL', oper_a, oper_b)
        self.pc += 3

    def PUSH(self, oper_a, oper_b):
        self.push(self.reg[oper_a])
        self.pc += 2

    def POP(self, oper_a, oper_b):
        self.reg[oper_a] = self.pop()
        self.pc += 2

    def CALL(self, oper_a, oper_b):
        self.reg[SP] -= 1
        self.ram[self.reg[SP]] = self.pc + 2
        update_reg = self.ram[self.pc + 1]
        self.pc = self.reg[update_reg]

    def RET(self, oper_a, oper_b):
        self.pc = self.ram[self.reg[SP]]
        self.reg[SP] += 1

    def CMP(self, oper_a, oper_b):
        self.alu('CMP', oper_a, oper_b)
        self.pc += 3

    def JMP(self, oper_a, oper_b):
        self.pc = self.reg[oper_a]

    def JEQ(self, oper_a, oper_b):
        if self.flags & equaltf:
            self.pc = self.reg[oper_a]
        else:
            self.pc += 2

    def JNE(self, oper_a, oper_b):
        if not self.flags & equaltf:
            self.pc = self.reg[oper_a]
        else:
            self.pc += 2

    def push(self, value):
        self.reg[SP] -= 1
        self.ram_write(value, self.reg[7])

    def pop(self):
        value = self.ram_read(self.reg[7])
        self.reg[SP] += 1
        return value

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""
        address = 0
        with open(sys.argv[1]) as f:
            for line in f:
                # Ignore comments
                comment_split = line.split("#")
                num = comment_split[0].strip()
                if num == "":
                    continue  # Ignore blank lines
                instruction = int(num, 2)  # Base 10, but ls-8 is base 2
                self.ram[address] = instruction
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.flags = lesstf
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flags = greatertf
            else:
                self.flags = equaltf
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while self.running:
            IR = self.ram_read(self.pc)
            oper_a = self.ram_read(self.pc + 1)
            oper_b = self.ram_read(self.pc + 2)
            if int(bin(IR), 2) in self.commands:
                self.commands[IR](oper_a, oper_b)
            else:
                raise Exception(
                    f'Invalid {IR}')
