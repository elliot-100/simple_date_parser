from parse_date import parse_date

print(parse_date.parse_date('15/06/1978'))
print(parse_date.parse_date('15-6-78'))
print(parse_date.parse_date('5.6.78'))
print(parse_date.parse_date('05-06-78', yy_leniency=1))
print(parse_date.parse_date('05-06-78', yy_leniency=2))
