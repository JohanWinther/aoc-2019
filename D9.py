from intcode import Intcode

with open(__file__.replace(".py", "I.txt")) as f:
    t = f.readline().rstrip()

# Test 1
t = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
m = [int(n) for n in t.split(',')]
computer = Intcode(m, name="BOOST")
computer.run()
out = computer.output_buffer
print("Test 1:")
print(out)
print(out == m, end="\n\n")

# Test 2
t = "1102,34915192,34915192,7,4,7,99,0"
m = [int(n) for i, n in enumerate(t.split(','))]
computer = Intcode(m, name="BOOST")
computer.run()
print("Test 2:")
out = computer.output_buffer[0]
print(out)
print(len(str(out)) == 16, end="\n\n")
