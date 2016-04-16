#--*-- coding:utf-8 --*--
import random
import math

class QualityControl:
    def __init__(self,usernum, workernum,tasknum, tasksteps,threshold):
        self.usernum=usernum  #用户总数

        self.workernum=workernum  #每一轮工作的用户数(工作者)

        self.tasknum=tasknum  #任务总数`

        self.tasksteps=tasksteps  #每一轮需要完成的任务数

        self.phasenum =(tasknum) / tasksteps   #完成任务一共需要多少轮

        self.userError={}   #用户的错误率字典，初始每个用户的错误率都是1,key为workerid，value为错误率

        for i in range(self.usernum):
            self.userError[i]=1.0

        self.currentWork=[] #当前工作者的集合

        self.threshold=threshold #错误率的阈值

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
            content = file.readlines()
        finally:
            file.close()
        allGolden=[]
        for item in content:
            lists = item.strip("\n")
            allGolden.append(lists)
        return  allGolden

    def selectWorker(self):  #选出初始工作者集合
        alist=[]  #模拟全部工作者集合
        for i in range(self.usernum):
            alist.append(i)
        print ("all the user ",alist)
        selectList = random.sample(alist, self.workernum) #从全部工作者中选取worker来进行本轮的工作，个数为workernum

        for item in selectList :
            self.currentWork.append(item)    #更新当前工作者集合

        print ("first choosen user",self.currentWork )


    def selectTask(self,turn):
        taskList=[]
        for i in range((turn-1)*self.tasksteps,(turn-1)*self.tasksteps+self.tasksteps):    #turn从1开始计算？
            taskList.append(i)
        return taskList

    def substituteWorker(self,workid):              #替换错误率较高的工作者，从剩余工作者集合中选取错误率较低的用户
        restlist={}  #模拟剩余工作者的错误率集
        for item in self.userError:
            if item not in self.currentWork:
                restlist[item]=self.userError[item]

        minError =sorted(restlist.values())[0]   #找到错误率的最小值
        for item in restlist:                   #找到拥有最小错误率的workid，并进行替换【这段代码可以简单一点】
            if restlist[item]==minError:
                self.currentWork.remove(workid)
                self.currentWork.append(item)
                print "we choose a "
                break


    def countAgree(self,list1,list2):  #统计两个用户本轮所提交相同答案的个数
        count=0
        for i in range (self.tasksteps):
            if list1[i]==list2[i]:
                count+=1
        return count

    def countError(self,q12,q13,q23):  #计算用户的错误率
        return 0.5-math.sqrt(((q12-0.5)*(q13-0.5))/ (2*(q23-0.5)))

    def vote(self,workerAnswer,i):
        voteResult={}  #作为投票的结果,投票时以正确率作为权重
        for item in workerAnswer:
            if workerAnswer[item][i] !=-1:
                if workerAnswer[item][i] not in voteResult:
                    voteResult[workerAnswer[item][i]]=1
                else:
                    voteResult[workerAnswer[item][i]]+=(1-self.userError[item])
        return max(voteResult.items(),key=lambda x:x [1])[0]

    def process(self):
        answers=self.getAnswer()
        golden=self.getGolden()
        self.selectWorker()


        workerParam={} #设计一个字典，用来表示每个被选中的工作者的一些参数（与其他工作者相同答案的个数），用于计算错误率，key为workid，value为参数值（list形式）,
        # 这里要改，因为每一次迭代worker就清空了，应该有之前的记录
        for item in self.currentWork:
            workerParam[item]=[0 for i in range(3)]
        print "workerParam ",workerParam


        count=0.0
        for i in range(1,self.phasenum):
            print i," turn start ************************************************************"
            selectedTask=self.selectTask(i)
            print ("selectedtask",selectedTask)
            workerAnswer={}  #设计一个字典，用来表示每个被选中的工作者的答案，key为workid，value为工作者本轮的答案(list形式)
            for item in self.currentWork:
                workerAnswer[item]=[]

            for taskid in selectedTask:        #从所有答案中截取本轮测试需要的答案
                for workerid in workerAnswer:
                    workerAnswer[workerid].append(answers[workerid][taskid])

            print workerAnswer


            for workerid in workerAnswer: #当多个工作者的时候，这里暂且选择随即选取的方式作为S和T,还得再改
                print "Now we evaluate worker", workerid
                othercurrent=[]
                for item in self.currentWork:
                    othercurrent.append(item)
                othercurrent.remove(workerid)
                print "othercurrent",othercurrent

                workerParam[workerid][0]=workerParam[workerid][0]+self.countAgree(workerAnswer[workerid],workerAnswer[othercurrent[random.randint(0,len(othercurrent)-1)]])
                workerParam[workerid][1]=workerParam[workerid][1]+self.countAgree(workerAnswer[workerid],workerAnswer[othercurrent[random.randint(0,len(othercurrent)-1)]])
                workerParam[workerid][2]=workerParam[workerid][2]+self.countAgree(workerAnswer[othercurrent[random.randint(0,len(othercurrent)-1)]],workerAnswer[othercurrent[random.randint(0,len(othercurrent)-1)]])

                #计算错误率

                error=self.countError(workerParam[workerid][0]/(float)(self.tasksteps),workerParam[workerid][1]/(float)(self.tasksteps),workerParam[workerid][2]/(float)(self.tasksteps))

                #更新错误率
                self.userError[workerid]=error

                #错误率太大需要替换，同时将此人的答案剔除出去（或者标记为false）
                if error>self.threshold:
                    print "someone is out of the current worker team ", workerid
                    #del workerAnswer[workerid]   #这一句会引起bug，在workerAnswer中循环却又改变workerAnswer的大小
                    workerAnswer[workerid]=-1
                    self.substituteWorker(workerid)

            #统计正确答案的个数
            for taskid in selectedTask:
                if golden[taskid]==self.vote(workerAnswer,selectedTask.index(taskid)):
                    count=count+1

        print "let us see our worker's error rate:"
        print self.userError
        print "the final result:"
        print (float)(count)/self.tasknum


test=QualityControl(19,5,48,6,0.1)
test.process()



