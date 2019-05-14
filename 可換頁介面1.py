import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import *

ratios_list = ['ROE', '流動比率', '速動比率', '資產負債比', '權益資產比', '負債與股東權益比率', '毛利率', '營業利益率', 
	'現金創造力',  '償債力', '短期償債力', '現金流量資本支出比率', '每股現金流量比率', '股利支付比率']
			   
			   

import requests
import pandas as pd
class Firm:
	def __init__(self, year, season, stock_number):	
			self.year = str(year)
			self.season = str(season)
			self.stock_number = str(stock_number)
			
			self.flag = 1 #判斷是否該股票代碼是有效代碼
			
			self.get_statements()
			if self.flag == 0:
				self.flag = 1
				self.get_statements(type = 'A')
				
			self.ratios = []
			if self.flag == 1:
				self.getratios()
			
			
			
	def get_statements(self, type = 'C') :
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
		  'REPORT_ID': type,
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

		if 	len(df_list) == 3:	
		# 0:資產負債表 1:損益表 2:現金流量表
			pd.set_option('display.max_rows', None)
			
			if season == '4':

				df_list[0].columns = ['item', 'now', 'past']
			else:
				df_list[0].columns = ['item', 'now', '2', 'past']
				
			df_list[1] = df_list[1].iloc[:,0:2]
			df_list[1].columns = ['item', 'now']
			df_list[2] = df_list[2].iloc[:,0:2]
			df_list[2].columns = ['item', 'now']
		
			self.BS , self.IS, self.CS = df_list
			
		else:
			self.flag = 0
		
	def getratios(self):
		#ROE
		try:
			self.ave_equity =  int(  self.BS[self.BS.item.isin( ['權益總額', '權益總計'] ) ].values[0][1] )+ int(  self.BS[self.BS.item.isin( ['權益總額'] ) ].values[0][2] )
			self.NI = int( self.IS[self.IS.item.isin( ['本期淨利（淨損）', '繼續營業單位本期淨利（淨損）', '本期稅後淨利（淨損）'] ) ].values[0][1] )
			self.ROE = self.NI/self.ave_equity 
		except:
			self.ROE='n/a'
		self.ratios.append(self.ROE)

		#流動比率
		try:
			self.current_assets =  int(  self.BS[self.BS.item.isin( ['流動資產合計'] ) ].values[0][1] ) 
			self.current_liabilities =    int(  self.BS[self.BS.item.isin( ['流動負債合計'] ) ].values[0][1] )
			self.current_ratio=self.current_assets/self.current_liabilities
		except:
			self.current_ratio='n/a'
		self.ratios.append(self.current_ratio)

		#速動比率
		try:
#			self.current_assets =  int(  self.BS[self.BS.item.isin( ['流動資產合計'] ) ].values[0][1] ) 
#			self.current_liabilities =  int(  self.BS[self.BS.item.isin( ['流動負債合計'] ) ].values[0][1] ) 
			self.inventory =    int(  self.BS[self.BS.item.isin( ['存貨','存貨合計'] ) ].values[0][1] )
			self.Accounts_receivable =    int(  self.BS[self.BS.item.isin( ['應收帳款淨額'] ) ].values[0][1] )
			self.speed_ratio=(self.current_assets-self.inventory-self.Accounts_receivable)/self.current_liabilities
		except:
			self.speed_ratio='n/a'
		self.ratios.append(self.speed_ratio)
		#資產負債率
		try:
			self.total_liabilities =  int(  self.BS[self.BS.item.isin( ['負債總額','負債總計'] ) ].values[0][1] ) 
			self.total_assets =    int(  self.BS[self.BS.item.isin( ['資產總額','資產總計'] ) ].values[0][1] )
			self.debt_asset_ratio=self.total_liabilities/self.total_assets
		except:
			self.debt_asset_ratio='n/a'
		self.ratios.append(self.debt_asset_ratio)
		#股東權益比率
		try:
			self.Total_shareholders_equity =  int(  self.BS[self.BS.item.isin( ['權益總額'] ) ].values[0][1] ) 
#			self.total_assets =    int(  self.BS[self.BS.item.isin( ['資產總額'] ) ].values[0][1] )
			self.Equity_ratio=self.Total_shareholders_equity/self.total_assets
		except:
			self.Equity_ratio='n/a'
		self.ratios.append(self.Equity_ratio)
			
		#負債與股東權益比率
		try:
