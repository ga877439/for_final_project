import requests
import pandas as pd


def get_statements(year, season, stock_number) :
#爬取目標網站
	year = str(year)
	season = str(season)
	stock_number= str(stock_number)

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
			
	df_list = df_list[0:3]
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

	
	return df_list		#傳回3個panal data (三張表)




def Cashflow_statement_adjust(Cashflow_statement, IE= 1, IG= 1, DE=1, DG = 1):

#此函數可輸入一個現金流量表，並根據option決定要將現金流量表改成什麼樣子。若IE輸入0代表利息支出為營業活動，若DG輸入1則代表股利收入為投資活動，以此類推。
	
	
	def Cashflow_adjust(location, number = 0, plus = 1 ) :
	#此function 主要是讓使用者輸入代號後，把對應的數字從該活動之現金流做調整，如果plus == 1 代表加；否則輸入 -1 代表減
		nonlocal CFO, CFI, CFF
			
		if location == 1:
			CFO += 	plus * number 

		elif location == 2:
			CFI += 	plus * number 	

		elif location == 3:
			CFF += 	plus * number 	

	##開始計算
	row_len, column_len  = Cashflow_statement.shape	#得到此panal data的行數以及列數
	location = 1	#1表示現在在營運活動	2在投資活動 3在籌資活動
	Interest_recieve = Interest_give = Dividend_recieve = Dividend_give = CFO = CFI = CFF  = 0

	for i in range( 1, row_len  ):
		string = Cashflow_statement.values[i][0].strip()		#第i列第0行是項目
		number = Cashflow_statement.values[i][1].strip() 	#第i列第1行是我們想要得到的財報數字
		
		try:	#把逗號去掉並且轉成整數
			number = number.replace(',' , '')
			number = int(number)
		except:
			number = 0
	
		if string == '收取之利息' :
			Interest_recieve = number 
			Cashflow_adjust(location, Interest_recieve , -1)
		


		elif string == '支付之利息':
			Interest_give = number 
			Cashflow_adjust(location, Interest_give , -1)
			
		elif string == '收取之股利': 
			Dividend_recieve = number 
			Cashflow_adjust(location, Dividend_recieve , -1)

		elif string == '發放現金股利':
			Dividend_give  = number 
			Cashflow_adjust(location, Dividend_give , -1)


		elif string[0:10] == '營業活動之淨現金流入':	
			CFO += number 
			location += 1		#1表示現在在營運活動	2在投資活動 3在籌資活動
		elif string[0:10] == '投資活動之淨現金流入':
			CFI += number 
			location += 1
		elif string[0:10] == '籌資活動之淨現金流入':
			CFF += number 
			
	
	Cashflow_adjust(IE*2+1, Interest_give, 1)		#IE=0代表 營業活動； IE=1 代表 籌資活動
	Cashflow_adjust(IG+1, Interest_recieve , 1)		#IG=0代表 營業活動； IG=1 代表 投資活動
	Cashflow_adjust(DE*2+1, Dividend_give, 1)		#DE=0代表 營業活動； DE=1 代表 籌資活動
	Cashflow_adjust(DG+1, Dividend_recieve, 1)		#DG=0代表 營業活動； DG=1 代表 投資活動
 	
	print('利息支付 = %d, 利息收入 = %d, 股利發放 = %d, 股利收入 = %d' %(-Interest_give, Interest_recieve, -Dividend_give , Dividend_recieve) )

	
	return CFO,CFI,CFF

	





BalanceSheet, income_statement, Cashflow_statement = get_statements( 2013, 1, 1101)

print(BalanceSheet)
print(income_statement)
print(Cashflow_statement)



inventory = int(( BalanceSheet[BalanceSheet.item == '存貨合計'] ).values[0][1]  )
print(inventory)




