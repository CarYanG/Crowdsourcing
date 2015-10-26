#--*-- coding:utf-8 --*--
__author__ = 'carl'
import random
import math

class QualityControl:
    def __init__(self,usernum,tasknum, workernum, tasksteps):
        self.usernum=usernum  #用户总数

        self.workernum=workernum  #每一轮工作的用户数(工作者)

        self.tasknum=tasknum  #任务总数

        self.tasksteps=tasksteps  #每一轮需要完成的任务数

        self.phasenum =(float)(tasknum) / tasksteps   #完成任务一共需要多少轮

        self.userError={}   #用户的错误率字典，初始每个用户的错误率都是1,key为workerid，value为错误率

        for i in range(self.usernum):
            self.userError[i]=1.0

        self.currentWork=[] #当前工作者的集合

    def getAnswer(self):  #获取用户答案 一个二维列表，每一行是一个用户的所有答案
         file = open("data/ic_data")
         try:
             content = file.readlines()
         finally:
            file.close()

         allAnswer=[]
         for item in content:
             lists = item.strip("\n").split(" ")
             allAnswer.append(lists)

         return  map(list,zip(*allAnswer))

    def getGolden(self):  #获取标准答案
        file =open ("data/ic_data_golden")
        try:
            allGolden = file.readlines()
        finally:
            file.close()
        return  allGolden

    def selectWorker(self):  #选出初始工作者集合
        alist=[]  #模拟全部工作者集合
        for i in range(self.usernum):
            alist.extend(i)
            print alist
        selectList = random.sample(alist, self.workernum) #从全部工作者中选取worker来进行本轮的工作，个数为workernum

        for item in selectList :
            self.currentWork.append(item)    #更新当前工作者集合


    def selectTask(self,turn):
        taskList=[]
        for i in range((turn-1)*self.tasksteps,(turn-1)*self.tasksteps+self.tasksteps):
            taskList.append(i)
        return taskList


    def substituteWorker(self,workid):              #替换错误率较高的工作者，从剩余工作者集合中选取错误率较低的用户
        restlist={}  #模拟剩余工作者的错误率集
        for item in self.userError:
            if item not in self.currentWork:
                restlist[item]=self.currentWork[item]

        minError =sorted(restlist.values())[0]   #找到错误率的最小值
        for item in restlist:                   #找到拥有最小错误率的workid，并进行替换
            if restlist[item]==minError:
                self.currentWork.remove(workid)
                self.currentWork.append(item)
                break


    def countAgree(self,list1,list2):  #统计两个用户本轮所提交相同答案的个数
        count=0
        for i in range (self.phasenum):
            if list1[i]==list2[i]:
                count+=1
        return count

    def countError(self,q12,q13,q23):  #计算用户的错误率
        return 0.5-math.sqrt(((q12-0.5)*(q13-0.5))/ (2*(q23-0.5)))


    def process(self):
        for i in range(self.phasenum):
            selectedTask=self.selectTask(i)
            self.selectWorker()

            answers=self.getAnswer()
            golden=self.getGolden()

            workerAnswer={}  #设计一个字典，用来表示每个被选中的工作者的答案，key为workid，value为工作者本轮的答案(list形式)
            for item in self.currentWork:
                workerAnswer[item]=[]

            for taskid in selectedTask:        #从所有答案中截取测试需要的答案
                for workerid in workerAnswer:
                    workerAnswer[workerid].append(answers[workerid][taskid])


            workerParam={} #设计一个字典，用来表示每个被选中的工作者的一些参数，用于计算错误率，key为workid，value为参数值（list形式）
            for item in self.currentWork:
                workerParam[item]=[]

            for workerid in workerParam: #我们第一次测试先三个人的情况
                current=self.currentWork
                current.remove(workerid)
                workerParam[workerid].append(self.countAgree(workerAnswer[workerid],workerAnswer[current[0]])/float(self.tasksteps))
                workerParam[workerid].append(self.countAgree(workerAnswer[workerid],workerAnswer[current[1]])/float(self.tasksteps))
                workerParam[workerid].append(self.countAgree(workerAnswer[current[0]],workerAnswer[current[1]])/float(self.tasksteps))

                workerid.

def getAnswer():  #获取用户答案 一个二维列表，每一行是一个用户的所有答案
    file = open("data/ic_data")
    try:
        content = file.readlines()
    finally:
        file.close()

    allAnswer=[]
    for item in content:
        lists = item.strip("\n").split(" ")
        allAnswer.append(lists)

    return  map(list,zip(*allAnswer))


a=getAnswer()
print type(a)
print a[1][4]