#			self.Total_shareholders_equity =  int(  self.BS[self.BS.item.isin( ['權益總額'] ) ].values[0][1] ) 
#			self.total_liabilities =  int(  self.BS[self.BS.item.isin( ['負債總額'] ) ].values[0][1] ) 
			self.debt_equity_ratio=self.total_liabilities/self.Total_shareholders_equity
		except:
			self.debt_equity_ratio='n/a'
		self.ratios.append(self.debt_equity_ratio)
		#毛利率
		try:
			self.net_revenue =  int(  self.IS[self.IS.item.isin( ['營業毛利（毛損）'] ) ].values[0][1] ) 
			self.revenue =  int(  self.IS[self.IS.item.isin( ['營業收入合計'] ) ].values[0][1] ) 
			self.Gross_margin=self.net_revenue/self.revenue
		except:
			self.Gross_margin='n/a'
		self.ratios.append(self.Gross_margin)
			
			
		#營業利益率
		try:
#			self.revenue =  int(  self.IS[self.IS.item.isin( ['營業收入合計'] ) ].values[0][1] ) 
			self.Operating_Income =  int(  self.IS[self.IS.item.isin( ['營業利益(合計)','營業利益（損失）'] ) ].values[0][1] ) 
			self.Operating_Profit_Margin=self.Operating_Income/self.revenue
		except:
			self.Operating_Profit_Margin='n/a'
		self.ratios.append(self.Operating_Profit_Margin)
		
		
		# 企業自身創造現金能力的比率 : 這個比率越高，表明企業自身創造現金能力越強，財力基礎越穩固
		try:
			self.operating_cashflow = int( self.CS[self.CS.item.isin(['營業活動之淨現金流入（流出）'])].values[0][1])
			self.total_cashflow = int( self.CS[self.CS.item.isin([ '本期現金及約當現金增加（減少）數'])].values[0][1])
			self.power_of_creating_cash = self.operating_cashflow / self.total_cashflow
		except:
			self.power_of_creating_cash = "n/a"
		self.ratios.append(self.power_of_creating_cash)
		

		# 企業償付全部債務能力的比率 : 這個比率反映企業一定時期，每1元負債由多少經營活動現金流量所補充，這個比率越大，説明企業償還全部債務能力越強。
		try:
			self.total_debt = int( self.BS[self.BS.item.isin( [ "負債總額","負債總計"] ) ].values[0][1] ) 
			self.power_of_paying_debt = self.operating_cashflow / self.total_debt
		except:
			self.power_of_paying_debt = "n/a"
		self.ratios.append(self.power_of_paying_debt)

		# 企業短期償債能力的比率 : 這個比率越大，説明企業短期償債能力越強。
		try:
			self.current_debt = int( self.BS[self.BS.item.isin( [ "流動負債合計"] ) ].values[0][1] )
			self.power_of_paying_debt_SR = self.operating_cashflow / self.current_debt
		except:
			self.power_of_paying_debt_SR = "n/a"
		self.ratios.append(self.power_of_paying_debt_SR)

		# 現金流量資本支出比率 : 個比率主要反映企業利用經營活動産生的凈現金流量維持或擴大生産經營規模的能力，其值越大，説明企業發展能力越強
		try:
			self.capital_expenditures = -1* int( self.CS[self.CS.item.isin(["取得不動產、廠房及設備", "取得不動產及設備"] ) ].values[0][1] )
			self.cash_flow_capital_expenditure_ratio = self.operating_cashflow / self.capital_expenditures
		except:
			self.cash_flow_capital_expenditure_ratio = "n/a"

		self.ratios.append(self.cash_flow_capital_expenditure_ratio)

		# 每股流通股的現金流量比率 : 比率越大，説明企業進行資本支出的能力越強
		try:
			self.EPS = float( self.IS[self.IS.item.isin( ['基本每股盈餘','基本每股盈餘合計'] ) ].values[0][1] )
			#self.NI = int( self.IS[self.IS.item.isin( ['本期淨利（淨損）', '繼續營業單位本期淨利（淨損）'] ) ].values[0][1] )
			self.outstanding_shares = self.NI / self.EPS
			self.cash_flow_of_per_share_ratio = self.operating_cashflow / self.outstanding_shares
		except:
			self.cash_flow_of_per_share_ratio = "n/a"
		self.ratios.append(self.cash_flow_of_per_share_ratio)

		# 支付現金股利的比率 : 比率越大，説明企業支付現金股利能力越強
		try:
			self.cash_div = -1 * int( self.CS[self.CS.item.isin(["發放現金股利"] ) ].values[0][1] )
			self.cash_pay_div_ratio = self.operating_cashflow / self.cash_div
		except:
			self.cash_pay_div_ratio = "n/a"
		self.ratios.append(self.cash_pay_div_ratio)
		
		
		




class TwoPageApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
	

	
	
	
company_name = []
year_seasons = []    
ratios_to_be_printed = []    
check_list = [] #用來判別是圈還是叉  ( O or X )

