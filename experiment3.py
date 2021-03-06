#--*-- coding:utf-8 --*--
import random
import math

class QualityControl:
    def __init__(self,usernum, workernum,tasknum, tasksteps,threshold1,threshold2):
        self.usernum = usernum  #用户总数

        self.workernum = workernum  #淘汰阶段之后，稳定下来的维持保有的用户数

        self.tasknum = tasknum  #任务总数`

        self.tasksteps=tasksteps  #每一轮需要完成的任务数

        self.phasenum =(tasknum) / tasksteps   #完成任务一共需要多少轮

        self.userError={}   #用户的错误率字典，初始每个用户的错误率都是1,key为workerid，value为错误率

        for i in range(self.usernum):
            self.userError[i]=1.0  #设置初始错误率

        self.currentWork=[] #当前工作者的集合

        self.threshold1=threshold1 #第一阶段错误率的阈值，即从全部工作者淘汰时用到的阈值（此时不进行替换），只进行淘汰

        self.threshold2=threshold2 #第二阶段错误率的阈值，即进行替换阶段时用到的的阈值

    def getAnswer(self):  #获取用户答案 一个二维列表，每一行是一个用户的所有答案
         file = open("data/ic_data")
         try:
             content = file.readlines()
         finally:
            file.close()

         allAnswer=[]
         for item in content:
             lists = item.strip("\n").split(" ")
             # lists = item.strip("\n").split(", ")
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

    def selectWorker(self):  #刚开始我们选择所有All的工作者作为初始工作者集合，
                              # 在随后的每一轮工作中，逐步淘汰掉错误率高的工作者，直到工作者集合的大小达到我们想要的值。
        alllist=[]  #模拟全部工作者集合
        for i in range(self.usernum):
            alllist.append(i)
        print ("all the user ",alllist)
        # selectList = random.sample(alist, self.workernum) #从全部工作者中选取worker来进行本轮的工作，个数为workernum

        for item in alllist :
            self.currentWork.append(item)    #当前工作者集合即所有工作者

        print ("first choosen user",self.currentWork )


    def selectTask(self,turn):
        taskList=[]
        for i in range((turn-1)*self.tasksteps,(turn-1)*self.tasksteps+self.tasksteps):    #turn从1开始计算
            taskList.append(i)
        return taskList

    def substituteWorker(self,workid):         #替换错误率较高的工作者，从剩余工作者集合中选取错误率较低的用户
        restWorkerError={}  #模拟剩余工作者的错误率集
        for item in self.userError:
            if item not in self.currentWork:
                restWorkerError[item]=self.userError[item]

        print "restWorkers and their userError: "
        for item in restWorkerError:
            print item,"--->",restWorkerError[item]

        #在有剩余工作者的情况下
        if(len(restWorkerError)!=0):
            minError =sorted(restWorkerError.values())[0]   #找到剩余工作者中错误率的最小值
            for item in restWorkerError:                   #找到拥有最小错误率的workid，并进行替换【这段代码可以简单一点】
                if restWorkerError[item]==minError:
                    self.currentWork.remove(workid)
                    self.currentWork.append(item)
                    print "we choose ", item, "from restWorker to substitute"
                    break


    def countAgree(self,list1,list2):  #统计两个用户本轮所提交相同答案的个数
        count=0
        for i in range (self.tasksteps):
            if list1[i]==list2[i]:
                count+=1
        return count

    def countError(self,q12,q13,q23):  #计算用户的错误率
        print q12,q13,q23
        if(q23==0.5):
            q23=0.5001

        if(((q12-0.5)*(q13-0.5))/ (2*(q23-0.5))<0):
            print "ohmygod"
            return 0.5
        else:
            if (0.5-math.sqrt(((q12-0.5)*(q13-0.5))/ (2*(q23-0.5))) )<0:
                return 0
            else:
                return 0.5-math.sqrt(((q12-0.5)*(q13-0.5))/ (2*(q23-0.5)))

    def vote(self,workerAnswer,i):
        voteResult={1:0,0:0}  #作为投票的结果,投票时以正确率作为权重
        for workerid in workerAnswer:
            if workerAnswer[workerid][i] !=-1:
                if workerAnswer[workerid][i] not in voteResult:
                    voteResult[workerAnswer[workerid][i]]=1
                else:
                    voteResult[workerAnswer[workerid][i]]+=(1-self.userError[workerid])
        return max(voteResult.items(),key=lambda x:x [1])[0]

    def process(self):
        answers=self.getAnswer()
        golden=self.getGolden()
        self.selectWorker()


        workerParam={} #设计一个字典，用来表示所有在工作中的工作者的一些参数（与其他工作者相同答案的个数），用于计算错误率，key为workid，value为参数值（list形式）,
                        # 这里要改，因为每一次迭代workerParam就清空了，应该有之前的记录，如果某个工作者从未工作过，那么他的三个value值都为0
        for item in range(self.usernum):
            workerParam[item]=[0 for i in range(3)]   #每个工作者有三个value值,q12,q13,q23
        print "workerParam ",workerParam


        count=0.0
        for i in range(1,self.phasenum+1):
            print i," turn start ************************************************************"
            selectedTask=self.selectTask(i)
            print ("selectedtask",selectedTask)
            workerAnswer={}  #设计一个字典，用来表示每个被选中的工作者的答案，key为workid，value为工作者本轮的答案(list形式)
                            # 每一轮开始前，WorkerAnswer即被清空
            for item in self.currentWork:
                workerAnswer[item]=[]

            for taskid in selectedTask:        #从所有答案中截取本轮测试需要的答案
                for workerid in workerAnswer:
                    workerAnswer[workerid].append(answers[workerid][taskid])

            print "current worker answer:",workerAnswer
            print "current worker list :",workerAnswer.keys()

            awfulworker = []  # 标记作为此轮要被淘汰出去的工作者
            badworker=[]     #标记作为次轮要被替换出去的工作者

            for workerid in workerAnswer: #当多个工作者的时候，这里暂且选择随即选取的方式作为S和T,还得再改
                print "*"
                print "Now we evaluate worker", workerid
                othercurrent=[]
                for item in self.currentWork:
                    othercurrent.append(item)
                othercurrent.remove(workerid)
                print "othercurrent",othercurrent

                otherOne=othercurrent[random.randint(0,len(othercurrent)-1)]
                otherTwo=othercurrent[random.randint(0,len(othercurrent)-1)]
                print "we compare ",workerid," with ",otherOne," and ",otherTwo
                workerParam[workerid][0]=workerParam[workerid][0]+self.countAgree(workerAnswer[workerid],workerAnswer[otherOne])
                workerParam[workerid][1]=workerParam[workerid][1]+self.countAgree(workerAnswer[workerid],workerAnswer[otherTwo])
                workerParam[workerid][2]=workerParam[workerid][2]+self.countAgree(workerAnswer[otherOne],workerAnswer[otherTwo])

                #计算错误率
                arg1=workerParam[workerid][0]/(float)((self.tasksteps)*(i))
                arg2=workerParam[workerid][1]/(float)((self.tasksteps)*(i))
                arg3=workerParam[workerid][2]/(float)((self.tasksteps)*(i))
                print "args about ",workerid," (q12,q13,q23):"
                error=self.countError(arg1,arg2,arg3)
                print self.tasksteps
                print "fuck  ",i
                print "we have done ",self.tasksteps * i,"  tasks"
                print workerid,"  his Workparam",workerParam[workerid][0],workerParam[1],workerParam[2]
                print "error about ",workerid," ",error


                #更新错误率
                self.userError[workerid]=error


                if (len(self.currentWork)-len(awfulworker)>self.workernum):  #此时还处于第一阶段，应当进行淘汰，并不替换
                    if error >= self.threshold1:        #错误率太大需要淘汰掉，同时将此人的答案剔除出去（或者标记为-1）
                        workerAnswer[workerid] = [-1 for m in range(self.tasksteps)]
                        awfulworker.append(workerid)
                        print workerid, "has been into awfulworker list, and his answer has become :",workerAnswer[workerid]
                else:
                    if error>=self.threshold2:                      #此时处于第二阶段，即替换阶段
                        #del workerAnswer[workerid]   #这一句会引起bug，在workerAnswer中循环却又改变workerAnswer的大小
                        workerAnswer[workerid]=[-1 for m in range(self.tasksteps) ]        #将这个被替换出去的工作者的答案设为-1，即空答案
                        badworker.append(workerid)
                        print workerid,"has been into badworker list,and his answer has become :",workerAnswer[workerid]


            #统计正确答案的个数，不包含被淘汰工作者的成绩
            for taskid in selectedTask:
                if golden[taskid]==self.vote(workerAnswer,selectedTask.index(taskid)):
                    count=count+1

            #开始进行淘汰
            for workerid in awfulworker:
                print "someone is out of the current worker team ", workerid
                self.currentWork.remove(workerid);
            #开始进行替换
            for workerid in badworker:
                print "someone is substituted of the current worker team ", workerid
                self.substituteWorker(workerid)



        print "let us see our worker's error rate:"
        print self.userError
        print "the final result:"
        print (float)(count)/self.tasknum


test=QualityControl(19,3,48,8,0.2,0.1)
# def __init__(self,usernum, workernum,tasknum, tasksteps,threshold1,threshold2):
test.process()



