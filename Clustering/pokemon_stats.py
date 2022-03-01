"""
Created on Nov 9 2020

@author: Tianyi Zhao
"""

import math
import csv
import numpy as np

def load_data(filepath):
    dataset1 = []
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            dataset1.append(row)        
    dataset2 = []
    for i in range (0, 20):
         dictData = dict.fromkeys(['#','Name','Type 1','Type 2', 'Total','HP','Attack','Defense','Sp. Atk','Sp. Def','Speed'])
         dictData['#'] = dataset1[i]['#']
         dictData['Name'] = dataset1[i]['Name']
         dictData['Type 1'] = dataset1[i]['Type 1']
         dictData['Type 2'] = dataset1[i]['Type 2']
         dictData['Total'] = dataset1[i]['Total']
         dictData['HP'] = dataset1[i]['HP']
         dictData['Attack'] = dataset1[i]['Attack']
         dictData['Defense'] = dataset1[i]['Defense']
         dictData['Sp. Atk'] = dataset1[i]['Sp. Atk']
         dictData['Sp. Def'] = dataset1[i]['Sp. Def']
         dictData['Speed'] = dataset1[i]['Speed']
         dataset2.append(dictData)
    return dataset2

def calculate_x_y(stats):
    x = (int)(stats['Attack']) + (int)(stats['Sp. Atk']) + (int)(stats['Speed'])
    y = (int)(stats['Defense']) + (int)(stats['Sp. Def']) + (int)(stats['HP'])
    xy = (x,y)
    return xy
 
def hac(dataset):
    clusters = []
    for i in range (0,len(dataset)):
        dictData = dict.fromkeys(['cluster_index','value'])
        dictData['cluster_index'] = i
        dictData['value'] = [dataset[i]]
        clusters.append(dictData)
        
    distance_set = []
    for i in range(0, len(dataset)-1):  
        for j in range(i+1, len(dataset)):  
            distance = math.sqrt((clusters[i]['value'][0][0] - clusters[j]['value'][0][0])**2 + (clusters[i]['value'][0][1] - clusters[j]['value'][0][1])**2)
            distance_set.append((distance,dataset[i],dataset[j]))
    distance_set.sort()
    for i in range (0,len(dataset)-1):
        if distance_set[i][0] == distance_set[i+1][0]:
            index1 = -1
            index2 = -1
            for j in range (0,len(dataset)):
                if distance_set[i][1] == clusters[j]['value'][0]:
                    index1 = clusters[j]['cluster_index']
                if distance_set[i+1][1] == clusters[j]['value'][0]:
                    index2 = clusters[j]['cluster_index']
            if index1 > index2:
                temp = distance_set[i]
                distance_set[i] = distance_set[i+1]
                distance_set[i+1] = temp
                
    Z = np.empty([len(dataset)-1,4])
    d = 0
    i = 0
    while i != len(Z):
        value1 = distance_set[i+d][1]
        value2 = distance_set[i+d][2]
        Z[i][2] = distance_set[i+d][0]
        flag1 = False
        flag2 = False
        dictData = dict.fromkeys(['cluster_index','value'])
        dictData['cluster_index'] = len(clusters)
        dictData['value'] = []
        for j in range (1,len(clusters)+1):
            count = 0
            values = clusters[len(clusters)-j]['value']
            for k in range (0,len(values)):  
                if value1 == values[k] and flag1 == False:
                    Z[i][0] = clusters[len(clusters)-j]['cluster_index']
                    for z in range (0,len(values)):
                        dictData['value'].append(clusters[len(clusters)-j]['value'][z])
                    flag1 = True
                    count += 1
                if value2 == values[k] and flag2 == False:
                    Z[i][1] = clusters[len(clusters)-j]['cluster_index']
                    for z in range (0,len(values)):
                        dictData['value'].append(clusters[len(clusters)-j]['value'][z])
                    flag2 = True
                    count += 1
            if count == 2:
                i -= 1
                d += 1
                break
            if flag1 == True and flag2 == True:
                clusters.append(dictData)
                Z[i][3] = len(dictData['value'])
                if Z[i][0] > Z[i][1]:
                    temp = Z[i][0] 
                    Z[i][0] = Z[i][1]
                    Z[i][1] = temp
                break
            
        i += 1
  
    return Z


dataset = load_data('Pokemon.csv')
print(hac(dataset))




