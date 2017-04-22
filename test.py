#--*-- coding:utf-8 --*--
import random
import math

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

a=random.randint(0,10)
print a

print "----------------我是一条分割线------------------"

userError={}

userError[1]=12
userError[2]=11

print userError.items()
print min(userError.items(),key=lambda x:x[1])[0]

print len(userError)



print "----------------我是一条分割线20160416------------------"
print "对的" if 1==0 else "错的"
badworker=[]
for workerid in badworker:
    print "someone is out of the current worker team ", workerid

voteResult={1:0,0:0}
print max(voteResult.items(),key=lambda x:x [1])[0]

print math.sqrt(0.28125)

for item in range(1,7):
    print item

test=[1,2,3,4]
print test
test=[-1 for m in range(5)]
print test


print "***************"
c={"aa":11,"bb":22,"dd":44,"cc":33}
sorted(c.items(), key=lambda item : item[1],reverse=True)  #False是升序
for item in c:
    print c[item]