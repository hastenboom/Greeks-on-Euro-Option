import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as ss
from scipy.stats import norm as n
from plotnine import *

s, K, sigma, r, inte, option = np.linspace(0.00001, 100, 100), 50, 0.28, 0.05, 9 / 12, "p"


class Greeks:
    def __init__(self, s, K, sigma, r, inte, option):
        # S price of underlying price
        # K the strike price # sigma the volatility, implied volatility
        # r risk free rate # inte time interval
        self.s, self.K, self.sigma, self.r = s, K, sigma, r
        self.inte, self.option = inte, option
        self.d1 = (np.log(self.s / self.K) + (self.r + self.sigma ** 2 / 2) * self.inte) / (
                self.sigma * np.sqrt(self.inte))
        self.d2 = self.d1 - self.sigma * np.sqrt(self.inte)

    def payoff(self):
        payoff = np.zeros(s.__len__())
        if (self.option == 'c'):
            for i in range(0, (s.__len__())):
                payoff[i] = max(self.s[i] - self.K, 0)

        if (self.option == 'p'):
            for i in range(0, (s.__len__())):
                payoff[i] = max(self.K - self.s[i], 0)

        return payoff

    def value(self):
        value = np.zeros(self.s.__len__())
        if (self.option == 'c'):
            for i in range(0, (s.__len__())):
                value[i] = self.s[i] * n.cdf(self.d1[i]) - self.K * np.exp(1) ** (-self.r * self.inte) * n.cdf(
                    self.d2[i])

        if (self.option == 'p'):
            for i in range(0, (self.s.__len__())):
                value[i] = self.K * np.exp(1) ** (-self.r * self.inte) * n.cdf(-1 * self.d2[i]) - self.s[i] * n.cdf(
                    -1 * self.d1[i])

        return value

    def delta(self):
        delta = np.zeros(self.s.__len__())
        if (self.option == 'c'):
            for i in range(0, (self.s.__len__())):
                delta[i] = n.cdf(self.d1[i])

        if (self.option == 'p'):
            for i in range(0, (s.__len__())):
                delta[i] = n.cdf(self.d1[i]) - 1
        return delta

    def gamma(self):
        gamma = np.zeros(self.s.__len__())
        for i in range(0, (self.s.__len__())):
            gamma[i] = (np.exp(1) ** (-0.5 * self.d1[i] ** 2)) / (
                    self.s[i] * self.sigma * np.sqrt(2 * np.pi * self.inte))

        return gamma

    def vega(self):
        vega = np.zeros(self.s.__len__())
        for i in range(0, (self.s.__len__())):
            vega[i] = self.s[i] * np.sqrt(inte) * (np.exp(1) ** (-self.d1[i] ** 2 / 2)) / np.sqrt(2 * np.pi)

        return vega


call = Greeks(s, K, sigma, r, inte, 'c')
put = Greeks(s, K, sigma, r, inte, 'p')

# value and payoff
value = pd.DataFrame({'price': call.s,
                      'value_c': call.value(),
                      'value_p': put.value(),
                      'payoff_c': call.payoff(),
                      'payoff_p': put.payoff()})
value_melt = value.melt(id_vars='price')

value_melt['a'] = np.nan
value_melt.a[value_melt.variable.str.contains('_p')] = 'put'
value_melt.a[~value_melt.variable.str.contains('_p')] = 'call'

(ggplot(data=value_melt, mapping=aes('price', 'value', color='variable')) +
 geom_line(size=1.5) +
 facet_wrap('~a', nrow=2, ncol=1) +
 scale_color_manual(['Steelblue', 'Steelblue', 'black', 'black']))

# the Greeks
greeks = pd.DataFrame({'price': call.s, 'delta_c': call.delta(),
                       'delta_p': put.delta(), 'gamma_c': call.gamma(),
                       'gamma_p': put.gamma(), 'vega_c': call.vega(),
                       'vega_p': put.vega()})

greeks_melt = greeks.melt(id_vars='price')

greeks_melt['type'] = np.nan
greeks_melt.type[greeks_melt.variable.str.contains('_p')] = 'put'
greeks_melt.type[greeks_melt.variable.str.contains('_c')] = 'call'
greeks_melt.variable=greeks_melt.variable.str.replace('_c',' ')
greeks_melt.variable=greeks_melt.variable.str.replace('_p',' ')

(ggplot(greeks_melt,aes('price','value',color='type'))+
 geom_line(size=1.5)+
 facet_wrap('~variable',nrow=3,ncol=2,shrink = 'FALSE'))

