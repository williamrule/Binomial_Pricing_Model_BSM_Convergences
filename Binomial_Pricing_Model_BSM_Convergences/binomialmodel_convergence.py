import math
import matplotlib.pyplot as plt
from scipy.stats import norm

#Parameters
s0 = 100 #initial stock price
k = 100 #Strike Price
r = 0.06 #Risk-free interest rate
sigma = 0.2 #volatility of the stock price
t = 1 #Time to maturity in years
n = 10 #time steps
delta_t = t/n
u = math.exp(sigma * math.sqrt(delta_t))
d = 1/u
opttype = 'C' #Option Type 'C' or 'P'

def terminal_stock_price(u,d,n,s0):
    price_list = []
    for j in range(n+1):
        price = s0 * u**j * d**(n-j)
        price_list.append(price)
    return price_list

def terminal_option_price(k,u,d,n,s0, opttype):
    price = terminal_stock_price(u,d,n,s0)
    option_price_list = []
    if opttype == 'C' or opttype == 'c':
        for index in price:
            option_price = max(index-k,0)
            option_price_list.append(option_price)
    elif opttype == 'P' or opttype == 'p':
        for index in price:
            option_price = max(0,k-index)
            option_price_list.append(option_price)
    else:
        raise ValueError("No option type was provided")

    return option_price_list

def risk_neutral_probability(r, u, d, delta_t):
    if not (d < math.exp(r*delta_t) < u):
        raise ValueError("No-arbitrage condition violated: need d < 1 + r < u")
    return ((math.exp(r*delta_t)) - d) / (u - d)

#function that does the backward step once
def backward_step(values,p,r, delta_t):
    new_price_list = []
    for j in range(len(values) - 1):
        v_down = values[j]
        v_up = values[j+1]
        price = (math.exp(-r*delta_t)) * (p * v_up + (1-p) * v_down)
        new_price_list.append(price)
    return new_price_list


#Computes the backward steps multiple times until we get the price
def binomial_option_price(p, r, option_payoff, delta_t):
    values = option_payoff
    while len(values) > 1:
        values = backward_step(values, p, r, delta_t)
    return values[0]


#convergence test
n_list = [1, 2, 5, 10, 25, 50, 100, 250]

def binomial_option_price_list(t,r, n_list, s0, opttype):
    results = []
    for n in n_list:
        delta_t = t / n
        u = math.exp(sigma * math.sqrt(delta_t))
        d = 1/u
        term_option_price = terminal_option_price(k,u,d,n,s0,opttype)
        p = risk_neutral_probability(r, u, d, delta_t)
        price = binomial_option_price(p,r,term_option_price, delta_t)
        results.append(price)
    return results

def bsm_call_value(s0, k, r, t, sigma):
    if t <= 0 or sigma <= 0 or s0 <= 0 or k <= 0:
        # degenerate / immediate payoff case
        return max(s0 - k * math.exp(-r * t), 0.0)

    a = sigma * math.sqrt(t)  # sigma * sqrt(T)
    d1 = (math.log(s0 / k) + (r + 0.5 * sigma**2) * t) / a
    d2 = d1 - a

    return s0 * norm.cdf(d1) - k * math.exp(-r * t) * norm.cdf(d2)

#p = risk_neutral_probability(r,u,d, delta_t)
#values = terminal_option_price(k,u,d,n,s0, opttype)
#print(values)
#print(binomial_option_price(p,r,values, delta_t))
prices_list = binomial_option_price_list(t,r, n_list, s0, opttype)
bsm_value = bsm_call_value(s0,k, r,t, sigma)
print("List of binomial prices for increasing n: " + str(prices_list))
print("BSM value: " + str(bsm_value))

#Plots the convergence
plt.figure(1)
plt.plot(n_list,prices_list, marker ='o', label = "CRR Binomial Prices")
plt.xscale('log')
plt.title("Convergence of Binomial Prices to the Black–Scholes Value")
plt.xlabel("Time Steps N")
plt.ylabel("Option Value")
plt.axhline(y=bsm_value, color = 'r', label = "Black–Scholes Benchmark")
plt.legend()

#Plots the Absolute Error
abs_diff = [abs(x - bsm_value) for x in prices_list]
plt.figure(2)
plt.plot(n_list, abs_diff)
plt.xscale('log')
plt.title("Absolute Error Between Binomial and Black–Scholes Prices")
plt.ylabel("Absolute Error")
plt.xlabel("Time Steps N")
plt.show()