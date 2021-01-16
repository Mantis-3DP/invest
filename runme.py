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
df = pd.read_csv(str(datapath)+"/data/roomPrices.csv", index_col=0)

class investment:

    def __init__(self, maxGeschoss, aGrund, GFZ, wertHaus):

        self.maxGeschoss = maxGeschoss
        self.aGrund = aGrund
        self.GFZ = GFZ
        self.wertHaus = wertHaus


        pass

    def calcNetRent(self, N_aprt, Qm_aprt, count_room):
        #dictionarys for the different amount of rooms



        one_room_prices = dict([
                (15 , 19.02),
                (20 , 15),
                (25 , 12.73),
                (30 , 11.34),
                (35 , 10.44),
                (40 , 9.85),
                (45 , 9.45),
                (50 , 9.19),
                (55 , 9.01),
                (60 , 8.91),
                (65 , 8.85),
                (70 , 8.83)])

        two_room_prices = dict([
                (25, 12.86),
                (30, 11.45),
                (35, 10.53),
                (40, 9.93),
                (45, 9.52),
                (50, 9.25),
                (55, 9.07),
                (60, 8.96),
                (65, 8.90),
                (70, 8.88),
                (75, 8.88),
                (80, 8.90),
                (85, 8.93),
                (90, 8.97),
                (95, 9.02),
                (100, 9.07)])

        three_room_prices = dict([
                (40, 9.45),
                (45, 9.09),
                (50, 8.86),
                (55, 8.72),
                (60, 8.64),
                (65, 8.61),
                (70, 8.60),
                (75, 8.62),
                (80, 8.66),
                (85, 8.71),
                (90, 8.76),
                (95, 8.82),
                (100, 8.88),
                (105, 8.93),
                (110, 8.99),
                (115, 9.04),
                (120, 9.08),
                (125, 9.12),
                (130, 9.15)])

        four_room_prices = dict([
                (55, 8.48),
                (60, 8.42),
                (65, 8.40),
                (70, 8.42),
                (75, 8.45),
                (80, 8.50),
                (85, 8.55),
                (90, 8.61),
                (95, 8.68),
                (100, 8.74),
                (105, 8.81),
                (110, 8.87),
                (115, 8.92),
                (120, 8.98),
                (125, 9.01),
                (130, 9.05),
                (135, 9.08),
                (140, 9.09),
                (145, 9.10),
                (150, 9.10),
                (155, 9.09),
                (160, 9.07)])

        five_room_prices = dict([
                (70, 8.31),
                (75, 8.35),
                (80, 8.40),
                (85, 8.46),
                (90, 8.53),
                (95, 8.60),
                (100, 8.67),
                (105, 8.73),
                (110, 8.80),
                (115, 8.85),
                (120, 8.91),
                (125, 8.95),
                (130, 8.99),
                (135, 9.02),
                (140, 9.04),
                (145, 9.05),
                (150, 9.05),
                (155, 9.04),
                (160, 9.02),
                (165, 8.99)])

        # dictionary for the different amount of rooms  
        qm_prices = dict([  (1, one_room_prices),
                            (2, two_room_prices),
                            (3, three_room_prices),
                            (4, four_room_prices),
                            (5, five_room_prices)])

        # fail safe if apartment has more that 5 rooms 
        if count_room > 5:
            count_room = 5


        #calculation of the qm price with linear interpolation
        if Qm_aprt%5 == 0:
            return round((qm_prices[count_room][Qm_aprt] * Qm_aprt) * N_aprt, 2)

        else:
            Qm_aprt_lower = Qm_aprt - Qm_aprt%5
            Qm_aprt_upper = Qm_aprt_lower + 5
            interpolation = ((qm_prices[count_room][Qm_aprt_upper] - qm_prices[count_room][Qm_aprt_lower]) / 5) * (Qm_aprt%5)

            return round(((qm_prices[count_room][Qm_aprt_lower] + interpolation) * Qm_aprt) * N_aprt, 2)

    def aWohn(self):
        maxA = self.aGrund * self.GFZ


        return maxA



    def ruecklagen(self):

        rueckpa = self.wertHaus * 0.02
        rueckpm = rueckpa/12

        return rueckpa, rueckpm





if __name__ == "__main__":

    test = investment(2,564,0.4,700000)
    print(test.aWohn())
    print(test.calcNetRent(N_aprt = 6, Qm_aprt = 74.53, count_room = 3))
