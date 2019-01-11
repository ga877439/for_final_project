import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import *
import numpy as np
import scipy.stats as si
import sympy as sy
import requests
import pandas as pd

ratios_list = ['ROE', '流動比率', '速動比率', '資產負債比', '權益資產比', '負債與股東權益比率', '毛利率', '營業利益率', 
	'現金創造力',  '償債力', '短期償債力', '現金流量資本支出比率', '每股現金流量比率', '股利支付比率']

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

        for F in (StartPage, PageOne, PageAtt1, PageAtt2, PageAtt3, PageAtt4):

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
        f2 = tkFont.Font(size = 15, family = "Courier New")
        f3 = tkFont.Font(size = 25, family = "Courier New")

        self.lblNum = tk.Label(self, text = "Num", height = 1, width = 7, font = f,fg = "white", bg = "red")
        self.lblSeason = tk.Label(self, text = "Season", height = 1, width = 9, font = f,fg = "white", bg = "green2")

        self.lblRatio = tk.Label(self, text = "Ratio", height = 1, width = 20, font = f,fg = "white", bg = "dark orange")
        self.btnNext = tk.Button(self, text="下一頁", height = 1, width = 8,font = f3, bg = "gold",
                    command = lambda: controller.show_frame(PageOne))##
        self.btngetvalues = tk.Button(self, text="輸入完畢", height = 1, width = 8,font = f3, bg = "gold",
                    command = self.getvalues )		
					
        self.lblNum.grid(row = 0, column = 1, sticky = tk.W)
        self.lblSeason.grid(row = 0, column = 2, sticky = tk.E)

        self.lblRatio.grid(row = 0, column = 3, columnspan = 2)
        self.btnNext.grid(row = 8, column = 4, columnspan = 1, sticky = tk.E)    		
        self.btngetvalues.grid(row = 8, column = 3, columnspan = 2)

        self.btnAtt1 = tk.Button(self, text="選擇權定價", height = 1, width = 17, font = f2, fg = "white", bg = "DeepPink2",
                    command = lambda: controller.show_frame(PageAtt1))
        self.btnAtt1.grid(row = 8, column = 0, columnspan = 2, sticky = tk.E)
        
        self.btnAtt2 = tk.Button(self, text="債券市值計算", height = 1, width = 17, font = f2, fg = "white", bg = "purple1",
                    command = lambda: controller.show_frame(PageAtt2))
        self.btnAtt2.grid(row = 9, column = 0, columnspan = 2, sticky = tk.E)
        
        self.btnAtt3 = tk.Button(self, text="權證價格計算", height = 1, width = 17, font = f2, fg = "white", bg = "purple1",
                    command = lambda: controller.show_frame(PageAtt3))
        self.btnAtt3.grid(row = 8, column = 1, columnspan = 2, sticky = tk.E)
        
        self.btnAtt4 = tk.Button(self, text="可轉換公司債價值計算", height = 1, width = 17, font = f2, fg = "white", bg = "DeepPink2",
                    command = lambda: controller.show_frame(PageAtt4))
        self.btnAtt4.grid(row = 9, column = 1, columnspan = 2, sticky = tk.E)
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
            self.enterNums.append(tk.Entry(self, width = 7, font = f))
            self.enterNums[i].grid(row = i+3, column = 1, sticky = tk.W)
################################################# column = 2 self.comboSeasons
        self.seasons = [] # 放107-4 107-3 107-2 ...
        for i in range(107, 95, -1):
            for j in range(4, 0, -1):
                self.seasons.append("%d-%d" % (i, j))
                
        self.comboSeasons = []
        for i in range(5):
            self.comboSeasons.append(ttk.Combobox(self ,width = 8, values = self.seasons, font = f))
            self.comboSeasons[i].current(1)
            self.comboSeasons[i].grid(row = i+3, column = 2)
