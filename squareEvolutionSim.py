#Square Evolution Sim

#This program draws squares to the screen, the squares travel around the screen, 
#the squares have "genes" that give them different properties,
#the squares occasionally have square 'children', who receive the parent genes, with small changes
#bigger squares eat little squares
#squares can "see" other squares, they run away from predators and run towards prey
#squares eventually die from age or not eating
#over time the squares "evolve" and develop more ideal properties

#currently, the squares eventually develop into two "species" (it takes a while)
#big, fast, short-sighted, slow-reproducing squares  ::  and small, slow, long-sighted, fast-reproducing squares

#controls: left right arrows change FPS cap, "sflpgdhn" changes hist display, click on a square to highlight it and display its stats, 
#k to use killBig function, z: spawn z strain square



import pygame ; pygame.init() #pip install pygame
import random ; random.seed(1) #must change/remove seed to get different run

WIN = pygame.display.set_mode((1600,900))
mapX = 1600
mapY = 900

DIFFTOEAT = 10
ANIMALCAP = 400




animals = []
class Animal: #square
    def __init__(self,speed,size,color,gestationNeeded,x,y,perception,lifespan,hungriness,freePoint,strainName,mutationRate):
        #stats
        self.perception = perception
        self.speed = speed
        self.gestationSpeed =.2
        self.size = size
        self.lifespan = lifespan
        self.lifespanInit = lifespan
        self.hungriness = hungriness
        self.agespeed = 1
        self.freePoint = freePoint #doesn't do anything
        self.gestationNeeded = gestationNeeded
        self.strainName=strainName
        self.mutationRate=mutationRate
        
        #statuses
        self.gestationCounter = 0
        self.fullness = 110
        self.selected = False
        
        #tracking
        self.x = x
        self.y = y
        self.color = color
        self.destination = self.get_destination()
        
        
        
        animals.append(self)
        self.mutate()
        
        
    def move(self):   
        if self.x > self.destination[0]:
            self.x -= self.speed
        else:
            self.x += self.speed
        if self.y > self.destination[1]:
            self.y -= self.speed
        else:
            self.y += self.speed
            
            
        if abs(round(self.x) - self.destination[0])<self.speed+1 and abs(round(self.y) - self.destination[1])<self.speed+1: #arrived!
            self.destination = self.get_destination()
        
    def hunger(self):
        self.fullness -= self.hungriness
        if self.fullness < 0:
            self.die()
            
        elif self.fullness > 2000: #
            self.fullness-=1000
            self.gestationCounter+=100
                
    
    def see_enemy(self):
        predators = []
        for animal in animals:
            if animal.size-DIFFTOEAT > self.size:
                predators.append(animal)
        if predators:
            threat = min(predators,key = lambda z: distance(z.x , z.y, self.x,self.y))
            if distance(threat.x,threat.y,self.x,self.y) < self.perception:
                if threat.x > self.x: #pred is to the right
                    newX = random.randint(0,max(self.x,0)) #move left
                else:                       #pred is to the left
                    newX = random.randint(min(self.x,mapX),mapX)
                if threat.y > self.y: #pred is above
                    newY = random.randint(0,max(self.y,0))
                else:                        #pred below
                    newY = random.randint(min(self.y,mapY),mapY)
                self.destination = (newX,newY)            
        
                    
    def see_prey(self):
        prey = []
        for animal in animals:
            if animal.size+DIFFTOEAT < self.size:
                prey.append(animal)
        if prey:
            target = min(prey,key = lambda z: distance(z.x , z.y, self.x,self.y)) #sort by nearest
            if distance(target.x,target.y,self.x,self.y) < self.perception:
                self.destination= (target.x,target.y)            
        
                
    def check_age(self):
        self.lifespan -= self.agespeed
        if self.lifespan< 0:
            self.die()        
    
    def die(self):
        if self in animals: #get occasional crash without this line
            animals.remove(self)
    
    def get_destination(self):
        x = random.randint(50,mapX-50)
        y = random.randint(50,mapY-50)
        return (x,y)
    
    def prune(self):
        if self.size < 0:
            self.die()
        elif self.perception < 0:
            self.die()
        elif self.speed < 0:
            self.die()
        elif self.gestationNeeded < 50:
            self.die()
        elif self.speed < 0.1:
            self.die()
        elif self.freePoint < 0:
            self.die()
        elif self.lifespanInit < 1:
            self.die()
            
    def mutate(self):
        r = random.randint(1,100)
        if r<=self.mutationRate:   
            r1 = random.randint(0,6)
            r2 = random.randint(0,6) 
            if   r1 ==0: 
                self.size+=3
            elif r1 ==1:
                self.speed +=1
            elif r1 ==2:
                self.gestationNeeded/=1.18
            elif r1 ==3:
                self.perception+=35
            elif r1 ==4:
                self.lifespanInit*=1.65
            elif r1 == 5:
                self.hungriness /=1.2
            elif r1 == 6:
                self.freePoint +=1
                
            if   r2 ==0:
                self.size-=3                
            elif r2 ==1:
                self.speed -=1            
            elif r2 ==2:
                self.gestationNeeded*=1.18  
            elif r2 ==3:
                self.perception-=35        
            elif r2 ==4:
                self.lifespanInit /=1.65        
                self.lifespan /=1.65
            elif r2 ==5:
                self.hungriness *=1.2      
            elif r2 ==6:
                self.freePoint-=1
                 
            self.color = (min(self.perception*2,255),0,255-min(self.perception*2,255))  #color square by attribute
            #self.color = (min(self.lifespan/4,255),0,255-min(self.lifespan/4,255))
            
            self.prune()


