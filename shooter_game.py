from pygame import *
from random import randint
from time import time as timer

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')






points = 0
lost = 0

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,player_wight,player_height,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(player_wight,player_height))
        self.size_x = player_wight
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width-85:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.y, 15, 20, -20 )
        bullets.add(bullet)
#классс  пуль
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
           self.kill()

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height+50:
            self.rect.y = -50
            self.rect.x = randint(0,win_width-80)
            if self.size_x == 80:
                lost += 1




font.init()
font1 = font.SysFont('Arial',80)
font2 = font.SysFont('Arial',36)
win = font1.render('Матиматик отменили,', True,(255,255,255))
win1 = font1.render('ураааа:)', True,(255,255,255))

lose = font1.render('Иду на математик,', True,(180,5,5))
lose1 = font1.render('плачу:(', True,(180,5,5))
win_width = 700
win_height = 500
window = display.set_mode((win_width,win_height))
display.set_caption('Галактический мусор атакует самсунг гелаксти 50км')
background = transform.scale(image.load('galaxy.jpg'),(win_width,win_height))

samsung = Player('rocket.png',win_width/2-40, win_height - 110,80,100,10)
iphones = sprite.Group()
bullets = sprite.Group()
for i in range(6):
    iphone = Enemy('ufo.png', randint(0,win_width-80),-50, 80,50,randint(1,5))
    iphones.add(iphone)

nokias = sprite.Group()
for i in range(6):
    nokia = Enemy('asteroid.png', randint(0,win_width-80),-50, 50,50,randint(5,15))
    nokias.add(nokia)

num_fire = 0
game = True
finish = False
clock = time.Clock()

rel_time = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                if num_fire < 5 and rel_time == False:
                    samsung.fire()
                    fire_sound.play()
                    num_fire += 1

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True



    if not finish:
        window.blit(background,(0,0))
        samsung.reset()
        iphones.draw(window)
        bullets.draw(window)
        nokias.draw(window)



        samsung.update()
        iphones.update()
        bullets.update()
        nokias.update()
        
        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('ПЕРЕЗЯРЯЖАЮЮЮЮЮЮЮЮЮЮЮСЬ!!!!', 1,(250,0,0))
                window.blit(reload,(90,win_height-70))
            else:
                num_fire = 0
                rel_time = False

        text_point = font2.render('Счёт:'+str(points), True,(5,180,5))
        window.blit(text_point,(10,10))
        
        text_lost = font2.render('Пропущенно:'+str(lost), True,(180,5,5))
        window.blit(text_lost,(10,60))

        sprites_list = sprite.groupcollide(iphones, bullets, True, True)
        for t in sprites_list:
            points += 1
            iphone = Enemy('ufo.png', randint(0,win_width-80),-50, 80,50,randint(1,5))
            iphones.add(iphone)

        if points > 9:
            finish = True
            window.blit(win,(50,250))
            window.blit(win1,(50,300))

        if lost > 2:
            finish = True
            window.blit(lose,(50,250))            
            window.blit(lose1,(50,300))            


        display.update()
    else:
        time.delay(3000)
        finish = 0
        points = 0
        lost = 0
        for b in bullets:
            b.kill()
        for i in iphones:
            i.kill()
        for i in range(6):
            iphone = Enemy('ufo.png', randint(0,win_width-80),-50, 80,50,randint(1,5))
            iphones.add(iphone)
    time.delay(30)

