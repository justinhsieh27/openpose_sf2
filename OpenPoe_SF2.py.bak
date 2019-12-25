import json
import glob
import os
import math
import time
from subprocess import Popen, PIPE



class PoseClass:
    def __init__(self, jsonData):
        self.__data = jsonData
        # Angles: total 23 angles        
        self.A0_1_2 = None
        self.A0_1_5 = None
        self.A0_1_8 = None
       
        self.A1_2_3 = None
        self.A2_3_4 = None
        self.A2_1_8 = None

        self.A1_5_6 = None
        self.A5_6_7 = None
        self.A5_1_8 = None

        self.A1_8_9 = None
        self.A8_9_10 = None
        self.A9_10_11 = None
        self.A10_11_24 = None
        self.A10_11_22 = None
        self.A24_11_22 = None
        self.A11_22_23 = None

        self.A1_8_12 = None
        self.A8_12_13 = None
        self.A12_13_14 = None
        self.A13_14_21 = None
        self.A13_14_19 = None
        self.A21_14_19 = None
        self.A14_19_20 = None

        self.A1_8 = None    # body absolute angle

        self.listAngle = []

        self.__pt = []


    def getPointValue(self):
        lstData = self.__data['people'][0]['pose_keypoints_2d']
       
        for i in range(int(len(lstData)/3)):
            self.__pt.append([lstData[i*3],lstData[i*3+1]])

        #print(self.__pt)

    def calAngle(self, pt0, pt1, pt2):
        #pt[0]: x coordinate, pt[1]:y coordinate        
        #print(pt0, pt1, pt2)   
        if pt0[0] < 0 or pt0[1] <0 or pt1[0] < 0 or pt1[1] <0 or pt2[0] < 0 or pt2[1] < 0 :
            return None

        vector1 = [pt1[0]-pt0[0], pt1[1]-pt0[1]]
        vector2 = [pt2[0]-pt1[0], pt2[1]-pt1[1]]
        angle = math.atan2(vector2[1], vector2[0]) - math.atan2(vector1[1], vector1[0])
        angle = angle/math.pi*180	# change arc to degree
        if angle < 0:
            angle= angle + 360

        return angle



    def getAngle(self):
        self.getPointValue()
        #print(len(self.__pt))
        
        self.A0_1_2 = self.calAngle(self.__pt[0], self.__pt[1], self.__pt[2])  
        self.A0_1_5 = self.calAngle(self.__pt[0], self.__pt[1], self.__pt[5])  
        self.A0_1_8 = self.calAngle(self.__pt[0], self.__pt[1], self.__pt[8])  
       
        self.A1_2_3 = self.calAngle(self.__pt[1], self.__pt[2], self.__pt[3])
        self.A2_3_4 = self.calAngle(self.__pt[2], self.__pt[3], self.__pt[4])
        self.A2_1_8 = self.calAngle(self.__pt[2], self.__pt[1], self.__pt[8])

        self.A1_5_6 = self.calAngle(self.__pt[1], self.__pt[5], self.__pt[6])
        self.A5_6_7 = self.calAngle(self.__pt[5], self.__pt[6], self.__pt[7])
        self.A5_1_8 = self.calAngle(self.__pt[5], self.__pt[1], self.__pt[8])

        self.A1_8_9 = self.calAngle(self.__pt[1], self.__pt[8], self.__pt[9])
        self.A8_9_10 = self.calAngle(self.__pt[8], self.__pt[9], self.__pt[10])
        self.A9_10_11 = self.calAngle(self.__pt[9], self.__pt[10], self.__pt[11])
        self.A10_11_24 = self.calAngle(self.__pt[10], self.__pt[11], self.__pt[24])
        self.A10_11_22 = self.calAngle(self.__pt[10], self.__pt[11], self.__pt[22])
        self.A24_11_22 = self.calAngle(self.__pt[24], self.__pt[11], self.__pt[22])
        self.A11_22_23 = self.calAngle(self.__pt[11], self.__pt[22], self.__pt[23])

        self.A1_8_12 = self.calAngle(self.__pt[1], self.__pt[8], self.__pt[12])
        self.A8_12_13 = self.calAngle(self.__pt[8], self.__pt[12], self.__pt[13])
        self.A12_13_14 = self.calAngle(self.__pt[12], self.__pt[13], self.__pt[14])
        self.A13_14_21 = self.calAngle(self.__pt[13], self.__pt[14], self.__pt[21])
        self.A13_14_19 = self.calAngle(self.__pt[13], self.__pt[14], self.__pt[19])
        self.A21_14_19 = self.calAngle(self.__pt[21], self.__pt[14], self.__pt[19])
        self.A14_19_20 = self.calAngle(self.__pt[14], self.__pt[19], self.__pt[20])


        self.A1_8 = self.calAngle([0, self.__pt[1][1]], self.__pt[1], self.__pt[8])
        if self.A1_8 != None :
            self.A1_8 = int(self.A1_8)

        self.listAngle = [self.A0_1_2, self.A0_1_5, self.A0_1_8,
        self.A1_2_3, self.A2_3_4, self.A2_1_8,
        self.A1_5_6, self.A5_6_7, self.A5_1_8,
        self.A1_8_9, self.A8_9_10,
        self.A1_8_12, self.A8_12_13]

        


