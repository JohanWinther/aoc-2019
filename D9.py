from intcode import Intcode

with open(__file__.replace(".py","I.txt")) as f:
    m = [int(n) for n in f.readline().rstrip().split(',')]

computer = Intcode(m, name="BOOST")
