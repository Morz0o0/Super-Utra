from time import time as timer
from pygame import *
from random import randint

mixer.init()
mixer.music.load("space.ogg")
#mixer.music.play()
fire_sound = mixer.Sound("space.ogg")
 
score = 0 
lost = 0 
life = 3

font.init()
font2 = font.Font(None,36)
win = font2.render("You win!!!:)",True,(255,255,255))
lose = font2.render("Нажаль ви програли",True,(171,33,33))


win_width = 700
win_height = 500
display.set_caption("Star War ")
window = display.set_mode((win_width,win_height))
background = transform.scale(image.load("galaxy.png"),(win_width,win_height))
fon = transform.scale(image.load("galaxy.jpg"),(win_width,win_height))


class GamaSprite(sprite.Sprite):

    def __init__(self, player_image,player_x,player_y, size_x,size_y, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x,self.rect.y))

class Player(GamaSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed 
        if keys[K_RIGHT] and self.rect.x < win_width-80:
            self.rect.x += self.speed 

    def fire(self):
        bullet = Bullet("bullet.png",self.rect.centerx,self.rect.top, 10, 20, 20)
        bullets.add(bullet)



class Enemy(GamaSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if  self.rect.y > win_height:
            self.rect.x = randint(80,win_width-80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GamaSprite):
    def update(self):
        self.rect.y -=self.speed


        if self.rect.y < 0:
            self.kill()
def collidepoint(self, x, y):
    return self.rect.collidepoint(x, y)






ship = Player("rocket.png", 5 , win_height-100,120,100,20)
#life = GamaSprite("")

monsters = sprite.Group()

for i in range(6):
    monster = Enemy("ufo.png", randint(80,win_width-80), -40,80 ,50 ,randint(1,5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(30,win_width-30), -40,80 ,60 ,randint(1,5))
    asteroids.add(asteroid)
bullets = sprite.Group()
isMenu = True
finish = True
run = True
rel_time = False
num_fire = 0
clock = time.Clock()
while run:
     

    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                #ship.fire()
                #fire_sound.play()
                if num_fire < 8 and rel_time == False:
                    num_fire += 1
                    ship.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    if isMenu:
        window.blit(fon,(0,0))
        text_natusnit = font2.render("Натисніть Enter для початку гри",2,(0,59,89))
        window.blit(text_natusnit,(150,400))
        for e in event.get():            
            if e.type == KEYDOWN:
                if e.key == K_RETURN:
                    isMenu = False
                    finish = False
        display.update()

        
        
    
                    

    if not finish:
        window.blit(background,(0,0))

        text = font2.render("Счет: " + str(score),2,(0,225,21))
        window.blit(text,(10,20))

        text_lose = font2.render("Пропуск: " + str(lost),1,(85,132,255))
        window.blit(text_lose,(10,50))
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        if rel_time ==True:
            now_time = timer()
            if now_time - last_time < 3:
                relead = font2.render('Wait........reload',1 ,(157, 59, 45))   
                window.blit(relead, (250, 450))
            else:
                num_fire = 0
                rel_time = False 
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        sprites_list = sprite.groupcollide(monsters,bullets, True,True)

        for c in sprites_list:
            score += 1
            monster = Enemy("ufo.png", randint(80,win_width-80), -40,80 ,50 ,randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life -=1

        if score >= 10:
            finish = True
            window.blit(win,(win_width/2-100,win_height/2))
        sprites2_list = sprite.spritecollide( ship, monsters, True)
        if lost >= 3 or life == 0:
            finish = True
            window.blit(lose,(win_width/2-100,win_height/2))
        
                                      
        if life == 3:
            life_color = (0, 150, 0)
        elif life == 2:
            life_color = (150, 150, 0)
        elif life == 1:
            life_color = (150, 0, 0) 
        else:
            life_color = (0, 0, 0)
        text_life = font2.render(str(life), 1, (life_color))
        window.blit(text_life, (650, 10))   
        display.update()
    

    clock.tick(40)