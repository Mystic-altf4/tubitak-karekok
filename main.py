import pygame
import random
import math
import time

# Pygame ayarları
pygame.init()
width, height = 1000, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sayı Doğrusu Oyun")

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fontlar
font = pygame.font.Font(None, 36)

# Oyun değişkenleri
score = 0
time_limit = 10
game_over = False

# Karakter resmi ve konumu
character_image = pygame.image.load("character.png")  # Karakterin resmi
character_image = pygame.transform.scale(character_image, (50, 80))  # Resmi yeniden boyutlandır
character_position = (width // 2 - 25, height - 230)  # Yeni karakter konumu

# Ok değişkenleri
arrow_position = [width // 2, height - 150]  # Ok başlangıç pozisyonu
target_position = None  # Hedef pozisyon
shooting = False  # Ok atma animasyonu başlangıçta devre dışı

# Yeni sayı ve süreyi başlat
def new_round():
    global number, sqrt_number, start_time, user_input, arrow_position, target_position, shooting
    number = random.randint(10, 100)  # Gösterilecek rastgele sayı
    sqrt_number = math.sqrt(number)
    start_time = time.time()  # Süreyi başlat
    user_input = ''  # Kullanıcı tahmin girişi
    arrow_position = [width // 2, height - 150]  # Ok başlangıç pozisyonu (liste olarak tanımlandı)
    target_position = None  # Hedef pozisyon
    shooting = False  # Ok animasyonu başlangıçta devre dışı

# Ok çizme fonksiyonu
def draw_arrow(position):
    pygame.draw.circle(screen, RED, position, 10)  # Ok için kırmızı bir daire çiz

# Karakteri çizme fonksiyonu (görselle)
def draw_character():
    screen.blit(character_image, character_position)

# Sayı doğrusu çizme fonksiyonu
def draw_number_line():
    for i in range(11):  # 0'dan 10'a kadar aralıklar
        x = i * (width // 10)  # Sayı doğrusu üzerindeki her sayı için pozisyon
        pygame.draw.line(screen, BLACK, (x, height - 50), (x, height - 30), 2)
        num_text = font.render(str(i), True, BLACK)
        screen.blit(num_text, (x - num_text.get_width() // 2, height - 25))

# Ok pozisyonunu hedefe doğru ilerletme
def update_arrow_position():
    global arrow_position, shooting, target_position, game_over
    
    if shooting and target_position:
        # Ok pozisyonunu hedefe doğru hareket ettir
        x_dist = target_position[0] - arrow_position[0]
        y_dist = target_position[1] - arrow_position[1]
        distance = math.sqrt(x_dist ** 2 + y_dist ** 2)
        
        if distance < 5:  # Hedefe ulaştıysa animasyonu bitir
            arrow_position = target_position
            shooting = False
            if not game_over:
                time.sleep(1)  # Yeni turdan önce biraz beklet
                new_round()  # Yeni tur başlat
        else:
            # Okun hareket yönünü belirle ve güncelle
            step = 10
            arrow_position[0] += int(step * x_dist / distance)
            arrow_position[1] += int(step * y_dist / distance)

# Oyuna başla
new_round()

# Ana oyun döngüsü
running = True
while running:
    screen.fill(WHITE)
    
    # Geri sayım
    elapsed_time = time.time() - start_time
    remaining_time = max(0, time_limit - int(elapsed_time))
    
    # Oyuncu süreyi geçtiyse oyunu bitir
    if remaining_time == 0:
        game_over = True
    
    # Sayıyı ve karekökünü ekranda göster
    number_text = font.render(f"√({number}) = ?", True, BLACK)
    screen.blit(number_text, (width // 2 - number_text.get_width() // 2, height // 2 - 50))
    
    # Geri sayımı ekranda göster
    timer_text = font.render(f"Kalan Süre: {remaining_time}s", True, BLACK)
    screen.blit(timer_text, (10, 10))
    
    # Kullanıcının tahmin girişini ekranda göster
    guess_text = font.render(f"Tahmin: {user_input}", True, BLACK)
    screen.blit(guess_text, (width // 2 - guess_text.get_width() // 2, height - 100))
    
    # Skoru ekranda göster
    score_text = font.render(f"Puan: {score}", True, BLACK)
    screen.blit(score_text, (width - 150, 10))
    
    # Oyun bitti mesajı
    if game_over:
        game_over_text = font.render("Oyun Bitti!", True, RED)
        screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 + 25))
    
    # Sayı doğrusunu çiz
    draw_number_line()
    
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
            if event.key == pygame.K_RETURN:  # Enter'a basıldıysa tahmini kontrol et
                try:
                    if sqrt_number.is_integer():  # Karekökü tam sayı mı?
                        user_input = str(int(sqrt_number))  # Kullanıcıdan alınan değeri tam sayı olarak ayarla
                        target_position = [int(user_input) * (width // 20), height - 50]  # Hedef pozisyonunu ayarla
                        shooting = True  # Ok animasyonunu başlat
                        score += 1  # Doğru tahminse puan artır
                        time.sleep(1)  # Yeni turdan önce beklet
                        new_round()  # Yeni tur başlat
                    else:
                        lower, upper = map(int, user_input.split('-'))
                        target_x = (lower + upper) * (width // 20)  # Hedef pozisyonu belirle
                        target_position = [target_x, height - 50]  # Okun düşeceği hedef pozisyon
                        shooting = True  # Ok animasyonunu başlat
                        if lower <= sqrt_number < upper:
                            score += 1  # Doğru tahminse puan artır
                        else:
                            game_over = True  # Yanlışsa oyun biter
                except ValueError:
                    pass  # Hatalı giriş varsa hiçbir şey yapma
                user_input = ''  # Girişi temizle
            elif event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]  # Bir karakter sil
            else:
                user_input += event.unicode  # Kullanıcı girişini birleştir

    # Eğer oyun biterse ana döngüyü yavaşlat
    if game_over:
        pygame.time.delay(2000)
        running = False

pygame.quit()
