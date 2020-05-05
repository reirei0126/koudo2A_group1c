import json
import csv
import numpy as np
str1="RUshort_00000000"
str2="_keypoints.json"
data2=[[0 for i in range(3) ] for j in range(10000) ] #kata
data4=[[0 for i in range(3) ] for j in range(10000) ] #migite
for i in range(1,10000):
	if i<10 :
		filestr=str1+"000"+str(i)+str2
	elif i<100 :
		filestr=str1+"00"+str(i)+str2
	elif i<1000 :
		filestr=str1+"0"+str(i)+str2
	else:
		filestr=str1+str(i)+str2
	try:
		a=open(filestr)
		b=json.load(a)
		data2[i-1][0]=b["people"][0]['pose_keypoints_2d'][6]
		data2[i-1][1]=b["people"][0]['pose_keypoints_2d'][7]
		data2[i-1][2]=b["people"][0]['pose_keypoints_2d'][8]
		if b["people"][0]['pose_keypoints_2d'][8]<0.3 :
			if i==1:
				data2[i-1][0]=0
				data2[i-1][1]=0
				data2[i-1][2]=0
			else:
				data2[i-1][0]=data2[i-2][0]
				data2[i-1][1]=data2[i-2][1]
				data2[i-1][2]=data2[i-2][2]
				
		data4[i-1][0]=b["people"][0]['pose_keypoints_2d'][12]
		data4[i-1][1]=b["people"][0]['pose_keypoints_2d'][13]
		data4[i-1][2]=b["people"][0]['pose_keypoints_2d'][14]
		if b["people"][0]['pose_keypoints_2d'][14]<0.3 :
			if i==1:
				data2[i-1][0]=0
				data2[i-1][1]=0
				data2[i-1][2]=0
			else:
				data4[i-1][0]=data4[i-2][0]
				data4[i-1][1]=data4[i-2][1]
				data4[i-1][2]=data4[i-2][2]
	except:
		print("end")
		data2=np.resize(data2,(i-1,3))
		data4=np.resize(data4,(i-1,3))
		break
with open("csvmigite.csv","w",newline="") as f:
	writer = csv.writer(f)
	writer.writerows(data4)
f.close()
with open("csvkata.csv","w",newline="") as f:
	writer = csv.writer(f)
	writer.writerows(data2)
f.close()
