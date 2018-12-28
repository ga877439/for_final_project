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
		
	def getratios(self):
		self.inventory=int(  self.BS[self.BS.item.isin( ['存貨合計' , '存貨'] ) ].values[0][1] )
		
#以下是 example	
x = Firm(2013,1,1101)
print(x.BS)
print('')
print(x.IS)
print('')
print(x.CS)
print('')