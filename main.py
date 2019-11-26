import pygame, classes, random

clock = pygame.time.Clock()
framerate = 500
time = 0

health = 50            #defining important variables
boss_health = 5040
level = 1
xp = 0
boss_countdown = 3
super_countdown = 10
boss_death_countdown = 6
timer = 0

bullet_directions = [(1,0),(-1,0),(0,1),(0,-1),(0.5,0.5),(-0.5,0.5),(0.5,-0.5),(-0.5,-0.5)]     #these are used in for loops to create alot of class variables efficiently
background_positions = [(0,0),(0,1080),(0,-1080),(1920,0),(-1920,0),(1920,1080),(-1920,1080),(1920,-1080),(-1920,-1080)]

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0) #colors used
blue = (0,0,255)
purple = (255,0,255)
gold = (255,215,0)

pygame.init()
pygame.mixer.init(22050, -16, 2, 64) #this makes it so the delay on sound effect is alot less

game_music = pygame.mixer.music.load("PygameGameMusic.mp3")
win_sound = pygame.mixer.Sound("Win.wav")
lose_sound = pygame.mixer.Sound("Lose.wav")
shoot_sound = pygame.mixer.Sound("Shoot.wav") #defining all music
levelup_sound = pygame.mixer.Sound("LevelUp.wav")

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
logo = pygame.image.load("PygameLogo.png")  #setting up display
pygame.display.set_icon(logo)
pygame.display.set_caption("PIXEL WARRIOR")

player = classes.Player(screen)

health_text = classes.Score(25, (1100, 30))
level_text = classes.Score(25, (100, 30))
xp_text = classes.Score(25, (1600, 30))
super_text = classes.Score(25, (500, 30))
time_text = classes.Score(25,(875, 30))
                                                #All text used in game
title_text = classes.Score(60, (612, 325))
subtitle_text = classes.Score(30, (675, 600))
win_text = classes.Score(60,(762,325))
lose_text = classes.Score(60,(738,325))
quit_text = classes.Score(30,(687,600))
pause_text = classes.Score(60,(780,325))
resume_text = classes.Score(30,(663,675))
boss_text = classes.Score(60, (732,325))

player_sprites = pygame.sprite.Group()
nonplayer_sprites = pygame.sprite.Group()
background_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()      #all sprite groups used
bullet_sprites = pygame.sprite.Group()
score_sprites = pygame.sprite.Group()
title_text_sprites = pygame.sprite.Group()
super_bullet = pygame.sprite.Group()

for x in background_positions:
    temp_background = classes.Background(x)
    background_sprites.add(temp_background)  #quickly defining all 9 background images
    nonplayer_sprites.add(temp_background)

player_sprites.add(player)
score_sprites.add(health_text)
score_sprites.add(level_text)  #adding all needed variables to sprite group
score_sprites.add(xp_text)
score_sprites.add(super_text)
score_sprites.add(time_text)
title_text_sprites.add(title_text)
title_text_sprites.add(subtitle_text)

pygame.mixer.music.play(-1)    #starting game music
pygame.time.set_timer(pygame.USEREVENT, 1000) #this timer is for the super ability, but is also used at the end during the boss death animation

on_boss_start = True
start = True
run = True
boss = False   #all booleans used in while loops
lose = False
win = False
pause = False
boss_intro = False
can_super = False

title_text.draw("PIXEL WARRIOR", "", "", black)
subtitle_text.draw("Press ENTER To START", "", "", black)
health_text.draw("HEALTH: ", health, "/" + str(50), black)
level_text.draw("LEVEL: ", level, "", black)
xp_text.draw("XP: ", xp, "/" + str(100), black)
win_text.draw("YOU WIN!", "", "", black)      #drawing all text used
lose_text.draw("YOU DIED!", "", "", black)
quit_text.draw("Press ESCAPE To QUIT", "", "", black)
pause_text.draw("PAUSED", "", "", black)
resume_text.draw("Press ENTER To RESUME", "", "", black)
super_text.draw("SUPER: ", super_countdown, "", black)
time_text.draw("TIME: 0", "", "", black)

"""All different times when you can see the screen but are not able to control the character are there own for loop with its own
event for loop and drawing all needed sprites to the screen each frame, this is because the game should always be able to quit,
and if the screen is not drawn every frame the program can crash.
"""

