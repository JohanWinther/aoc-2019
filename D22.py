import itertools
from timeit import default_timer as timer

class Deck():

    class Card():

        def __init__(self, number=0):
            self.number = number
            self.next = None
            self.prev = None

        def __str__(self):
            return str(self.number)

    def __init__(self, length):
        self.length = length
        self.direction = 1

        # Create cards
        self.start = Deck.Card()
        prev_card = self.start
        for i in range(1, self.length):
            card = Deck.Card(i)
            prev_card.next = card
            card.prev = prev_card
            prev_card = card
        # Link last and first
        prev_card.next = self.start
        self.start.prev = prev_card

    def cards(self):
        card = self.start
        while True:
            yield card
            if self.direction == 1:
                card = card.next
            elif self.direction == -1:
                card = card.prev

    def list_cards(self):
        return list(itertools.islice(self.cards(), self.length))

    def card(self, N):
        if N >= 0:
            return next(itertools.islice(self.cards(), N, N + 1))
        else:
            return next(itertools.islice(self.cards(), self.length + N, self.length + N + 1))

    def find(self, number):
        position = 0
        cards = self.cards()
        card = next(cards)
        while card.number != number:
            card = next(cards)
            position += 1
        return position

    def reverse(self):
        self.direction *= - 1
        if self.direction == 1:
            self.start = self.start.next
        elif self.direction == -1:
            self.start = self.start.prev

    def cut(self, N):
        self.start = self.card(N)

    # Solve this without a stack?
    def increment(self, N):
        stack = [None] * self.length
        index = 0
        dealt_cards = 0
        cards = self.cards()
        while dealt_cards < self.length:
            stack[index] = next(cards)
            index = (index + N) % self.length
            dealt_cards += 1

        self.direction = 1
        self.start = stack[0]
        prev_card = self.start
        for i in range(1, self.length):
            card = stack[i]
            card.prev = prev_card
            prev_card.next = card
            prev_card = card
        prev_card.next = self.start
        self.start.prev = prev_card

    def parse(self, instructions):
        for instruction in instructions:
            if "deal with increment " in instruction:
                self.increment(int(instruction[20:]))
            elif "deal into new stack" in instruction:
                self.reverse()
            elif "cut " in instruction:
                self.cut(int(instruction[4:]))

    def __str__(self):
        return " ".join([str(card) for card in self.list_cards()])


class MathDeck():

    def __init__(self, length):
        self.length = length
        self.shuffles = []
        self.inv_methods = [self.rev, self.icut, self.iinc]
        self.methods = [self.rev, self.cut, self.inc]

    def parse(self, instructions):
        for i, instruction in enumerate(instructions):
            if "deal into new stack" in instruction:
                self.shuffles.append((0, 0))
            elif "cut " in instruction:
                self.shuffles.append((1, int(instruction[4:])))
            elif "deal with increment " in instruction:
                self.shuffles.append((2, int(instruction[20:])))

    def compact_multiple(self, iterations):
        factor = self.compact(shuffles=self.shuffles)
        self.shuffles = []

        iterations_left = self.length - iterations - 1
        while iterations_left != 0:
            if iterations_left % 2 == 1:
                self.shuffles += factor
                self.compact()
            factor += factor
            factor = self.compact(shuffles=factor)
            iterations_left //= 2

    def compact(self, shuffles=None):
        
        will_return = True
        if not shuffles:
            will_return = False
            shuffles = self.shuffles

        # Compact rev
        compacted = []
        reverse = False
        for method, value in shuffles:
            if method == 0:
                reverse = not reverse
                continue
            elif not reverse:
                compacted.append((method, value))
                continue
            elif method == 1:
                cut = (value + self.length) % self.length
                compacted.append((1, self.length - cut))
            elif method == 2:
                compacted.append((method, value))
                compacted.append((1, self.length + 1 - value))
        if reverse:
            compacted.append((0, 0))

            
        shuffles = compacted
        # Compact cut
        compacted = []
        cut = 0
        for method, value in shuffles:
            if method == 0:
                if cut != 0:
                    compacted.append((1, cut))
                    cut = 0
                compacted.append((method, value))
            elif method == 1:
                cut = (cut + value) % self.length
            elif method == 2:
                compacted.append((method, value))
                cut = (cut * value) % self.length

        if cut != 0:
            compacted.append((1, cut))
            cut = 0

        shuffles = compacted
        # Compact inc
        compacted = []
        increment = 1
        for method, value in shuffles:
            if method == 2:
                increment = (increment * value) % self.length
            else:
                if increment != 1:
                    compacted.append((2, increment))
                    increment = 1
                compacted.append((method, value))

        if increment != 1:
            compacted.append((2, increment))
            increment = 1

        if not will_return:
            self.shuffles = compacted
        else:
            return compacted

    def cards(self):
        for position in range(self.length):
            yield self.card(position)

    def find(self, x):
        for method, n in self.shuffles:
            x = self.methods[method](x, n)
        return x

    def card(self, y):
        for method, n in reversed(self.shuffles):
            y = self.inv_methods[method](y, n)
        return y

    def rev(self, y, n):
        return self.length - 1 - y

    def cut(self, x, n):
        return (x - n) % self.length

    def icut(self, y, n):
        return (y + n) % self.length

    def inc(self, x, n):
        return (x * n) % self.length

    '''
    https://math.stackexchange.com/questions/684550/how-to-reverse-modulo-of-a-multiplication
    https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
    '''

    def iinc(self, y, n):
        t, nt = 0, 1
        r, nr = self.length, n
        while nr != 0:
            q = r // nr
            (t, nt) = (nt, t - q * nt)
            (r, nr) = (nr, r - q * nr)
        if r > 1:
            raise ArithmeticError(
                f"{n} and {self.length} are not coprime: " +
                f"gcd({n}, {self.length}) = {r} != 1"
            )
        if t < 0:
            t += self.length
        return (t * y) % self.length

    def __str__(self):
        shuffles = ['rev', 'cut', 'inc']
        return (
            "Shuffles:\n" +
            "\n".join([f"{shuffles[s[0]]} {s[1] if s[0] != 0 else ''}" for s in self.shuffles])
        )


with open(__file__.replace(".py", "I.txt")) as f:
    t = f.read()
instructions = t.split("\n")

# Part 1

print("Doubly linked list:")
start = timer()

deck = Deck(10007)
deck.parse(instructions)
pos = deck.find(2019)

end = timer()
list_result = end - start
print("Time:", end - start, "s")
print("Card 2019 is at",pos)

print()

print("Modulus math:")
start = timer()

deck = MathDeck(10007)
deck.parse(instructions)
deck.compact()
pos = deck.find(2019)

end = timer()
math_result = end - start
print("Time:", end - start, "s")
print("Card 2019 is at", pos)

print()

print("Modulus math is", int(list_result // math_result), "times faster")

print()

# Part 2
CARDS = 119315717514047
SHUFFLES = 101741582076661
POSITION = 2020

start = timer()

deck = MathDeck(CARDS)
deck.parse(instructions)
deck.compact_multiple(SHUFFLES)
card = deck.find(POSITION)

end = timer()
math_result = end - start
print("Time:", end - start, "s")
print("Card", card, "is at", POSITION)
