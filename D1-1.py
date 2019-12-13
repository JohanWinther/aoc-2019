import math
def fuel_req(mass):
    return mass//3 - 2

with open('day1-input.txt') as f:
    masses = [int(l) for l in f.readlines()]

fuel = [fuel_req(m) for m in masses]
print(sum(fuel))