"""CPU functionality."""

import sys

lesstf = 0b100
greatertf = 0b010
equaltf = 0b001


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.flags = 0b00000001
        self.running = True
        self.commands = {
            0b00000001: self.hlt,
            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b10100010: self.mul,
            0b01000101: self.push,
            0b01000110: self.pop,
            0b01010100: self.jmp,
            0b01010101: self.jeq,
            0b01010110: self.jne,
            0b10100111: self.cmp
        }

    def cmp(self, oper_a, oper_b):
        self.alu('CMP', oper_a, oper_b)
        self.pc += 3

    def jmp(self, oper_a, oper_b):
        self.pc = self.reg[oper_a]

    def jeq(self, oper_a, oper_b):
        if self.flags & equaltf:
            self.pc = self.reg[oper_a]
        else:
            self.pc += 2

    def jne(self, oper_a, oper_b):
        if not self.flags & equaltf:
            self.pc = self.reg[oper_a]
        else:
            self.pc += 2

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def hlt(self, operand_a, operand_b):
        self.running = False

    def ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        return (3, True)

    def prn(self, operand_a, operand_b):
        print(self.reg[operand_a])
        return (2, True)

    def mul(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)
        return (3, True)

    def push(self, operand_a, operand_b):
        self.reg[7] -= 1
        sp = self.reg[7]
        value = self.reg[operand_a]
        self.ram[sp] = value
        return (2, True)

    def pop(self, operand_a, operand_b):
        sp = self.reg[7]
        value = self.ram[sp]
        self.reg[operand_a] = value
        self.reg[7] += 1
        return (2, True)

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
