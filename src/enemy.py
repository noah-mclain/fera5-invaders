# Enemy class for chicken behavior
import pygame
class Chicken:

    chickenCounter=0
    
    def __init__(self,x,y) -> None:
        self.image=pygame.image.load('/assets/images/Enemy/chiken.png')
        self.x=x
        self.y=y
        self.isChickenAlive=True
        self.rect=self.image.get_rect(top_left=(x,y))
        chickenCounter+=1


    # def moveLeft(self,left):
    #     self.x-=left
    #     self.rect.x=self.x
        

    # def moveRight(self,right):
    #     self.x+=right
    #     self.rect.x=self.x
       
    
    def draw(self,screen):
        screen.blit(self.image,self.rect)
        
        
        
    def update(self,xChange,yChange,screenWidth,screenHeight):
        self.rect.x+=xChange
        self.rect.y+=yChange
        
        if self.rect.x<0 : 
            self.rect.x=0
        elif self.rect.x>screenWidth-self.rect.x:
            self.rect.x=screenWidth
            
        if self.rect.y<0: 
            self.rect.y=0
        elif self.rect.y>screenHeight- self.rect.y:
            self.rect.y=screenHeight
        

    def killChicken(self):   
        self.image=pygame.image.load('/assets/images/Enemy/dead.png') 
        chickenCounter-=1
        self.isChickenAlive=False

    # def __del__(self): # to kill the chicken
            

    def layEggs():
        pass

