import pygame

import random

import math

import time

import serial
try:
    port = serial.Serial('com3', 9600)
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    port = None


# Pygame ayarları

pygame.init()

width, height = 1000, 600

screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("Sayı Doğrusu Oyun")

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Renkler

BLACK = (0, 0, 0)

PHOSPHOR_BLUE = (0, 200, 255)

PHOSPHOR_YELLOW = (255, 255, 0)

RED = (255, 0, 0)

GREEN = (0, 255, 0)

BLUE = (0, 0, 255)



# Fontlar

font = pygame.font.Font(None, 36)


pygame.mixer.init()
# Oyun değişkenleri

# Oyun değişkenleri

score = 0

time_limit = 15

game_over = False



# Karakter resmi ve konumu

character_image = pygame.image.load("character.png")  # Başlangıçta karakterin resmi

character_image = pygame.transform.scale(character_image, (50, 80))  # Resmi yeniden boyutlandır

character_position = (width * 0.25, height - 230)  # Karakterin başlangıç konumu



# Ok değişkenleri

arrow_position = [width * 0.33, height - 150]  # Ok başlangıç pozisyonu

position = None  # Hedef pozisyon

shooting = False  # Ok atma animasyonu başlangıçta devre dışı



# Yeni sayı ve süreyi başlat

def new_round():
    global number, sqrt_number, start_time, user_input, arrow_position, target_position, shooting, question
    
    question = random.randint(2, 10)  # Sorulacak karekök değeri
    number = question ** 2  # Tam kareyi hesapla
    sqrt_number = question  # Karekökü doğrudan ata!


    start_time = time.time()  # Timer'ı başlat
    user_input = ''  # Kullanıcı girişini sıfırla
    shooting = False  # Ok atışı devre dışı bırak

    arrow_position = [width * 0.33, height - 225]  # Ok başlangıç pozisyonu

    # Sayı doğrusundaki hedefi ayarla
    number_line_start_x = 0  
    number_line_end_x = width  
    num_points = 10  

    scaled_position = int((sqrt_number / num_points) * (number_line_end_x - number_line_start_x)) + number_line_start_x
    target_position = [scaled_position, height - 50]




def update_arrow_position():

    global arrow_position, shooting, target_position, game_over, character_image, character_position



    if shooting and target_position:

        x_dist = target_position[0] - arrow_position[0]

        y_dist = target_position[1] - arrow_position[1]

        distance = math.sqrt(x_dist ** 2 + y_dist ** 2)



        # Ok hareket ediyor, karakterin resmini "archery.png" yap

        character_image = pygame.image.load("archery.png")  # Ok animasyonu sırasında "archery.png" yükleyin

        character_image = pygame.transform.scale(character_image, (50, 80))  # Resmi yeniden boyutlandır

        character_position = (width * 0.25, height - 230)  # Yeni karakter konumu



        if distance < 5:  # Hedefe ulaştıysa

            arrow_position = target_position  # Okun hedef pozisyonu

            shooting = False  # Ok animasyonunu sonlandır

            if not game_over:

                time.sleep(0.5)  # Yeni turdan önce beklet

                character_image = pygame.image.load("character.png")  # "character.png" yüklensin

                character_image = pygame.transform.scale(character_image, (50, 80))  # Resmi yeniden boyutlandır

                character_position = (width * 0.25, height - 230)  # Karakterin başlangıç pozisyonuna geri dön

                new_round()  # Yeni tur başlat
                



        else:

            step = 1.5

            arrow_position[1] += int(step * y_dist / distance)            

            arrow_position[0] += int(step * x_dist / distance)



# Ana oyun döngüsünde update_arrow_position çağrılacak, karakterin resmini değiştirmek için



# OK ÇİZME FONKSİYONU

def draw_arrow(position, target_position=None):

    # Okun başı ve ucu arasındaki iki nokta

    arrow_length = 50  # Ok uzunluğu

    arrow_width = 10   # Okun başının genişliği



    # Okun başı (başlangıç noktası)

    arrow_start = position

    # Eğer hedef pozisyonu verilmişse okun ucunu ona göre ayarla

    if target_position:

        x_dist = target_position[0] - arrow_start[0]

        y_dist = target_position[1] - arrow_start[1]

        angle = math.atan2(y_dist, x_dist)  # Yönü hesapla

    else:

        angle = 0  # Hedef yoksa düz çizim



    # Okun ucu (bitiş noktası)

    arrow_end = (arrow_start[0] + arrow_length * math.cos(angle), arrow_start[1] + arrow_length * math.sin(angle))



    # Okun ana çizgisini çiz

    pygame.draw.line(screen, RED, arrow_start, arrow_end, 5)  # Kalınlık 5



    # Ok başını çizmek için küçük üçgen (veya ok ucu)

    left_tip = (arrow_end[0] - arrow_width * math.cos(angle + math.pi / 4), 

                arrow_end[1] - arrow_width * math.sin(angle + math.pi / 4))

    right_tip = (arrow_end[0] - arrow_width * math.cos(angle - math.pi / 4), 

                 arrow_end[1] - arrow_width * math.sin(angle - math.pi / 4))



    # Üçgeni çiz

    pygame.draw.polygon(screen, RED, [arrow_end, left_tip, right_tip])  # Ok başı üçgeni





# Karakteri çizme fonksiyonu (görselle)

def draw_character():

    screen.blit(character_image, character_position)



# Sayı doğrusu çizme fonksiyonu

