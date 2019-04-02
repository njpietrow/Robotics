from pyCreate2 import create2
import lab10_map
import random
import numpy
import vertex


class Run:
    def __init__(self, factory):
        self.create = factory.create_create()
        self.time = factory.create_time_helper()
        self.map = lab10_map.Map("lab10.png")
        self.RRTree = RRTree(1,self.map)

    def run(self):

        for i in range(2000):
            #generate random x
            x_pos = random.randint(0,299)
            y_pos = random.randint(0,334)
            randompoint = vertex.vertex(x_pos,y_pos)
            closest = self.RRTree.find_nearest(randompoint)
            actual = self.RRTree.place_point(closest, randompoint)
            if actual is None:
                continue
            if closest.getDistance(actual.x, actual.y) < self.RRTree.delta:
                continue
            else:
                print("adding point", i)
                self.RRTree.vertices.append(actual)
                self.RRTree.pairs.append((actual, closest))
                actual.parent = closest

        self.RRTree.draw(self.RRTree.pairs)
        print(len(self.RRTree.vertices))

        solution = self.RRTree.find_nearest(self.RRTree.goal)
        path = []
        while True:
            if solution.parent is not None:
                self.map.draw_line((solution.x, solution.y), (solution.parent.x, solution.parent.y), (0, 0, 255))
                path.append(solution)
                solution = solution.parent
            else:
                break

        self.map.save("lab10_rrt.png")



class RRTree:
    def __init__(self, delta, lab10map):
        self.vertices = []
        # starting point defined below
        self.vertices.append(vertex.vertex(270, 300))
        self.map = lab10map
        self.pairs = []
        self.delta = delta
        self.goal = vertex.vertex(40,120)

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
                    return vertex.vertex(x_array[i - 1], y_array[i - 1])
                else:
                    return None
        return vertex2

    def draw(self, array):
        for v in array:
            self.map.draw_line((v[0].x, v[0].y), (v[1].x, v[1].y), (255, 0, 0))

















