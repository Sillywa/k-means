from matplotlib import pyplot as plt
import random
import math
import copy
class Kmeans:
    __dataList = []
    __k = 1
    __kSample = []
    __count = 0
    def __init__(self,fileName,k):
        self.__dataList = self.__readData(fileName)
        self.__kSample = self.__getKSample(self.__dataList,k)
        self.__k = k

    # 开始聚类
    def start(self):
        while(True):
            #计算每一个点与均值向量之间的距离,确定每一个点的类别
            for index,item in enumerate(self.__dataList):
                self.__caculateType(self.__dataList[index],self.__kSample)
            # 保存均值向量的副本
            copiedKSample = copy.deepcopy(self.__kSample)
            # 重新计算均值向量
            self.__caculateKSampleByAverge(self.__kSample)
            # 如果两个均值向量相等，则循环停止
            if copiedKSample == self.__kSample:
                break
            self.__count += 1
    # 绘制散点图
    def drawPic(self):
        # 由于是二维坐标，因此只需x，y即可
        x = []
        y = []
        c = []
        for i in range(len(self.__dataList)):
            x.append(self.__dataList[i][0])
            y.append(self.__dataList[i][1])
            c.append(self.__dataList[i][2])
        plt.title("dataset k=" + str(self.__k))
        plt.scatter(x, y,c=c)
        plt.show()
    # 获取迭代次数
    def getCount(self):
        return self.__count

    # 从文件中读取数据
    def __readData(self,fileName):
        # 用存放数据的列表
        dataList = []
        try:
            fp = open(fileName,"r")
            fpList = fp.read().splitlines()
            # 将数据分割成二维列表
            for item in fpList:
                dataList.append(item.split("\t"))
            # 将字符数据转化成浮点数
            for i in range(len(dataList)):
                for j in range(len(dataList[i])):
                    dataList[i][j] = float(dataList[i][j])
            # 如果数据不包含类别信息
            # for i in range(len(dataList)):
            #     dataList[i].append(0)
        except IOError:
            print("error")
        #返回数据
        return dataList
    # 获取初始k个点，也就是初始均值向量
    def __getKSample(self,dataList, k):
        kSample = []    
        for i in range(k):
            #从所有数据集中随机选取k个数据
            num = random.randint(0,len(dataList)-1)
            kSample.append(copy.deepcopy(dataList[num]))
        return kSample
    
    # 计算两个点之间的距离
    def __getDistance(self,dataPoint1,dataPoint2):
            
        distance = 0
        # 因为每一项数据的最后一位为类别，所以不参与计算距离
        for i in range(len(dataPoint1)-1):
            distance = distance + pow(dataPoint1[i]-dataPoint2[i],2)		
        distance = math.sqrt(distance)
        return distance
    # 根据每个样本距离均值向量的长短，计算每个样本所属的类别
    def __caculateType(self,dataPoint,kSample):
        # 首先假设该样本距离第一个均值向量最近,即该样本属于第一类
        minDistance = self.__getDistance(dataPoint,kSample[0])
        # 记录该样本所属的类别
        type = 0
        
        # 计算该样本与每一个均值向量之间的距离
        for index,item in enumerate(kSample):
            distance = self.__getDistance(dataPoint,item)
            # 如果该数据点距离该类别较小
            if distance < minDistance:
                minDistance = distance  # 更新最短距离
                type = index    # 更新样本点所属类别
        # 修改数据点的类别
        dataPoint[len(dataPoint)-1] = type

    # 重新计算均值向量
    def __caculateKSampleByAverge(self,kSample):
         # 对于每个均值向量，其下标为类别
        for i in range(len(kSample)):
            typeI = []
            # 遍历所有数据找到与其类别一致的数据点
            for item in self.__dataList:
                if item[(len(item)-1)] == i:
                    typeI.append(copy.deepcopy(item))
            #求和
            for j in range(1,len(typeI)):
                for k in range(len(typeI[j])):
                    typeI[j][k] += typeI[j-1][k]
            # 求均值并更改每一类的聚类中心
            for j in range(len(kSample[i])):
                kSample[i][j] = typeI[len(typeI)-1][j]/len(typeI)

# 注意修改路径
# a = Kmeans(filename,3)

# a.start()
# print(a.getCount())
#二维坐标才可以画散点图
# a.drawPic()