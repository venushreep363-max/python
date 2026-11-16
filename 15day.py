# import time
# print('rama')
# time.sleep(3)
# print('seetha')
# time.sleep(3)

# import sys
# lst=[1,2,23,55]
# p=sys.getsizeof(lst)
# print(p)



import sys
tup=(1,2,23,55)
p=sys.getsizeof(tup)
print(p)

val='rama is going to school'
vowels='aeiou'
for x in val:
    if x in vowels:
        print(x)



txt='my name is venu'
vowels='aeiou'
count=0
for  x in txt:
    if x in vowels:
        count+=1
print('total count=',count)



name='arjun' 
marks=67
print(f"my name is {name} and my  marks are {marks} ")

name='venu'
marks=90
print('my name is{}and my marks{}'.format(name,marks))

print(len('python'))

print(min(10,30,59))