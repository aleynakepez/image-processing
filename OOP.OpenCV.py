import cv2
import numpy as np

class Person:
    def __init__(self, name, color, shape):
        self.name = name
        self.order = []
        self.color= color
        self.shape= shape
        

    def Detector(self, color, shape):
        if color == "red":
            if shape == "circle":
                print("soup")
            elif shape == "rectangle":
                print("cheese platter")
            elif shape == "triangle":
                print("garlic bread")

        elif color == "blue":
            if shape == "circle":
                print("crispy chicken")
            elif shape == "rectangle":
                print("fish & chips")
            elif shape == "triangle":
                print("omlet")

        elif color == "green":
            if shape == "circle":
                print("meatballs")
            elif shape == "rectangle":
                print("casseroles")
            elif shape == "triangle":
                print("fajitas")


        elif color == "yellow":
            if shape == "circle":
                print("souffle")
            elif shape == "rectangle":
                print("tiramisu")
            elif shape == "triangle":
                print("cheesecake")

        

class MenuDetector:
    def __init__(self, image,Object):
        self.image = image
        self.Object=Object
    
        self.color()

    def color(self):
        
        self.hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

        self.red_lower = np.array([0, 100, 100], np.uint8)
        self.red_upper = np.array([10, 255, 255], np.uint8)
        self.red_mask = cv2.inRange(self.hsv, self.red_lower, self.red_upper)

        self.blue_lower = np.array([110,100,100], np.uint8)
        self.blue_upper = np.array([130,255,255], np.uint8)
        self.blue_mask = cv2.inRange(self.hsv, self.blue_lower, self.blue_upper)

        self.green_lower = np.array([35, 40,40], np.uint8)
        self.green_upper = np.array([70, 255, 255], np.uint8)
        self.green_mask = cv2.inRange(self.hsv, self.green_lower, self.green_upper)

        self.yellow_lower = np.array([35, 55, 50], np.uint8)
        self.yellow_upper = np.array([180, 255, 255], np.uint8)
        self.yellow_mask = cv2.inRange(self.hsv, self.yellow_lower, self.yellow_upper)
        
        self.kernel = np.ones((10,10), np.uint8) 
        self.red_mask=cv2.dilate(self.red_mask,self.kernel)
        self.green_mask=cv2.dilate(self.green_mask,self.kernel)
        self.blue_mask=cv2.dilate(self.blue_mask,self.kernel)

        self.contourred , hiearchy = cv2.findContours(self.red_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        self.contourblue, hiearchy = cv2.findContours(self.blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.contourgreen, hiearchy = cv2.findContours(self.green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.contouryellow, hiearchy = cv2.findContours(self.yellow_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        self.counter=0
        self.color="x"
       
        cv2.imshow("red",self.red_mask)

        # for contour in self.contourred:
        #     if cv2.contourArea(contour) > 1000:
        #         self.contour = contour
        #         self.color = "red"
        #         self.shape

        for i in range(len(self.contourred)):
            if cv2.contourArea(self.contourred[i]) > 20000:
                self.contour = self.contourred
                self.color = "red"
                self.detectshape()
                

        for i in range(len(self.contourblue)):
            
            if cv2.contourArea(self.contourblue[i]) > 5000:
                
                self.contour = self.contourblue
                self.color = "blue"
        
                self.detectshape()
                

        for i in range(len(self.contourgreen)):
            if cv2.contourArea(self.contourgreen[i]) > 20000:
                self.contour = self.contourgreen
                self.color = "green"
                
                self.detectshape()
                

        for i in range(len(self.contouryellow)):
            if cv2.contourArea(self.contouryellow[i]) > 20000:
                self.contour = self.contouryellow
                self.color = "yellow"

                self.detectshape()
                
                

    def detectshape(self):
        self.list=[]
        for i in self.contour:
             area=cv2.contourArea(i)
             
             if area > 1000:
                    
                    peri=cv2.arcLength(i, True)
                    approx=cv2.approxPolyDP(i, 0.02*peri, True)
                    self.list.append(len(approx))
                    
        self.number=self.most_frequent(self.list)  
        if self.number==3:
            self.Object.Detector(self.color,"triangle")
        elif self.number==4:
            self.Object.Detector(self.color,"rectangle")
        else:
            self.Object.Detector(self.color,"circle")
    def most_frequent(self,List):
        counter = 0
        num = List[0]
         
        for i in List:
            curr_frequency = List.count(i)
            if(curr_frequency> counter):
                counter = curr_frequency
                num = i
     
        return num

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
Aleyna=Person("Aleyna","red", "circle")

while True:
    
    ret, frame = cap.read()
    
    camera=MenuDetector(frame,Aleyna)
   
    

    if cv2.waitKey(1) & 0xFF == ord('q'): 
        cap.release() 
        cv2.destroyAllWindows() 
        break