while start == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                start = False
                                    #intro screen, draws the title and intro text, as well as takes the enter input to start
    screen.fill(white)
    background_sprites.draw(screen)
    player_sprites.draw(screen)
    title_text_sprites.draw(screen)
    score_sprites.draw(screen)
    pygame.display.flip()

while run:          #main for loop
    time = clock.tick(framerate)/10 #time is used in all functions where things move, it is good to define it first

    health_max = 25 + (level * 25)
    xp_max = 100 * level
    damage = 5 + (level * 5)
    player_speed = 9 + level        #redifine all of these before anything else incase they are used in programs below
    enemy_cap = 5 + (level * 2)

    if xp >= xp_max:
        levelup_sound.play()
        level +=1            #plays a level up sound along with reseting the health to current level max health.
        xp = 0
        health = 25 + (level * 25)

    enemy_list = [] #this list only contains possible enemies that could be spawned, not enemies currently in the game.
                    #if this is not reset every frame but instead enemies are only added once the same enemy will spawn in
                    #when the enemy loop is hit. This means that all enemies of the same type are in the same spot, to prevent this
                    #enemies are reset each frame

    for event in pygame.event.get():        #main event loop, contains code for quiting, pausing, shooting, and shooting the super
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0] == True:
                shoot_sound.play()
                mouse_position = pygame.mouse.get_pos()
                temp_bullet = classes.Bullet(screen, black, mouse_position, (20,20), 1, 0, 0)
                bullet_sprites.add(temp_bullet)
        if event.type == pygame.USEREVENT:
            super_countdown -= 1
            timer += 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause = True
            if event.key == pygame.K_SPACE and can_super == True:
                mouse_position = pygame.mouse.get_pos()
                temp_bullet = classes.Bullet(screen, black, mouse_position, (40,40), 1, 0, 0)
                super_bullet.add(temp_bullet) #each time the timer is called the countdown is minus 1. When it reaches 0 this if statement can be called,
                super_countdown = 10            #once called the countdown is reset to 10 and this if statement can no longer be called
                can_super = False

    if super_countdown == 0: #for timer
        can_super = True

    if level >= 1:
        enemy_list.append(classes.Enemy(screen, green, 30, 5, (40,40), 10, 3, False))
    if level >= 3:
        enemy_list.append(classes.Enemy(screen, red, 50, 10, (50,50), 20, 4, False))
    if level >= 5:
        enemy_list.append(classes.Enemy(screen, blue, 70, 20, (50,50), 40, 5, False))  #each round this adds the possible enemies that can be spawned to the enemy list
    if level >= 7:                                                                      #as you level up this possible list gets bigger
        enemy_list.append(classes.Enemy(screen, purple, 100, 30, (30,30), 60, 7, False))
    if level >= 8:
        enemy_list.append(classes.Enemy(screen, gold, 150, 50, (70,70), 80, 3, False))
    if level >= 10 and on_boss_start == True:
        on_boss_start = False
        boss = True         #these change what some of the loops do
        boss_intro = True
        boss_music = pygame.mixer.music.load("PygameBossMusic.mp3")         #once level 10 is reached the boss battle is initiated, this code can only run once
        pygame.mixer.music.play(-1)
        for enemy in enemy_sprites:
            enemy_sprites.remove(enemy)
        temp_enemy = classes.Enemy(screen, black, 10000, 0, (250,250), 0, 10, True) #this calls the boss enemy and does not let any other enemies be called
        enemy_sprites.add(temp_enemy)
        nonplayer_sprites.add(temp_enemy)
        pygame.time.set_timer(pygame.K_BACKSPACE, 1000) #this sets a timer for the boss countdown, while backspace could be used to bypass that, as long as no one
                                                        #knows this could be done it doesnt really matter
    if len(enemy_sprites) < enemy_cap and boss == False:
        if len(enemy_list) < 2:                 #this adds a random enemy of the current enemy pool if the amount of enemies is less than the cap
            temp_enemy = enemy_list[0]
        else:
            randnum = random.randint(0,len(enemy_list) - 1)
            temp_enemy = enemy_list[randnum]
        enemy_sprites.add(temp_enemy)
        nonplayer_sprites.add(temp_enemy)

    for enemy in enemy_sprites:     #this is a loop that runs for all enemies in the game currently, all collisions happen in this for loop
        enemy.enemy_move(time, enemy_sprites)
        if enemy.rect.colliderect(player.rect) == True:
            if boss == True:
                health -= 100
                enemy.rect.x = 835      #if the boss hits you during the fight, 100 damage is done and it is reset to the tio
                enemy.rect.y = -250
            elif boss == False:
                enemy.on_death(enemy, enemy_sprites)
                health -= enemy.damage      #if not the boss fight then reqular damge is done and enemy is destroyed
        for bullet in bullet_sprites:
            if enemy.rect.colliderect(bullet.rect):
                if boss == True:
                    boss_health -= damage       #the boss health is seperate from its class so it can be used to the heath bar
                enemy.bullet_collide(damage)    #else, when a bullet hits a enemy it does damage and the bullet it destroyed
                bullet_sprites.remove(bullet)
        for bullet in super_bullet:
            if enemy.rect.colliderect(bullet.rect):
                if boss == True:
                    boss_health -= 100                        #tests collision of the super bullet
                enemy.bullet_collide(100)   #when the bullet is destroyed 8 more bullets are spawned at the same location
                super_position = bullet.rect    #going out in all directions
                super_bullet.remove(bullet)
                for x in bullet_directions:
                    temp_bullet = classes.Bullet(screen, black, 0, (20,20), 2, x, super_position)
                    bullet_sprites.add(temp_bullet)
        if enemy.health <= 0:
            enemy.on_death(enemy, enemy_sprites)
            xp += enemy.xp
        if enemy.rect.x > 2880 or enemy.rect.x < -960 or enemy.rect.y > 1620 or enemy.rect.y < -540:
            enemy_sprites.remove(enemy) #if the enemy goes beyond 1.5 times the game window, it is destroyed. If this is not here, enemies could get clogged very
                                        #far off screen and enemy spawning could slow or stop
    for bullet in bullet_sprites:
        bullet.bullet_move(time)
        if (bullet.rect.x > screen.get_width()) or (bullet.rect.x < 0):
            bullet_sprites.remove(bullet)                   #moves current bullets and tests if they are off screen
        if (bullet.rect.y > screen.get_height()) or (bullet.rect.y < 0):
            bullet_sprites.remove(bullet)
    for bullet in super_bullet:
        bullet.bullet_move(time)
        if (bullet.rect.x > screen.get_width()) or (bullet.rect.x < 0):
            super_bullet.remove(bullet)     #moves current super bullets and tests if it goes off screen
        if (bullet.rect.y > screen.get_height()) or (bullet.rect.y < 0):
            super_bullet.remove(bullet)

    for background in background_sprites: #this is for the infinitly scrolling background, see classes
        background.move()

    health_text.draw("HEALTH: ", health, "/" + str(health_max), black)
    level_text.draw("LEVEL: ", level,"", black) #redrawing health, xp, and level incase they have changed
    xp_text.draw("XP: ", xp, "/" + str(xp_max), black)
    time_text.draw("TIME:",timer, "", black)
    if super_countdown <= 0:
        super_text.draw("SUPER: ", "SHOOT!", "", black)  #this draws the number in super_countdown unless 0 or below, then it says SHOOT
    else:
        super_text.draw("SUPER: ", super_countdown, "", black)

    if health <= 0:
        pygame.mixer.music.pause() #if health is 0, lose is true
        lose_sound.play()
        run = False
        lose = True

    if boss_health <= 0:
        for enemy in enemy_sprites:
            boss_position = (enemy.rect.x + 125 ,enemy.rect.y + 125)
        for bullet in bullet_sprites:
            bullet_sprites.remove(bullet) #if boss health is 0, win is true
        pygame.mixer.music.pause()
        win_sound.play()
        run = False
        win = True
    if boss_health < 0:
        boss_health = 0

    classes.move(nonplayer_sprites, player_speed, time) #moves all sprites that are not connected to the player/in the game world, does not include bullets

    screen.fill(white)
    background_sprites.draw(screen)
    player_sprites.draw(screen) #draws all sprites
    enemy_sprites.draw(screen)
    bullet_sprites.draw(screen)
    super_bullet.draw(screen)
    score_sprites.draw(screen)
    if boss == True:
        pygame.draw.rect(screen, black, (100, 905, 1720, 100))
        pygame.draw.rect(screen, white, (120, 920, 1680, 70))       #If boss fight, draw the health bar
        pygame.draw.rect(screen, black, (120, 920, (boss_health / 3), 70))
    pygame.display.flip()
    clock.tick(framerate)

    while pause == True:    #this draws all current sprites but does not run any game functions, if pause is true
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: #from the pause screen, you can either return, or quit
                    quit()
                if event.key == pygame.K_RETURN:
                    pause = False

        screen.fill(white)
        background_sprites.draw(screen)
        player_sprites.draw(screen)
        enemy_sprites.draw(screen)
        bullet_sprites.draw(screen)
        super_bullet.draw(screen)
        score_sprites.draw(screen)
        screen.blit(quit_text.image, (quit_text.rect.x, quit_text.rect.y))
        screen.blit(pause_text.image, (pause_text.rect.x, pause_text.rect.y))
        screen.blit(resume_text.image, (resume_text.rect.x, resume_text.rect.y))
        if boss == True:
            pygame.draw.rect(screen, black, (100, 905, 1720, 100))
            pygame.draw.rect(screen, white, (120, 920, 1680, 70)) #incase paused during boss battle
            pygame.draw.rect(screen, black, (120, 920, (boss_health / 3), 70))
        pygame.display.flip()
        clock.tick(framerate)

    while boss_intro == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.K_BACKSPACE:
                boss_countdown -= 1 #this loop runs when the boss fight starts

        boss_text.draw("BOSS IN: ", str(boss_countdown), "", black)
        if boss_countdown == 0:
            boss_intro = False #draws a 3 second countdown and leaves imediatly after

        screen.fill(white)
        background_sprites.draw(screen)
        player_sprites.draw(screen) #does not draw health bar, because it is always before the boss fight
        score_sprites.draw(screen)
        screen.blit(boss_text.image, (boss_text.rect.x, boss_text.rect.y))
        pygame.display.flip()
        clock.tick(framerate)

