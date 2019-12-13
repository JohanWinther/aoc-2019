class Intcode():
    def __init__(self, m, name='Unnamed Computer'):
        self.name = name
        self.m_start = m.copy()
        self.input_buffer = []
        self.output_buffer = []
        self.opcodes = {
            1: {"nparams": 3, "fun": self.add},
            2: {"nparams": 3, "fun": self.mul},
            3: {"nparams": 1, "fun": self.inp},
            4: {"nparams": 1, "fun": self.out},
            5: {"nparams": 2, "fun": self.jit},
            6: {"nparams": 2, "fun": self.jif},
            7: {"nparams": 3, "fun": self.lt},
            8: {"nparams": 3, "fun": self.eq},
            9: {"nparams": 1, "fun": self.rb},
            99: {"nparams": 0, "fun": self.exit},
        }
        self.reset()
    
    def reset(self):
        self.m = self.m_start.copy()
        self.ip = 0
        self.relative_base = 0
        self.completed = False
        while (self.input_buffer):
            self.input_buffer.pop()
        while (self.output_buffer):
            self.output_buffer.pop()
    

    def set_input(self, inp):
        self.input_buffer.insert(0, inp)

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

        opcode = self.m[self.ip] % 100
        if opcode == 3 and len(self.input_buffer) == 0:
            return

        try:
            oc = self.opcodes[opcode]
        except KeyError:
            print(f'Unkown opcode: {opcode}')
            self.completed = True
            return
        
        param_mode = self.m[self.ip] // 100
        if oc['fun'](param_mode, self.m[self.ip + 1: self.ip + 1 + oc['nparams']]):
            self.ip += oc['nparams'] + 1

    def parse_params(self, param_mode, params):
        return list(self.param_generator(param_mode, params))

    def param_generator(self, param_modes, params):
        for i, p in enumerate(params):
            param_mode = param_modes // 10 ** i % 10
            if param_mode == 0:
                yield self.m[p]
            elif param_mode == 1:
                yield p
            elif param_mode == 2:
                yield self.m[self.relative_base+p]
            else:
                return ValueError("Invalid parameter mode.")

    def add(self, param_mode, params):
        parsed_params = self.parse_params(param_mode, params)
        self.m[params[2]] = parsed_params[0] + parsed_params[1]
        return True

    def mul(self, param_mode, params):
        parsed_params = self.parse_params(param_mode, params)
        self.m[params[2]] = parsed_params[0] * parsed_params[1]
        return True

    def inp(self, param_mode, params):
        self.m[params[0]] = self.input_buffer.pop()
        return True
    
    def out(self, param_mode, params):
        parsed_params = self.parse_params(param_mode, params)
        self.output_buffer.insert(0, parsed_params[0])
        return True

    def jit(self, param_mode, params):
        parsed_params = self.parse_params(param_mode, params)
        if parsed_params[0]:
            self.ip = parsed_params[1]
            return False
        else:
            return True

    def jif(self, param_mode, params):
        parsed_params = self.parse_params(param_mode, params)
        if not parsed_params[0]:
            self.ip = parsed_params[1]
            return False
        else:
            return True

    def lt(self, param_mode, params):
        parsed_params = self.parse_params(param_mode, params)
        self.m[params[2]] = int(parsed_params[0] < parsed_params[1])
        return True
    
    def eq(self, param_mode, params):
        parsed_params = self.parse_params(param_mode, params)
        self.m[params[2]] = int(parsed_params[0] == parsed_params[1])
        return True
    
    def rb(self, param_mode, params):
        parsed_params = self.parse_params(param_mode, params)
        self.relative_base = parsed_params[0]
        return True
        
    def exit(self, param_mode, params):
        self.completed = True
        return False
