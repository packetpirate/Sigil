#from __future__ import division

import numpy as np
import pygame
import math

WIDTH = 1024
HEIGHT = 768

TITLE = "Gesture Recognition Test"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

HALF_PI = (math. pi / 2)
TWO_PI = (math. pi * 2)

POINT_DIST = 10

# I guess Python's trigonometric functions don't play nicely with a y-down coordinate system. Dumb...
#DIRECTIONS = [0, (math.pi / 4), HALF_PI, (math.pi * (3 / 4)), math.pi, (math.pi * (5 / 4)), ((3 / 2) * math.pi), (math.pi * (7 / 4)), TWO_PI]
DIRECTIONS = [0, (math.pi * (7 / 4)), (math.pi * (3 / 2)), (math.pi * (5 / 4)), math.pi, (math.pi * (3 / 4)), HALF_PI, (math.pi / 4), TWO_PI]

SIGILS = ["222888",
          "55677811",
          "5577117755",
          "777111333",
          "456781876",
          "7774411"]
SIGIL_MAP = dict({"222888":"Fire",
                  "55677811":"Wind",
                  "5577117755":"Water",
                  "777111333":"Earth",
                  "456781876":"Darkness",
                  "7774411":"Light"})

def hyp(p1, p2):
    theta = math.atan2((p2[1] - p1[1]), (p2[0] - p1[0]))
    theta = ((theta + (math.pi * 2)) % (math.pi * 2))
    return theta

def leven(s, t):
    n = len(s) + 1
    m = len(t) + 1

    matrix = np.zeros((n, m))

    for x in range(n):
        matrix[x][0] = x
    for y in range(m):
        matrix[0][y] = y

    for x in range(1, n):
        for y in range(1, m):
            cost = 1
            if s[x - 1] == t[y - 1]:
                cost = 0

            matrix[x][y] = min(
                (matrix[x - 1][y] + 1),
                (matrix[x - 1][y - 1] + cost),
                (matrix[x][y - 1] + 1)
            )

    return int(matrix[n - 1][m - 1])

class Sigil:
    def __init__(self, points):
        self.directions = self.normalize(points)

    def normalize(self, points):
        dir = []
        for p in range(len(points) - 1):
            p1 = points[p]
            p2 = points[p + 1]
            theta = hyp(p1, p2)
            closest = 0
            cDiff = TWO_PI
            for i in range(len(DIRECTIONS)):
                direction = DIRECTIONS[i]
                diff = abs(theta - direction)
                if diff < cDiff:
                    cDiff = diff
                    closest = i
            if closest == (len(DIRECTIONS) - 1):
                dir.append(1)
            else:
                dir.append(closest + 1)
        return dir

    def findMatch(self):
        start = self.__repr__()
        closest = 0
        cDist = len(start) * 1000 # Just a ridiculous length to ensure anything will be less than it.
        for i in range(len(SIGILS)):
            sigil = SIGILS[i]
            dist = leven(start, sigil)
            if dist < cDist:
                cDist = dist
                closest = i
        return SIGILS[closest]

    def __repr__(self):
        return ''.join(str(x) for x in self.directions)

class App:
    def __init__(self):
        self.running = False
        self.cTime = 0

        self.points = []

        self.lmb, self.mmb, self.rmb = False, False, False

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        #pygame.display.toggle_fullscreen()

    def handleEvents(self):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)):
                self.running = False
        self.lmb, self.mmb, self.rmb = pygame.mouse.get_pressed()

    def update(self):
        pos = pygame.mouse.get_pos()
        if self.lmb:
            if len(self.points) == 0:
                self.points.append(pos)
            else:
                last = self.points[len(self.points) - 1]
                dist = math.sqrt(((last[0] - pos[0]) ** 2) + ((last[1] - pos[1]) ** 2))
                if dist >= POINT_DIST:
                    self.points.append(pos)
        else:
            if len(self.points) > 1:
                sigil = Sigil(self.points)
                match = sigil.findMatch()
                print("User Input: %s\nMatch: %s\nSpell: %s" % (sigil, match, SIGIL_MAP[match]))
                self.points = []

        if self.rmb:
            self.points = []

    def render(self):
        self.screen.fill(BLACK)
        if len(self.points) > 1:
            pygame.draw.lines(self.screen, WHITE, False, self.points, 2)
        pygame.display.update()

    def execute(self):
        self.running = True
        while self.running:
            self.cTime = pygame.time.get_ticks()
            self.handleEvents()
            self.update()
            self.render()

app = App()
app.execute()