################################################# column = 3 self.listboxRatios
        self.listboxRatios = Listbox(self, width = 20, height = 8, selectmode = MULTIPLE,
                            fg = "white", bg = 'DeepSkyBlue2', font = f)
        self.scrollbar = Scrollbar(self, orient = "vertical")
        self.listboxRatios.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.listboxRatios.yview)
        self.listboxRatios.grid(row = 1, column = 3, rowspan = 7, columnspan = 2, sticky = "NEWS")
        self.scrollbar.grid(row = 1, column = 5, rowspan = 7, sticky = N+S)

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

			
#@$%^#@$%^#@$%^#@$%^#@$%^#@$%^#@$%^#@$%^#@$%^#@$%^#@$%^#@$%^#@$%^#@$%^附加功能
def euro_vanilla_call(S, K, T, r, sigma):
    
    #S: spot price
    #K: strike price
    #T: time to maturity
    #r: interest rate
    #sigma: volatility of underlying asset
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d1_normal = si.norm.cdf(d1, 0.0, 1.0)#holding shares
    d2_normal = K * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0)#borrow 
    call = (S * si.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0))
    bond_price = S - call
    default_prob = si.norm.cdf(-d2, 0.0, 1.0)
    return (call, d1_normal, d2_normal, bond_price, default_prob)    
  
def euro_vanilla_put(S, K, T, r, sigma):
    
    #S: spot price
    #K: strike price
    #T: time to maturity
    #r: interest rate
    #sigma: volatility of underlying asset
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    
    put = (K * np.exp(-r * T) * si.norm.cdf(-d2, 0.0, 1.0) - S * si.norm.cdf(-d1, 0.0, 1.0))
    
    return put

def euro_vanilla_call_4(S, K, T, r, sigma):
    
    #S: spot price
    #K: strike price
    #T: time to maturity
    #r: interest rate
    #sigma: volatility of underlying asset
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d1_normal = si.norm.cdf(d1, 0.0, 1.0)#holding shares
    d2_normal = K * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0)#borrow 
    call = (S * si.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * si.norm.cdf(d2, 0.0, 1.0))
    bond_price = S - call
    default_prob = si.norm.cdf(-d2, 0.0, 1.0)
    return call


class PageAtt1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        f1 = tkFont.Font(size = 20, family = "Courier New")
        f2 = tkFont.Font(size = 20, family = "Courier New")

        self.lblNumList = []
        text = ("選擇權定價:", "請輸入股票價格:", "請輸入執行價格:", "請輸入期限(Year):",
                "請輸入無風險資產年利率(ex:0.01):", "請輸入股價波動率(ex:0.25):",
                "答案:", "Call Price:", "Put Price:")
        for i in range(9):
            self.lblNumList.append(tk.Label(self, height = 1, width = 40, font = f1))
            self.lblNumList[i]["text"] = text[i]
            self.lblNumList[i].grid(row = i, column = 0, sticky = tk.NE + tk.SW)
        self.lblNumList[0]["bg"] = "firebrick2"

        self.txtNumList = []
        for i in range(5):
            self.txtNumList.append(tk.Entry(self, width = 20, font = f1))   
            self.txtNumList[i].grid(row = i+1, column = 1, sticky = tk.NE + tk.SW)

        self.ansList = []
        for i in range(2):
            self.ansList.append(tk.Entry(self, width = 20, font = f1))
            self.ansList[i].grid(row = i+7, column = 1, sticky = tk.NE + tk.SW)
        
        self.btnNum1 = tk.Button(self, text = "開始計算", command = self.clickBtnNum1, height = 1, width = 10, bg = "gold", font = f2)
        self.btnNum1.grid(row = 6, column = 0, columnspan = 2, sticky = tk.NE + tk.SW)

        self.btnBack = tk.Button(self, text="回主畫面", height = 1, width = 8,font = f1, fg = "white", bg = "blue",
                    command = lambda: controller.show_frame(StartPage))
        self.btnBack.grid(row = 12, column = 0, sticky = tk.W)

    def clickBtnNum1(self):	
        S = float(self.txtNumList[0].get())
        K = float(self.txtNumList[1].get())
        T = float(self.txtNumList[2].get())
        R = float(self.txtNumList[3].get())
        sigma = float(self.txtNumList[4].get())


        call_ans = euro_vanilla_call(S, K, T, R, sigma)[0]
        call_final_ans = round(call_ans, 2)
        hold_share = round(euro_vanilla_call(S, K, T, R, sigma)[1], 2)
        borrow_price = round(euro_vanilla_call(S, K, T, R, sigma)[2], 2)

        put_ans = euro_vanilla_put(S, K, T, R, sigma)
        put_final_ans = round(put_ans, 2)
                        
        self.ansList[0].delete(0,END)
        self.ansList[0].insert(0, str(call_final_ans))

        self.ansList[1].delete(0,END)
        self.ansList[1].insert(0, str(put_final_ans))



