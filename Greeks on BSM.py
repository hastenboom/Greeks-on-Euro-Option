import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as ss
from scipy.stats import norm as n

s, K, sigma, r, inte, option = np.linspace(0.00001, 100, 100), 50, 0.28, 0.05, 9 / 12, "p"


class Greeks:
    def __init__(self, s, K, sigma, r, inte, option):
        # S price of underlying price
        # K the strike price # sigma the volatility, implied volatility
        # r risk free rate # inte time interval
        self.s = s
        self.K = K
        self.sigma = sigma
        self.r = r
        self.inte = inte
        self.option = option
        self.d1 = (np.log(self.s / self.K) + (self.r + self.sigma ** 2 / 2) * self.inte) / (self.sigma * np.sqrt(self.inte))
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
                value[i] = self.s[i]*n.cdf(self.d1[i]) - self.K*np.exp(1)**(-self.r*self.inte)*n.cdf(self.d2[i])

        if (self.option == 'p'):
            for i in range(0, (self.s.__len__())):
                value[i] = self.K*np.exp(1) ** (-self.r * self.inte) * n.cdf(-1*self.d2[i]) - self.s[i] * n.cdf(-1*self.d1[i])

        return value

    def delta(self):
        delta = np.zeros(self.s.__len__())
        if (self.option == 'c'):
            for i in range(0, (self.s.__len__())):
                delta[i] = n.cdf(self.d1[i])

        if(self.option == 'p'):
            for i in range(0, (s.__len__())):
                delta[i] = n.cdf(self.d1[i])-1
        return delta

    def gamma(self):
        gamma = np.zeros(self.s.__len__())
        for i in range(0, (self.s.__len__())):
            gamma[i] = (np.exp(1)**(-0.5*self.d1[i]**2)) / (self.s[i]*self.sigma*np.sqrt(2*np.pi*self.inte))

        return gamma

    def vega(self):
        vega = np.zeros(self.s.__len__())
        for i in range(0, (self.s.__len__())):
            vega[i] = self.s[i] * np.sqrt(inte) * (np.exp(1)**(-self.d1[i]**2/2)) / np.sqrt(2*np.pi)

        return vega



x1 = Greeks(s, K, sigma, r, inte, 'c')

x1.value()
plt.plot(s,x1.value())
plt.plot(s,x1.payoff())
plt.plot(s,x1.delta())
plt.plot(s,x1.vega())
