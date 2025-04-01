
class Stock:
    def __init__(self, stock_p):
        self.stock_p = stock_p
        self.price = stock_p
        # define these to make the object compatible with the option object
        # it is not that nice... but it works
        self.strike = 0
        self.sigma = 0
        self.dividend = 0
        self.interest_rate = 0
        self.dte = 0
        self.delta = 1
        self.gamma = 0
        self.theta = 0
        self.vega = 0
    def recalculate(self):
        return self
    def pricing_model(self, stock_p, strike, sigma, dividend, interest_rate, dte, Nofnodes):
        return stock_p
    def __str__(self):
        return f"Stock with stock price: {self.stock_p}"
