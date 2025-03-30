import yfinance as yf
import pandas as pd
from time import sleep
from datetime import datetime, timedelta, timezone
import curses
import threading
import argparse
import os

def setup():
    global stock_data, process_done, stock_data_lock, process_done_lock

    #Parse cmd line arguments
    parser = argparse.ArgumentParser(prog='stock-watcher', description='Deliver live data for your portfolio in your terminal')
    parser.add_argument('config_csv', help='config csv with your portfolio')
    parser.add_argument('-f', '--from', default='CAD', help='currency to display USD exchange rate for (default: %(default)s)')

    args = vars(parser.parse_args())

    #Global variable holding current data for all tickers in the config csv
    try:
        f = open(args['config_csv'], 'r')
        f.close()
    except os.error as e:
        raise e
    try:
        stock_data = pd.read_csv(args['config_csv'], index_col='Ticker')
    except Exception as e:
        raise RuntimeError(args['config_csv'] + " could not be read: " + str(e))
    #Add columns to stock_data
    current_prices = pd.DataFrame({'Current Price': [0.0]*len(stock_data), 'Yesterday Close Price': [0.0]*len(stock_data), 'Total Change %': [0.0]*len(stock_data), 'Change Today %': [0.0]*len(stock_data), 'Total Change $': [0.0]*len(stock_data), 'Change Today $': [0.0]*len(stock_data), 'Currency': 'USD'}, index=stock_data.index)
    stock_data = pd.concat([stock_data, current_prices], axis=1)

    #Check for any NaNs in the df
    if stock_data.isnull().values.any():
        raise RuntimeError(args['config_csv'] + ' has empty values, please ensure all values are filled in')

    #Find any duplicates and set Buy Price as weighted average
    duplicates = stock_data.index.duplicated()
    for i in range(len(duplicates)):
        if duplicates[i]:
            duplicated_ticker = stock_data.index[i]
            weighted_average = 0
            total_shares = stock_data.loc[duplicated_ticker, 'Num Stocks'].sum()
            for row in stock_data.loc[duplicated_ticker].iterrows():
                weighted_average += row[1]['Buy Price']*(row[1]['Num Stocks']/total_shares)
            
            #Set the new data
            stock_data.loc[duplicated_ticker].iloc[0]['Buy Price'] = weighted_average
            stock_data.loc[duplicated_ticker].iloc[0]['Num Stocks'] = total_shares

    #Drop duplicates
    stock_data = stock_data[~stock_data.index.duplicated(keep='first')]

    #Set when the user exits to faciliate thread killing
    process_done = False

    stock_data_lock = threading.Lock()
    process_done_lock = threading.Lock()

#Convert currency to USD
def convert(currency, value):
    got_data = False
    x_ticker = currency + 'USD=X'
    for i in range(60):
        try:
            #Fetch exchange rates
            rates = yf.download(x_ticker, period='5d', interval='1m', progress=False, threads=False)
            if len(rates) > 0:
                got_data = True
                break
        except:
            sleep(1)
    if got_data:
        return value*rates.iloc[-1, 2]
    else:
        return -1

#yfinance gives data with gmt timestamps
def gmt_to_local(gmt_dt):
    return gmt_dt.to_pydatetime().replace(tzinfo=timezone.utc).astimezone(tz=None)