def distance(x1,y1,x2,y2):
    return abs(x2-x1)+abs(y2-y1)

        
def move(TIMER):
    for animal in animals:
        animal.move()
        animal.hunger()
    if TIMER %14 == 0:
        eat()
    elif TIMER%14 == 7:
        for animal in animals:
            animal.see_prey()
            animal.see_enemy()
            animal.check_age()

def make_children():
    for animal in animals:
        animal.gestationCounter += animal.gestationSpeed
        if (animal.gestationCounter>animal.gestationNeeded): 
            animal.gestationCounter -= animal.gestationNeeded
            #new animal
            if len(animals)<ANIMALCAP:
                Animal(animal.speed,animal.size,animal.color,animal.gestationNeeded,animal.x,animal.y,animal.perception,animal.lifespanInit,animal.hungriness,animal.freePoint,animal.strainName,animal.mutationRate) #speed,size,color,x,y


def overlap_check(x1,y1,size1,x2,y2,size2): #check if two squares overlap
    if (x1<x2+size2) and (x1+size1>x2) and (y1 > y2-size2) and (y1-size1 < y2):
        return True
    return False


def eat():
    for predator in animals:
        if predator.size <= DIFFTOEAT:
            continue
        for prey in animals:
            if predator.size-DIFFTOEAT > prey.size: #eat
                if overlap_check(predator.x,predator.y,predator.size,prey.x,prey.y,prey.size+10):
                    predator.fullness+= (50+prey.size*2)
                    prey.die()
                    
                    
                    
def select_animal(mouseXY): #mark an animal that is at the mousexy as "selected" (to display stats)
    noneSelected = True
    for animal in animals:
        if mouseXY[0]+3>animal.x and mouseXY[0]-3<animal.x+animal.size and mouseXY[1]+3>animal.y and mouseXY[1]-3<animal.y+animal.size and noneSelected: #mouse in animal
                animal.selected=True
                noneSelected =False
        else:
            animal.selected=False

def draw_histogram(chartType,bigFont,smallFont):
    
    yConst = 2 #stretch graph height
    bucketSums = [0]*11
    buckets=[0]*11
    
    for animal in animals:
        if chartType ==   "none":
            return
        elif chartType == "lifespanInit":
            value = animal.lifespanInit ; buckets = [12.5,25,50,100,200,400,800,1200,1600,2400,"+"]
        elif chartType == "freePoint":
            value = animal.freePoint ; buckets = [0,1,2,3,4,5,6,7,8,9,"+"]
        elif chartType == "perception":
            value = animal.perception; buckets = [5,40,75,110,145,180,215,250,285,320,"+"]
        elif chartType == "size":
            value = animal.size; buckets = [1,4,7,10,13,16,22,28,37,46,"+"]
        elif chartType == "gestationTime":
            value = animal.gestationNeeded; buckets = [15,20,30,50,75,100,150,225,300,400,"+"]
        elif chartType == "speed":
            value = animal.speed; buckets = [1,2,3,4,5,6,7,8,9,10,"+"]
        elif chartType == "hungriness":
            value = animal.hungriness; buckets = [.07,.1,.15,.2,.3,.45,.6,.75,1,1.5,"+"]        
        
        for i in range(11):
            if buckets[i]=="+" or value <=buckets[i]:
                bucketSums[i]+=1
                break
    barN = 0        
    for bar in bucketSums:
        pygame.draw.rect(WIN,(200,200,200),(mapX-232+21*barN ,mapY-(bar*yConst)-12,20,bar*yConst))
        print_text(smallFont,str(buckets[barN]),mapX-232+21*barN+3,mapY-12)
        barN +=1
    print_text(bigFont,"S/L/F/P/G/D/H/N  "+chartType,mapX-232-240,mapY-20)
    
            
    
