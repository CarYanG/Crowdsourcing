#-*-coding:utf-8 -*-
__author__ = 'carl'

def getAnswer():  #获取用户答案
         file = open("data/data_2")
         try:
             content = file.readlines()
         finally:
            file.close()

         allAnswer=[]
         for item in content:
             lists = item.strip("\n").split("\t")
             allAnswer.append(lists)

         answers={}

         for i in range(42):
             answers[i]=[]


         for item in allAnswer:
             if int(item[0]) in answers.keys():
                 answers[int(item[0])].append(int(item[1]))

         commonList=[]
         for item in answers:
             commonList.append(set(answers[item]))

         return commonList

a=getAnswer()
b=[]
for item in range(102):
    b.append(item)
c=set(b)

print len(a)

for i in range(25,40) :
    c=c&set(a[i])

print c


print "-----------i am a line ------------------"
def getGolden():  #获取标准答案
        file =open ("data/ic_data_golden")
        try:
            content = file.readlines()
        finally:
            file.close()
        allGolden=[]
        for item in content:
            lists = item.strip("\n")
            allGolden.append(int(lists))
        return  allGolden

a=getGolden()

print a
print type(a[0])
print a[0]==1
print len(a)


b=[0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 24, 25, 26, 28, 29, 31, 33, 34, 35, 36, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
print len(b)
for i in  range(60):
    if i in b:
        print a[i]



