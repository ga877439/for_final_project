import requests
import pandas as pd

class Firm:
	def __init__(self, year, season, stock_number):	
			self.year = str(year)
			self.season = str(season)
			self.stock_number = str(stock_number)
			self.get_statements()
			self.getratios()
	def get_statements(self) :
	#爬取目標網站
		year = self.year
		season = self.season
		stock_number= self.stock_number

		url = "http://mops.twse.com.tw/server-java/t164sb01";
		form_data = {
			'step': 1,
		 'CO_ID': stock_number,
		  'SYEAR': year,
		  'SSEASON': season,
		  'REPORT_ID': "C",
		}

		r = requests.post(url,form_data)
		r.encoding = 'big5'
		html_df = pd.read_html(r.text)

	# 篩選出資產負債表、損益表、現金流量表
		df_list = []
		
		for df in html_df :
			if df.values[0][0] == '會計項目':
				df_list.append(df)

			if len(df_list) == 3:
				break
		
		for i in range(len(df_list)):
			df_list[i] = df_list[i].dropna(axis=0,how='any') 
			df_list[i] = df_list[i].reset_index(drop=True) 

			
	# 0:資產負債表 1:損益表 2:現金流量表
		pd.set_option('display.max_rows', None)
		
		
		df_list[0] = df_list[0].iloc[:,0:4]
		df_list[0].columns = ['item', 'now','2', 'past']
		df_list[0] = df_list[0].drop(columns="2")
		df_list[1] = df_list[1].iloc[:,0:2]
		df_list[1].columns = ['item', 'now']
		df_list[2] = df_list[2].iloc[:,0:2]
		df_list[2].columns = ['item', 'now']
	
		self.BS , self.IS, self.CS = df_list
<<<<<<< HEAD
=======
	def getratios(self):
				#ROE
		try:
			self.ave_equity =  int(  self.BS[self.BS.item.isin( ['權益總額'] ) ].values[0][1] )+ int(  self.BS[self.BS.item.isin( ['權益總額'] ) ].values[0][2] )
			self.NI =    int(  self.IS[self.IS.item.isin( ['本期綜合損益總額'] ) ].values[0][1] )  
			self.ROE = self.NI/self.ave_equity 
		except:
			self.ROE='n/a'
		print('ROE=',self.ROE)

		#流動比率
		try:
			self.current_assets =  int(  self.BS[self.BS.item.isin( ['流動資產合計'] ) ].values[0][1] ) 
			self.current_liabilities =    int(  self.BS[self.BS.item.isin( ['流動負債合計'] ) ].values[0][1] )
			self.current_ratio=self.current_assets/self.current_liabilities
		except:
			self.current_ratio='n/a'
		print('流動比率=',self.current_ratio)

		#速動比率
		try:
#			self.current_assets =  int(  self.BS[self.BS.item.isin( ['流動資產合計'] ) ].values[0][1] ) 
#			self.current_liabilities =  int(  self.BS[self.BS.item.isin( ['流動負債合計'] ) ].values[0][1] ) 
			self.inventory =    int(  self.BS[self.BS.item.isin( ['存貨','存貨合計'] ) ].values[0][1] )
			self.Accounts_receivable =    int(  self.BS[self.BS.item.isin( ['應收帳款淨額'] ) ].values[0][1] )
			self.speed_ratio=(self.current_assets-self.inventory-self.Accounts_receivable)/self.current_liabilities
		except:
			self.speed_ratio='n/a'
		print('速動比率=',self.speed_ratio)
		#資產負債率
		try:
			self.total_liabilities =  int(  self.BS[self.BS.item.isin( ['負債總額','負債總計'] ) ].values[0][1] ) 
			self.total_assets =    int(  self.BS[self.BS.item.isin( ['資產總額','資產總計'] ) ].values[0][1] )
			self.debt_asset_ratio=self.total_liabilities/self.total_assets
		except:
			self.debt_asset_ratio='n/a'
		print('資產負債率=',self.debt_asset_ratio)
		#股東權益比率
		try:
			self.Total_shareholders_equity =  int(  self.BS[self.BS.item.isin( ['權益總額'] ) ].values[0][1] ) 
#			self.total_assets =    int(  self.BS[self.BS.item.isin( ['資產總額'] ) ].values[0][1] )
			self.Equity_ratio=self.Total_shareholders_equity/self.total_assets
		except:
			self.Equity_ratio='n/a'
		print('股東權益比率=',self.Equity_ratio)
			
		#負債與股東權益比率
		try:
