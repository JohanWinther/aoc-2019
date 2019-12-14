from intcode import Intcode

def get_output(t):
    m = [int(n) for i, n in enumerate(t.split(','))]
    computer = Intcode(m, name="BOOST")
    computer.run()
    return computer.output_buffer

# Test 1
print("Test 1:")
t = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
m = [int(n) for i, n in enumerate(t.split(','))]
out = get_output(t)
print(out)
print(out == m, end="\n\n")

# Test 2
print("Test 2:")
t = "1102,34915192,34915192,7,4,7,99,0"
out = get_output(t)
print(out[0])
print(len(str(out[0])) == 16, end="\n\n")

# Test 3
print("Test 3:")
t = "104,1125899906842624,99"
out = get_output(t)
print(out[0])
print(out[0] == 1125899906842624, end="\n\n")

# Day 9.1
print("Day 9.1")
with open(__file__.replace(".py", "I.txt")) as f:
    t = f.readline().rstrip()
m = [int(n) for i, n in enumerate(t.split(','))]
computer = Intcode(m, name="BOOST")
computer.set_input(1)
computer.run()
out = computer.output_buffer
print(out[0])
