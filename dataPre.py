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

#print len(a)

for i in range(25,40) :
    c=c&set(a[i])

print c


print "-----------i am a line ------------------"
def getGolden():  #获取标准答案
        file =open ("data/data_2_golden")
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


b=[0, 1, 2, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30, 31, 32, 33, 35, 36, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
print len(b)
for i in  range(102):
    if i in b:
        print a[i]

print "-----------i am a line 2  ------------------"

def getAnswer2():  #获取用户答案
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

         for i in range(25,41):
             answers[i]={}

         dddd=[0, 1, 2, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30, 31, 32, 33, 35, 36, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]

         print len(allAnswer)
         #bbbb=set(allAnswer)
         #print len(bbbb)
         print type(allAnswer)


         for i in range(25,41):
             haha={}
             for item in allAnswer:
                 if int(item[0]) ==i:
                     if int(item[1]) in dddd:
                         haha[int(item[1])]=int(item[2])

             answers[i]=haha




         commonList=[]
         for item in answers:
             commonList.append(set(answers[item]))

         return answers

a=getAnswer2()
for item in a:
    print a[item]
print len(a)
print len(a[item])
print a.keys()
print "-----------i am a line 3  ------------------"

aaaa=[]
for item in a:
    aaaa.append(a[item].values())

ccc= map(list,zip(*aaaa))
for item in ccc:
    print item