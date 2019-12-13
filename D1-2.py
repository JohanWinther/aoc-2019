import math
def fuel_req(mass):
    fuel_m = mass//3-2
    if (fuel_m < 0):
        return 0
    else:
        return fuel_m + fuel_req(fuel_m)

with open('day1-input.txt') as f:
    masses = [int(l) for l in f.readlines()]
fuel = [fuel_req(m) for m in masses]
print(sum(fuel))