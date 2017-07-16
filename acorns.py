#!/usr/bin/python3

from yahoo_finance import Share

def daily_statistics(ETF) :
	print("Daily Statistics")
	print("Current Price: ", ETF.get_price())
	print("Change: ", ETF.get_change())

def main() :
	SP500_ETF = Share('VOO')

	ETFs = [SP500_ETF]

	for etf in ETFs :
		print("---",etf.get_name(),"---")
		daily_statistics(etf)

main()