#			self.Total_shareholders_equity =  int(  self.BS[self.BS.item.isin( ['權益總額'] ) ].values[0][1] ) 
#			self.total_liabilities =  int(  self.BS[self.BS.item.isin( ['負債總額'] ) ].values[0][1] ) 
			self.debt_equity_ratio=self.total_liabilities/self.Total_shareholders_equity
		except:
			self.debt_equity_ratio='n/a'
		print('負債與流動比率=',self.debt_equity_ratio)
		#毛利率
		try:
			self.net_revenue =  int(  self.IS[self.IS.item.isin( ['營業毛利（毛損）'] ) ].values[0][1] ) 
			self.revenue =  int(  self.IS[self.IS.item.isin( ['營業收入合計'] ) ].values[0][1] ) 
			self.Gross_margin=self.net_revenue/self.revenue
		except:
			self.Gross_margin='n/a'
		print('毛利率=',self.Gross_margin)
			
			
		#營業利益率
		try:
#			self.revenue =  int(  self.IS[self.IS.item.isin( ['營業收入合計'] ) ].values[0][1] ) 
			self.Operating_Income =  int(  self.IS[self.IS.item.isin( ['營業利益(合計)','營業利益（損失）'] ) ].values[0][1] ) 
			self.Operating_Profit_Margin=self.Operating_Income/self.revenue
		except:
			self.Operating_Profit_Margin='n/a'
		print('營業利益率=',self.Operating_Profit_Margin)
		
		
		# 企業自身創造現金能力的比率 : 這個比率越高，表明企業自身創造現金能力越強，財力基礎越穩固
		try:
			self.operating_cashflow = int( self.CS[self.CS.item.isin(['營業活動之淨現金流入（流出）'])].values[0][1])
			self.total_cashflow = int( self.CS[self.CS.item.isin([ '本期現金及約當現金增加（減少）數'])].values[0][1])
			self.power_of_creating_cash = self.operating_cashflow / self.total_cashflow
		except:
			self.power_of_creating_cash = "n/a"
		print("企業自身創造現金能力的比率 =", self.power_of_creating_cash)

		# 企業償付全部債務能力的比率 : 這個比率反映企業一定時期，每1元負債由多少經營活動現金流量所補充，這個比率越大，説明企業償還全部債務能力越強。
		try:
			self.total_debt = int( self.BS[self.BS.item.isin( [ "負債總額"] ) ].values[0][1] ) 
			self.power_of_paying_debt = self.operating_cashflow / self.total_debt
		except:
			self.power_of_paying_debt = "n/a"
		print("企業償付全部債務能力的比率 =", self.power_of_paying_debt)

		# 企業短期償債能力的比率 : 這個比率越大，説明企業短期償債能力越強。
		try:
			self.current_debt = int( self.BS[self.BS.item.isin( [ "流動負債合計"] ) ].values[0][1] )
			self.power_of_paying_debt_SR = self.operating_cashflow / self.current_debt
		except:
			self.power_of_paying_debt_SR = "n/a"
		print("企業短期償債能力的比率 =", self.power_of_paying_debt_SR)

		# 現金流量資本支出比率 : 個比率主要反映企業利用經營活動産生的凈現金流量維持或擴大生産經營規模的能力，其值越大，説明企業發展能力越強
		try:
			self.capital_expenditures = int( self.CS[self.CS.item.isin(["取得不動產、廠房及設備"] ) ].values[0][1] )
			self.cash_flow_capital_expenditure_ratio = self.operating_cashflow / self.capital_expenditure
		except:
			self.cash_flow_capital_expenditure_ratio = "n/a"
		print("現金流量資本支出比率 =", self.cash_flow_capital_expenditure_ratio)

		# 每股流通股的現金流量比率 : 比率越大，説明企業進行資本支出的能力越強
		try:
			self.EPS = int( self.IS[self.IS.item.isin( ['基本每股盈餘'] ) ].values[0][1] )
			self.NI = int( self.IS[self.IS.item.isin( ['本期淨利（淨損）'] ) ].values[0][1] )
			self.outstanding_shares = self.NI / self.EPS
			self.cash_flow_of_per_share_ratio = self.operating_cashflow / self.outstanding_shares
		except:
			self.cash_flow_of_per_share_ratio = "n/a"
		print("每股流通股的現金流量比率 =", self.cash_flow_of_per_share_ratio)

		# 支付現金股利的比率 : 比率越大，説明企業支付現金股利能力越強
		try:
			self.cash_div = int( self.CS[self.CS.item.isin(["發放現金股利"] ) ].values[0][1] )
			self.cash_pay_div_ratio = self.operating_cashflow / self.cash_div
		except:
			self.cash_pay_div_ratio = "n/a"
		print("支付現金股利的比率 =", self.cash_pay_div_ratio)
		
>>>>>>> dba0d0f6584eb7f2cd6c7e304616ec02782cf122
		


#以下是 example	
<<<<<<< HEAD
x = Firm(2013,1,1101)
print(x.BS)
print('')
print(x.IS)
print('')
print(x.CS)
print('')
=======
x= Firm(2013,1,1101)

>>>>>>> dba0d0f6584eb7f2cd6c7e304616ec02782cf122
