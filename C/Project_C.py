#C项目：汽车产品聚类分析
from sklearn.cluster import KMeans
from sklearn import preprocessing
import pandas as pd
import numpy as np
data = pd.read_csv('CarPrice_Assignment.csv')#载入数据
train_x = data.drop(['car_ID'],axis=1)
# 使用LabelEncoder
from sklearn.preprocessing import LabelEncoder
cols = ['CarName','fueltype','aspiration','doornumber','carbody','drivewheel','enginelocation','enginetype','cylindernumber','fuelsystem']#待转化字段
le = LabelEncoder()
train_x['CarName'] = le.fit_transform(train_x['CarName'])
train_x['fueltype'] = le.fit_transform(train_x['fueltype'])
train_x['aspiration'] = le.fit_transform(train_x['aspiration'])
train_x['doornumber'] = le.fit_transform(train_x['doornumber'])
train_x['carbody'] = le.fit_transform(train_x['carbody'])
train_x['drivewheel'] = le.fit_transform(train_x['drivewheel'])
train_x['enginelocation'] = le.fit_transform(train_x['enginelocation'])
train_x['enginetype'] = le.fit_transform(train_x['enginetype'])
train_x['cylindernumber'] = le.fit_transform(train_x['cylindernumber'])
train_x['fuelsystem'] = le.fit_transform(train_x['fuelsystem'])
# 将数据规范化到 [0,1] 空间
min_max_scaler=preprocessing.MinMaxScaler()
train_x=min_max_scaler.fit_transform(train_x)
# 使用K-Means 手肘法：统计不同K取值的误差平方和，选取合适的K值
import matplotlib.pyplot as plt
sse = []
for k in range(1, 100):
	# kmeans算法
	kmeans = KMeans(n_clusters=k)
	kmeans.fit(train_x)
	# 计算inertia簇内误差平方和
	sse.append(kmeans.inertia_)
x = range(1, 100)
plt.xlabel('K')
plt.ylabel('SSE')
plt.plot(x, sse, 'o-')
#plt.show()
#由手肘法绘图可取K=10，使用KMeans聚类
kmeans = KMeans(n_clusters=10)#尝试将数据分为10类
kmeans.fit(train_x)
predict_y = kmeans.predict(train_x)
# 合并聚类结果，插入到原数据中
result = pd.concat((data,pd.DataFrame(predict_y)),axis=1)
result.rename({0:u'聚类结果'},axis=1,inplace=True)
result.to_csv('CarPrice_Assignment_cluster_result.csv',index=False)#保存聚类结果
VW=['vokswagen rabbit','volkswagen 1131 deluxe sedan','volkswagen model 111','volkswagen type 3','volkswagen 411 (sw)','volkswagen super beetle','volkswagen dasher','vw dasher','vw rabbit','volkswagen rabbit','volkswagen rabbit custom']
for vw in VW:
    Group = result[result['CarName'].isin([vw])]['聚类结果'].tolist()#
    cars= result.loc[result['聚类结果']==int(Group[0])]['CarName']
    print(vw+'的竞品车型为：')
    print(cars)#打印VW车型竞品车型名称