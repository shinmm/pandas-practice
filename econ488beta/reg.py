#script to extract stock data, specifically PNC Bank and the s&p 500 
#and run a linear regression 
# Practice from https://medium.com/python-data/capm-analysis-calculating-stock-beta-as-a-regression-in-python-c82d189db536

# import libraries
import pandas as pd
import statsmodels.api as sm
import glob, os
import matplotlib.pyplot as plt


'''
Download S&P 500 weekly for the past 3 years, and monthly for the
past 5 years. Calculate the weekly and monthly returns 
script to extract stock data, specifically PNC Bank and the s&p 500 
#and run a linear regression 
'''
#List available CSV files
csvfiles = []
i = 1
os.chdir("/Users/shinmitsuno/Desktop/econ488beta")
for file in sorted(glob.glob("*.csv")):
    print("{}) {}".format(i,file))
    csvfiles.append(file)
    i+=1

print(csvfiles)
#save selection
stock_to_read = csvfiles[int(input("What stock(Number above) : ")) - 1]
sp_500type = csvfiles[int(input("What S&P 500(Number above) : ")) -1]

stock1 = pd.read_csv(stock_to_read, parse_dates=True, index_col='Date',)
print(stock1)

sp_500 = pd.read_csv(sp_500type, parse_dates=True, index_col='Date')

# joining the closing prices of the two datasets 
monthly_prices = pd.concat([stock1['Close'], sp_500['Close']], axis=1)
monthly_prices.columns = [stock_to_read.replace(".csv", ''), sp_500type.replace(".csv", '')]

# check the head of the dataframe
#monthly_prices holds monthly returns on Facebook and S&P 500
#dfToList = monthly_prices['one'].tolist()
print (stock1['Close'])
print(monthly_prices)
print(type(stock1))

# calculate monthly returns, percent change 
monthly_returns = monthly_prices.pct_change(1)
#drop the missing rows
clean_monthly_returns = monthly_returns.dropna(axis=0)
print("Printing monthly returns")

print(monthly_returns)
# split dependent and independent variable
X = clean_monthly_returns[sp_500type.replace(".csv", '')]
y = clean_monthly_returns[stock_to_read.replace(".csv", '')]
print("Printing monthly")
print(X,y)

# Add a constant to the independent value
X1 = sm.add_constant(X)

# make regression model 
model = sm.OLS(y, X1)

# fit model and print results
results = model.fit()
print(results.summary())

# alternatively scipy linear regression
from scipy import stats
slope, intercept, r_value, p_value, std_err = stats.linregress(X, y)
print(slope)

# save OLS Regression Results as a PNG
plt.rc('figure', figsize=(12, 7))
plt.text(0.01, 0.05, str(results.summary()), {'fontsize': 10}, fontproperties = 'monospace')
plt.axis('off')
plt.tight_layout()
plt.savefig('output.png')