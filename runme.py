# import yfinance as yf
#
#
#
# data = yf.download("SPY AAPL", start="2017-01-01", end="2017-04-30")
#
# print(data)


import numpy as np
import pandas as pd
import pathlib

datapath = pathlib.Path(__file__).parent
roomPrices = pd.read_csv(str(datapath) + "/data/qmPrices.csv", index_col=0)


class investment:

    def __init__(self, maxGeschoss, aGrund, GFZ, wertHaus, wohnlagenklasse, Baujahr, N_aprt, count_room):

        self.maxGeschoss = maxGeschoss
        self.aGrund = aGrund
        self.GFZ = GFZ
        self.wertHaus = wertHaus
        self.wohnlagenklasse = wohnlagenklasse
        self.Baujahr = Baujahr
        self.N_aprt = N_aprt
        self.count_room = count_room

    def calcNetRent(self):

        # N_aprt: total number of apartments in the building
        # Qm_aprt: Size of a single of the apartments
        # count_room: number of rooms in each apartment
        # qmPrices: price per qm in dependence of number of rooms in that apartment

        # dictionaries for the different amount of rooms

        datapath = pathlib.Path(__file__).parent
        qmPrices = pd.read_csv(str(datapath) + "/data/qmPrices.csv", index_col=0)
        qmPrices.columns = qmPrices.columns.astype(int)

        # fail safe if apartment has more than 5 rooms 
        if self.count_room > 5:
            self.count_room = 5

        # calculation of the qm price
        Qm_aprt = self.aWohn() / self.N_aprt

        if Qm_aprt % 5 == 0:
            return round((qmPrices[self.count_room][Qm_aprt] * Qm_aprt) * self.N_aprt, 2)

        else:
            # with linear interpolation
            Qm_aprt_lower = Qm_aprt - Qm_aprt % 5
            Qm_aprt_upper = Qm_aprt_lower + 5
            interpolation = ((qmPrices[self.count_room][Qm_aprt_upper] - qmPrices[self.count_room][Qm_aprt_lower]) / 5) * (
                        Qm_aprt % 5)

            return round(((qmPrices[self.count_room][Qm_aprt_lower] + interpolation) * Qm_aprt) * self.N_aprt, 2)

    def calcSurchargeRent(self):
        surcharge = 0

        wohnlagenklasseDict = dict([(1,-0.07),(2,0.02),(3,0.07),(4,0.19)])

        try:
            surcharge += wohnlagenklasseDict[self.wohnlagenklasse]  
        except KeyError as e:
            print('Wohnlagenklasse {} außerhalb der erlaubten 1-4'.format(e))

        if self.Baujahr <= 1948:
            surcharge += 0.03
        elif self.Baujahr >= 1949 and self.Baujahr <= 1977:
            pass
        elif self.Baujahr >= 1978 and self.Baujahr <= 2001:
            surcharge += 0.02
        elif self.Baujahr >= 2002 and self.Baujahr <= 2009:
            surcharge += 0.04
        elif self.Baujahr >= 2010 and self.Baujahr <= 2013:
            surcharge += 0.07
        elif self.Baujahr >= 2014:
            surcharge += 0.14
        else:
            print('Baujahr außerhalb der Tabelle')

        return surcharge

    def calcRent(self):

        netRent = self.calcNetRent()
        rent = round(netRent + netRent * self.calcSurchargeRent(), 2)

        return rent


    def aWohn(self):
        maxA = self.aGrund * self.GFZ
        return round(maxA, 2)

    def ruecklagen(self):
        rueckpa = self.wertHaus * 0.02
        rueckpm = rueckpa / 12

        return rueckpa, rueckpm


if __name__ == "__main__":
    test = investment(maxGeschoss = 4, aGrund = 564, GFZ = 0.8, wertHaus = 700000, wohnlagenklasse= 4, Baujahr= 2000, N_aprt= 6, count_room= 3)
    print("Monatliche Nettomieteinnahmen sind:  {}€"
        .format(test.calcNetRent()))
    print("Monatliche Mieteinnahmen sind:       {}€"
        .format(test.calcRent()))
