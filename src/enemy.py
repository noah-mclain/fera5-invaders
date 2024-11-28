# Enemy class for chicken behavior
import pygame
class Chicken:

    chicken_counter=0
    
    def __init__(self,x,y) -> None:
        image=pygame.image.load('assets/images/Enemy/chiken.png')
        self.width = 50
        self.height = 50
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.isChickenAlive=True
        self.rect=self.image.get_rect(topleft=(x,y))
        Chicken.chicken_counter+=1
        
        self.speed_x = 2
        self.direction = 1
       
    
    def draw(self,screen):
        if self.isChickenAlive:
            screen.blit(self.image,self.rect)

    def update(self, screenWidth,screenHeight):
        if not self.isChickenAlive:
            return
        
        self.rect.x += self.speed_x * self.direction
        
        if self.rect.left <= 0:
            self.direction =1
            self.rect.y += 20
        elif self.rect.right >= screenWidth:
            self.direction = -1
            self.rect.y += 20
            
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screenHeight:
            self.rect.bottom = screenHeight
        

    def killChicken(self):   
        if self.isChickenAlive:
            death_image = pygame.image.load('assets/images/Enemy/dead.png')
            self.image = pygame.transform.scale(death_image, (50, 50))
            Chicken.chicken_counter-=1
            self.isChickenAlive=False

    # def __del__(self): # to kill the chicken
    @staticmethod
    def get_chicken_count():
        return Chicken.chicken_counter

    def layEggs():
        pass

