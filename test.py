__author__ = 'carl'
#--*-- coding:utf-8 --*--
import random


a = [ [1,2,3], ["a","c","b"], [4,5,6], [7,8,9], ["e","f","g"]]

print a
print map(list, zip(*a))

b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
slice = random.sample(b, 5) #从list中随机获取5个元素，作为一个片断返回
print slice
print b #原有序列并没有改变。


def selectTask(tasksteps,turn):
        taskList=[]
        for i in range((turn-1)*tasksteps,(turn-1)*tasksteps+tasksteps):
            taskList.append(i)
        return taskList

c=selectTask(5,2)
print c


d=[1,2,3,4,5,6,3.5,2.5,1.5]
sorted(d)[0]
print sorted(d)[len(d)-1]
print d


userError={}

userError[1]=12
userError[2]=11


print sorted(userError.values())[0]


print "----------------我是一条分割线------------------"

a=[1,2,3,4,56,7]
print a
a.remove(7)
print a


for i in range(10):
    if i==2:
        print "hahahahahahah"
        break
    else:
        print "adsa"


workerAnswer=[[] for i in range(4)]
print workerAnswer