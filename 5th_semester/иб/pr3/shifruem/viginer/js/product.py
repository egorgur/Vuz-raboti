from datetime import datetime
from itertools import product
с = "КАПП"
a = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯАBCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
counter = 0
r = ""
t = datetime.now()
for k in product (a, repeat=4):
	for i in k:
		r += a[(a.find(с[counter]) + a.find(i)) % len(a)]
		counter = (counter + 1) % len(k)
	r = ""
	counter = 0
print(datetime.now() - t)