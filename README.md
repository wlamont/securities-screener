# Security (stock) Screener

Want to invest like Warren Buffett?  Yeah, me too.  Well we can't.  But we can use some of the methodology Warren's teacher and mentor Benjamin Graham imparted on Warren and is available in the book "The Intelligent Investor".  Here are two files that helps screen some of the basic stocks.  

``For the defensive investor we suggested an upper limit of purchase price at 25 times average earnings [per share] of the past seven years.'' p. 159 from "The Intelligent Investor"

stock_analysis_01.py 

Uses beautifulsoup to scrape html financial data for each company in the S&P500.  Reads in the last 5 years worth of EPS plus the current price. Outputs the stock symbol, current price, 5 yr EPS average, max price I would pay based on 25 x (5 yr AVG of EPS) and outputs a ratio of the price / max (smaller numbers are better)


``In general, a price/earnings ratio (or "P/E" ratio) below 10 is considered low, between 10 and 20 is considered moderate, and greater than 20 is considered expensive." p. 70 

``The investor should impose some limit on the price he will pay for an issue in relation to its average earnings over, say, the past seven years.  We suggest that this limit be set at 25 times such average earnings, and not more than 20 times those of the last twelve-month period.'' p. 115 

and 

"The conservative investor should concentrate on issues selling at no more than 1.3 of book value (P/BV < 1.3)." p. 199

This conservatie investor therefore wants to concentrate on stocks with the following financial characteristics P/E * P/BV < 22.5 (price to earnings muliplied by price to book)

stock_analysis_BV_02.py

Uses beautifulsoup to scrape html financial data for each company in the S&P500.  Reads in the current P/E and P/BV.  Generally want P/E * P/BV < 22.5 (which indicates a good investment).

Should probably store this data in a database (perhaps mongoDB) and use Pandas for accessing.  