class StartPage(tk.Frame):


    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        f = tkFont.Font(size = 36, family = "Courier New")

        self.lblNum = tk.Label(self, text = "Num", height = 1, width = 5, font = f,fg = "white", bg = "red")
        self.lblSeason = tk.Label(self, text = "Season", height = 1, width = 7, font = f,fg = "white", bg = "orange")

        self.lblRatio = tk.Label(self, text = "Ratio", height = 1, width = 15, font = f,fg = "white", bg = "blue")
        self.btnNext = tk.Button(self, text="下一頁", height = 1, width = 8,font = f, fg = "white", bg = "black",
                    command = lambda: controller.show_frame(PageOne))##
        self.btngetvalues = tk.Button(self, text="輸入完畢", height = 1, width = 8,font = f, fg = "white", bg = "black",
                    command = self.getvalues )##			
					
        self.lblNum.grid(row = 0, column = 1, sticky = tk.W)
        self.lblSeason.grid(row = 0, column = 2, sticky = tk.E)

        self.lblRatio.grid(row = 0, column = 3, columnspan = 2)
        self.btnNext.grid(row = 8, column = 4, columnspan = 1, sticky = tk.E)    		
        self.btngetvalues.grid(row = 9, column = 4, columnspan = 1, sticky = tk.E)
#################################################column = 0 self.btnOXs
        self.btnOXs = []
        for i in range(5):
            self.btnOXs.append(tk.Button(self, text = "O", height = 1, width = 2, font = f, bg = "cyan"))
            self.btnOXs[i].grid(row = i+3, column = 0)
        self.btnOXs[0]["command"] = self.clickBtnOX0
        self.btnOXs[1]["command"] = self.clickBtnOX1
        self.btnOXs[2]["command"] = self.clickBtnOX2
        self.btnOXs[3]["command"] = self.clickBtnOX3
        self.btnOXs[4]["command"] = self.clickBtnOX4
################################################# column = 1 self.enterNums
        self.enterNums = []
        for i in range(5):
            self.enterNums.append(tk.Entry(self, width = 5, font = f))
            self.enterNums[i].grid(row = i+3, column = 1, sticky = tk.W)
################################################# column = 2 self.comboSeasons
        self.seasons = [] # 放107-4 107-3 107-2 ...
        for i in range(107, 95, -1):
            for j in range(4, 0, -1):
                self.seasons.append("%d-%d" % (i, j))
                
        self.comboSeasons = []
        for i in range(5):
            self.comboSeasons.append(ttk.Combobox(self ,width = 6, values = self.seasons, font = f))
            self.comboSeasons[i].current(1)
            self.comboSeasons[i].grid(row = i+3, column = 2)
################################################# column = 3 self.comboSheets


################################################# column = 4 self.listboxRatios
        self.listboxRatios = Listbox(self, width = 15, height = 8, selectmode = MULTIPLE,
                            fg = "white", bg = 'purple', font = f)
        self.scrollbar = Scrollbar(self, orient = "vertical")
        self.listboxRatios.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.listboxRatios.yview)
        self.listboxRatios.grid(row = 1, column = 4, rowspan = 7, columnspan = 2, sticky = "NEWS")
        self.scrollbar.grid(row = 1, column = 6, rowspan = 7, sticky = N+S)

        for ratio in ratios_list:
            self.listboxRatios.insert(END, ratio)
################################################# function

    def getvalues(self):
        self.getBtnOXValue()
        self.getNumValue()
        self.getSeasonValue()

		
    def clickBtnOX0(self): # get按鈕是O還是X 然後傳入函數self.changeBtnOX
        OorX = self.btnOXs[0].cget("text")
        self.changeBtnOX(0, OorX)
    def clickBtnOX1(self):
        OorX = self.btnOXs[1].cget("text")
        self.changeBtnOX(1, OorX)
    def clickBtnOX2(self):
        OorX = self.btnOXs[2].cget("text")
        self.changeBtnOX(2, OorX)
    def clickBtnOX3(self):
        OorX = self.btnOXs[3].cget("text")
        self.changeBtnOX(3, OorX)  
    def clickBtnOX4(self):
        OorX = self.btnOXs[4].cget("text")
        self.changeBtnOX(4, OorX)
        
    def changeBtnOX(self, i, OorX):
        self.btnOXs[i].config(text = "X") if OorX == "O" else self.btnOXs[i].config(text = "O")

    def getBtnOXValue(self): # 取值
        global check_list
        check_list = []
        for i in self.btnOXs:
            check_list.append(i.cget("text"))

    def getNumValue(self): # 取值
        global company_name 
        company_name = []
        for i in self.enterNums:
            company_name.append( i.get() )
    
    def getSeasonValue(self): # 取值
        global year_seasons 
        year_seasons = []
        for i in self.comboSeasons:
            year_seasons.append(i.get())



    def getRatioValue(self): # 取值
        for i in self.listboxRatios.curselection():
            ratios_to_be_printed.append(self.listboxRatios.get(i))

			
			
