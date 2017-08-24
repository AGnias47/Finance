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
import matplotlib.pyplot as Plot
import numpy

def daily_statistics(ETF) :
	"""Gets information of the day to day performance of a stock"""
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
	d_prices = dict()
	d_dates = dict()
	for stock in StockTicker_list :
		hist = get_historical_data(stock, days)
		prices = []
		dates = []
		for day in hist :
			#print(day["Date"].replace(" ","_").replace(",",""), end=":")
			#print(day["Open"], end=" ")
			prices.append(day["Open"])
			dates.append(day["Date"].split(", ")[0])
		full_name = Share(stock).get_name().replace(" ", "_")
		d_prices[full_name] = list(reversed(prices))
		d_dates[full_name] = list(reversed(dates))
	return (d_prices, d_dates)


def get_historical_data(name, number_of_days):
	#Source: https://github.com/lukaszbanasiak/yahoo-finance/issues/128
	data = []
	url = "https://finance.yahoo.com/quote/" + name + "/history/"
	rows = BeautifulSoup(urllib.request.urlopen(url).read(),"lxml").findAll('table')[1].tbody.findAll('tr')

	for each_row in rows:
		divs = each_row.findAll('td')
		if divs[1].span.text != 'Dividend': #Ignore this row in the table
			#I'm only interested in 'Open' price; For other values, play with divs[1 - 5]
			data.append({'Date': divs[0].span.text, 'Open': float(divs[1].span.text.replace(',',''))})

	return data[:number_of_days]


def plot_historical_data(DATES_list, PRICES_list, NAME) :
	Plot.style.use('bmh')
	x_init = list(range(0, len(DATES_list)))
	i = 0
	while i < len(DATES_list) :
		if i % 3 != 0 :
			DATES_list[i] = ""
		i += 1
	x = numpy.array(x_init)
	y = numpy.array(PRICES_list)
	Plot.xticks(x, DATES_list)
	Plot.plot(x, PRICES_list)
	Plot.title(NAME)
	Plot.ylabel("USD")
	Plot.show()
	
	
def initialize_website_head(fname) :
	title = "Acorns Performance Analysis"
	description = "Analyzes stockes used in Acorns investing portfolios."
	author = "A. Gnias"
	with open(fname, 'w') as f :
		f.write("<!doctype html>\n<html lang=\"en\">\n<head>\n\t<meta charset=\"utf-8\">")
		f.write("\n\t<title>%s</title>\n\t<meta name=\"description\"" % title)
		f.write("content=\"%s\">" % description)
		f.write("\n\t<meta name=\"author\" content=\"%s\">\n</head>\n" % author)


def add_website_data(fname) :
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
	AcornsAllocation_ModAgg = [0.2, 0.3, 0.15, 0.1, 0.1, 0.07, 0.08, 0.00]
	
	f = open(fname, "a")
	f.write("<body>\n")
	i = 0
	f.write("<h2 class=\"Profile Type Headers\">Moderately Aggresive Portfolio</h2>\n")
	for etf in ETFs :
		name = etf.get_name()
		allocation_string = str(AcornsAllocation_ModAgg[i] * 100) + "%"
		f.write("\t<h3 class=\"ETF Headers\">%s</h3>\n" % name)
		f.write("\t\t<p>Acorns Allocation: %s</p>\n" % allocation_string)
		f.write("\t\t<p>Current Price: %s</p>\n" % etf.get_price())
		f.write("\t\t<p>Change: %s</p>\n" % etf.get_percent_change())
		f.write("\t\t<p>Year High: %s</p>\n" % etf.get_year_high())
		f.write("\t\t<p>Year Low: %s</p>\n" % etf.get_year_low())
		f.write("\t\t<p>50 Day Average: %s</p>\n" % etf.get_50day_moving_avg())
		i += 1
	f.write("</body>\n</html>")
	f.close()


def main() :
	#initialize shares
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
		#Get numerical statistics
		print("---", etf.get_name(), "---")
		
		

	#Get historical plots
	(d_prices, d_dates) = initialize_historical_data("hist.txt",
												 ['VOO', 'VB', 'VWO', 'VNQ', 'LQD', 'SHY', 'LMT', 'VEA'], 30)
	plot_historical_data(d_dates["Vanguard_S&P_500_ETF"], d_prices["Vanguard_S&P_500_ETF"],
						 "Vanguard S&P 500 ETF")
	plot_historical_data(d_dates["Vanguard_Small-Cap_ETF_-_DNQ"], d_prices["Vanguard_Small-Cap_ETF_-_DNQ"],
						 "Vanguard Small-Cap ETF - DNQ")
	#plot_historical_data(d_dates["Vanguard_FTSE_Developed_Markets"], d_prices["Vanguard_FTSE_Developed_Markets"],
	#					 "Vanguard FTSE Developed Markets")
	#plot_historical_data(d_dates["Vanguard_FTSE_Emerging_Markets"], d_prices["Vanguard_FTSE_Emerging_Markets"],
	#					 "Vanguard FTSE Emerging Markets")
	#plot_historical_data(d_dates["Vanguard_REIT_ETF_-_DNQ"], d_prices["Vanguard_REIT_ETF_-_DNQ"],
	#					 "Vanguard REIT ETF - DNQ")
	#plot_historical_data(d_dates["Shares_iBoxx_$_Investment_Grad"], d_prices["Shares_iBoxx_$_Investment_Grad"],
	#					 "Shares iBoxx $ Investment Grad")
	#plot_historical_data(d_dates["iShares_iBoxx_$_Investment_Grad"], d_prices["iShares_iBoxx_$_Investment_Grad"],
	#					 "iShares iBoxx $ Investment Grad")
	#plot_historical_data(d_dates["iShares_1-3_Year_Treasury_Bond"], d_prices["iShares_1-3_Year_Treasury_Bond"],
	#					 "iShares 1-3 Year Treasury Bond")
	#plot_historical_data(d_dates["Lockheed_Martin_Corporation"], d_prices["Lockheed_Martin_Corporation"],
	#					 "Lockheed Martin Corporation")


#main()
fname = "C:/Users/Andy/Desktop/Finance/index.html"
initialize_website_head(fname)
add_website_data(fname)