def draw_selected(animal,bigFont):
    print_text(bigFont,("Size: "+str(animal.size)),              mapX-125,15)
    print_text(bigFont,("Speed: "+str(animal.speed)),             mapX-125,35)
    print_text(bigFont,("GestCounter: "+str(round(animal.gestationCounter))),  mapX-125,55)
    print_text(bigFont,("GestNeeded: "+str(round(animal.gestationNeeded))),  mapX-125,75)
    print_text(bigFont,("Perception: "+str(animal.perception)),        mapX-125,95)            
    print_text(bigFont,("Lifespan: "+str(round(animal.lifespan))),          mapX-125,115)
    print_text(bigFont,("LifespanInit: "+str(round(animal.lifespanInit))),          mapX-125,135)
    print_text(bigFont,("Hungriness: "+str(round(animal.hungriness,2))),     mapX-125,155)
    print_text(bigFont,("Fullness: "+str(round(animal.fullness))),          mapX-125,175)
    print_text(bigFont,("Free Points: "+str(animal.freePoint)),          mapX-125,195)

    
def print_text(font,text,x,y,color=(255,255,255)):
    toPrint = font.render(str(text),1,color)
    WIN.blit(toPrint,(x,y))
    
def draw_window(smallFont,bigFont,activeGraph,FPS):
    WIN.fill((30,110,50)) #green
    
    for animal in animals:
        if animal.selected:
            draw_selected(animal,bigFont)
            pygame.draw.rect(WIN,(180,250,0),(animal.x,animal.y,animal.size,animal.size))
        else:
            pygame.draw.rect(WIN,animal.color,(animal.x,animal.y,animal.size,animal.size))
        
        sizeText= smallFont.render(str(animal.size),1,(255,255,255))
        WIN.blit(sizeText,(animal.x,animal.y))
        
    print_text(bigFont,len(animals),5,5)
    print_text(bigFont,"FPS "+str(round(FPS)),mapX-90,2)
    draw_histogram(activeGraph,bigFont,smallFont)
    pygame.display.update()
    
def killBig(thresh): #only kills half for some reason
    for animal in animals:
        if animal.size>thresh:
            animal.die()

def update_squaresLog(squaresLog,TIMER): 
    for animal in animals:
        squaresLog.write(str(animal.size)+","+
                         str(animal.speed)+","+
                         str(animal.perception)+","+
                         str(animal.lifespanInit)+","+
                         str(animal.hungriness)+","+
                         str(animal.gestationNeeded)+","+
                         str(animal.freePoint)+","+
                         str(animal.strainName)+","+
                         str(TIMER))
        squaresLog.write("\n")

def main():
    for _ in range(6): #initialize 12 squares
        Animal(2,4,(255,100, 90),155,452,452,40,200,0.075,2,"salmon",100) #salmon
        #Animal(2,4,(  0,  0,160),155,452,452,40,200,0.075,2,"blue",75)    #blue
        #Animal(2,4,(160,  0,  0),155,454,454,40,200,0.075,2,"red",50)     #red
        #Animal(2,4,(  0,160,  0),155,456,456,40,200,0.075,2,"green",25)   #green
    #SPEED 2 #SIZE 4 #color #GEST 160 # initxy #PERCEPT 40 #lifesp 200 #hungry .07 #freepoints 0-3 #strainName   
    TIMER=0
    FPSCAP = 90
    clock = pygame.time.Clock()
    
    smallFont=pygame.font.SysFont("comicsans",8)
    bigFont  =pygame.font.SysFont("comicsans",15)
    activeGraph = "size"

    squaresLog=open('squaresLog.csv','w')

    run = True
    while run:
        clock.tick(FPSCAP)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                select_animal(pygame.mouse.get_pos())
            elif event.type == pygame.QUIT:
                run =False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                activeGraph="none"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                activeGraph="lifespanInit"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                activeGraph="freePoint"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                activeGraph="perception"  
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                activeGraph="size" 
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                activeGraph="gestationTime"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                activeGraph="hungriness"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                activeGraph="speed"            
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                FPSCAP*=1.2
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                FPSCAP/=1.2
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                killBig(int(input("kill squares bigger than: ")))
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                Animal(5,22,(0,0,0),55,1,1,222,200,1,0,"z",33)        
                
                
                
        move(TIMER)
        make_children()
               
        draw_window(smallFont,bigFont,activeGraph,clock.get_fps())
        
        if TIMER%1000==0:
            print("log: ",int(TIMER/1000))
            update_squaresLog(squaresLog,TIMER/1000)
        
        TIMER +=1
         
    squaresLog.close()        
                
if __name__ == "__main__":
    main()