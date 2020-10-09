"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self, program):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        for instruction in program:
            self.ram_write(address, instruction)
            address += 1

    def get_instr_name(self, IR):
        instructions = {
            0b10000010: "LDI",
            0b01000111: "PRN",
            0b01000101: "PUSH",
            0b01000110: "POP",
            0b00000001: "HLT",
            0b01010000: "CALL",
            0b00010001: "RET"
        }
        return instructions.get(IR, "unknown")

    def alu_identifier(self, num):
        if num == 0b0000:
            return "ADD"
        elif num == 0b1000:
            return "AND"
        elif num == 0b0111:
            return "CMP"
        elif num == 0b0110:
            return "DEC"
        elif num == 0b0011:
            return "DIV"
        elif num == 0b0101:
            return "INC"
        elif num == 0b0100:
            return "MOD"
        elif num == 0b0010:
            return "MUL"
        elif num == 0b1001:
            return "NOT"
        elif num == 0b1010:
            return "OR"
        elif num == 0b1100:
            return "SHL"
        elif num == 0b1101:
            return "SHR"
        elif num == 0b0001:
            return "SUB"
        elif num == 0b1011:
            return "XOR"
        else:
            return 'error'

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            # print('hey add')
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            # print('hey mul')
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == "INC":
            self.reg[reg_a] += 1
        elif op == "DEC":
            self.reg[reg_a] -= 1
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
        running = True
        stackPointer = 0xF4

        while running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            num_of_operands = IR >> 6
            alu_oper = True if IR & 0b00100000 == 32 else False
            set_pc_directly = IR & 0b00010000 == 16
            instruction = self.get_instr_name(IR)

            # self.trace()
            if alu_oper:
                num = IR & 0b00001111
                # print('mul is 2', num)
                instruction = self.alu_identifier(num)
                # print('operation', operation)
                self.alu(instruction, operand_a, operand_b)
            elif instruction == "LDI":
                self.reg[operand_a] = operand_b
            elif instruction == "PRN":
                print(self.reg[operand_a])
            elif instruction == "PUSH":
                stackPointer -= 1
                self.ram_write(stackPointer, self.reg[operand_a])
            elif instruction == "POP":
                self.reg[operand_a] = self.ram_read(stackPointer)
                stackPointer += 1
            elif instruction == "CALL":
                ret_addr = self.pc + 2
                stackPointer -= 1
                self.ram_write(stackPointer, ret_addr)

                self.pc = self.reg[operand_a]

            elif instruction == "RET":
                self.pc = self.ram_read(stackPointer)
                stackPointer += 1

            elif instruction == "HLT":
                running = False
            else:
                print('unknown instruction!')
                return

            # print('instruction', instruction, '--',
            #       'pc directly', set_pc_directly)

            # increment program counter to the next operation:
            if not set_pc_directly:
                self.pc += (num_of_operands + 1)
