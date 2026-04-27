import numpy as np
#Paramters
s0 = 100 #initial stock price
u = 1.5 #up stock factor
d = 0.5 #down stock factor
k = 100 #Strike Price
r = 0.10 #Risk-free interest rate


def terminal_stock_price(s0,u,d):
    return  u * s0, d * s0

def call_option_payoff(k,su,sd):
    cu = max(0,su-k)
    cd = max(0,sd-k)
    return cu,cd

def risk_neutral_probability(r, u, d):
    if not (d < 1 + r < u):
        raise ValueError("No-arbitrage condition violated: need d < 1 + r < u")
    return (1 + r - d) / (u - d)

def option_price_today(r,p,cu,cd):
    return (1/(1+r)) * ((p * cu) + ((1-p)*cd))

su, sd = terminal_stock_price(s0, u, d)
cu, cd = call_option_payoff(k, su, sd)
p = risk_neutral_probability(r, u, d)
c0 = option_price_today(r, p, cu, cd)

print("Su =", su)
print("Sd =", sd)
print("Cu =", cu)
print("Cd =", cd)
print("p =", p)
print("C0 =", c0)