#Get sell price of a stock
def update_data():
    #Get new data 
    for ticker in stock_data.index:
        got_data = False
        for i in range(5):
            #Fetch data from yahoo finance
            try:
                prices = []
                prices = yf.download(ticker, period='5d', interval='1m', prepost=True, progress=False, threads=False)
            except:
                sleep(1)
                continue

            #Make sure we got something
            if len(prices > 0):
                got_data = True
                break
            else:
                sleep(1)
        if got_data:
            #Update Current Price
            stock_data.at[ticker, 'Current Price'] = prices.iloc[-1, 2]

            #Update Yesterday Close Price
            today = datetime.today()
            for dt_str in reversed(prices.index):
                dt = gmt_to_local(dt_str)
                if (dt.date() != today.date()):
                    try:
                        prices.loc[dt_str, ('Close', ticker)]
                        break
                    except:
                        pass
            stock_data.at[ticker, 'Yesterday Close Price'] = prices.loc[dt_str, ('Close', ticker)]

            #Update other data
            stock_data.at[ticker, 'Total Change %'] = (1 - stock_data.loc[ticker, 'Buy Price']/stock_data.loc[ticker, 'Current Price'])*100
            stock_data.at[ticker, 'Change Today %'] = (1 - stock_data.loc[ticker, 'Yesterday Close Price']/stock_data.loc[ticker, 'Current Price'])*100

            stock_data.at[ticker, 'Total Change $'] = convert(stock_data.at[ticker, 'Currency'], stock_data.loc[ticker, 'Num Stocks']*(stock_data.loc[ticker, 'Current Price'] - stock_data.loc[ticker, 'Buy Price']))
            stock_data.at[ticker, 'Change Today $'] = convert(stock_data.at[ticker, 'Currency'], stock_data.loc[ticker, 'Num Stocks']*(stock_data.loc[ticker, 'Current Price'] - stock_data.loc[ticker, 'Yesterday Close Price']))
            
            #Sort data by total change for when we display it
            stock_data.sort_index(inplace=True)
            stock_data.sort_values(by=['Total Change $', 'Change Today $'], ascending=False, inplace=True)

#Update all of our stock data
def get_updates():
    while True:
        stock_data_lock.acquire()
        update_data()
        stock_data_lock.release()
        process_done_lock.acquire()
        if process_done:
            process_done_lock.release()
            break
        process_done_lock.release()

        #If we update too often, yfinance will get API rate limited
        sleep(60)

def get_x_usd():
    got_data = False
    cur_x = args['from'] + 'USD=X'
    for i in range(60):
        try:
            #Fetch exchange rates
            rates = yf.download(cur_x, period='5d', interval='1m', progress=False, threads=False)
            if len(rates) > 0:
                got_data = True
                break
        except:
            sleep(1)
    if got_data:
        today = datetime.today()
        for dt_str in rates.index:
            dt = gmt_to_local(dt_str)
            if dt.date() == today.date():
                break
            last_dt_str = dt_str
        return (rates.iloc[-1, 2], rates.loc[last_dt_str, ('Close', cur_x)])
    else:
        return 0

#Check if market is open
def get_market_status():
    got_data = False
    for i in range(60):
        try:
            market = yf.Market('us', timeout=60)
            if 'yfit_market_status' in market.status:
                got_data = True
                break
        except:
            sleep(1)

    if got_data:
        return 0 if market.status['status'] == 'closed' else 1
    else:
        return -1
