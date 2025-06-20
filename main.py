import pygame
import constants
from character import Character
from weapon import Weapon

pygame.init()



screen = pygame.display.set_mode((constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT))
pygame.display.set_caption('Dungeon Crawler')


#creating clock for FPS
clock = pygame.time.Clock()

#define player movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False

#define font
font = pygame.font.Font('assets/fonts/AtariClassic.ttf', 20)


# helper function to scale image
def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()

    return pygame.transform.scale(image,(w*scale, h*scale))


#load heart images
heart_empty = scale_img(pygame.image.load('assets/images/items/heart_empty.png').convert_alpha(), constants.ITEM_SCALE)
heart_half= scale_img(pygame.image.load('assets/images/items/heart_half.png').convert_alpha(), constants.ITEM_SCALE)
heart_full = scale_img(pygame.image.load('assets/images/items/heart_full.png').convert_alpha(), constants.ITEM_SCALE)

# load weapon image
bow_image = scale_img(pygame.image.load('assets/images/weapons/bow.png').convert_alpha(), constants.WEAPON_SCALE)
arrow_image = scale_img(pygame.image.load('assets/images/weapons/arrow.png').convert_alpha(), constants.WEAPON_SCALE)


#load character images
mob_animation = []
mob_types = ["elf", "imp", "skeleton", 'goblin', 'muddy', 'tiny_zombie', 'big_demon']

for mob in mob_types:
    animation_types = ["idle", "run"]
    #load images
    animation_list = []
    for animation in animation_types:
        #reset temprorary list of images
        temp_list = []
        for i in range(4):
            #player image
            img = pygame.image.load(f'assets/images/characters/{mob}/{animation}/{i}.png').convert_alpha()
            img = scale_img(img, constants.SCALE)
            temp_list.append(img)

        animation_list.append(temp_list)
    mob_animation.append(animation_list)

# display game info
def draw_info():
    pygame.draw.rect(screen, constants.PANEL, (0,0,constants.SCREEN_WIDTH, 50))
    pygame.draw.line(screen,constants.WHITE, (0,50), (constants.SCREEN_WIDTH, 50))
    #draw lives
    half_heart_drawn = False
    for i in range(5):
        if player.health >= ((i+1)*20):
            screen.blit(heart_full, (10 + i * 50, 0))
        elif (player.health % 20 > 0) and half_heart_drawn == False:
            half_heart_drawn = True
            screen.blit(heart_half, (10 + i * 50, 0))
        else:
            screen.blit(heart_empty, (10 + i * 50, 0))


# damage text class
class DamageText(pygame.sprite.Sprite):
    def __init__(self,x,y,damage,color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.counter = 0

    def update(self):
        # move damage text up
        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30:
            self.kill()

# create player
player = Character(100,100,15, mob_animation, 0)

# create enemy
enemy = Character(200,300, 100,mob_animation, 1)

# create weapon
bow = Weapon(bow_image,arrow_image)

#create empty enemy list
enemy_list = []
enemy_list.append(enemy)

#sprite groups
damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()


#main game loop
run = True

while run:

    clock.tick(constants.FPS)

    screen.fill(constants.BG)

    #calculate player movement
    dx = 0
    dy = 0
    if moving_right == True:
        dx = constants.SPEED
    if moving_left == True:
        dx = -constants.SPEED
    if moving_up == True:
        dy = -constants.SPEED
    if moving_down == True:
        dy = constants.SPEED


    #move player
    player.move(dx,dy)

    # update enemy
    for enemy in enemy_list:
        enemy.update()


    #update player
    player.update()
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)
    for arrow in arrow_group:
        damage, damage_pos = arrow.update(enemy_list)
        if damage:
            damage_text = DamageText(damage_pos.centerx,damage_pos.y, str(damage), constants.RED)
            damage_text_group.add(damage_text)
    damage_text_group.update()



    #draw player on the screen
    for enemy in enemy_list:
        enemy.draw(screen)
    player.draw(screen)
    bow.draw(screen)
    for arrow in arrow_group:
        arrow.draw(screen)
    damage_text_group.draw(screen)
    draw_info()



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        #keyboard bytton pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False 
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True     
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True

                #keyboard bytton up
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False     
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False
            
        
    pygame.display.update()

pygame.quit()