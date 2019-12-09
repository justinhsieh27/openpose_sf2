import json
import glob
import os
import math
import time
import matplotlib
from matplotlib import pyplot as plt



def getShoulderAngle(jsonData):

    for p in data['people']:
        #print(p['pose_keypoints_2d'])

        #print('1-neck:')
        indexS = 1*3
        listNeck = p['pose_keypoints_2d'][indexS: indexS+3]
        #print(listNeck)

        #print('2-RShoulder:')
        indexS = 2*3
        listRShoulder = p['pose_keypoints_2d'][indexS: indexS+3]
        #print(listRShoulder)

        #print('3-RElbow:')
        indexS = 3*3
        listRElbow = p['pose_keypoints_2d'][indexS: indexS+3]
        #print(listRElbow)

        #print('5-LShoulder:')
        indexS = 5*3
        listLShoulder = p['pose_keypoints_2d'][indexS: indexS+3]
        #print(listLShoulder)

        #print('6-LElbow:')
        indexS = 6*3
        listLElbow = p['pose_keypoints_2d'][indexS: indexS+3]
        #print(listLElbow)

        # origin: RShoulder
        vector1 = [listNeck[0]-listRShoulder[0], listNeck[1]-listRShoulder[1]]
        vector2 = [listRElbow[0]-listRShoulder[0], listRElbow[1]-listRShoulder[1]]
        angleRSoulder = math.atan2(vector2[1], vector2[0]) - math.atan2(vector1[1], vector1[0])
        angleRSoulder = angleRSoulder/math.pi*180	# change arc to degree
        if angleRSoulder < 0:
            angleRSoulder= angleRSoulder + 360
        #print("angleRSoulder = " + str(angleRSoulder))

        # origin: LShoulder
        vector1 = [listNeck[0]-listLShoulder[0], listNeck[1]-listLShoulder[1]]
        vector2 = [listLElbow[0]-listLShoulder[0], listLElbow[1]-listLShoulder[1]]
        angleLSoulder = math.atan2(vector2[1], vector2[0]) - math.atan2(vector1[1], vector1[0])
        angleLSoulder = angleLSoulder/math.pi*180	# change arc to degree
        if angleLSoulder < 0:
            angleLSoulder= angleLSoulder + 360                    
        #print("angleLSoulder = " + str(angleLSoulder))

        return(angleRSoulder, angleLSoulder)





# main()



listAngleRShoulder = [0.0]*10
listAngleLShoulder = [0.0]*10

'''
fig,ax = plt.subplots(nrows=2)

#ax[0].tick_params(axis='both', which='major', labelsize=3)
#ax[1].tick_params(axis='both', which='major', labelsize=3)

ax[0].plot(listAngleRShoulder)
ax[1].plot(listAngleLShoulder)

#plt.show()
'''

while(True):
    list_of_files = glob.glob('/dev/shm/temp/output/*.json') # list all the *.json file
    if (len(list_of_files)) != 0:   
        latest_file = max(list_of_files, key=os.path.getctime)
        #print(latest_file)
        time.sleep(0.05)        
        
        with open(latest_file , 'r') as reader:
            data = json.loads(reader.read())
            angleRSoulder, angleLSoulder = getShoulderAngle(data)
            print("angleRSoulder = " + str(angleRSoulder))
            print("angleLSoulder = " + str(angleLSoulder))
            
            del listAngleRShoulder[0]
            listAngleRShoulder.append(angleRSoulder)
            del listAngleLShoulder[0]
            listAngleLShoulder.append(angleLSoulder)

            '''
            ax[0].cla()
            ax[1].cla() 
            
            ax[0].plot(listAngleRShoulder)
            ax[1].plot(listAngleLShoulder)
            
            ax[0].axis([0,10,0,360])
            ax[1].axis([0,10,0,360])

            ax[0].tick_params(axis='both', which='major', labelsize=5)
            ax[1].tick_params(axis='both', which='major', labelsize=5)


            plt.draw()
            plt.pause(0.0001)
            '''

        for p in list_of_files:
            os.remove(p)


    #time.sleep(0.1)

