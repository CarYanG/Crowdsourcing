#--*-- coding:utf-8 --*--

class majorityVote:
    def __init__(self):
        return None


    def getAnswer(self):  #获取用户答案 一个二维列表，并使每一行是一个用户的所有答案
             file = open("data/cooking_makeup_data")
             try:
                 content = file.readlines()
             finally:
                file.close()

             allAnswer=[]
             for item in content:
                 lists = item.strip("\n").split(", ")
                 allAnswer.append(lists)
             return  map(list,zip(*allAnswer))

    def getGolden(self):  #获取标准答案
        file =open ("data/cooking_makeup_data_golden")
        try:
            content = file.readlines()
        finally:
            file.close()
        allGolden=[]
        for item in content:
            lists = item.strip("\n")
            allGolden.append(int(lists))
        return  allGolden

    def vote(self,taskid):
        answer=self.getAnswer()
        voteResult={}  #作为投票的结果

        for i in range(len(answer)):  #len(answer)表示工作者的个数
            if answer[i][taskid] not in voteResult:
                voteResult[answer[i][taskid]]=1
            else:
                 voteResult[answer[i][taskid]]+=1

        return max(voteResult.items(),key=lambda x:x [1])[0]   #返回投票最多的结果


    def getAccuracy(self):
        golden=self.getGolden()

        count=0
        for i in range(len(golden)):
            if golden[i]==int(self.vote(i)):
                count+=1

        print count
        print len(golden)
        print float(count)/len(golden)

test=majorityVote()
test.getAccuracy()



