import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def EMA(data, currentDay, dayCount):
    oneMinusAlpha = 1.-(2./(dayCount-1))
    numerator = 0.
    denominator = 0.
    for i in range (dayCount+1):
        tmp = oneMinusAlpha**i
        if (currentDay - i) > 0:
            numerator += tmp * data.iloc[currentDay-1-i, 1]
            denominator += tmp
    return (numerator / denominator)

def MACD(data, n):
    return (EMA(data, n, 12) - EMA(data, n,26)) 

def SIGNAL(data, n):
    return EMA(data, n, 9)

def Buy(value, capital, howMuchToInvest):
    actions = howMuchToInvest/value
    capital -= value*actions
    return (capital, actions)

def SellAll(value,capital, actions):
    capital += value*actions
    actions = 0
    return (capital, actions)


capital = 10000                # kapitał początkowy
c = capital
p = 0.4                        # część kapitału początkowego jaki przeznaczam na kupno nowych akcji
numberOfActions = 0
n = 1000                        # liczba próbek
script_dir = os.path.dirname(os.path.abspath(__file__)) + "\\"
data = pd.read_csv(script_dir + "mbank.csv", usecols=["Data","Zamknięcie"],encoding='utf-8')
data = data.head(n)
data = data.iloc[::-1]
data.reset_index(inplace = True)
data.drop('index',axis =1, inplace=True)
macd = pd.DataFrame(np.zeros(n*2).reshape(n,2))
signal = pd.DataFrame(np.zeros(n*2).reshape(n,2))

print("Kapitał początkowy: " + str(capital) + " PLN")

for i in range (0,n):
    macd.iloc[i,1] = MACD(data, i+1)
    signal.iloc[i,1] = SIGNAL(macd, i+1)
    if (i > 26):
        if (macd.iloc[i-1,1] <= signal.iloc[i-1,1] and macd.iloc[i,1] >= signal.iloc[i,1]):
          (capital,numberOfActions) = Buy(data.loc[i,"Zamknięcie"],capital, capital*p)
        elif (macd.iloc[i-1,1] >= signal.iloc[i-1,1] and macd.iloc[i,1] <= signal.iloc[i,1]):
          (capital,numberOfActions) = SellAll(data.loc[i,"Zamknięcie"], capital, numberOfActions)

(capital,numberOfActions) = SellAll(data.loc[999,"Zamknięcie"], capital, numberOfActions)

print("Kapitał końcowy: {0:.2f} PLN".format(round(capital) ,2))
print("Zysk: {0:.2f} PLN".format(round(capital - c) ,2))
macd[0] = data['Data']
signal[0] = data['Data']

plt.rc('figure', figsize = [18,8], autolayout = True)
plt.figure(num='Wojciech Niewiadomski 172166')
#print(plt.rcParams.keys())
plt.subplot(2, 1, 1)
wykres = plt.plot(data.iloc[:,0],data.iloc[:,1])
plt.title('Wykres zmian cen akcji na przestrzeni 1000 dni spółki mBank SA')
plt.ylabel("Wartość akcji [PLN]")
plt.xlabel("Data")
plt.grid(color='gray', linestyle='-', linewidth=0.07)
myTicks = np.arange(0,n,n/50)
myTicks = np.append(myTicks,n-1)
plt.xticks(myTicks, rotation = 45, fontsize = "x-small")
plt.subplot(2, 1, 2)
wykres2 = plt.plot(signal.iloc[:,0], signal.iloc[:,1], 'r-',macd.iloc[:,0], macd.iloc[:,1], 'b-')
plt.legend(('SIGNAL','MACD'),loc = 'upper right')
plt.xticks(myTicks, rotation = 45, fontsize = "x-small")
plt.grid(color='gray', linestyle='-', linewidth=0.07)
plt.show()
