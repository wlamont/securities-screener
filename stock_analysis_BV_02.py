'''
Uses beautifulsoup to scrape html financial data for each company in the S&P500.  Reads in the current P/E and P/BV.  Generally want P/E * P/BV < 22.5 (which indicates a good investment)

Date: 20-April-2014

Copyright (c): Warren Lamont

'''

import time
START = time.time()
from urllib import urlopen
from BeautifulSoup import BeautifulSoup
import numpy as np

#def quote(ticker_symbol):
##    print ticker_symbol
##    print type(ticker_symbol)
#    url = 'http://www.marketwatch.com/investing/stock/'
#    full_url = url + ticker_symbol + '/profile'
##    print full_url
#    text_soup = BeautifulSoup(urlopen(full_url).read()) #read in
#    #print text_soup
#    price = text_soup.find('p', {'class': 'data bgLast'})
#    #print 'Current/Last Price:', price.string
#    titles = text_soup.findAll('p', {'class': 'data lastcolumn'})
#    print titles
##    eps = []
#    for title in titles:
#        print title
#        if 'EPS (Basic)' in title.text:
#            for td in title.findNextSiblings(attrs={'class': 'valueCell'}):
#                #trap if there is a - as an entry
#                if td.text == '-':
#                    eps.append('0')
#                else:
#                    eps.append(td.text)
#    tot = 0
#    for vals in range(0, len(eps), 1):
#        #need to trap if the eps is negative.  Will have ( ).  
#        #Need to convert to negative value
#        single_eps = eps[vals]
#        if single_eps[0] == '(':
#            clean = single_eps[1:-1]
#            eps[vals] = float(clean)*(-1) #makes it negative
#        tot = float(eps[vals]) + tot
#        mean = tot/len(eps)
#        if mean < 0:
#            maximum = 0.0
#        else:
#            maximum = 25.0*mean
#    return #float(price.string), mean, maximum



def buffett_score(ticker_symbol):
    url = 'http://www.marketwatch.com/investing/stock/'
    full_url = url + ticker_symbol + '/profile'
#    print full_url
    try:
        text_soup = BeautifulSoup(urlopen(full_url).read()) #read in
    except:
        print 'An error has occured reading this stock'
        pass
        
        
#    print text_soup

    price = text_soup.find('p', {'class': 'data bgLast'})
    
#    print price
#    print type(price)
    if price is None:
        print '<<< price is None >>>', 
        return 0, 0, 0, 0
    else:
        price = price.string.replace(',', '') #trap for comma in price
    #    print 'Current/Last Price:', price.string
        titles = text_soup.findAll('p', {'class': 'column'})
    #    print titles
        flag1 = 0   #use these to trap if P/E or PBR do not exist like for CRS
        flag2 = 0 
        for title in titles:
    #        print title
            if 'P/E Current' in title.text:
                for PE in title.findNextSiblings(attrs={'class': 'data lastcolumn'}):
                    pe = PE.text
                    pe = pe.replace(',','')  # if there is a comma, remove it
                    flag1 = 1
                    
            if 'Price to Book Ratio' in title.text:
                for PBR in title.findNextSiblings(attrs={'class': 'data lastcolumn'}):
                    pbr = PBR.text
                    pbr = pbr.replace(',', '') 
                    flag2 = 1
        if 'pbr' not in locals():
            pbr = 0.0
        if 'pe' not in locals():
            pe = 0.0
            
        if flag1 == 0:
            pe = np.nan
        if flag2 == 0:
            pbr = np.nan
    #    print pe
        #trapping for negative PE
        if flag1 == 1:
            if pe[0] == '-':
                pe = 0
            elif pe[1] == ',':
                pe = pe[0] + pe[2:]
        # using price.replace above to trap for comma
    #    if price.string[1] == ',':
    #        price.string =  price.string[0] + price.string[2:]
        return float(price), float(pe), float(pbr), float(pe) * float(pbr)


if __name__ == '__main__':
#    symbol = 'F'
#    print symbol
    
    print __doc__
    
#    symbol = ['crs']
    symbol = []
    
    ifile = open('sp500_3.csv', 'r')#S&P 500 
#    ifile = open('sp400.csv','r') #S&P 400 Mid Cap
#    ifile = open('sp600.csv','r') #S&P 400 Mid Cap
    
#    OFILE = open('test_20150314.txt', 'w')
    OFILE = open('data_buffett_largecap_20150314.txt', 'w')
#    OFILE = open('data_buffett_midcap_20140503.txt', 'w')
#    OFILE = open('data_buffett_smallcap_20140503.txt', 'w')
    
    for line in ifile:      
        sym = line
        sym.strip('\r\n')
        symbol.append(str(sym[0:(len(sym)-1)]))  
    
#    symbol = ['PETM']
    
#    print symbol     
    i = 0
    OFILE.write('Symbol, Price, P/E, P/BR, Buffett Score \n')
    for items in symbol:
        print items, 
        performance = buffett_score(items) 
        OFILE.write(items + ',  %5.1f, %5.1f, %5.1f, %5.2f' % (performance[0], 
                                                               performance[1], 
                                                                performance[2], 
                                                                performance[3])
                                                                + '\n')
        print 'Score = ', performance[3]
#        #print 'Price: %5.1f, EPS (5 yr avg): %5.1f, Max price: %5.1f, Ratio: %5.2f'
#        #% (performance2[0], performance2[1], performance2[2], performance2[3])
#
#
    ifile.close()
    OFILE.close()
#    print 'The P/E current is', pe
#    print 'The Price to Book Ratio is', pbr
#    print 'The Buffett score is ', float(pe) * float(pbr)
#    print 'Want Buffett score below 22.5'    
    print 'It took', time.time()-START,'seconds.'
