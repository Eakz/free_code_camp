import random

class Hat:
    def __init__(self, **contents):
        # initializing empty array
        self.contents = []
        # populating self.contents array with required amount of balls to draw
        [[self.contents.append(i[0]) for _ in range(i[1])]
         for i in contents.items()]
        self.backup = self.contents[:]

    # Draw method with number of attempts to try and draw the ball
    #  - returning full stack if attempts > len
    def draw(self, attempts):
        self.contents = self.backup[:]
        return [self.contents.pop(random.randint(0, len(self.contents)-1)) for i in range(attempts)] if attempts <= len(self.contents) else self.contents

def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    # '''
    # Main experiment function:
    # hat - Hat object with seeded balls
    # epxected_expected balls - exected combination of balls to be drawn for success
    # num_balls_drawn - number of attempts for new draw
    # num_experiments - total number of new draws
    # '''
    result = 0
    for _ in range(num_experiments):
        single_draw = hat.draw(num_balls_drawn)
        if(all([True if single_draw.count(i) >= expected_balls[i] else False for i in expected_balls])):
            result += 1
    return result/num_experiments