class PageAtt2(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        f1 = tkFont.Font(size = 20, family = "Courier New")
        f2 = tkFont.Font(size = 20, family = "Courier New")

        self.lblNumList = []
        text = ("債券市值計算:", "請輸入公司資產總值:", "請輸入一張債券的面額:", "請輸入總共有幾張債券:",
                "請輸入債券到期期限(Year):", "請輸入無風險資產年利率(ex:0.01):",
                "請輸入股價波動率(ex:0.25)", "答案:", "公司權益總市值:",
                "債券當下市值:", "債券倒帳機率:", "債券總面額:")
        for i in range(12):
            self.lblNumList.append(tk.Label(self, height = 1, width = 45, font = f1))
            self.lblNumList[i]["text"] = text[i]
            self.lblNumList[i].grid(row = i, column = 0, sticky = tk.NE + tk.SW)
        self.lblNumList[0]["bg"] = "firebrick2"
        
        self.txtNumList = []
        for i in range(6):
            self.txtNumList.append(tk.Entry(self, width = 20, font = f1))   
            self.txtNumList[i].grid(row = i+1, column = 1, sticky = tk.NE + tk.SW)

        self.ansList = []
        for i in range(4):
            self.ansList.append(tk.Entry(self, width = 20, font = f1))
            self.ansList[i].grid(row = i+8, column = 1, sticky = tk.NE + tk.SW)

        self.btnNum1 = tk.Button(self, text = "開始計算", command = self.clickBtnNum1, height = 1, width = 10, bg = "gold", font = f2)
        self.btnNum1.grid(row = 7, column = 0, columnspan = 2, sticky = tk.NE + tk.SW)
        
        self.btnBack = tk.Button(self, text="回主畫面", height = 1, width = 8,font = f1, fg = "white", bg = "blue",
                    command = lambda: controller.show_frame(StartPage))
        self.btnBack.grid(row = 13, column = 0, sticky = tk.W)


    def clickBtnNum1(self):
        S2 = float(self.txtNumList[0].get())
        k2 = float(self.txtNumList[1].get())
        n2 = float(self.txtNumList[2].get())
        T2 = float(self.txtNumList[3].get())
        R2 = float(self.txtNumList[4].get())
        sigma2 = float(self.txtNumList[5].get())

        K2 = k2 * n2
        call_ans2 = euro_vanilla_call(S2, K2, T2, R2, sigma2)[0]
        call_final_ans2 = round(call_ans2, 6)
        hold_share2 = round(euro_vanilla_call(S2, K2, T2, R2, sigma2)[1], 6)
        borrow_price2 = round(euro_vanilla_call(S2, K2, T2, R2, sigma2)[2], 6)
        bond_price2 = euro_vanilla_call(S2, K2, T2, R2, sigma2)[3]
        default_prob2 = euro_vanilla_call(S2, K2, T2, R2, sigma2)[4]
                
        self.ansList[0].delete(0,END)
        self.ansList[0].insert(0, str(call_final_ans2))

        self.ansList[1].delete(0,END)
        self.ansList[1].insert(0, str(bond_price2))

        self.ansList[2].delete(0,END)
        self.ansList[2].insert(0, str(default_prob2))

        self.ansList[3].delete(0,END)
        self.ansList[3].insert(0, str(K2))


class PageAtt3(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        f1 = tkFont.Font(size = 20, family = "Courier New")
        f2 = tkFont.Font(size = 20, family = "Courier New")

        self.lblNumList = []
        text = ("權證價格計算:", "公司資產總值:", "權證執行價格:", "權證到期年限(Year):",
                "無風險資產年利率(ex:0.01):", "公司資產波動率(ex:0.25)",
                "公司原本在外流通股數ex(20(shares)):", "所有權證可換得的公司股數: ex(2(shares))",
                "答案:", "稀釋比為:", "一張權證的價格為:", "權證總價格為:")
        for i in range(12):
            self.lblNumList.append(tk.Label(self, height = 1, width = 45, font = f1))
            self.lblNumList[i]["text"] = text[i]
            self.lblNumList[i].grid(row = i, column = 0, sticky = tk.NE + tk.SW)
        self.lblNumList[0]["bg"] = "firebrick2"
        
        self.txtNumList = []
        for i in range(7):
            self.txtNumList.append(tk.Entry(self, width = 20, font = f1))   
            self.txtNumList[i].grid(row = i+1, column = 1, sticky = tk.NE + tk.SW)

        self.ansList = []
        for i in range(3):
            self.ansList.append(tk.Entry(self, width = 20, font = f1))
            self.ansList[i].grid(row = i+9, column = 1, sticky = tk.NE + tk.SW)
        
        self.btnBack = tk.Button(self, text="回主畫面", height = 1, width = 8,font = f1, fg = "white", bg = "blue",
                    command = lambda: controller.show_frame(StartPage))
        self.btnBack.grid(row = 13, column = 0, sticky = tk.W)

        self.btnNum1 = tk.Button(self, text = "開始計算", command = self.clickBtnNum1, height = 1, width = 10, bg = "gold", font = f2)                
        self.btnNum1.grid(row = 8, column = 0, columnspan = 2, sticky = tk.NE + tk.SW)

                        
    def clickBtnNum1(self):	
        S3 = float(self.txtNumList[0].get())
        K3 = float(self.txtNumList[1].get())
        T3 = float(self.txtNumList[2].get())
        R3 = float(self.txtNumList[3].get())
        sigma3 = float(self.txtNumList[4].get())
        n3 = float(self.txtNumList[5].get())
        m3 = float(self.txtNumList[6].get())

        dilution_correction_factor3 = round((n3 / (n3 + m3)), 4)
        call_ans3 = euro_vanilla_call(S3/n3, K3, T3, R3, sigma3)[0]
        call_final_ans3 = round(call_ans3, 4)
        warrant_per_share3 = round(dilution_correction_factor3 * call_final_ans3, 4)
        hold_share3 = round(euro_vanilla_call(S3, K3, T3, R3, sigma3)[1], 4)
        Total_Value_of_Warrent3 = m3 * warrant_per_share3
                
        self.ansList[0].delete(0,END)
        self.ansList[0].insert(0, str(dilution_correction_factor3))

        self.ansList[1].delete(0,END)
        self.ansList[1].insert(0, str(warrant_per_share3))
        
        self.ansList[2].delete(0,END)
        self.ansList[2].insert(0, str(Total_Value_of_Warrent3))


class PageAtt4(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        f1 = tkFont.Font(size = 20, family = "Courier New")
        f2 = tkFont.Font(size = 20, family = "Courier New")


        self.lblNumList = []
        text = ("可轉換公司債價值計算:", "公司資產總值:", "債券到期期限(Year):",
                "無風險資產年利率(ex:0.01):", "公司資產波動率(ex:0.25):", "公司原本在外流通股數: ex(20(shares)):",
                "一張可轉換公司債可換得的公司股數: ex(3.03(shares)):", "總共有幾張可轉換公司債: ex(120(張)):",
                "一張公司債的票面金額: ex(1000):", "答案:", "公司權益總市值:", "每股價值:", "可轉換債券總價值:",
                "每張債券價值:")
        for i in range(14):
            self.lblNumList.append(tk.Label(self, height = 1, width = 55, font = f1))
            self.lblNumList[i]["text"] = text[i]
            self.lblNumList[i].grid(row = i, column = 0, sticky = tk.NE + tk.SW)
        self.lblNumList[0]["bg"] = "firebrick2"
        
        self.txtNumList = []
        for i in range(8):
            self.txtNumList.append(tk.Entry(self, width = 15, font = f1))   
            self.txtNumList[i].grid(row = i+1, column = 1, sticky = tk.NE + tk.SW)

        self.ansList = []
        for i in range(4):
            self.ansList.append(tk.Entry(self, width = 15, font = f1))
            self.ansList[i].grid(row = i+10, column = 1, sticky = tk.NE + tk.SW)
            

        self.btnBack = tk.Button(self, text="回主畫面", height = 1, width = 8,font = f1, fg = "white", bg = "blue",
                    command = lambda: controller.show_frame(StartPage))
        self.btnBack.grid(row = 15, column = 0, sticky = tk.W)

        self.btnNum1 = tk.Button(self, text = "開始計算", command = self.clickBtnNum1, height = 1, width = 10, bg = "gold", font = f2)                
        self.btnNum1.grid(row = 9, column = 0, columnspan = 2, sticky = tk.NE + tk.SW)
        
    def clickBtnNum1(self):	
        S4 = float(self.txtNumList[0].get())
        T4 = float(self.txtNumList[1].get())
        R4 = float(self.txtNumList[2].get())
        sigma4 = float(self.txtNumList[3].get())
        n4 = float(self.txtNumList[4].get())
        m4 = float(self.txtNumList[5].get())
        b4 = float(self.txtNumList[6].get())
        bond_face_value4 = float(self.txtNumList[7].get())

        total_bond_face_value4 = round(bond_face_value4 * b4, 4)
        success_covert_share4 = round(n4 + (b4 * m4), 4)
        covert_ratio4 = round((b4 * m4)/success_covert_share4,4)
        strike_price4 = round(total_bond_face_value4 / covert_ratio4,4)

        call_ans4 = euro_vanilla_call(S4, total_bond_face_value4, T4, R4, sigma4)[0]
        total_equity4 = round(call_ans4, 4)
        total_bond_price4 = S4 - total_equity4
        convert_bond4 = round(euro_vanilla_call_4(S4, strike_price4, T4, R4, sigma4), 4)
        final_covert_bond_price4 = total_bond_price4 + (covert_ratio4 * convert_bond4)
        per_convert_bond4 = round(final_covert_bond_price4/b4 ,4) 
        final_value_of_equity4 = S4 - final_covert_bond_price4
        per_final_price_share4 = round(final_value_of_equity4/n4,4)
                        
        self.ansList[0].delete(0,END)
        self.ansList[0].insert(0, str(final_value_of_equity4))

        self.ansList[1].delete(0,END)
        self.ansList[1].insert(0, str(per_final_price_share4))
        
        self.ansList[2].delete(0,END)
        self.ansList[2].insert(0, str(final_covert_bond_price4))

        self.ansList[3].delete(0,END)
        self.ansList[3].insert(0, str(per_convert_bond4))

#@$%^#@$%^#@$%^#@$%^#@$%^#@$%^#@$%^#@$%^#@$%^#@$%^#@$%^#@$%^#@$%^#@$%^
			
firm_list = []
class PageOne(tk.Frame):

	def __init__(self, parent, controller):
		f = tkFont.Font(size = 36, family = "Courier New")
		tk.Frame.__init__(self, parent)

		self.button1 = tk.Button(self, text="Back to Home", font = f, bg = "gold",
			command=lambda: controller.show_frame(StartPage))
		self.button1.grid(row = 0, column = 0, sticky = tk.NE + tk.SW)
		
		self.button2 = tk.Button(self, text="開始計算", font = f, bg = "gold",
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
app.title("$$$$$$$$$$")
app.mainloop()
