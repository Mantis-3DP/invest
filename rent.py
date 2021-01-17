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


class rent:

    def __init__(self, wohnlagenklasse, Baujahr):

        # Characteristics of the building

        self.wohnlagenklasse = wohnlagenklasse
        self.Baujahr = Baujahr


    def calcNetRent(self, Qm_aprt, count_room):

        # N_aprt: total number of apartments in the building
        # Qm_aprt: Size of a single of the apartments
        # count_room: number of rooms in each apartment
        # qmPrices: price per qm in dependence of number of rooms in that apartment

        # dictionaries for the different amount of rooms

        qmPrices = pd.read_csv(str(pathlib.Path(__file__).parent) + "/data/qmPrices.csv", index_col=0)
        qmPrices.columns = qmPrices.columns.astype(int)

        # fail safe if apartment has more than 5 rooms 
        if count_room > 5:
            count_room = 5

        # calculation of the qm price


        if Qm_aprt % 5 == 0:
            return round((qmPrices[count_room][Qm_aprt] * Qm_aprt), 2)

        else:
            # with linear interpolation
            Qm_aprt_lower = Qm_aprt - Qm_aprt % 5
            Qm_aprt_upper = Qm_aprt_lower + 5
            interpolation = ((qmPrices[count_room][Qm_aprt_upper] - qmPrices[count_room][Qm_aprt_lower]) / 5) * (
                        Qm_aprt % 5)

            return round(((qmPrices[count_room][Qm_aprt_lower] + interpolation) * Qm_aprt), 2)

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

    def calcRent(self, Qm_aprt, count_room):

        netRent = self.calcNetRent(Qm_aprt, count_room)
        rent = round(netRent + netRent * self.calcSurchargeRent(), 2)

        return rent

    def calcRentBuilding(self):
        aprts = pd.read_csv(str(pathlib.Path(__file__).parent) + "/data/aprts.csv")
        rentBuilding: int = 0
        netRentBuilding: int = 0
        for i in range(aprts.shape[0]):
            rentBuilding += self.calcRent(Qm_aprt=aprts["Qm_aprt"][i], count_room=aprts["count_room"][i])
            netRentBuilding += self.calcNetRent(Qm_aprt=aprts["Qm_aprt"][i], count_room=aprts["count_room"][i])
        return rentBuilding, netRentBuilding



if __name__ == "__main__":
    test = rent(wohnlagenklasse= 4, Baujahr= 2000)
    print("Monatliche Nettomieteinnahmen dieser Wohnung sind:   {}€"
        .format(test.calcNetRent(Qm_aprt=75.62, count_room=3)))
    print("Monatliche Mieteinnahmen dieser Wohnung sind:        {}€"
        .format(test.calcRent(Qm_aprt=75.62, count_room=3)))

    rentBuilding, netRentBuilding = test.calcRentBuilding()
    print("Monatliche Nettomieteinnahmen des Gebäudes sind:     {}€"
        .format(netRentBuilding))
    print("Monatliche Mieteinnahmen des Gebäudes sind:          {}€"
        .format(rentBuilding))



