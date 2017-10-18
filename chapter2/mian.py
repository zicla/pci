from recommendations import critics
from recommendations import sim_distance
from math import sqrt

if __name__ == '__main__':
    d = sim_distance(critics, 'Lisa Rose', 'Claudia Puig')
    print d