def getLastJsonFileName():
    while(True):
        list_of_files = glob.glob('/dev/shm/temp/output/*.json') # list all the *.json file
        if (len(list_of_files)) != 0:   
            latest_file = max(list_of_files, key=os.path.getctime)
            #print(latest_file)
            time.sleep(0.05)
            return latest_file     



def getPosedDiff(pose1, pose2):
    sumSqrDiff = 0
    cntValid = 0
    for i in range(len(pose1.listAngle)):
        if pose1.listAngle[i] != None and pose2.listAngle[i] != None :

            angleDiff = pose1.listAngle[i] - pose2.listAngle[i]
            if angleDiff > 180:
                angleDiff= 360 - angleDiff

            sumSqrDiff = sumSqrDiff + angleDiff ** 2
            cntValid = cntValid + 1
        '''        
        else: # One of pose1 or Pose2 is None, use sumSqrDiff average
            if i != 0:            
                sumSqrDiff = sumSqrDiff + sumSqrDiff/i
        '''
    if sumSqrDiff != 0:
        sumSqrDiff = sumSqrDiff / cntValid
    if sumSqrDiff == 0: # No valid sumSqrDiff was calculated
        sumSqrDiff = None
        return sumSqrDiff
    else:
        return int(sumSqrDiff)



# Key settings
# single keyjjjjjjjjjjjjjjjjdsdk
up_Key = '''key W
'''
down_Key = '''key S
'''
left_Key = '''key A
'''
right_Key = '''key D
'''
j_Key = '''key J
'''
k_Key = '''key K
'''
l_Key = '''key L
'''
# key down
up_KeyDown = '''keydown W
'''
down_KeyDown = '''keydown S
'''
left_KeyDown = '''keydown A
'''
right_KeyDown = '''keydown D
'''
j_KeyDown = '''keydown J
'''
k_KeyDown = '''keydown K
'''
l_KeyDown = '''keydown L
'''
# key up
up_KeyUp = '''keyup W
'''
down_KeyUp = '''keyup S
'''
left_KeyUp = '''keyup A
'''
right_KeyUp = '''keyup D
'''
j_KeyUp = '''keyup J
'''
k_KeyUp = '''keyup K
'''
l_KeyUp = '''keyup L
'''

def keypress(sequence):
    if isinstance(sequence, str):
        sequence = sequence.encode('ascii')
    p = Popen(['xte'], stdin=PIPE)
    p.communicate(input=sequence)

def setBallKen():
    # Ballken
    keypress(down_KeyDown)
    time.sleep(0.05)
    keypress(right_KeyDown)
    time.sleep(0.05)
    keypress(down_KeyUp)
    time.sleep(0.05)
    keypress(l_KeyDown)
    time.sleep(0.1)
    keypress(right_KeyUp)
    keypress(l_KeyUp)


def setHoluKen():
    # Holuken
    keypress(right_KeyDown)
    time.sleep(0.03)
    keypress(down_KeyDown)
    time.sleep(0.03)
    keypress(right_KeyUp)
    time.sleep(0.03)
    keypress(right_KeyDown)
    time.sleep(0.03)
    keypress(down_KeyUp)
    time.sleep(0.03)
    keypress(k_KeyDown)
    time.sleep(0.1)
    keypress(right_KeyUp)
    keypress(k_KeyUp)
    
def setNormal():
    # Normal
    keypress(right_KeyUp)
    keypress(right_KeyUp)
    keypress(down_KeyUp)    
    keypress(k_KeyUp)


