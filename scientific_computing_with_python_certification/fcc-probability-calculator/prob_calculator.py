import random
# Consider using the modules imported above.


class Hat:
    def __init__(self, **contents):
        self.contents = []
        [[self.contents.append(i[0]) for _ in range(i[1])]
         for i in contents.items()]
        self.backup = self.contents[:]

    def draw(self, attempts):
        self.contents = self.backup[:]
        return [self.contents.pop(random.randint(0, len(self.contents)-1)) for i in range(attempts)] if attempts <= len(self.contents) else self.contents


def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    result = 0
    for _ in range(num_experiments):
        single_draw = hat.draw(num_balls_drawn)
        if(all([True if single_draw.count(i) >= expected_balls[i] else False for i in expected_balls])):
            result += 1
    return result/num_experiments


# newHat = Hat(red=3, blue=5)
# print(newHat.contents)
# print(newHat.draw(3))

# newestHat = Hat(black=6,red=4,green=3)
# probability = experiment(hat=newestHat,
#                   expected_balls={"red":2,"green":1},
#                   num_balls_drawn=5,
#                   num_experiments=2000)
# print(probability)
hat = Hat(blue=3, red=2, green=6)
probability = experiment(hat=hat, expected_balls={
                         "blue": 2, "green": 1}, num_balls_drawn=4, num_experiments=1000)
actual = probability
expected = 0.272
print(actual, ' - ', expected)
# self.assertAlmostEqual(actual, expected, delta = 0.01, msg = 'Expected experiemnt method to return a different probability.')
# hat = Hat(yellow=5, red=1, green=3, blue=9, test=1)
# probability = experiment(hat=hat, expected_balls={
#                          "yellow": 2, "blue": 3, "test": 1}, num_balls_drawn=20, num_experiments=100)
# actual = probability
# expected = 1.0
# print(actual, ' - ', expected)
