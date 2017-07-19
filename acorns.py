#!/usr/bin/python3
#
#   acorns.py - Finance app to show performance of Acorns allocations.
#
#   A. Gnias
#   Created: 7/16/2017
#
#   Python 3.4.2
#   Linux raspberrypi 4.1.7+
#   Vim 7.4 - tabstop=3

from yahoo_finance import Share
import urllib.request
from bs4 import BeautifulSoup
from pprint import pprint
import json
import time

def daily_statistics(ETF) :
	"""Gets information of the day to day performance of a stock"""
	#print("Daily Statistics")
	print("Current Price: ", ETF.get_price())
	print("Change: ", ETF.get_percent_change())

def aggregate_statistics(ETF) :
	"""Gets aggregate information of a stock"""
	#print("Aggregate Statistics")
	print("Year High: ", ETF.get_year_high())
	print("50 Day Average: ", ETF.get_50day_moving_avg())

def yearly_statistics(ETF) :
	"""Use this to analyze yearly statistics; APY, etc."""
	pass


def initialize_historical_data(f_out, StockTicker_list, days) :
	"""Used to gather historical data for specified stocks that can be plotted"""
	#Since this is for daily open price, just run this once a day on the website
	d = dict()
	for stock in StockTicker_list :
		hist = get_historical_data(stock, days)
		prices = []
		for day in hist :
			#print(day["Date"].replace(" ","_").replace(",",""), end=":")
			#print(day["Open"], end=" ")
			prices.append(day["Open"])
		full_name = Share(stock).get_name().replace(" ","_")
		d[full_name] = prices
	return d


def get_historical_data(name, number_of_days):
	#Source: https://github.com/lukaszbanasiak/yahoo-finance/issues/128
	data = []
	url = "https://finance.yahoo.com/quote/" + name + "/history/"
	rows = BeautifulSoup(urllib.request.urlopen(url).read(),"html5lib").findAll('table')[1].tbody.findAll('tr')

	for each_row in rows:
		divs = each_row.findAll('td')
		if divs[1].span.text  != 'Dividend': #Ignore this row in the table
			#I'm only interested in 'Open' price; For other values, play with divs[1 - 5]
			data.append({'Date': divs[0].span.text, 'Open': float(divs[1].span.text.replace(',',''))})

	return data[:number_of_days]


def main() :
	SP500_ETF = Share('VOO')
	SmallCap_ETF = Share('VB')
	International_ETF = Share('VEA')
	EmergingMarkets_ETF = Share('VWO')
	RealEstate_ETF = Share('VNQ')
	Corporate_BOND = Share('LQD')
	Government_BOND = Share('SHY')
	LockheedMartin_STOCK = Share('LMT')

	ETFs = [SP500_ETF, SmallCap_ETF, International_ETF, EmergingMarkets_ETF, 
				RealEstate_ETF, Corporate_BOND, Government_BOND, LockheedMartin_STOCK]
	AcornsAllocation_ModAgg = ["20%", "30%", "15%", "10%", "10%", "7%", "8%", "0%"]
	i = 0
	for etf in ETFs :
		print("---",etf.get_name(),"---")
		print("Acorns Allocation: ", AcornsAllocation_ModAgg[i])
		daily_statistics(etf)
		aggregate_statistics(etf)
		print("")
		i += 1


main()
d = initialize_historical_data("hist.txt", ['VOO', 'VB', 'VEA', 'VWO', 'VNQ', 'LQD', 'SHY', 'LMT'], 15)
print(d["Vanguard_S&P_500_ETF"])