def main():
    # check if pose setting files exists.
    if not os.path.isfile("settingNormal.json"):
        print("settingNormal.json file does not exist. Create a new one.\nSet your Normal pose in 5 sec.")
        time.sleep(5)
        file = open("settingNormal.json", "w") 
        latest_file = getLastJsonFileName()
        with open(latest_file , 'r') as reader:
            reader.read
            file.write(reader.read())
            file.close() 

    if not os.path.isfile("settingForward.json"):
        print("settingForward.json file does not exist. Create a new one.\nSet your Forward pose in 5 sec.")
        time.sleep(5)
        file = open("settingForward.json", "w") 
        latest_file = getLastJsonFileName()
        with open(latest_file , 'r') as reader:
            reader.read
            file.write(reader.read())
            file.close() 
        
    if not os.path.isfile("settingBackward.json"):
        print("settingBackward.json file does not exist. Create a new one.\nSet your Backward pose in 5 sec.")
        time.sleep(5)
        file = open("settingBackward.json", "w") 
        latest_file = getLastJsonFileName()
        with open(latest_file , 'r') as reader:
            reader.read
            file.write(reader.read())
            file.close() 
            
    if not os.path.isfile("settingFist.json"):
        print("settingFist.json file does not exist. Create a new one.\nSet your Fist pose in 5 sec.")
        time.sleep(5)
        file = open("settingFist.json", "w") 
        latest_file = getLastJsonFileName()
        with open(latest_file , 'r') as reader:
            reader.read
            file.write(reader.read())
            file.close()             
            
    if not os.path.isfile("settingBallKen.json"):
        print("settingBallKen.json file does not exist. Create a new one.\nSet your BallKen pose in 5 sec.")
        time.sleep(5)
        file = open("settingBallKen.json", "w") 
        latest_file = getLastJsonFileName()
        with open(latest_file , 'r') as reader:
            reader.read
            file.write(reader.read())
            file.close()             
            
    if not os.path.isfile("settingHoluKen.json"):
        print("settingHoluKen.json file does not exist. Create a new one.\nSet your HoluKen pose in 5 sec.")
        time.sleep(5)
        file = open("settingHoluKen.json", "w") 
        latest_file = getLastJsonFileName()
        with open(latest_file , 'r') as reader:
            reader.read
            file.write(reader.read())
            file.close()    


    # read pose setting files and create pose objects
    with open("settingNormal.json" , 'r') as reader:
        data = json.loads(reader.read())
        poseNormal = PoseClass(data)
        poseNormal.getAngle()

    with open("settingForward.json" , 'r') as reader:
        data = json.loads(reader.read())
        poseForward = PoseClass(data)
        poseForward.getAngle()
    
    with open("settingBackward.json" , 'r') as reader:
        data = json.loads(reader.read())
        poseBackward = PoseClass(data)
        poseBackward.getAngle()

    with open("settingFist.json" , 'r') as reader:
        data = json.loads(reader.read())
        poseFist = PoseClass(data)
        poseFist.getAngle()

    with open("settingBallKen.json" , 'r') as reader:
        data = json.loads(reader.read())
        poseBallKen = PoseClass(data)
        poseBallKen.getAngle()

    with open("settingHoluKen.json" , 'r') as reader:
        data = json.loads(reader.read())
        poseHoluKen = PoseClass(data)
        poseHoluKen.getAngle()


    while(True):
        list_of_files = glob.glob('/dev/shm/temp/output/*.json') # list all the *.json file
        if (len(list_of_files)) != 0:   
            latest_file = max(list_of_files, key=os.path.getctime)
            #print(latest_file)
            #time.sleep(0.05)        
        
            with open(latest_file , 'r') as reader:
                strFile = reader.read()                
                if strFile == '':
                    #print("Got empty file")
                    continue    # skip this loop, but continue next loop

                data = json.loads(strFile)
                #print(data['people'][0]['pose_keypoints_2d'])
                
                pose = PoseClass(data)
                pose.getAngle()
                #print(pose.listAngle)
                
                                          
                
               
            
                # Attack
                diffFromNormal = getPosedDiff(pose, poseNormal)
                diffFromBallKen = getPosedDiff(pose, poseBallKen)
                diffFromHoluKen = getPosedDiff(pose, poseHoluKen)
                diffFromFist = getPosedDiff(pose, poseFist)
                #print(diffFromNormal, diffFromBallKen, diffFromHoluKen, diffFromFist)

                if diffFromNormal != None and diffFromNormal < 1000:
                    setNormal()
                elif diffFromBallKen != None and diffFromBallKen < 500:
                    setBallKen()
                    time.sleep(1)
                elif diffFromHoluKen != None and diffFromHoluKen < 500:
                    setHoluKen()
                    time.sleep(1)                                                  
                elif diffFromFist != None and diffFromFist < 300:
                    keypress(j_Key)     
                

                # Movement
                #print(pose.A1_8)
                if pose.A1_8 != None and pose.A1_8 < 70:
                    keypress(right_KeyDown)                    
                elif pose.A1_8 != None and pose.A1_8 > 110:
                    keypress(left_KeyDown)
                else:
                    keypress(left_KeyUp)
                    keypress(right_KeyUp)
                

            for p in list_of_files:
                os.remove(p)


if __name__ == "__main__":
    main()


