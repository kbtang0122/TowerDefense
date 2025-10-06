import pygame
import math 
import sys
import random

pygame.init()
clock=pygame.time.Clock()

#顔色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN=(0,255,0)
BLUE=(0,0,255)
GRAY=(50,50,50)
Hover_shadow=(0,0,139,50)
Light_blue=(100,100,255,50)
 
#字體規格設定
font=pygame.font.Font(None,40)

#熒幕大小
Grid_size=10
Tile_size=80
screen_width=Grid_size*Tile_size
screen_height=Grid_size*Tile_size
screen=pygame.display.set_mode((screen_width,screen_height))

#游戲名字
pygame.display.set_caption('塔防游戲')

#背景音樂
# pygame.mixer_music.load('venv/assets/sounds/background_music.mp3')
# pygame.mixer_music.load('venv/assets/sounds/music.mp3')
# pygame.mixer_music.play(-1)

#圖片載入
enemy_image=pygame.image.load('venv/assets/images/death.png').convert_alpha()
tower_image=pygame.image.load('venv/assets/images/lighthouse.png').convert_alpha()
item_image=pygame.image.load('venv/assets/images/item.png').convert_alpha()
player_image=pygame.image.load('venv/assets/images/player.png').convert_alpha()
attack_image=pygame.image.load('venv/assets/images/attack.png').convert_alpha()
castle_image=pygame.image.load('venv/assets/images/castle.png').convert_alpha()
mushroom_image=pygame.image.load('venv/assets/images/mushroom.png').convert_alpha()
start_image=pygame.image.load('venv/assets/images/start.png').convert_alpha()
pause_image=pygame.image.load('venv/assets/images/pause.png').convert_alpha()
game_image=pygame.image.load('venv/assets/images/game.png').convert_alpha()
level_image=pygame.image.load('venv/assets/images/level.png').convert_alpha()
tank_image=pygame.image.load('venv/assets/images/tank.png').convert_alpha()
speed_image=pygame.image.load('venv/assets/images/speed.png').convert_alpha()
silent_image=pygame.image.load('venv/assets/images/silent.png').convert_alpha()
ice_image=pygame.image.load('venv/assets/images/ice.png').convert_alpha()
fire_image=pygame.image.load('venv/assets/images/fire.png').convert_alpha()

#圖片控制大小
enemy_image=pygame.transform.scale(enemy_image,(50,50))
tower_image=pygame.transform.scale(tower_image,(50,50))
item_image=pygame.transform.scale(item_image,(50,50))
player_image=pygame.transform.scale(player_image,(50,50))
attack_image=pygame.transform.scale(attack_image,(50,50))
castle_image=pygame.transform.scale(castle_image,(70,70))
mushroom_image=pygame.transform.scale(mushroom_image,(80,80))
start_image=pygame.transform.scale(start_image,(80,80))
pause_image=pygame.transform.scale(pause_image,(80,80))
game_image=pygame.transform.scale(game_image,(80,80))
level_image=pygame.transform.scale(level_image,(80,80))
tank_image=pygame.transform.scale(tank_image,(80,80))
speed_image=pygame.transform.scale(speed_image,(80,80))
silent_image=pygame.transform.scale(silent_image,(80,80))
ice_image=pygame.transform.scale(ice_image,(80,80))
fire_image=pygame.transform.scale(fire_image,(80,80))




pause_rect=pause_image.get_rect(center=(760,40))

#攻擊音效
# laser_sound=pygame.mixer.Sound('venv/assets/sounds/laser_sound.wav')
# laser_sound.set_volume(0.5)

#設置地圖 (4:主堡 , 1:敵人移動路徑 , 0:防禦塔放置位置)
map = [
    [0,1,0,0,3,3,3,3,2,2],
    [0,1,1,1,0,3,3,3,2,2],
    [3,0,0,1,0,3,3,3,3,3],
    [3,3,0,1,0,3,3,3,3,3],
    [3,3,0,1,0,0,0,0,0,3],
    [3,3,0,1,1,1,1,1,1,0],
    [3,3,3,0,0,0,0,0,1,0],
    [3,3,3,3,3,3,3,0,1,0],
    [3,3,3,3,3,3,3,0,1,0],
    [3,3,3,3,3,3,3,0,1,1]
]

