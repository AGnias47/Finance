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

def daily_statistics(ETF) :
	#print("Daily Statistics")
	print("Current Price: ", ETF.get_price())
	print("Change: ", ETF.get_percent_change())

def aggregate_statistics(ETF) :
	#print("Aggregate Statistics")
	print("Year High: ", ETF.get_year_high())
	print("50 Day Average: ", ETF.get_50day_moving_avg())

def yearly_statistics(ETF) :
	"""Use this to analyze yearly statistics; APY, etc."""
	pass


def initialize_historical_data(f_out, StockTicker_list, days) :
	for stock in StockTicker_list :
		json = get_historical_data(stock, days)
		for j in json : 
			print(j)
		#data = json.load(json[0])
		#pprint(json)



def load_historical_data(f_in) :
	d = dict()
	f = open(f_in, "r")
	el = f.readlines()
	for line in el :
		line = line.strip()
		prices = line.split(" ")
		name = prices.pop(0)
		prices = [float(i) for i in prices]	
		d[name] = prices
	return d

def update_historical_data(ETF_list) :
	for ETF in ETF_list :
		name = ETF.get_name()
		name = name.replace(" ","_")
		prices = d[name]
		newest_price = ETF.get_prev_close()
		newest_price = float(newest_price)
		prev_new = prices[-1]
		if newest_price != prev_new :
			prices.pop(0)
			prices.append(newest_price)
			print(prices)
		

def hist(ETF) :
	pass
	#get_prev_close()


def weekly_statistics(ETF) :
	start = datetime.timedelta(weeks=1)
	end = datetime.date.today()
	print(start, end)


def get_historical_data(name, number_of_days):
	#Source: https://github.com/lukaszbanasiak/yahoo-finance/issues/128
	#Note: Incredibly time consuming - 30 seconds for 15 days
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

#main()
#SP500_ETF = Share('VOO')
#etfs = [SP500_ETF]
#d = dict()
#d = load_historical_data("hist.txt")
#update_historical_data(etfs)
#print(d["Vanguard_S&P_500_ETF"])
#t = get_historical_data('AMZN', 15)
#print(t)

initialize_historical_data("hist.txt", ['VOO'], 3) 
