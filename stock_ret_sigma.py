		return_sum_of_square += math.pow( ret, 2)
	
	index +=1

################
	
standard_deviation = math.sqrt( return_sum_of_square - math.pow( return_sum, 2)/price_number) 
print('標準差:', standard_deviation)
print('股價:', price_at_statement_date)
