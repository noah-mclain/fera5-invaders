import pygame

class Egg:
    
    isDisappear=False
    
    def __init__(self,x,y) -> None:
        image=pygame.image.load('assets/images/Enemy/egg.png')
        self.width=10
        self.height=10
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.rect=self.image.get_rect(topleft=(x,y))
        self.speedY=2
        

    def draw(self,screen):
        screen.blit(self.image,self.rect)
    
    def update(self,screenHeight):
        self.rect.y+=self.speedY
        
        #if egg hits bottom of screen
        if self.rect.bottom>screenHeight:
            self.rect.bottom=screenHeight
            Egg.isDisappear=True

        #if egg hits spaceship?
    
    def shouldDisappear(self):
        return Egg.isDisappear  
        
            
        