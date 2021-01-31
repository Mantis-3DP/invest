import requests
import time

class cryptoticker:

    def krak(self, ticker):
        uri = "https://api.kraken.com/0/public/Ticker"
        j_feed = uri + "?pair=" + ticker
        r = requests.get(j_feed)
        btc, size = r.json()["result"][ticker]["c"]
        # x = ( "last trade: %s BTC at %s EUR" ) %(size, btc)
        return float(btc), size

    def printPrice(self):
        price2 = 0
        while True:
            price, size = self.krak("XXBTZEUR")

            if price != price2:
                print("BTC: {} EUR".format(round(price, 1)))
            price2 = price
            time.sleep(1)


if __name__ == "__main__":
    cryptoticker().printPrice()
