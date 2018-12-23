import requests
from bs4 import BeautifulSoup
import math  

def get_stock_prices(year, season, stock_number) :
#爬取目標網站
	year = int(year)
	season =  int(season) 
	stock_number= str(stock_number)
	if season == 2 or season == 3:
		start_date = '%d/%02d/30' %(year-1, season*3)
		end_date = '%d/%02d/30' %(year, season*3)
	else:
		start_date = '%d/%02d/31' %(year-1, season*3)
		end_date = '%d/%02d/31' %(year, season*3)
	
	url = 'http://www.cnyes.com/twstock/ps_historyprice/' + stock_number +'.htm' ;
	form_data = {
    "ctl00$ContentPlaceHolder1$startText":start_date ,
   	"ctl00$ContentPlaceHolder1$endText": end_date,

	}

	r = requests.post(url,form_data)
	r.encoding = 'unicode'
	

	return r

	
######################################3
r = get_stock_prices(2015,2,2330)

soup = BeautifulSoup(r.text, 'lxml')
list = soup.find_all('td')
###################################

index = 0
return_sum = return_sum_of_square = 0
price_number = -1
ret = price = next_price = 0

price_at_statement_date = 0
for item in list:

	if index%10 == 4:
		try:
			price = float(item.text)
		except:
			break
		
		price_number += 1
		
		if index != 4:
			ret = (next_price - price)/price
		else:
			price_at_statement_date = price
			
		next_price = price
		return_sum += ret
		return_sum_of_square += math.pow( ret, 2)
	
	index +=1

################
	
standard_deviation = math.sqrt( return_sum_of_square - math.pow( return_sum, 2)/price_number) 
print('標準差:', standard_deviation)
print('股價:', price_at_statement_date)
