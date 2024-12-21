import sys
sys.set_int_max_str_digits(100000)

f1 = 0
f2 = 1
print(f1)
print(f2)
for i in range(1000000):
    f3 = f1+f2
    f1 = f2
    f2 = f3

    
print(f3, file=open('text.txt', 'w'))
