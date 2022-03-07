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

cities = json.loads(open(r"cities.json", encoding="utf8").read())
populations = json.loads(open(r"populations.json", encoding="utf8").read())

rankingDict = {}
for city in cities:
    population = populations[city]
    techCompanies = cities[city]
    techCompaniesPerCapita = round(population / techCompanies)
    rankingDict[city] = techCompaniesPerCapita

fig = plt.figure()
ax = fig.add_axes([1, 1, 1, 1])
citiesList = list(rankingDict.keys())
rankings = []
for city in citiesList:
    rankings.append(rankingDict[city])
print(citiesList)
print(rankings)
ax.bar(citiesList, rankings)
plt.show()

#%%