def main(stdscr):
    for ticker in stock_data.index:
        #Update currencies
        for i in range(5):
            try:
                info = yf.Ticker(ticker).info
                if 'financialCurrency' in info:
                    currency = info['financialCurrency']
                    stock_data.at[ticker, 'Currency'] = currency
                break
            except:
                sleep(1)
                continue
 
    data_checker = threading.Thread(target=get_updates, daemon=True)
    data_checker.start()

    curses.noecho()
    curses.cbreak()

    #Colours
    curses.start_color()
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    stdscr.clear()
    stdscr.refresh()

    curses.curs_set(0)

    #Main loop
    height = -1
    width = -1
    too_small = False
    last_stock_data = None
    while True:
        #Check terminal size and update dimensions if needed
        new_height, new_width = stdscr.getmaxyx()
        if (new_width != width) or (new_height != height):
            width = new_width
            height = new_height
            win = curses.newwin(height, width, 0, 0)
            win.nodelay(True)
            if (width < 69) or (height < (len(stock_data)+4)):
                too_small = True
            else:
                too_small = False
        
        #If it's too small to hold everything, we fill the screen with red hashtags
        if too_small:
            stdscr.erase()
            for y in range(height):
                for x in range(width):
                    stdscr.insch(y, x, ord('#'), curses.color_pair(1))
        #Check if we have new data and print it
        elif stock_data_lock.acquire(blocking=False):
            stdscr.erase()
            status = get_market_status()
            if status == 0:
                stdscr.addstr(0, (69-13)//2-1, 'MARKET CLOSED', curses.color_pair(1))
            elif status == 1:        
                stdscr.addstr(0, (69-11)//2-1, 'MARKET OPEN', curses.color_pair(2))
            stdscr.addstr(1, 0, '       % Change Today  $ Change Today  % Total Change  $ Total Change', curses.color_pair(3) | curses.A_BOLD)
            y = 2
            totals = [0, 0, 0, 0]
            for ticker in stock_data.index:
                stdscr.addstr(y, 0, ticker)
                x = 7
                for col in ('Change Today %', 'Change Today $', 'Total Change %', 'Total Change $'):
                    val = stock_data.loc[ticker, col]
                    if val > 0:
                        stdscr.addstr(y, x, (('{:.2f}'.format(val) + ('%' if col[-1] == '%' else '$')).rjust(14)), curses.color_pair(2))
                    elif val < 0:
                        stdscr.addstr(y, x, (('{:.2f}'.format(val) + ('%' if col[-1] == '%' else '$')).rjust(14)), curses.color_pair(1))
                    else:
                        stdscr.addstr(y, x, (('{:.2f}'.format(val) + ('%' if col[-1] == '%' else '$')).rjust(14)), curses.color_pair(3))
                    x+=16
                        
                    if col[-1] == '$':
                        totals[(x-7)//16-1]+=val
                    elif col == 'Change Today %':
                        totals[0]+=stock_data.loc[ticker, 'Num Stocks']*stock_data.loc[ticker, 'Buy Price']
                        totals[2]+=stock_data.loc[ticker, 'Num Stocks']*stock_data.loc[ticker, 'Yesterday Close Price']
                y+=1

            totals[0] = totals[1]/totals[0]*100
            totals[2] = totals[3]/totals[2]*100

            stdscr.addstr(y, 0, 'Total', curses.A_BOLD)
            x = 7
            for col in ('Change Today %', 'Change Today $', 'Total Change %', 'Total Change $'):
                val = totals[(x-7)//16]
                if val > 0:
                    stdscr.addstr(len(stock_data)+2, x, (('{:.2f}'.format(val) + ('%' if col[-1] == '%' else '$')).rjust(14)), curses.color_pair(2) | curses.A_BOLD)
                elif val < 0:
                    stdscr.addstr(len(stock_data)+2, x, (('{:.2f}'.format(val) + ('%' if col[-1] == '%' else '$')).rjust(14)), curses.color_pair(1) | curses.A_BOLD)
                else:
                    stdscr.addstr(len(stock_data)+2, x, (('{:.2f}'.format(val) + ('%' if col[-1] == '%' else '$')).rjust(14)), curses.color_pair(3) | curses.A_BOLD)
                x+=16

            #Flash the screen if prices changed
            if not stock_data.equals(last_stock_data):
                curses.flash()
                last_stock_data = stock_data.copy()

            usdx = get_x_usd()
            if usdx != -1:
                if usdx[0] > usdx[1]:
                    stdscr.addstr(len(stock_data)+3, (69-23)//2-1, '↗{0:.3f} {1} = 1.000 USD↗'.format(usdx[0], args['from']), curses.color_pair(2))
                elif usdx[0] < usdx[1]:
                    stdscr.addstr(len(stock_data)+3, (69-23)//2-1, '↘{0:.3f} {1} = 1.000 USD↘'.format(usdx[0], args['from']), curses.color_pair(1))
                else:
                    stdscr.addstr(len(stock_data)+3, (69-23)//2-1, '→{0:.3f} {1} = 1.000 USD→'.format(usdx[0], args['from']), curses.color_pair(3))
            
            stock_data_lock.release()
            
        stdscr.refresh()

        #Check for exit
        c = win.getch()
        if c == ord('q'): 
            break

    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()

    process_done_lock.acquire()
    process_done = True
    process_done_lock.release()

def main(): 
    setup()
    curses.wrapper(main)
