import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
df = pd.read_csv('c:/Users/qiany/OneDrive/桌面/Senior/Fin 427/HW/HW2/signals7.csv', parse_dates = ['DATE'])

print("RET's percentile")
perc = [0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99]
print(df['RET'].describe(percentiles = perc))
print('\n')

print("beme's percentile")
perc = [0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99]
print(df['beme'].describe(percentiles = perc))
print('\n')

plt.scatter(x = df['beme'], y = df['RET'])
plt.xlabel('Book to Market Ratio')
plt.ylabel('Return')
plt.show()

# Create the dataframe and test 
df['RET ex99'] = df['RET'][df['RET'] <= df['RET'].quantile(0.99)]
# Test whether the new dataframe excludes the outliers
print(df['RET ex99'][df['RET ex99'] == df['RET ex99'].max()])
print('\n')
df['beme ex99'] = df['beme'][df['beme'] <= df['beme'].quantile(0.99)]

# Replot the data in the scatter without outliers
plt.scatter(x = df['beme ex99'], y = df['RET ex99'])
plt.xlabel('Book to Market Ratio Excluding Outliers')
plt.ylabel('Return Excluding Outliers')
plt.show()
# Look much better this time!

# Find and print the correlation between the book-to-market ratio and the return over the whole sample
print(df[['beme', 'RET']].corr())

# Run a panel regression of return on book-to-market ratio
import statsmodels.formula.api as sm
df['RET'] = df['RET'] * 100
cluster_date_ols = sm.ols(formula = 'RET ~ beme', data = df).fit(cov_type = 'cluster', 
                                                              cov_kwds = {'groups': df['DATE']},
                                                               use_t = True)
print(cluster_date_ols.summary()) 

print(df['beme'].describe())
print('\n')
# For each 1.0 increase in B/M ratio, return increases by 16.57 bp per month
# A 1.0 sigma increase in B/M increases returns by 1.515 * 16.57 =  25.1 bp

# Add a column to your dataframe for the decile within each month of the book-to-market ratio
df['beme decile']=df.groupby(['DATE'])['beme'].\
    transform(lambda x: pd.qcut(x, 10, labels=False, duplicates='drop'))
# Construct equally-weighted portfolios on the basis of book-to-market ratio 
ewret = df.groupby(['DATE','beme decile'])['RET','beme'].mean().reset_index()
ewret = ewret.sort_values(by=['DATE','beme decile'])
cluster_date_port= sm.ols(formula = 'RET ~ beme', data = ewret).fit(cov_type = 'cluster',
                                                               cov_kwds = {'groups': ewret['DATE']},
                                                               use_t = True)
print(cluster_date_port.summary())
print('\n')
#Display the average returns on each portfolio
meanret = ewret.groupby(['beme decile'])['RET','beme'].mean()
print(meanret)
print('\n')

# Now, let's see if things look any different if returns are value- rather than equally weighted
def wavg(group, avg_name, weight_name):
    d = group[avg_name]
    w = group[weight_name]
    try:
        return (d * w).sum()/ w.sum()
    except ZeroDivisionError:
        return np.nan

vwret = df.groupby(['DATE','beme decile']).apply(wavg, 'RET','mvlag')
vwret = vwret.reset_index().rename(columns = {0: 'ret'})

# Print and plot the value-weighted mean returns
meanvwret = vwret.groupby(['beme decile'])['ret'].mean()
print(meanvwret)
print('\n')