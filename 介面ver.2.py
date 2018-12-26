import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import *

#放ratios的名稱
ratios_list = ["RatioA", "RatioB", "RatioC", "RatioD", "RatioE", "RatioF", "RatioG",
               "RatioH", "RatioI", "RatioJ", "RatioK", "RatioL", "RatioM", "RatioN"]


class Acct(tk.Frame):
    """
    每個widget都放在list裡 分別為self.btnOXs, self.enterNums,
    self.comboSeasons,self.comboSheets, self.listboxRatios (self.物件名 + 標題名 + s)
    """
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        f = tkFont.Font(size = 16, family = "Courier New")

        self.lblNum = tk.Label(self, text = "Num", height = 1, width = 5, font = f,fg = "white", bg = "red")
        self.lblSeason = tk.Label(self, text = "Season", height = 1, width = 7, font = f,fg = "white", bg = "orange")
        self.lblSheet = tk.Label(self, text = "Sheet", height = 1, width = 10, font = f,fg = "white", bg = "green")
        self.lblRatio = tk.Label(self, text = "Ratio", height = 1, width = 15, font = f,fg = "white", bg = "blue")
        self.btnNext = tk.Button(self, text = "執行",command = self.getRatioValue,
                                 height = 1, width = 8, font = f,fg = "white",  bg = "black")

        self.lblNum.grid(row = 0, column = 1, sticky = tk.W)
        self.lblSeason.grid(row = 0, column = 2, sticky = tk.E)
        self.lblSheet.grid(row = 0, column = 3, sticky = tk.E)
        self.lblRatio.grid(row = 0, column = 4, columnspan = 2)
        self.btnNext.grid(row = 8, column = 5, columnspan = 1, sticky = tk.E)
#################################################column = 0 self.btnOXs
        self.btnOXs = []
        for i in range(5):
            self.btnOXs.append(tk.Button(self, text = "O",
                                         height = 1, width = 2, font = f, bg = "cyan"))
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
        self.sheet = ["資產負債表", "綜合損益表", "現金流量表"]
        self.comboSheets = []
        for i in range(5):
            self.comboSheets.append(ttk.Combobox(self ,width = 9, values=self.sheet, font = f))
            self.comboSheets[i].grid(row = i+3, column = 3) 
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
        for i in self.btnOXs:
            print(i.cget("text"))

    def getNumValue(self): # 取值
        for i in self.enterNums:
            print(i.get())
    
    def getSeasonValue(self): # 取值
        for i in self.comboSeasons:
            print(i.get())

    def getSheetValue(self): # 取值
        for i in self.comboSheets:
            print(i.get())

    def getRatioValue(self): # 取值
        for i in self.listboxRatios.curselection():
            print(self.listboxRatios.get(i))

al = Acct()
al.master.title("ACCT")
al.mainloop()
