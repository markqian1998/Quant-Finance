# In this file, I am going to examine whether signals are related to alpha within a specific industry. I have previously downloaded a dataset with signals and returns related to this industry. You can find the dataset here: https://drive.google.com/file/d/1o1KhXdSjx2YYjQsPELPBj_wOMROKYCLM/view?usp=sharing 
<br/><br/>
## Task to complete
* Use .describe() to display the 1st, 5th, 25th, 50th, 75th, 95th, and 99th percentile of 'RET' and 'beme'.  We can find there are some apparent outliers.
* 'RET' stands for return, and 'beme' stands for Book-to-Market Ratio
* Further examine the data by producing a scatterplot with the book-to-market ratio on the x-axis and the return on the y-axis
* Create a dataframe that eliminates outliers by excluding observations of 'RET' and 'beme' above the 99th percentile
* Re-plot the data in a scatterplot.  The data look much better behaved.
* Find the correlation between the book-to-market ratio and the return over the whole sample
* Run a panel regression of return on book-to-market ratio. There is a statistically significant relation between returns and the book-to-market ratio
* The regression tells us about the response of returns to a one standard deviation increase in book-to-market ratio
* Add a column to the dataframe for the decile within each month of the book-to-market ratio
* Construct equally-weighted portfolios on the basis of book-to-market ratio.  Display the average returns on each portfolio.
* Things will look different if returns are value- rather than equally weighted. This requires a bit more coding. Assuming that the data is in a dataframe called "df", we can use this code to produce value-weighted portfolios:

* def wavg(group, avg_name, weight_name):\
    d = group[avg_name]\
    w = group[weight_name]\
    try:\
        return (d * w).sum()/ w.sum()\
    except ZeroDivisionError:\
        return np.nan\

  vwret = df.groupby(['DATE','BMDecile']).apply(wavg, 'RET','mvlag')\
  vwret = vwret.reset_index().rename(columns={0:'ret'})\

* Print and plot the value-weighted mean returns.  We can think about the relation between the book-to-market ratio and returns
