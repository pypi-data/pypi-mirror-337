def help():
    print("How to use the delta_library:")
    print('Call(stock_p, strike, dividend, interest_rate, dte, date, price, sigma, american_european="european", timezone="Europe/Amsterdam", date_format="%Y-%m-%d")')
    print('Put(stock_p, strike, dividend, interest_rate, dte, date, price, sigma, american_european="european", timezone="Europe/Amsterdam", date_format="%Y-%m-%d")')
    print("Options have the following attributes:")
    print("delta, gamma, theta, vega, leverage, probability_itm")
    print("\nstock_p, strike, dividend, interest_rate, are all required.")
    print("either price or sigma must be specified and either dte or date must be specified.")
    print("")
    print("Options have the following plotting methods:")
    print("plot_stockprice_price(stock_start, stock_end, Nofnodes, breaks)\n plot_stockprice_delta(stock_start, stock_end, Nofnodes, breaks)\n plot_stockprice_gamma(stock_start, stock_end, Nofnodes, breaks)\n plot_stockprice_theta(stock_start, stock_end, Nofnodes, breaks)\n plot_stockprice_vega(stock_start, stock_end, Nofnodes, breaks)\n plot_price_sigma(sigma_start, sigma_end, Nofnodes, breaks)\n plot_stockprice_time_value(stock_start, stock_end, days_in_future_start, days_in_future_end, Nofnodes, breaks)\n plot_stockprice_time_pnl(stock_start, stock_end, days_in_future_start, days_in_future_end, Nofnodes, breaks)")
    print('stock_p is the current stock price, strike is the strike price, dividend is the dividend yield, interest_rate is the interest rate, dte is the days to expiration, date is the expiration date, price is the option price, sigma is the implied volatility.')
    print("\nStock:")
    print('Stock(stock_p)')
    print("\nPortfolio:")
    print('Portfolio(stock_p, options, quantity)')
    print("stock_p is the current stock price, options is a list of options, quantity is a list of the quantity of each option.")



