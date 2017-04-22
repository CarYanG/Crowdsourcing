#--*-- coding:utf-8 --*--
import random
import math

class QualityControl:
    def __init__(self,usernum, workernum,tasknum, tasksteps,threshold):
        self.usernum = usernum  #用户总数

        self.workernum = workernum  #优质工作者集合的人数

        self.currentWork = []  # 当前工作者的集合,初始化之后即表示优质工作者集合

        self.tasknum = tasknum  #任务总数

        self.tasksteps=tasksteps  #每一轮需要完成的任务数

        self.phasenum =(tasknum) / tasksteps   #完成任务一共需要多少轮

        self.userHistoryError={}   #用户的历史错误率字典,key为workerid，value为历史错误率Ea

        self.threshold=threshold #进行替换阶段时用到的的阈值

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

    def initialization (self):# 1.初始化所有成员的历史错误率  2.根据成员的历史错误率，初始化优质工作者集合
        answers=self.getAnswer();
        for i in range(self.usernum):
            self.currentWork.append(i)  # 当前工作者集合即所有工作者
        print ("first choosen user", self.currentWork)

        workerAnswer = {}  # 设计一个字典，用来表示每个被选中的工作者的答案，key为workid，value为工作者本轮的答案(list形式)

        for worker in self.currentWork:
            workerAnswer[worker] = []

        for taskid in range(self.tasknum):  # 选取所有的答案
            for workerid in workerAnswer:
                workerAnswer[workerid].append(answers[workerid][taskid])

        print "initialization worker answer:", workerAnswer
        print "initialization worker list :", workerAnswer.keys()

        workerParam = {}  # 设计一个字典，用来表示所有在工作中的工作者的一些参数（与其他工作者相同答案的个数），
        # 用于计算错误率，key为workid，value为参数值（list形式）,

        for item in range(self.usernum):
            workerParam[item] = [0 for i in range(3)]  # 每个工作者有三个value值,q12,q13,q23
        print "workerParam ", workerParam

        for workerid in workerAnswer:
            print "Now we evaluate worker (initialization)", workerid
            othercurrent = []
            for item in self.currentWork:
                othercurrent.append(item)
            othercurrent.remove(workerid)
            print "othercurrent", othercurrent
            otherOne = othercurrent[random.randint(0, len(othercurrent) - 1)]
            otherTwo = othercurrent[random.randint(0, len(othercurrent) - 1)]
            print "we compare ", workerid, " with ", otherOne, " and ", otherTwo
            workerParam[workerid][0] = workerParam[workerid][0] + self.countAgree(workerAnswer[workerid],workerAnswer[otherOne])
            workerParam[workerid][1] = workerParam[workerid][1] + self.countAgree(workerAnswer[workerid],workerAnswer[otherTwo])
            workerParam[workerid][2] = workerParam[workerid][2] + self.countAgree(workerAnswer[otherOne],workerAnswer[otherTwo])

            # 计算错误率
            arg1 = workerParam[workerid][0] / (float)(self.tasknum)
            arg2 = workerParam[workerid][1] / (float)(self.tasknum)
            arg3 = workerParam[workerid][2] / (float)(self.tasknum)
            print "args about ", workerid, " (q12,q13,q23):"
            print workerid, "  his Workparam", workerParam[workerid][0], workerParam[1], workerParam[2]
            error = self.countError(arg1, arg2, arg3)
            print "initialization HistoryError(Ea) about ", workerid, " is ", error
            self.userHistoryError[workerid]=error

        sorted(self.userHistoryError.items(), key=lambda item: item[1], reverse=False) #False是升序
        此处要修改，因为字典并没有改变
        print "initialization userHistoryError ", self.userHistoryError

        self.currentWork=[]
        for item in range (self.workernum):
            self.currentWork.append(self.userHistoryError.keys(item))
        print "initialization completed"



    def selectTask(self,turn):
        taskList=[]
        for i in range((turn-1)*self.tasksteps,(turn-1)*self.tasksteps+self.tasksteps):    #turn从1开始计算
            taskList.append(i)
        return taskList

    def substituteWorker(self,workid,badworker):         #替换某轮错误率Eb较高的工作者，从剩余工作者集合中选取历史错误Ea率较低的用户
        restWorkerError={}  #复制剩余工作者的历史错误率集
        for item in self.userHistoryError:
            if (item not in self.currentWork) and (item not in badworker) :
                restWorkerError[item]=self.userHistoryError[item]

        print "restWorkers and their userHistoryError: "
        for item in restWorkerError:
            print item,"--->",restWorkerError[item]

        #在有剩余工作者的情况下
        if(len(restWorkerError)!=0):
            minError =sorted(restWorkerError.values())[0]   #找到剩余工作者中历史错误率的最小值
            for item in restWorkerError:                   #找到拥有最小历史错误率的workid，并进行替换【这段代码可以简单一点】
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
        voteResult={1:0,0:0}  #作为投票的结果,投票时以历史正确率作为权重
        for workerid in workerAnswer:
            if workerAnswer[workerid][i] !=-1:
                if workerAnswer[workerid][i] not in voteResult:
                    voteResult[workerAnswer[workerid][i]]=1
                else:
                    voteResult[workerAnswer[workerid][i]]+=(1-self.userHistoryError[workerid])
        return max(voteResult.items(),key=lambda x:x [1])[0]

    def process(self):
        answers=self.getAnswer()
        golden=self.getGolden()
        #计算初始历史错误率Ea
        self.initialization()

        workerParam={} #设计一个字典，用来表示所有在工作中的工作者的一些参数（与其他工作者相同答案的个数），用于计算错误率，key为workid，value为参数值（list形式）,
                        # 这里要改，因为每一次迭代workerParam就清空了，应该有之前的记录，如果某个工作者从未工作过，那么他的三个value值都为0
                        # 引入历史错误率之后，workerParam可以尝试每轮清空
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

            workerEb={} #优质工作者集合在本轮中的错误率Eb，key为workid，value为工作者的答案
            badworker=[]#标记作为次轮要被替换出去的工作者

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
                errorb=self.countError(arg1,arg2,arg3)
                print self.tasksteps
                print "we have done ",self.tasksteps * i,"  tasks"
                print workerid,"  his Workparam",workerParam[workerid][0],workerParam[1],workerParam[2]
                print "error(Eb) about ",workerid," is ",errorb


                #更新历史错误率  （已经完成的任务*目前的历史错误率+此次完成的任务数*此次的错误率Eb）/(已经完成的任务+此次完成的任务数)
                olduserHistoryError=self.userHistoryError[workerid];
                print "old userHistoryError about ", workerid, " is ", olduserHistoryError
                self.userHistoryError[workerid]=(olduserHistoryError*(self.tasknum+self.tasksteps*(i-1)) +errorb*self.tasksteps)/((self.tasksteps)*(i)+self.tasknum)
                print "New userHistoryError about ", workerid, " is ",self.userHistoryError[workerid]
                workerEb[workerid]=errorb;



            #需要替换的人数
            badworkerNumber=(int)(self.workernum*0.3)
            sorted(workerEb.items(),key=lambda item:item[1],reverse=True) #False是升序
            此处要修改，因为字典并没有改变
            print workerEb;
            for item in range(badworkerNumber):
                workerAnswer[workerEb.keys(item)] = [-1 for m in range(self.tasksteps)]  # 将这个被替换出去的工作者的答案设为-1，即空答案
                badworker.append(workerid)
                print workerEb.keys(item), "has been into badworker list,and his answer has become :", workerAnswer[workerEb.keys(item)]

            #统计正确答案的个数，不包含被替代工作者的成绩
            for taskid in selectedTask:
                if golden[taskid]==self.vote(workerAnswer,selectedTask.index(taskid)):
                    count=count+1


            #开始进行替换,标记之后统一替换,替换过程中要注意被替换出去的，此轮不能再被替换进来
            for workerid in badworker:
                print "someone is substituted of the current worker team ", workerid
                self.substituteWorker(workerid,badworker)

        print "let us see our worker's history error rate:"
        print self.userHistoryError
        print "the final result:"
        print (float)(count)/self.tasknum


test=QualityControl(19,3,48,8,0.2)
test.process()



