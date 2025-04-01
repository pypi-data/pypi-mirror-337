import math
from scipy.stats import norm


def EurCall(S, X, sigma, Q, r, Tdays, Nofnodes):
    """
    Calculate the European Call option price using the Binomial Tree method.
    
    Parameters:
        S (float): Initial stock price.
        X (float): Strike price.
        sigma (float): Volatility of the stock.
        Q (float): Dividend yield.
        r (float): Risk-free interest rate.
        Tdays (int): Time to maturity in days.
        Nofnodes (int): Number of nodes in the binomial tree.

    Returns:
        float: Price of the European Call option.
    """
    if Tdays <= 0:
        return max(S - X, 0)
    T = Tdays / 365.0      # Time in years
    dt = T / (Nofnodes - 1) # Length of each time step
    
    # Risk-neutral parameters
    a = math.exp((r - Q) * dt)
    b2 = a**2 * (math.exp(sigma**2 * dt) - 1)
    u = (a**2 + b2 + 1 + math.sqrt((a**2 + b2 + 1)**2 - 4 * a**2)) / (2 * a)
    d = 1 / u
    p = (a - d) / (u - d)
    q = 1 - p
    
    # Check if probabilities are valid
    if p <= 0 or q <= 0:
        print("Negative probabilities, increase volatility.")
        return "error"
    
    # Initialize option values at terminal nodes
    Q0 = [0] * Nofnodes
    Q1 = [0] * Nofnodes
    
    i = Nofnodes - 1
    Q0[0] = S * (d ** i)
    Q1[0] = max(Q0[0] - X, 0)
    
    for j in range(1, i + 1):
        Q0[j] = Q0[j - 1] * (u / d)
        Q1[j] = max(Q0[j] - X, 0)
    
    # Discount factor for each time step
    daydiscount = math.exp(-r * dt)
    
    # Backward calculation through the tree
    for k in range(Nofnodes - 1, 0, -1):
        for l in range(k):
            Q0[l] *= u
            Q1[l] = (q * Q1[l] + p * Q1[l + 1]) * daydiscount
    
    return Q1[0]


def EurPut(S, X, sigma, Q, r, Tdays, Nofnodes):
    """
    Calculate the European Put option price using the Binomial Tree method.
    
    Parameters:
        S (float): Initial stock price.
        X (float): Strike price.
        sigma (float): Volatility of the stock.
        Q (float): Dividend yield.
        r (float): Risk-free interest rate.
        Tdays (int): Time to maturity in days.
        Nofnodes (int): Number of nodes in the binomial tree.

    Returns:
        float: Price of the European Put option.
    """
    if Tdays <= 0:
        return max(X - S, 0)
    T = Tdays / 365.0      # Time in years
    dt = T / (Nofnodes - 1) # Length of each time step
    
    # Risk-neutral parameters
    a = math.exp((r - Q) * dt)
    b2 = a**2 * (math.exp(sigma**2 * dt) - 1)
    u = (a**2 + b2 + 1 + math.sqrt((a**2 + b2 + 1)**2 - 4 * a**2)) / (2 * a)
    d = 1 / u
    p = (a - d) / (u - d)
    q = 1 - p
    
    # Check if probabilities are valid
    if p <= 0 or q <= 0:
        print("Negative probabilities, increase volatility.")
        return "error"
    
    # Initialize option values at terminal nodes
    Q0 = [0] * Nofnodes
    Q1 = [0] * Nofnodes
    
    i = Nofnodes - 1
    Q0[0] = S * (d ** i)
    Q1[0] = max(X - Q0[0], 0)
    
    for j in range(1, i + 1):
        Q0[j] = Q0[j - 1] * (u / d)
        Q1[j] = max(X - Q0[j], 0)
    
    # Discount factor for each time step
    daydiscount = math.exp(-r * dt)
    
    # Backward calculation through the tree
    for k in range(Nofnodes - 1, 0, -1):
        for l in range(k):
            Q0[l] *= u
            Q1[l] = (q * Q1[l] + p * Q1[l + 1]) * daydiscount

    return Q1[0]


def AmPut(S, X, sigma, Q, r, Tdays, Nofnodes):
    if Tdays <= 0:
        return max(X - S, 0)
    #Declaring variables
    #p0 are stock prices, p1 are option prices
    p0 = [0]*Nofnodes
    p1 = [0]*Nofnodes
    T = Tdays / 365
    dt = T / (Nofnodes - 1)
    a = math.exp((r-Q)*dt)
    b2 = a*a*(math.exp(sigma**2*dt)-1)
    u = ((a*a+b2+1)+math.sqrt((a*a+b2+1)*(a*a+b2+1)-4*a*a))/(2*a)
    d = 1 / u
    p = (a-d)/(u-d)
    q = 1 - p

    #calculating the prices and values of the option
    #At time i*dt, the stock price is S*u^j*d^(i - j)
    if ((q > 0) and (p > 0)):
        i = Nofnodes 
        p0[0] = S*(d**(i-1))
        if p0[0] <= X:
            p1[0] = X-p0[0]
        else:
            p1[0] = 0
        for j in range(1, i):
            p0[j] = p0[j-1]*(u/d)
            if p0[j] <= X:
                p1[j] = X - p0[j]
            else:
                p1[j] = 0;
        daydiscount = math.exp(-r*dt)

        for k in range(Nofnodes, 0, -1):
            for l in range(k-1):
                p0[l] = p0[l]*u
                p1[l] = (q*(p1[l])+p*(p1[l+1]))*daydiscount
                if p1[l] < (X-p0[l]):
                    p1[l] = X - p0[l]

        return p1[0] 

def AmCall(S, X, sigma, Q, r, Tdays, Nofnodes):
    #debug:
    #print("S: ", S, "X: ", X, "sigma: ", sigma, "Q: ", Q, "r: ", r, "Tdays: ", Tdays, "Nofnodes: ", Nofnodes)
    if Tdays <= 0:
        return max(S - X, 0)
    #Declaring variables
    #p0 are stock prices, p1 are option prices
    p0 = [0]*Nofnodes
    p1 = [0]*Nofnodes
    T = Tdays / 365
    dt = T / (Nofnodes - 1)
    a = math.exp((r-Q)*dt)
    b2 = a*a*(math.exp(sigma**2*dt)-1)
    u = ((a*a+b2+1)+math.sqrt((a*a+b2+1)*(a*a+b2+1)-4*a*a))/(2*a)
    d = 1 / u
    p = (a-d)/(u-d)
    q = 1 - p

    #calculating the prices and values of the option
    #At time i*dt, the stock price is S*u^j*d^(i - j)
    if ((q > 0) and (p > 0)):
        i = Nofnodes 
        p0[0] = S*(d**(i-1))
        if p0[0] >= X:
            p1[0] = p0[0] - X
        else:
            p1[0] = 0
        for j in range(1, i):
            p0[j] = p0[j-1]*(u/d)
            if p0[j] >= X:
                p1[j] = p0[j] - X
            else:
                p1[j] = 0;
        daydiscount = math.exp(-r*dt)

        for k in range(Nofnodes, 0, -1):
            for l in range(k-1):
                p0[l] = p0[l]*u
                p1[l] = (q*(p1[l])+p*(p1[l+1]))*daydiscount
                if p1[l] < (p0[l]-X):
                    p1[l] = p0[l] - X

        return p1[0] 

