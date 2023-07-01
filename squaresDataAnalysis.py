#Evan Gascoyne 
#CSCI 270
#Final Project
#Squares data analysis

import pandas as pd
import matplotlib.pyplot as plt
import seaborn
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale

data = pd.read_csv('squaresLog.csv',header=None,names=['size','speed','perception','lifespan','hungriness','gestationNeeded','freePoint', 'strainName', 'timePoint'])

observations = int(data['timePoint'][data.shape[0]-1]) +1

BIG_THRESH = 14


#########################################
#Average value of freePoint
data.groupby('timePoint')['freePoint'].mean().plot()
plt.ylabel('Average freePoint stat')
plt.title("Change in freePoint stat over time")
plt.show()

############################
#Size Area Plot
#this way is really slow

big = [0 for i in range(observations)]
small = [0 for i in range(observations)]

for index, row in data.iterrows():
    if row['size']>=BIG_THRESH:
        big[int(row['timePoint'])]+=1
    else:
        small[int(row['timePoint'])]+=1
        
areaData=pd.DataFrame({'timePoint':range(observations),'small':small,'big':big})
areaData.plot.area(x='timePoint')
plt.title("Big v Small Square Population")
plt.show()


###########################
#Perception Area Plot

p5 = [0 for i in range(observations)]
p40 = [0 for i in range(observations)]
p75 = [0 for i in range(observations)]
p110 = [0 for i in range(observations)]
p145 = [0 for i in range(observations)]
p180 = [0 for i in range(observations)]
p215 = [0 for i in range(observations)]
p250 = [0 for i in range(observations)]

for index, row in data.iterrows():
    if row['perception']<6:
        p5[int(row['timePoint'])]+=1
    elif row['perception']<41:
        p40[int(row['timePoint'])]+=1
    elif row['perception']<76:
        p75[int(row['timePoint'])]+=1
    elif row['perception']<111:
        p110[int(row['timePoint'])]+=1
    elif row['perception']<146:
        p145[int(row['timePoint'])]+=1
    elif row['perception']<181:
        p180[int(row['timePoint'])]+=1       
    else:
        p215[int(row['timePoint'])]+=1
        
areaData=pd.DataFrame({'timePoint':range(observations),'p5':p5,'p40':p40,'p75':p75,'p110':p110,'p145':p145,'p180':p180,'p215+':p215})
areaData.plot.area(x='timePoint')
plt.title("Perception Values Among Square Population Over Time")
plt.show()

#########################################
#Different Attributes in big vs small over time
def plotBigSmall(var):
    big = data[data['size']>=BIG_THRESH]
    small = data[data['size']<BIG_THRESH]
    big=big.groupby('timePoint')[var].mean()
    small=small.groupby('timePoint')[var].mean()
    big=big.reindex(range(observations),fill_value=0) #add 0s to big
    smallbig = pd.concat([small,big],axis=1)
    smallbig.columns=['small','big']
    smallbig.plot()
    plt.title(var+"Values in Small and Big Squares Over Time")
    plt.ylabel("Mean " +var+" Value")
    plt.show()

plotBigSmall("size")
plotBigSmall("speed")
plotBigSmall("perception")
plotBigSmall("lifespan")
plotBigSmall("hungriness")
plotBigSmall("gestationNeeded")
plotBigSmall("freePoint")



########################################
#Attribute Correlation Heatmap

#subset = data[data['timePoint']==observations-1].iloc[:,:-2] #Data from last time point
subset = data.iloc[:,:-2] #all time points
cor = np.corrcoef(subset.T)
labels=['size','speed','perception','lifespan','hungriness','gestationNeeded','freePoint']
seaborn.heatmap(cor,annot=True,xticklabels=labels,yticklabels=labels)
plt.title("Attribute Correlations in Squares")
plt.show()

big = data[data['size']>=BIG_THRESH]
small = data[data['size']<BIG_THRESH]


#subsetSmall = small[small['timePoint']==observations-1].iloc[:,:-2] #Data from last time point
subsetSmall = small.iloc[:,:-2] 
corSmall = np.corrcoef(subsetSmall.T)
seaborn.heatmap(corSmall,annot=True,xticklabels=labels,yticklabels=labels)
plt.title("Attribute Correlations in Small Squares")
plt.show()


#subsetBig = big[big['timePoint']==observations-1].iloc[:,:-2] #Data from last time point
subsetBig = big.iloc[:,:-2] 
corBig = np.corrcoef(subsetBig.T)
seaborn.heatmap(corBig,annot=True,xticklabels=labels,yticklabels=labels)
plt.title("Attribute Correlations in Big Squares")
plt.show()





#########################################
#Principle Component Analysis over Time
pcaFitTimePoint = observations-1  #fit to final timepoint  

subset = data[data['timePoint']==pcaFitTimePoint].iloc[:,:-2]
pca=PCA(n_components=4)
pca.fit(scale(subset))       #note: doesn't work if simulation ends with low square count, have to change subset to a timepoint with both species
print("pca components\n",pca.components_)
print(pca.explained_variance_ratio_)


for t in range(0,observations,5): #step by 5
    subset = data[data['timePoint']==t].iloc[:,:-2]
    df_pca=pca.transform(scale(subset))
    subset['color']=np.where(subset['size']>=BIG_THRESH,'red','blue')
    #subset['color']=np.where(subset['lifespan']>800,'red','blue')
    
    plt.scatter(df_pca[:,0],df_pca[:,2],color=subset['color'])
    plt.title("TimePoint: "+str(t))
    plt.xlim([-4,10])
    plt.ylim([-7,7])
    plt.xlabel("1st Principle Component")
    plt.ylabel("3rd Principle Component") #2nd is usually mostly freePoint
    plt.show()
