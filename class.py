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
		df_list[1] = df_list[1].iloc[:,0:2]
		df_list[1].columns = ['item', 'now']
		df_list[2] = df_list[2].iloc[:,0:2]
		df_list[2].columns = ['item', 'now']
	
		self.BS , self.IS, self.CS = df_list
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
		
		
		


	





	
#以下是 example	
x= Firm(2013,1,1101)
