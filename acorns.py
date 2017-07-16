#!/usr/bin/python3

from yahoo_finance import Share

def daily_statistics(ETF) :
	print("Daily Statistics")
	print("Current Price: ", ETF.get_price())
	print("Change: ", ETF.get_percent_change())

def aggregate_statistics(ETF) :
	print("Aggregate Statistics")
	print("Year High: ", ETF.get_year_high())
	print("50 Day Average: ", ETF.get_50day_moving_avg())

def yearly_statistics(ETF) :
	"""Use this to analyze yearly statistics; APY, etc."""
	pass

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
