from datetime import datetime
import math
import scipy
from scipy.optimize import fsolve
from . import option_pricing
import matplotlib as mpl
mpl.rcParams['axes3d.mouserotationstyle'] = 'azel'
import matplotlib.pyplot as plt
import pytz
import numpy as np


class Call:
    def __init__(self, stock_p, strike, dividend, interest_rate, dte=None, date=None, price=None, sigma=None, american_european="european", timezone="Europe/Amsterdam", date_format='%Y-%m-%d'):
        self.stock_p = stock_p
        self.strike = strike
        self.sigma = sigma
        self.dividend = dividend
        self.interest_rate = interest_rate
        self.dte = dte
        self.date = date
        self.price = price

        # keep the old price in memory to enable changing the option price
        # to calculate new vol
        self.price_memory = price

        if american_european == "european":
            self.pricing_model = option_pricing.EurCall
        if american_european == "american":
            self.pricing_model = option_pricing.AmCall
        self.delta = None
        self.gamma = None
        self.theta = None
        self.vega = None
        self.leverage = None
        self.probability_itm = None
        self.timezone = pytz.timezone(timezone)
        self.date_format = date_format

        if self.dte is None:
            if self.is_date(date, date_format):
                self.dte = self.diff_dates()
            else:
                exit("Error: date is not a valid date")
        else:
            self.dte = dte
        self.recalculate()


    def is_date(self, val, format='%Y-%m-%d'):
        try:
            datetime.strptime(val, format)
            return True
        except ValueError:
            return False

    def diff_dates(self):
        self.date = datetime.strptime(self.date, '%Y-%m-%d')
        self.date = self.timezone.localize(self.date)
        date_diff = (self.date - datetime.now(self.timezone))
        return date_diff.days + date_diff.seconds / 86400


    def get_price(self, stock_p=None, strike=None, dividend=None, interest_rate=None, dte=None, date=None, price=None, sigma=None, Nofnodes=100):
        if sigma is None:
            sigma = self.get_vol(stock_p, strike, dividend, interest_rate, dte, date, price, sigma, Nofnodes)
        return self.pricing_model(stock_p, strike, sigma, dividend, interest_rate, dte, Nofnodes)

    def get_vol(self, stock_p=None, strike=None, dividend=None, interest_rate=None, dte=None, date=None, price=None, sigma=None, Nofnodes=100):
        sigma = fsolve(lambda x: self.pricing_model(stock_p, strike, x, dividend, interest_rate, dte, Nofnodes) - price, 0.2)
        return sigma[0]

    def get_delta(self, stock_p=None, strike=None, dividend=None, interest_rate=None, dte=None, date=None, price=None, sigma=None, Nofnodes=100, d=1):
        delta = (self.pricing_model(stock_p + d, strike, sigma, dividend, interest_rate, dte, Nofnodes) - self.pricing_model(stock_p - d, strike, sigma, dividend, interest_rate, dte, Nofnodes)) / (2 * d)
        return delta

    def get_gamma(self, stock_p=None, strike=None, dividend=None, interest_rate=None, dte=None, date=None, price=None, sigma=None, Nofnodes=100, dgamma=1, ddelta=1):
        gamma = (self.get_delta(stock_p-ddelta, strike, dividend, interest_rate, dte, date, price, sigma, Nofnodes) - self.get_delta(stock_p+ddelta, strike, dividend, interest_rate, dte, date, price, sigma, Nofnodes, d=-ddelta)) / (2 * dgamma)
        return gamma       

    def get_theta(self, stock_p=None, strike=None, dividend=None, interest_rate=None, dte=None, date=None, price=None, sigma=None, Nofnodes=100, d=1):
        theta = (self.pricing_model(stock_p, strike, sigma, dividend, interest_rate, dte - d, Nofnodes) - self.pricing_model(stock_p, strike, sigma, dividend, interest_rate, dte + d, Nofnodes)) / (2 * d)
        return theta

    def get_vega(self, stock_p=None, strike=None, dividend=None, interest_rate=None, dte=None, date=None, price=None, sigma=None, Nofnodes=100, d=0.01):
        vega = (self.pricing_model(stock_p, strike, sigma + d, dividend, interest_rate, dte, Nofnodes) - self.pricing_model(stock_p, strike, sigma - d, dividend, interest_rate, dte, Nofnodes)) / (2 * d)
        return vega
    
    def get_leverage(self, stock_p=None, strike=None, dividend=None, interest_rate=None, dte=None, date=None, price=None, sigma=None, Nofnodes=100):
        leverage = self.get_delta(stock_p, strike, dividend, interest_rate, dte, date, price, sigma, Nofnodes) * stock_p / price
        return leverage
    
    def get_probability_itm(self, stock_p=None, strike=None, dividend=None, interest_rate=None, dte=None, date=None, price=None, sigma=None, Nofnodes=100):
        d1 = (math.log(stock_p / strike) + (interest_rate - dividend + sigma ** 2 / 2) * dte / 365) / (sigma * math.sqrt(dte / 365))
        return scipy.stats.norm.cdf(d1)

    def recalculate(self):
        if self.price != self.price_memory:
            self.price_memory = self.price
        else:
            self.price = self.get_price(self.stock_p, self.strike, self.dividend, self.interest_rate, self.dte, self.date, self.price, self.sigma)
        self.sigma = self.get_vol(self.stock_p, self.strike, self.dividend, self.interest_rate, self.dte, self.date, self.price, self.sigma)
        self.price_memory = self.price
        self.delta = self.get_delta(self.stock_p, self.strike, self.dividend, self.interest_rate, self.dte, self.date, self.price, self.sigma)
        self.gamma = self.get_gamma(self.stock_p, self.strike, self.dividend, self.interest_rate, self.dte, self.date, self.price, self.sigma)
        self.theta = self.get_theta(self.stock_p, self.strike, self.dividend, self.interest_rate, self.dte, self.date, self.price, self.sigma)
        self.vega = self.get_vega(self.stock_p, self.strike, self.dividend, self.interest_rate, self.dte, self.date, self.price, self.sigma)
        self.leverage = self.get_leverage(self.stock_p, self.strike, self.dividend, self.interest_rate, self.dte, self.date, self.price, self.sigma)
        self.probability_itm = self.get_probability_itm(self.stock_p, self.strike, self.dividend, self.interest_rate, self.dte, self.date, self.price, self.sigma)
        return self




    #plotting functions

    def plot_stockprice_price(self, stock_start=None, stock_end=None, Nofnodes=100, breaks=30):
        if stock_start is None:
            stock_start = self.stock_p * math.exp(-2 * self.sigma * math.sqrt(self.dte/365))
        if stock_end is None:
            stock_end = self.stock_p * math.exp(2 * self.sigma * math.sqrt(self.dte/365))

        stock_p = [stock_start + (stock_end - stock_start) / breaks * i for i in range(breaks)]
        price = [self.get_price(stock_p[i], self.strike, self.dividend, self.interest_rate, self.dte, self.date, self.price, self.sigma, Nofnodes) for i in range(breaks)]

        self.plot(stock_p, price, Xlab='Stock Price', Ylab='Price', title='Option Price vs Stock Price')




    def plot_stockprice_delta(self, stock_start=None, stock_end=None, Nofnodes=100, breaks=30):
        if stock_start is None:
            stock_start = self.stock_p * math.exp(-2 * self.sigma * math.sqrt(self.dte/365))
        if stock_end is None:
            stock_end = self.stock_p * math.exp(2 * self.sigma * math.sqrt(self.dte/365))

        stock_p = [stock_start + (stock_end - stock_start) / breaks * i for i in range(breaks)]
        delta = [self.get_delta(stock_p[i], self.strike, self.dividend, self.interest_rate, self.dte, self.date, self.price, self.sigma, Nofnodes) for i in range(breaks)]

        self.plot(stock_p, delta, Xlab='Stock Price', Ylab='Delta', title='Option Delta vs Stock Price')



    def plot_stockprice_gamma(self, stock_start=None, stock_end=None, Nofnodes=100, breaks=30):
        if stock_start is None:
            stock_start = self.stock_p * math.exp(-2 * self.sigma * math.sqrt(self.dte/365))
        if stock_end is None:
            stock_end = self.stock_p * math.exp(2 * self.sigma * math.sqrt(self.dte/365))

        stock_p = [stock_start + (stock_end - stock_start) / breaks * i for i in range(breaks)]
        gamma = [self.get_gamma(stock_p[i], self.strike, self.dividend, self.interest_rate, self.dte, self.date, self.price, self.sigma, Nofnodes) for i in range(breaks)]

        self.plot(stock_p, gamma, Xlab='Stock Price', Ylab='Gamma', title='Option Gamma vs Stock Price')



    def plot_stockprice_theta(self, stock_start=None, stock_end=None, Nofnodes=100, breaks=30):
        if stock_start is None:
            stock_start = self.stock_p * math.exp(-2 * self.sigma * math.sqrt(self.dte/365))
        if stock_end is None:
            stock_end = self.stock_p * math.exp(2 * self.sigma * math.sqrt(self.dte/365))

        stock_p = [stock_start + (stock_end - stock_start) / breaks * i for i in range(breaks)]
        theta = [self.get_theta(stock_p[i], self.strike, self.dividend, self.interest_rate, self.dte, self.date, self.price, self.sigma, Nofnodes) for i in range(breaks)]

        self.plot(stock_p, theta, Xlab='Stock Price', Ylab='Theta', title='Option Theta vs Stock Price')



    def plot_stockprice_vega(self, stock_start=None, stock_end=None, Nofnodes=100, breaks=30):
        if stock_start is None:
            stock_start = self.stock_p * math.exp(-2 * self.sigma * math.sqrt(self.dte/365))
        if stock_end is None:
            stock_end = self.stock_p * math.exp(2 * self.sigma * math.sqrt(self.dte/365))

        stock_p = [stock_start + (stock_end - stock_start) / breaks * i for i in range(breaks)]
        vega = [self.get_vega(stock_p[i], self.strike, self.dividend, self.interest_rate, self.dte, self.date, self.price, self.sigma, Nofnodes) for i in range(breaks)]

        self.plot(stock_p, vega, Xlab='Stock Price', Ylab='Vega', title='Option Vega vs Stock Price')




    def plot_price_sigma(self, sigma_start=None, sigma_end=None, Nofnodes=100, breaks=30):
        if sigma_start is None:
            sigma_start = 0.01
        if sigma_end is None:
            sigma_end = 1

        sigma = [sigma_start + (sigma_end - sigma_start) / breaks * i for i in range(breaks)]
        price = [self.get_price(self.stock_p, self.strike, self.dividend, self.interest_rate, self.dte, self.date, self.price, sigma[i], Nofnodes) for i in range(breaks)]

        self.plot(sigma, price, Xlab='Volatility', Ylab='Price', title='Option Price vs Volatility')





    def plot_stockprice_time_value(self, stock_start=None, stock_end=None, days_in_future_start = None, days_in_future_end = None, Nofnodes=100, breaks=30):
        if stock_start is None:
            stock_start = self.stock_p * math.exp(-2 * self.sigma * math.sqrt(self.dte/365))
        if stock_end is None:
            stock_end = self.stock_p * math.exp(2 * self.sigma * math.sqrt(self.dte/365))
        if days_in_future_start is None:
            days_in_future_start = 0
        if days_in_future_end is None:
            days_in_future_end = self.dte

        stock_p = [stock_start + (stock_end - stock_start) / breaks * i for i in range(breaks)]
        days_in_future = [days_in_future_start + (days_in_future_end - days_in_future_start) / breaks * i for i in range(breaks)]
        option_price = [[self.get_price(stock_p[j], self.strike, self.dividend, self.interest_rate, self.dte - days_in_future[i], self.date, self.price, self.sigma, Nofnodes) for j in range(breaks)] for i in range(breaks)]
        option_price = np.array(option_price)

        self.plot(stock_p, days_in_future, option_price, Xlab='Stock Price', Ylab='Days in Future', Zlab='Price', title='Option Price vs Stock Price and Days in Future')

    def plot_stockprice_time_pnl(self, stock_start=None, stock_end=None, days_in_future_start = None, days_in_future_end = None, Nofnodes=100, breaks=30): 
        if stock_start is None:
            stock_start = self.stock_p * math.exp(-2 * self.sigma * math.sqrt(self.dte/365))
        if stock_end is None:
            stock_end = self.stock_p * math.exp(2 * self.sigma * math.sqrt(self.dte/365))
        if days_in_future_start is None:
            days_in_future_start = 0
        if days_in_future_end is None:
            days_in_future_end = self.dte

        stock_p = [stock_start + (stock_end - stock_start) / breaks * i for i in range(breaks)]
        days_in_future = [days_in_future_start + (days_in_future_end - days_in_future_start) / breaks * i for i in range(breaks)]
        pnl = [[self.get_price(stock_p[j], self.strike, self.dividend, self.interest_rate, self.dte - days_in_future[i], self.date, self.price, self.sigma, Nofnodes) - self.price for j in range(breaks)] for i in range(breaks)]
        pnl = np.array(pnl)
        self.plot(stock_p, days_in_future, pnl, Xlab='Stock Price', Ylab='Days in Future', Zlab='PnL', title='PnL vs Stock Price and Days in Future')


    def plot(self, X, Y, Z=None, Xlab=None, Ylab=None, Zlab=None, title=None):
        if Z is None:
            #2d plot
            plt.plot(X, Y)
            plt.xlabel('Stock Price')
            plt.ylabel(Ylab)
            plt.xlabel(Xlab)
            plt.show()
        else:
            # 3d plot
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            X, Y = np.meshgrid(X, Y)
            ax.plot_surface(X, Y, Z, cmap='viridis')
            ax.set_xlabel(Xlab)
            ax.set_ylabel(Ylab)
            ax.set_zlabel(Zlab)
            plt.show()



    def __str__(self):
        self.recalculate()
        return f"Call option with strike {self.strike} and price {self.price} and vol {self.sigma} at {self.date} ({self.dte} dte) \n Stock Price: {self.stock_p} \n Delta: {self.delta}\n Gamma: {self.gamma}\n Theta: {self.theta}\n Vega: {self.vega}\n Leverage: {self.leverage}\n Probability ITM: {self.probability_itm}"  

