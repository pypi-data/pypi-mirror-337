# stock-watcher
Deliver live data for your portfolio in your terminal

## Build
Install using pip:
```
pip install stock_watcher
```

## Usage
The interface is overall very simple:
```
usage: stock-watcher [-h] [-f FROM] config_csv

Deliver live data for your portfolio in your terminal

positional arguments:
  config_csv       config csv with your portfolio

options:
  -h, --help       show this help message and exit
  -f, --from FROM  currency to display USD exchange rate for (default: CAD)
```

Here's an example configuration csv:

| Ticker | Buy Price | Num Stocks |
| ------ | --------- | ---------- |
| SCHH | 19.98 | 59 |
| VTC | 75.77 | 18 |
| SPTM | 64.02 | 50 |
| SPDW | 35.68 | 75 |
| VWO | 41.94 | 55 |
| MMKT | 100.03 | 7 |
| 6758.T | 2618.00 | 51 |

In text it might look like this:
```
Ticker,Buy Price,Num Stocks
SCHH,19.98,59
VTC,75.77,18
SPTM,64.02,50
SPDW,35.68,75
VWO,41.94,55
MMKT,100.03,7
6758.T,2618.00,51
```
The seperator will be automatically detected by pandas, so you can use pretty much whatever you want. The ticker in the first column must be availible on yahoo finance. Any securities that use a currency other than USD should have their buy price entered in the local currency.

## Features
[Put a screenshot here]
The program gives 4 data points for each ticker, The % and absolute daily and total change. The daily changes are calculated from the last price point before today. It also shows whether US markets are currently open or closed. Fianlly, a currency exchange rate is displayed at the bottom. Absolute data for foreign securities is always converted to USD when displayed (though calculations are done in local currency). However percent changes are done in local currencies.

`q` is used to exit the program.