def draw_number_line():

    # Sayı doğrusunun genişliğini azaltmak için başlangıç ve bitiş noktalarını belirleyin

    number_line_start_x = 0  # Ekranın %25'inden başlat

    number_line_end_x = width    # Ekranın %75'ine kadar uzat

    num_points = 10  # 0-10 arasında 11 sayı noktası

    

    # 0-10 aralığındaki her sayıyı çizin

    for i in range(11):  

        x = number_line_start_x + i * (number_line_end_x - number_line_start_x) // num_points

        pygame.draw.line(screen, PHOSPHOR_BLUE, (x, height - 50), (x, height - 30), 2)

        

        # Sayı metnini fosforlu sarı renkte çizin

        num_text = font.render(str(i), True, PHOSPHOR_BLUE)

        screen.blit(num_text, (x - num_text.get_width() // 2, height - 25))



def draw_background_pattern():

    spacing = 50  # Çizgiler arasındaki boşluk

    for x in range(0, width, spacing):

        pygame.draw.line(screen, PHOSPHOR_YELLOW, (x, 0), (x, height), 1)

    for y in range(0, height, spacing):

        pygame.draw.line(screen, PHOSPHOR_YELLOW, (0, y), (width, y), 1)



def draw_user_input_boxes():

    # Split input into two numbers if there’s a hyphen

    inputs = user_input.split('-')

    box_width = 60  # Width of each input box

    box_height = 40  # Height of each input box

    spacing = 10  # Space between the boxes



    # Draw first box

    box1_rect = pygame.Rect(width // 2 - box_width - spacing, height - 100, box_width, box_height)

    pygame.draw.rect(screen, PHOSPHOR_YELLOW, box1_rect)

    if len(inputs) > 0:

        text1 = font.render(inputs[0], True, PHOSPHOR_BLUE)

        screen.blit(text1, (box1_rect.x + (box_width - text1.get_width()) // 2, box1_rect.y + (box_height - text1.get_height()) // 2))



    # Draw second box

    box2_rect = pygame.Rect(width // 2 + spacing, height - 100, box_width, box_height)

    pygame.draw.rect(screen, PHOSPHOR_YELLOW, box2_rect)

    if len(inputs) > 1:

        text2 = font.render(inputs[1], True, PHOSPHOR_BLUE)

        screen.blit(text2, (box2_rect.x + (box_width - text2.get_width()) // 2, box2_rect.y + (box_height - text2.get_height()) // 2))







# Oyuna başla

new_round()



# Ana oyun döngüsü
running = True
last_time = time.time()


while running:
    delta_time = clock.tick(60) / 1000.0  # Limit to 60 FPS and get delta_time in seconds

    screen.fill(BLACK)

    draw_background_pattern()  # Deseni arka planda çiz

    # Ana oyun döngüsünde ok çizme

    if shooting:

        update_arrow_position(delta_time)

        draw_arrow(arrow_position, target_position)  # Hedef pozisyonu vererek oku çiz

    else:

        draw_arrow(arrow_position)  # Eğer ok henüz atılmadıysa düz çizim



    # Geri sayım

    elapsed_time = time.time() - start_time

    remaining_time = max(0, time_limit - int(elapsed_time))

    

    # Oyuncu süreyi geçtiyse oyunu bitir

    if remaining_time == 0 and not game_over:
        game_over = True
        pygame.mixer.music.load("false.mp3")
        pygame.mixer.music.play()
        pygame.time.delay(2000)  # 2 saniye bekle


    

    # Sayıyı ve karekökünü ekranda göster
    
    number_text = font.render(f"√({question}) = ?", True, PHOSPHOR_BLUE)

    screen.blit(number_text, (width // 2 - number_text.get_width() // 2, height // 2 - 50))

    number_text = font.render(f"Nerede?", True, PHOSPHOR_BLUE)

    screen.blit(number_text, (width // 2 - number_text.get_width() // 2, height // 2 - 100))

    

    # Geri sayımı ekranda göster

    timer_text = font.render(f"Kalan Süre: {remaining_time}s", True, PHOSPHOR_YELLOW)

    screen.blit(timer_text, (10, 10))

    

    # Skoru ekranda göster

    score_text = font.render(f"Puan: {score}", True, PHOSPHOR_YELLOW)

    screen.blit(score_text, (width - 150, 10))

    

    # Oyun bitti mesajı

    if game_over:

        game_over_text = font.render("Oyun Bitti!", True, RED)

        screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 + 25))

    

    # Sayı doğrusunu çiz

    draw_number_line()

    draw_user_input_boxes()

    # Eğer ok animasyonu aktifse ok pozisyonunu güncelle

    if shooting:

        update_arrow_position()

    

    # Karakteri çiz

    draw_character()

    

    # Oku çiz

    draw_arrow(arrow_position)

    

    pygame.display.flip()

    

    # Etkinlikler

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        

        # Klavyeden girilen sayıları yakala



        elif event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_RETURN:
                try:
                    if user_input.isdigit() and int(user_input) == sqrt_number:

                        target_position = [int(user_input) * (width // 20), height - 50]  
                        shooting = True  
                        score += 1  
                        pygame.mixer.music.load("true.mp3")  
                        pygame.mixer.music.play()
                        time.sleep(1)  
                        new_round()  
                    else:
                        pygame.mixer.music.load("false.mp3")  
                        pygame.mixer.music.play()
                        time.sleep(1)  
                        new_round()  
                except ValueError:
                    pass  
                user_input = ''


            elif event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]  # Bir karakter sil
            else:
                user_input += event.unicode  # Kullanıcı girişini birleştir

    # Eğer oyun biterse oyun bitti mesajını göster ve kullanıcıdan çıkış bekle

    if game_over:
        game_over_text = font.render("Oyun Bitti! Çıkmak için ESC'ye basın", True, RED)
        screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 + 25))
        pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.time.delay(2000)
                try:
                    pygame.mixer.music.load("false.mp3")
                    pygame.mixer.music.play()
                except pygame.error as e:
                    print(f"Error playing sound: {e}")


pygame.quit()

