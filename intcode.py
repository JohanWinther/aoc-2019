from collections import deque

class Intcode():
    def __init__(self, m, name='Unnamed Computer'):
        self.name = name
        self.m_start = {i:v for i, v in enumerate(m)}
        self.input_buffer = deque()
        self.output_buffer = deque()
        self.opcodes = {
            1: {"nparams": [0,0,1], "fun": self.add},
            2: {"nparams": [0,0,1], "fun": self.mul},
            3: {"nparams": [1], "fun": self.inp},
            4: {"nparams": [0], "fun": self.out},
            5: {"nparams": [0,0], "fun": self.jit},
            6: {"nparams": [0,0], "fun": self.jif},
            7: {"nparams": [0,0,1], "fun": self.lt},
            8: {"nparams": [0,0,1], "fun": self.eq},
            9: {"nparams": [0], "fun": self.rb},
            99: {"nparams": [], "fun": self.exit},
        }
        self.reset()
    
    def reset(self):
        self.m = self.m_start.copy()
        self.ip = 0
        self.relative_base = 0
        self.completed = False
        while (self.input_buffer):
            self.input_buffer.popleft()
        while (self.output_buffer):
            self.output_buffer.popleft()
    
    def read_memory(self, loc):
        if loc < 0:
            raise ValueError("Cannot write to negative memory locations.")
        if loc not in self.m:
            self.m[loc] = 0
        return self.m[loc]

    def write_memory(self, loc, val):
        if loc < 0:
            raise ValueError("Cannot write to negative memory locations.")
        self.m[loc] = val

    def set_input(self, inp):
        self.input_buffer.append(inp)

    def set_previous(self, prev):
        self.input_buffer = prev.output_buffer

    def run(self):
        while not self.completed:
            self.run_step()
    
    def run_until_output(self):
        while not self.completed and not self.output_buffer:
            self.run_step()

    def run_step(self):
        if self.completed:
            return

        opcode = self.read_memory(self.ip) % 100
        if opcode == 3 and len(self.input_buffer) == 0:
            return

        try:
            oc = self.opcodes[opcode]
        except KeyError:
            print(f'Unkown opcode: {opcode}')
            self.completed = True
            return
        
        param_mode = self.read_memory(self.ip) // 100
        if oc['fun'](
            self.parse_params(
                param_mode,
                oc['nparams'],
                [self.read_memory(i + 1) for i in range(self.ip, self.ip + len(oc['nparams']))],
                )
            ):
                self.ip += len(oc['nparams']) + 1

    def parse_params(self, param_mode, write_mode, params, ):
        return list(self.param_generator(param_mode, write_mode, params))

    def param_generator(self, param_modes, write_mode, params):
        for i, p in enumerate(params):
            param_mode = param_modes // 10 ** i % 10
            if param_mode == 0:
                if write_mode[i]:
                    yield p
                else:
                    yield self.read_memory(p)
            elif param_mode == 1:
                yield p
            elif param_mode == 2:
                if write_mode[i]:
                    yield self.relative_base+p
                else:
                    yield self.read_memory(self.relative_base+p)
            else:
                return ValueError("Invalid parameter mode.")

    def add(self, parsed_params):
        self.write_memory(parsed_params[2], parsed_params[0] + parsed_params[1])
        return True

    def mul(self, parsed_params):
        self.write_memory(parsed_params[2], parsed_params[0] * parsed_params[1])
        return True

    def inp(self, parsed_params):
        self.write_memory(parsed_params[0], self.input_buffer.popleft())
        return True
    
    def out(self, parsed_params):
        self.output_buffer.append(parsed_params[0])
        return True

    def jit(self, parsed_params):
        if parsed_params[0]:
            self.ip = parsed_params[1]
            return False
        else:
            return True

    def jif(self, parsed_params):
        if not parsed_params[0]:
            self.ip = parsed_params[1]
            return False
        else:
            return True

    def lt(self, parsed_params):
        self.write_memory(parsed_params[2], int(parsed_params[0] < parsed_params[1]))
        return True
    
    def eq(self, parsed_params):
        self.write_memory(parsed_params[2], int(parsed_params[0] == parsed_params[1]))
        return True
    
    def rb(self, parsed_params):
        self.relative_base += parsed_params[0]
        return True
        
    def exit(self, parsed_params):
        self.completed = True
        return False