#敵人移動路徑（順序）
PATH_POINTS=[]
for col in range(Grid_size):
    for row in range(Grid_size):
        if map[row][col]==1:
            PATH_POINTS.append((col*Tile_size+Tile_size//2,row*Tile_size+Tile_size//2))
#反序移動
# PATH_POINTS.sort(reverse=True)

#地圖繪製
def draw_map():
    for row in range(Grid_size):
        for col in range(Grid_size):
            rect=pygame.Rect(col*Tile_size,row*Tile_size,Tile_size,Tile_size)

            if map[row][col]==1:
                color=RED
            elif map[row][col]==0:
                color=GREEN

            pygame.draw.rect(screen,color,rect)
            pygame.draw.rect(screen,BLACK,rect,1)
            if map[row][col]==3:
                pygame.draw.rect(screen,BLACK,rect)
                screen.blit(mushroom_image,(col*Tile_size,row*Tile_size))



#tower資料
tower_option=[
    {'name':'Tower','image':tower_image},
    {'name':'Ice_tower','image':ice_image},
    {'name':'Fire_tower','image':fire_image}
              ]

#敵人
class Enemy:
    def __init__(self):
        self.path_index=0
        self.x,self.y=PATH_POINTS[self.path_index]
        self.max_speed=5
        self.max_health=50
        self.health=self.max_health
        self.damage=10
        self.image= enemy_image
        self.rect=self.image.get_rect(center=(self.x,self.y))
        self.reward=10
        self.slow=0

    def draw(self):
        self.rect.center = (self.x, self.y)
        screen.blit(self.image,self.rect)
        health_width=30
        health_ratio=self.health/self.max_health
        current_width=health_ratio*health_width

        health_max_bar=pygame.Rect(self.x-15,self.y-25,health_width,5)
        health_current_bar=pygame.Rect(self.x-15,self.y-25,current_width,5)
        pygame.draw.rect(screen,BLACK,health_max_bar,1)
        pygame.draw.rect(screen,WHITE,health_current_bar,1)

    def move(self):
        if self.path_index< len(PATH_POINTS)-1:
            target_x,target_y=PATH_POINTS[self.path_index+1]
            dx=target_x-self.x
            dy=target_y-self.y
            distance= math.sqrt(dx**2+dy**2)

            if(pygame.time.get_ticks()<self.slow):
                actual_speed = self.max_speed*0.5
            
            else:
                actual_speed=self.max_speed


            if distance>0:
                direction_x=dx/distance
                direction_y=dy/distance
                self.x+=direction_x*actual_speed
                self.y+=direction_y*actual_speed
                
            
            if distance<self.max_speed:
                self.path_index+=1
                if self.path_index< len(PATH_POINTS):
                    self.x,self.y=PATH_POINTS[self.path_index]

#坦克敵人
class Tank(Enemy):
    def __init__(self):
        super().__init__()
        self.max_speed=3
        self.max_health*=1.2
        self.health=self.max_health
        self.image=tank_image
        self.rect=self.image.get_rect(center=(self.x,self.y))

#速度敵人
class Speed(Enemy):
    def __init__(self):
        super().__init__()
        self.max_speed=5
        self.max_health*=0.9
        self.health=self.max_health
        self.image=speed_image
        self.rect=speed_image.get_rect(center=(self.x,self.y))

          
                    

#塔       
class Tower:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.level=1
        self.upgrade_cost=50
        self.damage=20
        self.attack_range=Tile_size*1.5
        self.attack_cooldown=1000 
        self.last_attack_time=0
        self.image=tower_image
        self.rect=self.image.get_rect(center=(self.x,self.y))

    def draw(self):
        screen.blit(self.image,self.rect)
        level_font=font.render(str(self.level),True,BLACK)
        screen.blit(level_font,(self.x-5,self.y-15))
        surface=pygame.Surface((self.attack_range*2,self.attack_range*2),pygame.SRCALPHA)
        pygame.draw.circle(surface,Light_blue,(self.attack_range,self.attack_range),self.attack_range)
        screen.blit(surface,(self.x-self.attack_range,self.y-self.attack_range))

    def attack(self,enemies):
        current_time=pygame.time.get_ticks()
        if current_time-self.last_attack_time > self.attack_cooldown:
            target=None
            min_distance=9999
            for enemy in enemies:
                distance = math.sqrt((self.x - enemy.x)**2 + (self.y - enemy.y)**2)
                if self.attack_range>= distance and min_distance>distance:
                    target=enemy
                    min_distance=distance
            if target:
                self.hit(target)
                self.last_attack_time=current_time
                # laser_sound.play()

    def hit(self,enemy):
        enemy.health-=self.damage

    def upgrade(self):
        self.damage+=10
        self.upgrade_cost*=2
        self.attack_range+=40
        self.level+=1




#冰塔
class Ice_tower(Tower):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.damage=10
        self.image=ice_image
        self.rect=self.image.get_rect(center=(self.x,self.y))

    def hit(self,enemy):
        enemy.health-=self.damage
        enemy.slow=pygame.time.get_ticks()+2000

#火塔
class Fire_tower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.damage=10
        self.image=fire_image
        self.rect=self.image.get_rect(center=(self.x,self.y))

    def attack(self,enemies):
        current_time=pygame.time.get_ticks()
        if current_time-self.last_attack_time > self.attack_cooldown:
            for enemy in enemies:
                distance = math.sqrt((self.x - enemy.x)**2 + (self.y - enemy.y)**2)
                if self.attack_range>=distance:
                    self.hit(enemy)
                    self.last_attack_time=current_time
                # laser_sound.play()
    




#主選單（初始頁面）
def main_menu():
    game_rect=game_image.get_rect(center=((Grid_size*Tile_size)//2,(Grid_size*Tile_size)//2))

    while True:
        screen.fill(WHITE)
        title=font.render('Plz find the button to start the game',True,(BLACK))
        screen.blit(title,(200,200))

        mouse_pos=pygame.mouse.get_pos()
        if game_rect.collidepoint(mouse_pos):
            hover_image=pygame.transform.scale(game_image,((game_rect.width*1.1),(game_rect.height*1.1)))
            hover_rect=hover_image.get_rect(center=(game_rect.center))
            screen.blit(hover_image,hover_rect)
        #     active_rect=hover_rect
        
        # else:
        #     screen.blit(game_image,game_rect)
        #     active_rect=game_rect

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                if game_rect.collidepoint(event.pos):
                    return True

        pygame.display.flip()
        clock.tick(60)


#stage通關畫面
def Stage_interface(stage):
    time=pygame.time.get_ticks()
    while pygame.time.get_ticks() -time <4000:
        screen.fill(BLACK)
        text=font.render(f'Stage{stage-1} complete',True,WHITE)
        next_text=font.render(f'Next Stage:{stage} ready to go',True,WHITE)
        screen.blit(text,(screen_width // 2 - text.get_width() // 2, 300))
        screen.blit(next_text, (screen_width // 2 - next_text.get_width() // 2, 400))
        pygame.display.flip()
        clock.tick(60)


#防禦塔建立清單UI
def Build_tower_menu():
        Tower_information=pygame.Rect(0,7*Tile_size,7*Tile_size,3*Tile_size)
        pygame.draw.rect(screen,GRAY,Tower_information)
        tower_list=[]

        for i,option in enumerate (tower_option):
            icon_x= (i*Tile_size)+Tile_size//2
            icon_y= 600
            image_rect=option['image'].get_rect(center=(icon_x,icon_y))
            screen.blit(option['image'],image_rect)
            tower_list.append((option['name'],image_rect))

        return tower_list











#暫停效果
def pause_menu():

    while True:
        screen.fill(GRAY)
        title=font.render("Status=Paused",True,WHITE)
        resume=font.render('Click anywhere to Resume',True,WHITE)
        screen.blit(title,((Grid_size*6)//2,(Grid_size*6)//2))
        screen.blit(resume,(300,500))

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                return
            
        pygame.display.flip()
        clock.tick(60)








#主程式
def main():
    enemies=[]
    towers=[]
    money=300
    tower_cost=50
    HP=100

    #敵人stage關卡
    stage=1
    enemy_amount=5
    enemy_spawned_amount=0
    spawn_time=pygame.time.get_ticks()+2000
    wave_cooldown=5000
    next_wave=False

    #塔資訊
    Selected_tower=None
    Show_tower_menu=None
    tower_list=[]
    upgrade_rect=level_image.get_rect(center=(screen_width//2+100,screen_height-40))

    #建立/升級防禦塔
    running=True
    while running:
        mouse_pos=pygame.mouse.get_pos()
        mouse_col=mouse_pos[0]//Tile_size
        mouse_row=mouse_pos[1]//Tile_size

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                clicked_on_tower=any(tower.rect.collidepoint(mouse_pos[0],mouse_pos[1]) for tower in towers)
                if clicked_on_tower:
                    for tower in towers:
                        if tower.rect.collidepoint(event.pos):
                            Selected_tower=tower
                            break
                        else:
                            Selected_tower=None

                if Selected_tower and upgrade_rect.collidepoint(event.pos):
                    if money>= Selected_tower.upgrade_cost:
                        money-=Selected_tower.upgrade_cost
                        Selected_tower.upgrade()

                elif 0<=mouse_col<Grid_size and 0<=mouse_row<Grid_size and not clicked_on_tower:
                    if map[mouse_row][mouse_col]==0 :
                        tower_x=(mouse_col*Tile_size)+Tile_size//2
                        tower_y=(mouse_row*Tile_size)+Tile_size//2
                        Build_tower=(tower_x,tower_y)
                        Show_tower_menu=True

                for name,rect in tower_list:
                    if rect.collidepoint(event.pos) and money>=tower_cost:
                        if name=='Tower':
                            towers.append(Tower(Build_tower[0],Build_tower[1]))
                        elif name=='Ice_tower':
                            towers.append(Ice_tower(Build_tower[0],Build_tower[1]))
                        elif name=='Fire_tower':
                            towers.append(Fire_tower(Build_tower[0],Build_tower[1]))

                        money-=tower_cost
                        Show_tower_menu=False
                        break

                        

                



            #點擊暫停按鈕效果觸發
            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                if pause_rect.collidepoint(event.pos):
                    pause_menu()



        #敵人生成/關卡設置
        now=pygame.time.get_ticks()
        if not next_wave:
            if enemy_amount>enemy_spawned_amount and now> spawn_time:
                enemy_type=random.choice([Enemy,Tank,Speed])
                enemy=enemy_type()
                enemy.health*=1.2
                enemy.max_health*=1.2
                enemies.append(enemy)
                enemy_spawned_amount+=1
                spawn_time = now + random.randint(800,1000)
        
        if enemy_spawned_amount>=enemy_amount and not enemies :
            if not next_wave:
                wave_clear_time=now
                next_wave=True

            if next_wave and now-wave_clear_time>wave_cooldown:
                stage+=1
                Stage_interface(stage)
                money+=150
                enemy_amount = enemy_amount + (stage*2)
                enemy_spawned_amount=0
                next_wave=False
                spawn_time= now +1000




        screen.fill(BLACK)
        draw_map()  

        #防禦塔建立選擇UI
        if Show_tower_menu:
            tower_list=Build_tower_menu()

        #暫停按鈕
        screen.blit(pause_image,pause_rect)


        #防禦塔升級UI
        if Selected_tower:
            Tower_information=pygame.Rect(0,screen_height-100,screen_width-250,100)
            pygame.draw.rect(screen,GRAY,Tower_information)

            info_text=font.render(f'Tower lv{Selected_tower.level}| Damage={Selected_tower.damage} | upgrade={Selected_tower.upgrade_cost}',True,WHITE)
            atkrange_text=font.render(f'Atk Range={Selected_tower.attack_range}',True,WHITE)
            screen.blit(info_text,(20,screen_height-100))
            screen.blit(atkrange_text,(20,screen_height-50))
            screen.blit(level_image,upgrade_rect)

        #關卡字幕顯示
        stage_font=font.render(f'Stage={stage}',True,WHITE)
        screen.blit(stage_font,(3*Tile_size,2*Tile_size))

        for enemy in enemies:
            enemy.move()
        for tower in towers:
            tower.attack(enemies)
        
        for enemy in enemies:
            if enemy.health<=0:
                money+=enemy.reward

        enemies=[enemy for enemy in enemies if enemy.health>0]

        for enemy in enemies:
            if enemy.path_index>=len(PATH_POINTS)-1:
                HP-=enemy.damage
                enemies.remove(enemy)



        #防禦塔可放置區域顯示
        if map[mouse_row][mouse_col]==0:
            shadow_rect=pygame.Rect(mouse_col*Tile_size,mouse_row*Tile_size,Tile_size,Tile_size)
            shadow_surface=pygame.Surface(shadow_rect.size,pygame.SRCALPHA)
            pygame.draw.rect(shadow_surface,Hover_shadow,shadow_surface.get_rect())
            screen.blit(shadow_surface,shadow_rect)


        for enemy in enemies:
            enemy.draw()

        for tower in towers:
            tower.draw()
        

        money_font=font.render(f'money={int(money)}',True,WHITE)
        HP_font=font.render(f'HP={int(HP)}',True,WHITE)
        screen.blit(money_font,(8*Tile_size,1*Tile_size))
        screen.blit(HP_font,(7*Tile_size,2*Tile_size))

        Game_Over=font.render(f'Game Over, U lose ',True,WHITE)

        #生命值判定，GAME_OVER
        if(HP<=0):
            screen.fill(BLACK)
            screen.blit(Game_Over,(5*Tile_size,2*Tile_size))
            pygame.display.flip()
            pygame.time.delay(3000)
            running=False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__=='__main__':
    if main_menu():
        main()