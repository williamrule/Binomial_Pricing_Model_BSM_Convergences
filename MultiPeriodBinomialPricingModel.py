import numpy as np
s0 = 100 #initial stock price
k = 100 #Strike Price
u = 1.1 #up stock factor
d = 1/u #down stock factor
r = 0.06 #Risk-free interest rate
t = 1 #Time to maturity in years
n = 3 #Delta t
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

def risk_neutral_probability(r, u, d):
    if not (d < 1 + r < u):
        raise ValueError("No-arbitrage condition violated: need d < 1 + r < u")
    return (1 + r - d) / (u - d)

#function that does the backward step once
def backward_step(values,p,r):
    new_price_list = []
    for j in range(len(values) - 1):
        v_down = values[j]
        v_up = values[j+1]
        price = (1/(1+r)) * (p * v_up + (1-p) * v_down)
        new_price_list.append(price)
    return new_price_list


#Computes the backward steps multiple times until we get the price
def binomial_option_price(p, r, option_payoff):
    values = option_payoff
    while len(values) > 1:
        values = backward_step(values, p, r)
    return values[0]


p = risk_neutral_probability(r,u,d)
values = terminal_option_price(k,u,d,n,s0,'P')
print(values)
print(binomial_option_price(p,r,values))
