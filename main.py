import json
import random

import numpy as np
import mahotas
import math
import time
import geography as geo
from pprint import pprint

from matplotlib import pyplot as plt
import matplotlib.path as mplPath


def calculateCoordinates(latitude: float, longitude: float):
    blocks = 7680
    tiles = 15
    latitudeDirection = ""
    latitudeHour = 0
    latitudeMinute = 0
    latitudeSecond = 0

    if longitude < 0:
        latitudeDirection = "south"
        latitudeHour = math.floor(-1 * latitude)
        latitudeMinute = math.floor((-1 * latitude - latitudeHour) * 60)
        latitudeSecond = math.floor(-1 * latitude - (latitudeHour + latitudeMinute / 60)) * 3600
    else:
        latitudeDirection = "north"
        latitudeHour = math.floor(latitude)
        latitudeMinute = math.floor((latitude - latitudeHour) * 60)
        latitudeSecond = (latitude - (latitudeHour + latitudeMinute / 60)) * 3600

    longitudeDirection = ""
    longitudeHour = 0
    longitudeMinute = 0
    longitudeSecond = 0

    if longitude < 0:
        longitudeDirection = "west"
        longitudeHour = math.floor(-1 * longitude)
        longitudeMinute = math.floor((-1 * longitude - longitudeHour) * 60)
        longitudeSecond = (-1 * longitude - (longitudeHour + longitudeMinute / 60)) * 3600
    else:
        longitudeDirection = "east"
        longitudeHour = math.floor(longitude)
        longitudeMinute = math.floor((longitude - longitudeHour) * 60)
        longitudeSecond = (longitude - (longitudeHour + longitudeMinute / 60)) * 3600

    xCoordinate = round(longitude * blocks / tiles)
    yCoordinate = 255
    zCoordinate = -1 * round(latitude * blocks / tiles)
    return {
        "x": int(xCoordinate),
        "y": int(yCoordinate),
        "z": int(zCoordinate)
    }


def render(poly):
    """Return polygon as grid of points inside polygon.

    Input : poly (list of lists)
    Output : output (list of lists)
    """
    xs, ys = zip(*poly)
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)

    newPoly = [(int(x - minx), int(y - miny)) for (x, y) in poly]

    X = maxx - minx + 1
    Y = maxy - miny + 1

    grid = np.zeros((X, Y), dtype=np.int8)
    mahotas.polygon.fill_polygon(newPoly, grid)

    return [(x + minx, y + miny) for (x, y) in zip(*np.nonzero(grid))]


def renderBorders(alpha3: str):
    coordinatesFile = json.loads(open(fr"countries/{alpha3}.json").read())
    newList = []
    if len(coordinatesFile) > 1:
        for listTemp in coordinatesFile:
            for coor in listTemp[0]:
                temp = calculateCoordinates(coor[0], coor[1])
                newList.append([temp["x"], temp["z"]])
    else:
        for coor in coordinatesFile[0]:
            temp = calculateCoordinates(coor[0], coor[1])
            newList.append([temp["x"], temp["z"]])
    print("Done!")

    poly2 = newList

    plt.figure(None)
    x, y = zip(*render(poly2))
    plt.scatter(x, y)
    x, y = zip(*poly2)
    plt.plot(x, y, c="r")
    plt.show()
    return newList
