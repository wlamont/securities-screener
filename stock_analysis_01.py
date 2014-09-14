'''
Uses beautifulsoup to scrape html financial data for each company in the S&P500.  Reads in the last 5 years worth of EPS plus the current price. Outputs the stock symbol, current price, 5 yr EPS average, max price I would pay based on 25 x (5 yr AVG of EPS) and outputs a ratio of the price / max (smaller numbers are better)
'''


import time
START = time.time()
from urllib import urlopen
from BeautifulSoup import BeautifulSoup


def quote(ticker_symbol):
#    print ticker_symbol
#    print type(ticker_symbol)
    url = 'http://www.marketwatch.com/investing/stock/'
    full_url = url + ticker_symbol + '/financials'
#    print full_url
    text_soup = BeautifulSoup(urlopen(full_url).read()) #read in
    #print text_soup
    price = text_soup.find('p', {'class': 'data bgLast'})
    #print 'Current/Last Price:', price.string
    titles = text_soup.findAll('td', {'class': 'rowTitle'})
    eps = []
    for title in titles:
        #print title.text
        if 'EPS (Basic)' in title.text:
            for td in title.findNextSiblings(attrs={'class': 'valueCell'}):
                #trap if there is a - as an entry
                if td.text == '-':
                    eps.append('0')
                else:
                    eps.append(td.text)
    tot = 0
    for vals in range(0, len(eps), 1):
        #need to trap if the eps is negative.  Will have ( ).  
        #Need to convert to negative value
        single_eps = eps[vals]
        if single_eps[0] == '(':
            clean = single_eps[1:-1]
            eps[vals] = float(clean)*(-1) #makes it negative
        tot = float(eps[vals]) + tot
        mean = tot/len(eps)
        if mean < 0:
            maximum = 0.0
        else:
            maximum = 25.0*mean
    return float(price.string), mean, maximum

if __name__ == '__main__':
#    symbol = ['mmm','goog']
#    print type(symbol)
    
    symbol = []
    ifile = open('sp500.csv', 'r')
    OFILE = open('data', 'w')

    for line in ifile:      
        sym = line
        sym.strip('\r\n')
#        print sym
#        print long
        symbol.append(str(sym[0:(len(sym)-1)]))  
    
#    print symbol     
    i = 0
    OFILE.write('Symbol, Price, EPS (5 yr avg), Max Price, Ratio \n')
    for items in symbol:
        print items
        performance = quote(items)
        performance2 = []
        j = 0
        while j < 3:
            performance2.append(float(performance[j]))
            j += 1
        if performance[2] == 0.0:
            performance2.append(1000)
        else:
            performance2.append(performance[0]/performance[2]) #Price / max 
        OFILE.write(items + ',  %5.1f, %5.1f, %5.1f, %5.2f' % (performance2[0], 
                                                               performance2[1], 
                                                                performance2[2], 
                                                                performance2[3])
                                                                + '\n')
        #print 'Price: %5.1f, EPS (5 yr avg): %5.1f, Max price: %5.1f, Ratio: %5.2f'
        #% (performance2[0], performance2[1], performance2[2], performance2[3])


    ifile.close()
    OFILE.close()
    print 'It took', time.time()-START,'seconds.'
