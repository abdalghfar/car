import pygame
import os
import random

# إعدادات اللعبة
pygame.init()
pygame.mixer.init()  # تهيئة مكتبة الصوت

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Car Racing Game")

# تحميل الأصول
# assets_path = "Assets"
car_image = pygame.image.load(os.path.join("cars/1.png"))
opponent_car_image = pygame.image.load(os.path.join("cars/2.png"))
opponent_car_image2 = pygame.image.load(os.path.join("cars/3.png"))
road_image = pygame.image.load(os.path.join( "road.png"))
bg_image = pygame.image.load(os.path.join("bg.png"))

# تحميل الأصوات
collision_sound = pygame.mixer.Sound(os.path.join("collision.mp3"))
acceleration_sound = pygame.mixer.Sound(os.path.join("acceleration.mp3"))
restart_sound = pygame.mixer.Sound(os.path.join("collision.mp3"))

# إعداد اللاعب
car_width = 50
car_height = 100
car_x = screen_width // 2 - car_width // 2
car_y = screen_height - car_height - 20
car_speed = 0
brake_speed = 2
max_speed = 400

# إعداد الخلفية المتحركة
bg_y = 0
bg_speed = 5

# إعداد الطريق المتحرك
road_y = 0
road_speed = 0  # سيتم تحديثه بناءً على سرعة السيارة

# إعداد السيارة المنافسة
opponent_car_x = random.randint(0, screen_width - car_width)
opponent_car_y = -car_height
opponent_speed = 5

opponent_car_x2 = random.randint(0, screen_width - car_width)
opponent_car_y2 = -car_height
opponent_speed2 = 7

font = pygame.font.SysFont(None, 40)

def reset_game():
    global car_x, car_y, car_speed, opponent_car_x, opponent_car_y, opponent_car_x2, opponent_car_y2, road_y
    car_x = screen_width // 2 - car_width // 2
    car_y = screen_height - car_height - 20
    car_speed = 0
    road_y = 0
    opponent_car_x = random.randint(0, screen_width - car_width)
    opponent_car_y = -car_height
    opponent_car_x2 = random.randint(0, screen_width - car_width)
    opponent_car_y2 = -car_height

def draw_button(rect, color, text):
    pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (rect.x + rect.width // 2 - text_surface.get_width() // 2, rect.y + rect.height // 2 - text_surface.get_height() // 2))

def display_text(text, size, color, position):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

# حلقة اللعبة الرئيسية
running = True
distance = 0
high_score = 0
game_over = False

while running:
    if not game_over:
        # تحريك الخلفية
        bg_y += bg_speed
        if bg_y >= screen_height:
            bg_y = 0

        screen.blit(bg_image, (0, bg_y))
        screen.blit(bg_image, (0, bg_y - screen_height))  # التكرار لإعطاء تأثير الحركة

        # تحديث سرعة الطريق بناءً على سرعة السيارة
        road_speed = car_speed  # اجعل سرعة الطريق تتناسب مع سرعة السيارة

        # تحريك الطريق
        road_y += road_speed
        if road_y >= screen_height:
            road_y = 0

        screen.blit(road_image, (0, road_y))
        screen.blit(road_image, (0, road_y - screen_height))  # التكرار لإعطاء تأثير الحركة

        screen.blit(car_image, (car_x, car_y))
        screen.blit(opponent_car_image, (opponent_car_x, opponent_car_y))
        screen.blit(opponent_car_image2, (opponent_car_x2, opponent_car_y2))

        # عرض عداد السرعة والمسافة
        display_text(f"Speed: {car_speed}", 40, (255, 255, 255), (10, 10))
        display_text(f"Distance: {int(distance)}", 40, (255, 255, 255), (10, 50))
        display_text(f"High Score: {int(high_score)}", 40, (255, 255, 255), (10, 90))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # حركة اللاعب بناءً على السرعة
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_x > 0:
            car_x -= car_speed
        if keys[pygame.K_RIGHT] and car_x < screen_width - car_width:
            car_x += car_speed
        if keys[pygame.K_UP]:
            if car_speed < max_speed:
                car_speed += 1  # تسريع السيارة
                acceleration_sound.play()  # تشغيل صوت التسريع
        if keys[pygame.K_DOWN]:
            if car_speed > brake_speed:
                car_speed -= 1  # إبطاء السيارة

        # تحديث موضع السيارة بناءً على السرعة
        car_y -= car_speed
        distance += car_speed / 60  # حساب المسافة بناءً على الوقت

        # التأكد من أن السيارة لا تتخطى منتصف الطريق
        if car_y < screen_height // 2 - car_height:
            car_y = screen_height // 2 - car_height  # اجعل السيارة تبقى فوق منتصف الطريق

        # حركة السيارات المنافسة
        opponent_car_y += opponent_speed
        if opponent_car_y > screen_height:
            opponent_car_y = -car_height
            opponent_car_x = random.randint(0, screen_width - car_width)
        
        opponent_car_y2 += opponent_speed2
        if opponent_car_y2 > screen_height:
            opponent_car_y2 = -car_height
            opponent_car_x2 = random.randint(0, screen_width - car_width)

        # التحقق من الاصطدام
        if (car_y < opponent_car_y + car_height and
            car_y + car_height > opponent_car_y and
            car_x < opponent_car_x + car_width and
            car_x + car_width > opponent_car_x) or \
           (car_y < opponent_car_y2 + car_height and
            car_y + car_height > opponent_car_y2 and
            car_x < opponent_car_x2 + car_width and
            car_x + car_width > opponent_car_x2):
            collision_sound.play()  # تشغيل صوت الاصطدام
            if distance > high_score:
                high_score = distance  # تحديث أعلى رقم سرعة
            # عرض رسالة إعادة المحاولة
            screen.fill((0, 0, 0))  # ملء الشاشة باللون الأسود
            display_text("Collision! Click the button below to Restart or Q to Quit", 50, (255, 0, 0), (screen_width // 2 - 300, screen_height // 2 - 100))
            
            # رسم زر إعادة المحاولة
            restart_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2, 200, 50)
            draw_button(restart_button, (0, 255, 0), "Restart")
            
            pygame.display.flip()

            # الانتظار للتفاعل مع الزر
            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        waiting_for_input = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        if restart_button.collidepoint(mouse_pos):
                            restart_sound.play()  # تشغيل صوت إعادة المحاولة
                            reset_game()
                            distance = 0
                            car_speed = 0
                            game_over = False
                            waiting_for_input = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            running = False
                            waiting_for_input = False
    else:
        # شاشة النهاية تظهر أعلى السرعة والزر لإعادة المحاولة
        screen.fill((0, 0, 0))  # ملء الشاشة باللون الأسود
        display_text("Game Over! Click the button below to Restart or Q to Quit", 50, (255, 0, 0), (screen_width // 2 - 300, screen_height // 2 - 100))
        display_text(f"High Score: {int(high_score)}", 50, (255, 255, 255), (screen_width // 2 - 100, screen_height // 2 + 50))
        
        # رسم زر إعادة المحاولة
        restart_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2, 200, 50)
        draw_button(restart_button, (0, 255, 0), "Restart")

        pygame.display.flip()

        # الانتظار للتفاعل مع الزر
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting_for_input = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if restart_button.collidepoint(mouse_pos):
                        restart_sound.play()  # تشغيل صوت إعادة المحاولة
                        reset_game()
                        distance = 0
                        car_speed = 0
                        game_over = False
                        waiting_for_input = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                        waiting_for_input = False

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