while win == True:
    for event in pygame.event.get():  #this only runs if boss health becomes 0,
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()
        if event.type == pygame.USEREVENT and boss_death_countdown > 0 and boss == True:  #this for the simple boss death animation, bullets are shot 6 times and then boss dissapears
            for x in bullet_directions:
                temp_bullet = classes.Bullet(screen, black, 0, (20,20), 2, x, boss_position)  #used the same timer as the super shot, so does not always last the same amount of time
                bullet_sprites.add(temp_bullet)
            boss_death_countdown -= 1
    if boss_death_countdown == 0 and boss == True:
        for enemy in enemy_sprites:
            enemy_sprites.remove(enemy)

    for bullet in bullet_sprites: #this still moves bullet sprites even though everything else is unmoving
        bullet.bullet_move(time)

    screen.fill(white)
    background_sprites.draw(screen)
    player_sprites.draw(screen)
    enemy_sprites.draw(screen)
    bullet_sprites.draw(screen)
    score_sprites.draw(screen)
    screen.blit(win_text.image, (win_text.rect.x, win_text.rect.y))
    screen.blit(quit_text.image, (quit_text.rect.x, quit_text.rect.y))
    pygame.draw.rect(screen, black, (100, 905, 1720, 100))
    pygame.draw.rect(screen, white, (120, 920, 1680, 70))  #no if statement for these, because win can only start from the boss fight
    pygame.draw.rect(screen, black, (120, 920, (boss_health / 3), 70))
    pygame.display.flip()
    clock.tick(framerate)

while lose == True: #if health is 0 at anytime during the game this plays
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()

    screen.fill(white)
    background_sprites.draw(screen)
    player_sprites.draw(screen)
    enemy_sprites.draw(screen)
    score_sprites.draw(screen)
    screen.blit(lose_text.image, (lose_text.rect.x, lose_text.rect.y))
    screen.blit(quit_text.image, (quit_text.rect.x, quit_text.rect.y))
    if boss == True:
        pygame.draw.rect(screen, black, (100, 905, 1720, 100))
        pygame.draw.rect(screen, white, (120, 920, 1680, 70))  #incase lose during boss fight
        pygame.draw.rect(screen, black, (120, 920, (boss_health / 3), 70))
    pygame.display.flip()
    clock.tick(framerate)

pygame.quit() #if all loops do not run for some reason, then this is a backup