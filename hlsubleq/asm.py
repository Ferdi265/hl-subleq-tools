from functools import reduce
from .util import *

class Subleq:
    NEXT = object()
    AGAIN = object()

    @staticmethod
    def to_string(a):
        if a == Subleq.NEXT:
            return "NEXT"
        elif a == Subleq.AGAIN:
            return "AGAIN"
        elif a == None:
            return "NONE"
        else:
            return a

class Program:
    def __init__(self):
        self.memory = []
        self.labels = dict()
        self.idx = None

    def index(self):
        return self.idx or len(self.memory)

    def seek(self, index):
        self.idx = index

    def set(self, data, line):
        if self.idx == len(self.memory):
            self.idx = None

        if self.idx != None:
            if self.idx < len(self.memory):
                if self.memory[self.idx] == None:
                    self.memory[self.idx] = data
                    self.idx += 1
                else:
                    Error("trying to overwrite already written address 0x{:04x} in line {}".format(self.idx, self.line))
            elif data != None:
                while self.idx >= len(self.memory):
                    self.memory.append(None)
                self.memory[self.idx] = data
            self.idx += 1

        else:
            self.memory.append(data)

class Token:
    def is_seek(self, token):
        return token[0] == "@"

    def is_label(self, token):
        return token[-1] == ":"

    def is_number(self, token):
        return token[0] in "-0123456789" or token == "NONE"

    def is_symbol(self, token):
        return not (self.is_seek(token) or self.is_label(token) or self.is_number(token))

class Assembler:
    def __init__(self, token = None, program = None, **kwargs):
        if program == None:
            program = Program()
        if token == None:
            token = Token()

        self.program = program
        self.token = token

    def next_token(self):
        return self.tokens.pop(0)

    def parse_seek(self, line, token):
        token = token[1:]
        try:
            token = parse_int(token)
        except:
            Error("could not parse {} as integer in line {}".format(token, line))
        self.program.seek(token)

    def parse_label(self, line, token):
        token = token[:-1]
        if not self.token.is_symbol(token) or token == "NEXT" or token == "AGAIN":
            Error("definition of reserved label {} in line {}".format(token, line))
        if token in self.program.labels:
            Error("redefinition of label {} in line {}".format(token, line))
        self.program.labels[token] = self.program.index()

    def parse_number(self, line, token):
        if token == "NONE":
            token = None
        else:
            try:
                token = parse_int(token)
            except:
                Error("could not parse {} as integer in line {}".format(token, line))

        self.program.set(token, line)

    def parse_symbol(self, line, token):
        if token == "NEXT":
            token = Subleq.NEXT
        elif token == "AGAIN":
            token = Subleq.AGAIN
        self.program.set(token, line)

    def parse_token(self, line, token):
        if self.token.is_seek(token):
            self.parse_seek(line, token)
        elif self.token.is_label(token):
            self.parse_label(line, token)
        elif self.token.is_number(token):
            self.parse_number(line, token)
        else:
            self.parse_symbol(line, token)

    def parse_finish(self):
        pass

    def write_start(self):
        pass

    def write_word(self, word):
        pass

    def write_finish(self):
        pass

    def write_output(self):
        self.write_start()

        for i, word in enumerate(self.program.memory):
            if word == None:
                word = 0
            elif type(word) == str:
                try:
                    word = self.program.labels[word]
                except:
                    Error("undefined label {} at address 0x{:04x}".format(word, i))
            elif word == Subleq.NEXT:
                word = i + 1
            elif word == Subleq.AGAIN:
                word = i - 2
            word = neg2twos(word)

            self.write_word(word)

        self.write_finish()

    def assemble(self):
        data = self.read_input()

        lines = enumerate(data.split('\n'), 1)
        tokenlists = map(lambda e: list(map(lambda tok: (e[0], tok), e[1].split())), lines)

        self.tokens = reduce(lambda a, b: a + b, tokenlists, [])

        while len(self.tokens) != 0:
            line, token = self.next_token()
            self.parse_token(line, token)

        self.parse_finish()
        self.write_output()
