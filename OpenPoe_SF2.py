import json
import glob
import os
import math
import time
from pynput.keyboard import Key, Controller

keyboard = Controller()

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

        self.getAngle()
        


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

        


class ActionPoseClass(PoseClass):
    def __init__(self, name, threshold,func):
        self.actionName = name
        self.actionFileName = "setting_" + name + ".json"
        self.threshold = threshold
        self.actionFunc = func
        
        print(self.actionFileName)

        #check if setting file exist
        if not os.path.isfile(self.actionFileName):
            print(self.actionFileName + " file does not exist. Create a new one.")
            print("Set your " + self.actionName + " pose in 5 sec.")
            time.sleep(5)
            file = open(self.actionFileName, "w") 
            latest_file = getLastJsonFileName()
            with open(latest_file , 'r') as reader:
                reader.read
                file.write(reader.read())
                file.close()

        # read pose setting files and create pose objects
        with open(self.actionFileName , 'r') as reader:
            data = json.loads(reader.read())
            super().__init__(data)
            

    def setAction(self):
        self.actionFunc()
        

    def getPosedDiff(self, pose2):
        sumSqrDiff = 0
        cntValid = 0
        for i in range(len(self.listAngle)):
            if self.listAngle[i] != None and pose2.listAngle[i] != None :

                angleDiff = self.listAngle[i] - pose2.listAngle[i]
                if angleDiff > 180:
                    angleDiff= 360 - angleDiff

                sumSqrDiff = sumSqrDiff + angleDiff ** 2
                cntValid = cntValid + 1
            '''        
            else: # One of pose1 or Pose2 is None, use sumSqrDiff average
                if i != 0:            
                    sumSqrDiff = sumSqrDiff + sumSqrDiff/i
            '''
        if cntValid != 0:
            sumSqrDiff = sumSqrDiff / cntValid
            print(self.actionName + "\t" + str(sumSqrDiff))
        return int(sumSqrDiff)
    

    def isMatch(self, poseNow):
        result = self.getPosedDiff(poseNow)
        #print(self.actionName + "\t" + str(result))
        if result !=None and result < self.threshold :
            return True
        else:
            return False




def getLastJsonFileName():
    while(True):
        list_of_files = glob.glob('/dev/shm/temp/output/*.json') # list all the *.json file
        if (len(list_of_files)) != 0:   
            latest_file = max(list_of_files, key=os.path.getctime)
            #print(latest_file)
            time.sleep(0.05)
            return latest_file     








def setFireballR():
    # Fireball
    keyboard.press('s')   # press down
    time.sleep(0.05)
    keyboard.press('d')   # press right
    time.sleep(0.05)
    keyboard.release('s') # release down
    time.sleep(0.05)
    keyboard.press('l')   # press fist
    time.sleep(0.1)
    keyboard.release('d') # release right
    keyboard.release('l') # release fist

def setFireballL():
    # Fireball
    keyboard.press('s')   # press down
    time.sleep(0.05)
    keyboard.press('a')   # press left
    time.sleep(0.05)
    keyboard.release('s') # release down
    time.sleep(0.05)
    keyboard.press('l')   # press fist
    time.sleep(0.1)
    keyboard.release('a') # release left
    keyboard.release('l') # release fist

def setDragonPunchR():
    # DragonPunch  
    keyboard.press('d')   # press right
    time.sleep(0.03)
    keyboard.press('s')   # press down
    time.sleep(0.03)
    keyboard.release('d') # relese right
    time.sleep(0.03)
    keyboard.press('d')   # press right
    time.sleep(0.03)
    keyboard.release('s') # release down
    time.sleep(0.03)
    keyboard.press('k')   # press fist
    time.sleep(0.1)
    keyboard.release('d') # release right
    keyboard.release('k') # release fist
    
def setDragonPunchL():
    # DragonPunch  
    keyboard.press('a')   # press left
    time.sleep(0.03)
    keyboard.press('s')   # press down
    time.sleep(0.03)
    keyboard.release('a') # relese left
    time.sleep(0.03)
    keyboard.press('a')   # press left
    time.sleep(0.03)
    keyboard.release('s') # release down
    time.sleep(0.03)
    keyboard.press('k')   # press fist
    time.sleep(0.1)
    keyboard.release('a') # release left
    keyboard.release('k') # release fist


def setHurricanKickR():
    # HurricanKick
    keyboard.press('s')   # press down
    time.sleep(0.05)
    keyboard.press('a')   # press left
    time.sleep(0.05)
    keyboard.release('s') # release down
    time.sleep(0.05)
    keyboard.press('.')   # press kick
    time.sleep(0.1)
    keyboard.release('a') # release left
    keyboard.release('.') # release kick                

