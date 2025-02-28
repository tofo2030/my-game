import pygame
import random
import time

# تهيئة Pygame
pygame.init()

# الألوان
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
YELLOW = (255, 255, 102)

# أبعاد النافذة
WIDTH, HEIGHT = 800, 600

# إنشاء النافذة
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("لعبة الثعبان الكاملة")

# الساعة
clock = pygame.time.Clock()

# حجم الثعبان والطعام
BLOCK_SIZE = 20

# الخطوط
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# المؤثرات الصوتية
pygame.mixer.music.load("background_music.mp3")  # موسيقى الخلفية
eat_sound = pygame.mixer.Sound("eat_sound.wav")  # صوت أكل الطعام
game_over_sound = pygame.mixer.Sound("game_over.wav")  # صوت الخسارة

# صور
apple_img = pygame.image.load("apple.png")  # صورة التفاحة
enemy_img = pygame.image.load("enemy.png")  # صورة العدو

# وظيفة لعرض النقاط
def display_score(score):
    value = score_font.render("نقاطك: " + str(score), True, YELLOW)
    window.blit(value, [10, 10])

# وظيفة لعرض الرسائل
def display_message(msg, color):
    mesg = font_style.render(msg, True, color)
    window.blit(mesg, [WIDTH / 6, HEIGHT / 3])

# وظيفة لرسم الثعبان
def draw_snake(block_size, snake_list):
    for segment in snake_list:
        pygame.draw.rect(window, GREEN, [segment[0], segment[1], block_size, block_size])

# وظيفة لتغيير الخلفية
def change_background():
    colors = [
        (30, 60, 114),  # أزرق داكن
        (106, 48, 147),  # بنفسجي
        (29, 151, 108),  # أخضر
        (255, 95, 109)   # وردي
    ]
    return random.choice(colors)

# وظيفة اللعبة الرئيسية
def game_loop():
    pygame.mixer.music.play(-1)  # تشغيل موسيقى الخلفية بشكل متكرر

    game_over = False
    game_close = False

    # موضع الثعبان الأولي
    x1 = WIDTH / 2
    y1 = HEIGHT / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    # موضع الطعام الأولي
    food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

    # موضع العدو الأولي
    enemy_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    enemy_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    enemy_dx, enemy_dy = 0, 0

    score = 0
    lives = 3
    stage = 1
    background_color = BLACK

    while not game_over:

        while game_close:
            window.fill(BLUE)
            display_message("لقد خسرت! اضغط Q-للخروج أو C-للعب مجدداً", RED)
            display_score(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = BLOCK_SIZE
                    x1_change = 0

        # التحقق من تجاوز الحدود
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            lives -= 1
            if lives == 0:
                game_over_sound.play()
                game_close = True
            else:
                x1 = WIDTH / 2
                y1 = HEIGHT / 2
                x1_change = 0
                y1_change = 0

        x1 += x1_change
        y1 += y1_change
        window.fill(background_color)
        window.blit(apple_img, (food_x, food_y))
        window.blit(enemy_img, (enemy_x, enemy_y))

        # تحريك العدو
        if random.random() < 0.2:  # تحريك العدو بشكل عشوائي
            enemy_dx = random.choice([-BLOCK_SIZE, 0, BLOCK_SIZE])
            enemy_dy = random.choice([-BLOCK_SIZE, 0, BLOCK_SIZE])
        enemy_x += enemy_dx
        enemy_y += enemy_dy

        # التحقق من تجاوز العدو للحدود
        if enemy_x >= WIDTH or enemy_x < 0 or enemy_y >= HEIGHT or enemy_y < 0:
            enemy_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            enemy_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

        # التحقق من اصطدام الثعبان بالعدو
        if x1 == enemy_x and y1 == enemy_y:
            lives -= 1
            if lives == 0:
                game_over_sound.play()
                game_close = True
            else:
                x1 = WIDTH / 2
                y1 = HEIGHT / 2
                x1_change = 0
                y1_change = 0

        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # التحقق من اصطدام الثعبان بنفسه
        for segment in snake_list[:-1]:
            if segment == snake_head:
                lives -= 1
                if lives == 0:
                    game_over_sound.play()
                    game_close = True
                else:
                    x1 = WIDTH / 2
                    y1 = HEIGHT / 2
                    x1_change = 0
                    y1_change = 0

        draw_snake(BLOCK_SIZE, snake_list)
        display_score(score)

        pygame.display.update()

        # التحقق من أكل الطعام
        if x1 == food_x and y1 == food_y:
            food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            length_of_snake += 1
            score += 1
            eat_sound.play()
            background_color = change_background()

            # زيادة المرحلة كل 5 نقاط
            if score % 5 == 0:
                stage += 1

        clock.tick(15)

    pygame.quit()
    quit()

# تشغيل اللعبة
game_loop()
