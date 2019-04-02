from pyCreate2 import create2
import lab10_map
import random
import math
import numpy


class Run:
    def __init__(self, factory):
        self.create = factory.create_create()
        self.time = factory.create_time_helper()
        self.map = lab10_map.Map("lab10.png")
        self.RRTree = RRTree(5,self.map)

    def run(self):

        #define starting point

        # This is an example on how to check if a certain point in the given map is an obstacle
        # Each pixel corresponds to 1cm

        for i in range(6000):
            #generate random x
            x_pos = random.randint(0,299)
            y_pos = random.randint(0,334)
            self.RRTree.step(vertex(x_pos,y_pos))

        for v in self.RRTree.pairs:
            self.map.draw_line((v[0].x, v[0].y), (v[1].x, v[1].y), (255, 0, 0))
        print(len(self.RRTree.vertices))

        self.map.save("lab10_rrt.png")



class RRTree:
    def __init__(self, delta, lab10map):
        self.vertices = []
        self.vertices.append(vertex(270,300))
        self.map = lab10map
        self.pairs = []
        self.delta = 2

    def find_nearest(self,vertex):
        min_distance = 500
        closest_vertex = None
        for toCheck in self.vertices:
            if toCheck is not vertex:
                distance = toCheck.getDistance(vertex.x, vertex.y)
                if distance < min_distance:
                    closest_vertex = toCheck
                    min_distance = distance
        return closest_vertex

    def place_point(self, vertex1, vertex2):
        x_array = numpy.linspace(vertex1.x, vertex2.x, 800, dtype=numpy.int)
        y_array = numpy.linspace(vertex1.y, vertex2.y, 800, dtype=numpy.int)
        for i in range(800):
            if self.map.has_obstacle(int(x_array[i]), int(y_array[i])):
                if i >= 1:
                    print("chose these coordinates", (x_array[i], y_array[i]))
                    return vertex(x_array[i - 1], y_array[i - 1])
                else:
                    return None
        return vertex2

    def step(self, randompoint):
        closest = self.find_nearest(randompoint)
        actual = self.place_point(closest, randompoint)
        if actual is None:
            return
        if closest.getDistance(actual.x, actual.y) < self.delta:
            return
        else:
            self.vertices.append(actual)
            self.pairs.append((actual, closest))
            actual.parent = closest
            return

class vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None
        self.nb = []

    def addNeighbor(self, neighbor):
        self.nb.append(neighbor)

    def getDistance(self, x, y):
        dx = self.x - x
        dy = self.y - y
        return math.sqrt(pow(dx, 2) + pow(dy, 2))