def setHurricanKickL():
    # HurricanKick
    keyboard.press('s')   # press down
    time.sleep(0.05)
    keyboard.press('d')   # press right
    time.sleep(0.05)
    keyboard.release('s') # release down
    time.sleep(0.05)
    keyboard.press('.')   # press kick
    time.sleep(0.1)
    keyboard.release('d') # release right
    keyboard.release('.') # release kick      


def setFist():
    keyboard.type('j')

def moveRight():
    keyboard.press('d')

def moveLeft():
    keyboard.press('a')

def setNormal():
    # Normal
    keyboard.release('d')
    keyboard.release('a')
    

def main():

    poseFireballR = ActionPoseClass("FireballR", 500, setFireballR)
    poseFireballL = ActionPoseClass("FireballL", 500, setFireballL)
        
    poseDragonPunchR = ActionPoseClass("DragonPunchR", 500, setDragonPunchR)
    poseDragonPunchL = ActionPoseClass("DragonPunchL", 500, setDragonPunchL)
    
    poseHurricanKickR = ActionPoseClass("HurricanKickR", 500, setHurricanKickR)
    poseHurricanKickL = ActionPoseClass("HurricanKickL", 500, setHurricanKickL)
    
    poseFist = ActionPoseClass("Fist", 500, setFist)
    
    actionPoses = []
    actionPoses.append(poseFireballR)
    actionPoses.append(poseFireballL)
    actionPoses.append(poseDragonPunchR)
    actionPoses.append(poseDragonPunchL)
    actionPoses.append(poseHurricanKickR)
    actionPoses.append(poseHurricanKickL)
    actionPoses.append(poseFist)

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
                #print(pose.listAngle)
               
                
                # Find the minimum difference between defined action pose and current pose
                indexMin = 0
                minPoseDiff = 65535
                for i in range(len(actionPoses)):
                    poseDiff = actionPoses[i].getPosedDiff(pose)
                    if poseDiff < minPoseDiff:
                        minPoseDiff = poseDiff
                        indexMin = i 
                
                if minPoseDiff < actionPoses[indexMin].threshold :
                    actionPoses[indexMin].setAction()






                '''
                poseDiffFireballR = poseFireballR.getPosedDiff(pose)
                poseDiffFireballL = poseFireballL.getPosedDiff(pose)
                poseDiffDragonPunchR = poseDragonPunchR.getPosedDiff(pose)
                poseDiffDragonPunchL = poseDragonPunchL.getPosedDiff(pose)
                poseDiffHurricanKickR = poseHurricanKickR.getPosedDiff(pose)
                poseDiffHurricanKickL = poseHurricanKickL.getPosedDiff(pose)
                poseDiffFist = poseFist.getPosedDiff(pose)
                
                minPoseDiff = min(poseDiffFireballR, poseDiffFireballL,\
                                  poseDiffDragonPunchR, poseDiffDragonPunchL,\
                                  poseDiffHurricanKickR, poseDiffHurricanKickL,\
                                  poseDiffFist)

                if minPoseDiff < 500:
                    if minPoseDiff == poseDiffFireballR:
                        poseFireballR.setAction()
                        #time.sleep(1)                   
                    elif minPoseDiff == poseDiffFireballL:
                        poseFireballL.setAction()
                        #time.sleep(1)

                    elif minPoseDiff == poseDiffDragonPunchR:
                        poseDragonPunchR.setAction()
                        #time.sleep(1)   
                    elif minPoseDiff == poseDiffDragonPunchL:
                        poseDragonPunchL.setAction()
                        #time.sleep(1)  
                                                
                    elif minPoseDiff == poseDiffHurricanKickR:
                        poseHurricanKickR.setAction()
                        #time.sleep(1)                                                  
                    elif minPoseDiff == poseDiffHurricanKickL:
                        poseHurricanKickL.setAction()
                        #time.sleep(1)                                                  

                    elif minPoseDiff == poseDiffFist:
                        poseFist.setAction() 
                '''


                # Movement
                #print(pose.A1_8)
                if pose.A1_8 != None and pose.A1_8 < 70:
                    moveRight()
                elif pose.A1_8 != None and pose.A1_8 > 110:
                    moveLeft()
                else:
                    setNormal()


            for p in list_of_files:
                os.remove(p)


if __name__ == "__main__":
    main()