firm_list = []
class PageOne(tk.Frame):

	
	
	
	def __init__(self, parent, controller):
		f = tkFont.Font(size = 36, family = "Courier New")
		tk.Frame.__init__(self, parent)

		self.button1 = tk.Button(self, text="Back to Home", font = f ,
			command=lambda: controller.show_frame(StartPage))
		self.button1.grid(row = 0, column = 0, sticky = tk.NE + tk.SW)
		
		self.button2 = tk.Button(self, text="開始計算", font = f,
			command=self.createWidgets)
		self.button2.grid(row = 1, column = 0, sticky = tk.NE + tk.SW)

		
	def createWidgets(self):
		
		f1 = tkFont.Font(size = 12, family = "Courier New")
		self.button1.config( font = f1 )
		self.button2.config( font = f1 ) 
		
		#文字敘述  (第零欄)
		
		self.title1 = tk.Label(self, text = "公司代碼", height = 1, width = 16, font = f1) #第0列
		self.title1.grid(row = 0, column = 1, sticky = tk.NE + tk.SW)
		self.title2 = tk.Label(self, text = "年-季", height = 1, width = 16, font = f1) #第0列
		self.title2.grid(row = 1, column = 1, sticky = tk.NE + tk.SW)
		
		for i in range( len(ratios_list)):	#第i+1列
			temp = tk.Label(self, text = ratios_list[i] , height = 1, width = 16, font = f1) 
			temp.grid(row= 2+i , column=1, sticky=tk.NE + tk.SW)
		
		
		
		#開始處理公司	
		global firm_list #共有5家公司
		firm_list = []
		for i in range(5):
			if company_name[i] != '':
				firm_list.append(  Firm( year_seasons[i][0:3], year_seasons[i][-1], company_name[i] )  )
			else:
				firm_list.append( 0 )
		
		#插入 grid 以及數字 第j家公司  (第j欄)
		for j in range(5):

				
			if check_list[j] == 'O' and company_name[j] != '':
			
			
				
				if firm_list[j].flag != 1:
					self.label1	= tk.Label(self, text = '輸入錯誤' , height = 1, width = 16, font = f1) 	#第0列
					self.label1.grid(row = 0, column = 2+j, sticky = tk.NE + tk.SW)
					self.label2	= tk.Label(self, text = '輸入錯誤' , height = 1, width = 16, font = f1) 	#第1列
					self.label2.grid(row = 1, column = 2+j, sticky = tk.NE + tk.SW)
			
					for i in range( len(ratios_list)):		#第i+2列
						temp = tk.Label(self, text = 'None', height = 1, width = 16, font = f1) 
						temp.grid(row= i+2 , column=2+j, sticky=tk.NE + tk.SW)
		
				else:
					self.label1 = tk.Label(self, text = company_name[j] , height = 1, width = 16, font = f1) 	#第0列
					self.label1.grid(row = 0, column = 2+j , sticky = tk.NE + tk.SW)
					self.label1 = tk.Label(self, text = year_seasons[j] , height = 1, width = 16, font = f1) 	#第1列
					self.label1.grid(row = 1, column = 2+j , sticky = tk.NE + tk.SW)			
					for i in range( len(ratios_list)):		#第i+1列
						try:
							temp = tk.Label(self, text = '%0.4f' %  firm_list[j].ratios[i], height = 1, width = 16, font = f1) 
						except:
							temp = tk.Label(self, text = firm_list[j].ratios[i], height = 1, width = 16, font = f1) 
						temp.grid(row= i+2 , column=2+j , sticky=tk.NE + tk.SW)

	
			else:
				self.label1	= tk.Label(self, text = '未選擇' , height = 1, width = 16, font = f1) 	#第0列
				self.label1.grid(row = 0, column = 2+j, sticky = tk.NE + tk.SW)
				self.label2	= tk.Label(self, text = '未選擇' , height = 1, width = 16, font = f1) 	#第1列
				self.label2.grid(row = 1, column = 2+j, sticky = tk.NE + tk.SW)
		
				for i in range( len(ratios_list)):		#第i+1列
					temp = tk.Label(self, text = 'None', height = 1, width = 16, font = f1) 
					temp.grid(row= i+2 , column=2+j, sticky=tk.NE + tk.SW)
	
	
	



app = TwoPageApp()
app.mainloop()




