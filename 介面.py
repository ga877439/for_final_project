import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import *

ratios_list = ["RatioA", "RatioB", "RatioC", "RatioD", "RatioE", "RatioF", "RatioG",
               "RatioH", "RatioI", "RatioJ", "RatioK", "RatioL", "RatioM", "RatioN"]

class Acct(tk.Frame):

    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        f = tkFont.Font(size = 16, family = "Courier New")

        self.lblNum = tk.Label(self, text = "Num", height = 1, width = 5, font = f,fg = "white", bg = "red")
        self.lblSeason = tk.Label(self, text = "Season", height = 1, width = 7, font = f,fg = "white", bg = "orange")
        self.lblSheet = tk.Label(self, text = "Sheet", height = 1, width = 10, font = f,fg = "white", bg = "green")
        self.btnNext = tk.Button(self, text = "下一頁",command = self.printSelected, height = 1, width = 8, font = f, bg = "blue")

        self.lblNum.grid(row = 0, column = 1, sticky = tk.W)
        self.lblSeason.grid(row = 0, column = 2, sticky = tk.E)
        self.lblSheet.grid(row = 0, column = 3, sticky = tk.E)
        self.btnNext.grid(row = 8, column = 5, columnspan = 1, sticky = tk.E)
#################################################column = 0
        self.btnOX1 = tk.Button(self, text = "O", command = self.clickBtnOX1, height = 1, width = 2, font = f, bg = "cyan")
        self.btnOX2 = tk.Button(self, text = "O", command = self.clickBtnOX2, height = 1, width = 2, font = f, bg = "cyan")
        self.btnOX3 = tk.Button(self, text = "O", command = self.clickBtnOX3, height = 1, width = 2, font = f, bg = "cyan")
        self.btnOX4 = tk.Button(self, text = "O", command = self.clickBtnOX4, height = 1, width = 2, font = f, bg = "cyan")
        self.btnOX5 = tk.Button(self, text = "O", command = self.clickBtnOX5, height = 1, width = 2, font = f, bg = "cyan")

        self.btnOX1.grid(row = 3, column = 0)
        self.btnOX2.grid(row = 4, column = 0)
        self.btnOX3.grid(row = 5, column = 0)
        self.btnOX4.grid(row = 6, column = 0)
        self.btnOX5.grid(row = 7, column = 0)
#################################################column = 1
        self.txtNum = []
        for i in range(5):
            self.txtNum.append(tk.Text(self, height = 1, width = 5, font = f))
            self.txtNum[i].grid(row = i+3, column = 1, sticky = tk.W)
#################################################column = 2
        self.seasons = [] # 放107-4 107-3 107-2 ...
        for i in range(107, 95, -1):
            for j in range(4, 0, -1):
                self.seasons.append("%d-%d" % (i, j))
                
        self.comboSeasons = []
        for i in range(5):
            self.comboSeasons.append(ttk.Combobox(self ,width = 6, values = self.seasons, font = f))
            self.comboSeasons[i].current(1)
            self.comboSeasons[i].grid(row = i+3, column = 2)
#################################################column = 3
        self.sheet = ["資產負債表", "綜合損益表", "現金流量表"]
        self.comboSheet = []
        for i in range(5):
            self.comboSheet.append(ttk.Combobox(self ,width = 9, values=self.sheet, font = f))
            self.comboSheet[i].grid(row = i+3, column = 3) 
#################################################column = 4
        self.ratios = Listbox(self, width = 15, height = 8, selectmode = MULTIPLE,
                            fg = "white", bg = 'purple', font = f)
        self.scrollbar = Scrollbar(self, orient = "vertical")
        self.ratios.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.ratios.yview)
        self.ratios.grid(row = 1, column = 4, rowspan = 7, columnspan = 2, sticky = "NEWS")
        self.scrollbar.grid(row = 1, column = 6, rowspan = 7, sticky = N+S)

        for ratio in ratios_list:
            self.ratios.insert(END, ratio)
#################################################function
    def clickBtnOX1(self):
        OorX = self.btnOX1.cget("text")
        self.btnOX1.configure(text = "X") if OorX == "O" else self.btnOX1.configure(text = "O")

    def clickBtnOX2(self):
        OorX = self.btnOX2.cget("text")
        self.btnOX2.configure(text = "X") if OorX == "O" else self.btnOX2.configure(text = "O")
                
    def clickBtnOX3(self):
        OorX = self.btnOX3.cget("text")
        self.btnOX3.configure(text = "X") if OorX == "O" else self.btnOX3.configure(text = "O")
                
    def clickBtnOX4(self):
        OorX = self.btnOX4.cget("text")
        self.btnOX4.configure(text = "X") if OorX == "O" else self.btnOX4.configure(text = "O")
                
    def clickBtnOX5(self):
        OorX = self.btnOX5.cget("text")
        self.btnOX5.configure(text = "X") if OorX == "O" else self.btnOX5.configure(text = "O")

    def printSelected(self):
        self.selected_ratios_list = [self.ratios.get(i) for i in self.ratios.curselection()]
        print(self.selected_ratios_list)

al = Acct()
al.master.title("ACCT")
al.mainloop()
