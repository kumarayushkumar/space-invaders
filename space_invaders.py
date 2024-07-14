import pygame, sys, random, time, math
pygame.init()

#Title_and_icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('./images/spaceship.png')
pygame.display.set_icon(icon)

height = 600
width = 800
marginX = 20
marginY = 15
ship_img_px = 64
gameover_height = 120
ship_bullet_height_bt = 100

#sounds
shoot = pygame.mixer.Sound("./sounds/shoot.wav")
explosion = pygame.mixer.Sound("./sounds/explosion.wav")

bg_img = pygame.image.load('./images/bg.jpg')
bg_img = pygame.transform.scale(bg_img, (width, height))

ship_img = pygame.image.load('./images/spaceship.png')
ship_coordinateX = (width / 2) - (ship_img_px / 2)
ship_coordinateY = height - ship_bullet_height_bt
ship_coordinate_change = 0
ship_speed_px = 3

enemy_img = []
enemy_coordinateX = []
enemy_coordinateY = []
enemy_coordinateX_change = []
enemy_coordinateY_change = []
no_of_enemy = 6

for i in range(no_of_enemy):
    enemy_img.append(pygame.image.load('./images/enemy.png'))
    enemy_coordinateX.append(random.randint(marginX + 1, width - (ship_img_px + marginX + 1)))
    enemy_coordinateY.append(random.randint(marginY, height / 10))
    enemy_speed_px = 1.5
    enemy_coordinateX_change.append(enemy_speed_px)
    enemy_coordinateY_change.append(60)

bullet_img = pygame.image.load('./images/bullet.png')
bullet_img = pygame.transform.scale(bullet_img, (16, 16))
bullet_coordinateX = 0
bullet_coordinateY = height - ship_bullet_height_bt
bullet_coordinateX_change = 0

bullet_speed_px = 6
is_bullet_moving = False

gameover_img = pygame.image.load('./images/gameover.png')
gameover_img = pygame.transform.scale(gameover_img, (width,height))

#score_board
score = 0
font = pygame.font.Font("freesansbold.ttf",32)
score_boardX = 5
score_boardY = 5

def scoreBoard(x, y):
    score_board = font.render("Score: " + str(score), True, (255,255,255))
    screen.blit(score_board, (x, y))

def shipFunc(x, y):
    screen.blit(ship_img, (x, y))

def enemyFunc(x, y, i):
    screen.blit(enemy_img[i], (x, y))

def fireBulletFunc(x,y):
    global is_bullet_moving
    is_bullet_moving = True
    screen.blit(bullet_img, (x + 24, y + 2))

def collision(enemy_coordinateX, enemy_coordinateY, bullet_coordinateX, bullet_coordinateY):
    dist_bw = math.sqrt((math.pow(enemy_coordinateX - bullet_coordinateX, 2)) + (math.pow(enemy_coordinateY - bullet_coordinateY, 2)))
    if dist_bw < 30: 
        return True
    else: 
        return False

def gameOver():
    screen.blit(gameover_img, (0, 0))
    scoreBoard((width / 2) - 40, height / 10)
    pygame.display.update()
    time.sleep(3)
    sys.exit()

screen = pygame.display.set_mode((width, height))    #width_&_height_of_Frame
is_running = True

while is_running:
    screen.fill((25, 25, 25))                     #screen_color
    screen.blit(bg_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        
        #------------Key stroke------------
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                ship_coordinate_change = -ship_speed_px
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                ship_coordinate_change = ship_speed_px
            if event.key == pygame.K_SPACE:
                if is_bullet_moving == False:
                    bullet_coordinateX = ship_coordinateX
                    shoot.play()
                    fireBulletFunc(bullet_coordinateX, bullet_coordinateY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                ship_coordinate_change = 0

    #-------------ship_movement-------------
    if ship_coordinateX >= marginX and ship_coordinateX <= width - (ship_img_px + marginX):
        ship_coordinateX += ship_coordinate_change
    elif ship_coordinateX <= marginX:
        ship_coordinateX = marginX + 1
    elif ship_coordinateX >= width - (ship_img_px + marginX):
        ship_coordinateX = width - (ship_img_px + marginX + 1) 

    #-------------enemy_movement-------------
    for i in range(no_of_enemy):
        #game_over
        if enemy_coordinateY[i] > height - gameover_height:
            gameOver()
        if enemy_coordinateX[i] >= marginX and enemy_coordinateX[i] <= width - (ship_img_px + marginX):
            enemy_coordinateX[i] += enemy_coordinateX_change[i]
        elif enemy_coordinateX[i] <= marginX:
            enemy_coordinateX_change[i] = enemy_speed_px
            enemy_coordinateX[i] = marginX + 1
            enemy_coordinateY[i] += enemy_coordinateY_change[i]
        elif enemy_coordinateX[i] >= width - (ship_img_px + marginX):
            enemy_coordinateX_change[i] = -enemy_speed_px
            enemy_coordinateX[i] = width - (ship_img_px + marginX + 1) 
            enemy_coordinateY[i] += enemy_coordinateY_change[i]

        is_collision = collision(enemy_coordinateX[i], enemy_coordinateY[i], bullet_coordinateX, bullet_coordinateY)
        if is_collision:
            explosion.play()
            bullet_coordinateY = height - 100
            is_bullet_moving = False
            score += 1
            print(score)
            enemy_coordinateX[i] = random.randint(marginX + 1, width - (ship_img_px + marginX + 1))
            enemy_coordinateY[i] = random.randint(marginY, height / 10)

        enemyFunc(enemy_coordinateX[i], enemy_coordinateY[i], i)


    #bullet_movement
    if bullet_coordinateY <= 0:
        bullet_coordinateY = height - 100
        is_bullet_moving = False
    if is_bullet_moving:
        fireBulletFunc(bullet_coordinateX, bullet_coordinateY)
        bullet_coordinateY -= bullet_speed_px

    shipFunc(ship_coordinateX, ship_coordinateY)
    scoreBoard(score_boardX, score_boardY)
    pygame.display.update()
