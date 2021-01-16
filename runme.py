# import yfinance as yf
#
#
#
# data = yf.download("SPY AAPL", start="2017-01-01", end="2017-04-30")
#
# print(data)

import csv
import numpy as np


import pandas as pd
import pathlib

datapath = pathlib.Path(__file__).parent
roomPrices = pd.read_csv(str(datapath)+"/data/qmPrices.csv", index_col=0)

class investment:

    def __init__(self, maxGeschoss, aGrund, GFZ, wertHaus):

        self.maxGeschoss = maxGeschoss
        self.aGrund = aGrund
        self.GFZ = GFZ
        self.wertHaus = wertHaus


        pass

    def calcNetRent(self, N_aprt, Qm_aprt, count_room):

        # N_aprt: total number of apartments in the building
        # Qm_aprt: Size of a single of the apartments
        # count_room: number of rooms in each apartment
        # qmPrices: price per qm in dependence of number of rooms in that apartment

        #dictionarys for the different amount of rooms

        datapath = pathlib.Path(__file__).parent
        qmPrices = pd.read_csv(str(datapath) + "/data/qmPrices.csv", index_col=0)
        qmPrices.columns = qmPrices.columns.astype(int)

        # fail safe if apartment has more than 5 rooms 
        if count_room > 5:
            count_room = 5

        #calculation of the qm price
        if Qm_aprt%5 == 0:
            return round((qmPrices[count_room][Qm_aprt] * Qm_aprt) * N_aprt, 2)

        else:
        	# with linear interpolation
            Qm_aprt_lower = Qm_aprt - Qm_aprt%5
            Qm_aprt_upper = Qm_aprt_lower + 5
            interpolation = ((qmPrices[count_room][Qm_aprt_upper] - qmPrices[count_room][Qm_aprt_lower]) / 5) * (Qm_aprt%5)

            return round(((qmPrices[count_room][Qm_aprt_lower] + interpolation) * Qm_aprt) * N_aprt, 2)

    def aWohn(self):
        maxA = self.aGrund * self.GFZ
        return round(maxA, 2)

    def ruecklagen(self):
        rueckpa = self.wertHaus * 0.02
        rueckpm = rueckpa/12

        return rueckpa, rueckpm

if __name__ == "__main__":

    test = investment(4,75,0.4,700000)
    print(test.aWohn())
    print(test.calcNetRent(N_aprt = 6, Qm_aprt = 74.53, count_room = 3))
