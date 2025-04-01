from . import option_pricing
import matplotlib.pyplot as plt
import numpy as np
from . import Stock
import math

class Portfolio:
    def __init__(self, stock_p, options, quantity):
        self.options = options
        self.stock_p = stock_p
        self.quantity = quantity
        self.portfolio_price = 0
        self.delta = 0
        self.gamma = 0
        self.theta = 0
        self.vega = 0
        self.max_dte = 0
        self.min_dte = np.inf
        self.max_vol = 0
        self.recalculate()

    def recalculate(self):
        self.delta = 0
        self.gamma = 0
        self.theta = 0
        self.vega = 0
        for idx in range(len(self.options)):
            self.options[idx].recalculate()
            self.delta += self.options[idx].delta * self.quantity[idx]
            self.gamma += self.options[idx].gamma * self.quantity[idx]
            self.theta += self.options[idx].theta * self.quantity[idx]
            self.vega += self.options[idx].vega * self.quantity[idx]
            self.portfolio_price += self.options[idx].price * self.quantity[idx]
            self.max_dte = max(self.max_dte, self.options[idx].dte)
            if self.options[idx].dte > 0:
                self.min_dte = min(self.min_dte, self.options[idx].dte)
                self.max_vol = max(self.max_vol, self.options[idx].sigma)
        return self
   


    def plot_stockprice_time_value(self, stock_start=None, stock_end=None, days_in_future_start = None, days_in_future_end = None, Nofnodes=100, breaks=30):
        if stock_start is None:
            stock_start = self.stock_p * math.exp(-2*self.max_vol * math.sqrt(self.max_dte/365))
        if stock_end is None:
            stock_end = self.stock_p * math.exp(2*self.max_vol * math.sqrt(self.max_dte/365))
        if days_in_future_start is None:
            days_in_future_start = 0
        if days_in_future_end is None:
            days_in_future_end = self.min_dte
        S = [stock_start + (stock_end - stock_start) * i / breaks for i in range(breaks)]
        T = [days_in_future_end - (days_in_future_end - days_in_future_start) * i / breaks for i in range(breaks)]
        Z = [[0 for _ in range(breaks)] for _ in range(breaks)]
        for opt_idx in range(len(self.options)):  
            for stock_idx in range(breaks):
                for time_idx in range(breaks):
                    Z[time_idx][stock_idx] += self.options[opt_idx].pricing_model(S[stock_idx], self.options[opt_idx].strike, self.options[opt_idx].sigma, self.options[opt_idx].dividend, self.options[opt_idx].interest_rate, self.options[opt_idx].dte - T[time_idx], Nofnodes) * self.quantity[opt_idx]
        Z = np.array(Z)
        self.plot(S, T, Z, 'Stock Price', 'Days in Future', 'Portfolio Price', 'Portfolio Price vs Stock Price and Days in Future')

    def plot_stockprice_time_pnl(self, stock_start=None, stock_end=None, days_in_future_start = None, days_in_future_end = None, Nofnodes=100, breaks=30): 
        if stock_start is None:
            stock_start = self.stock_p * math.exp(-2*self.max_vol * math.sqrt(self.max_dte/365))
        if stock_end is None:
            stock_end = self.stock_p * math.exp(2*self.max_vol * math.sqrt(self.max_dte/365))
        if days_in_future_start is None:
            days_in_future_start = 0
        if days_in_future_end is None:
            days_in_future_end = self.min_dte
        S = [stock_start + (stock_end - stock_start) * i / breaks for i in range(breaks)]
        T = [days_in_future_end - (days_in_future_end - days_in_future_start) * i / breaks for i in range(breaks)]
        Z = [[-self.portfolio_price for _ in range(breaks)] for _ in range(breaks)]
        for opt_idx in range(len(self.options)):  
            for stock_idx in range(breaks):
                for time_idx in range(breaks):
                    Z[time_idx][stock_idx] += self.options[opt_idx].pricing_model(S[stock_idx], self.options[opt_idx].strike, self.options[opt_idx].sigma, self.options[opt_idx].dividend, self.options[opt_idx].interest_rate, self.options[opt_idx].dte - T[time_idx], Nofnodes) * self.quantity[opt_idx]
        Z = np.array(Z)
        self.plot(S, T, Z, 'Stock Price', 'Days in Future', 'PnL', 'Portfolio Price vs Stock Price and Days in Future')

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
        return f'Portfolio price: {self.portfolio_price},\n Stock price: {self.stock_p},\n Delta: {self.delta},\n Gamma: {self.gamma},\n Theta: {self.theta},\n Vega: {self.vega}'
