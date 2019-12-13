from intcode import Intcode

with open(__file__.replace(".py", "I.txt")) as f:
    t = f.readline().rstrip()

t = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
m = [int(n) for i, n in enumerate(t.split(','))]

computer = Intcode(m, name="BOOST")
computer.run()

print(computer.output_buffer)
