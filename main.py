import pygame
import random
import sys
import os
import json

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = '#fe2406'
GREEN = (0, 255, 0)
BLUE = '#0cf84c'
YELLOW = '#a8f58f'
ORANGE = '#effa89'
PURPLE = '#7d01b7'
CYAN = '#b8ccf4'
MAGENTA = '#a8f58f'

PLAYER_SIZE = 40
PLAYER_SPEED = 5
ENEMY_SIZE = 30
ENEMY_SPEED = 2
STAR_SIZE = 20
STAR_SPEED = 3
COIN_SIZE = 25
COIN_SPEED = 4
GEM_SIZE = 15
GEM_SPEED = 5
BULLET_SIZE = 10
BULLET_SPEED = 7
BULLET_COLOR = YELLOW
PLAYER_COLOR = BLUE
ENEMY_COLOR = RED
STAR_COLOR = WHITE
COIN_COLOR = ORANGE
GEM_COLOR = PURPLE
FONT_SIZE = 30
TEXT_COLOR = WHITE
BUTTON_COLOR = CYAN
BUTTON_HOVER_COLOR = MAGENTA
BUTTON_TEXT_COLOR = BLACK
BUTTON_FONT_SIZE = 20
# Загрузка настроек

SETTINGS_FILE = "settings.json"


def load_settings():
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "starting_enemies": 5,
            "max_enemies": 10,
            "starting_stars": 3,
            "max_stars": 7,
            "starting_coins": 2,
            "max_coins": 5,
            "starting_gems": 1,
            "max_gems": 3,
        }


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)


# Игровые настройки (по умолчанию)
global game_settings
game_settings = load_settings()

# Звуковые эффекты
if 'sound' in pygame.__dict__ and pygame.mixer.get_init():
    try:
        pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), 'bgm.mp3'))
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

        sound_shoot = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'shoot.wav'))
        sound_shoot.set_volume(0.1)
        sound_hit = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'hit.wav'))
        sound_hit.set_volume(0.5)
        sound_star = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'star.wav'))
        sound_star.set_volume(0.3)
        sound_coin = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'coin.wav'))
        sound_coin.set_volume(0.4)
        sound_gem = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'gem.wav'))
        sound_gem.set_volume(0.5)
    except pygame.error as e:
        print(f"Ошибка при загрузке звука: {e}")
        sound_shoot = None
        sound_hit = None
        sound_star = None
        sound_coin = None
        sound_gem = None
else:
    sound_shoot = None
    sound_hit = None
    sound_star = None
    sound_coin = None
    sound_gem = None


# Классы
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, PLAYER_COLOR, (PLAYER_SIZE // 2, PLAYER_SIZE // 2), PLAYER_SIZE // 2)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = 0
        self.speed_y = 0
        self.original_size = PLAYER_SIZE

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(self.image, ENEMY_COLOR, (0, 0, ENEMY_SIZE, ENEMY_SIZE))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = random.choice([-ENEMY_SPEED, ENEMY_SPEED])
        self.speed_y = random.choice([-ENEMY_SPEED, ENEMY_SPEED])

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed_x *= -1
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speed_y *= -1


class Star(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((STAR_SIZE, STAR_SIZE), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, STAR_COLOR, [(STAR_SIZE // 2, 0), (0, STAR_SIZE), (STAR_SIZE, STAR_SIZE)])
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_y = STAR_SPEED

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.rect.y = -STAR_SIZE
            self.rect.x = random.randint(0, WIDTH)


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((COIN_SIZE, COIN_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, COIN_COLOR, (COIN_SIZE // 2, COIN_SIZE // 2), COIN_SIZE // 2)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_y = COIN_SPEED

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.rect.y = -COIN_SIZE
            self.rect.x = random.randint(0, WIDTH)


class Gem(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((GEM_SIZE, GEM_SIZE), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, GEM_COLOR, [(GEM_SIZE // 2, 0), (0, GEM_SIZE // 2), (GEM_SIZE // 2, GEM_SIZE),
                                                    (GEM_SIZE, GEM_SIZE // 2)])
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_y = GEM_SPEED

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.rect.y = -GEM_SIZE
            self.rect.x = random.randint(0, WIDTH)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction_x, direction_y):
        super().__init__()
        self.image = pygame.Surface((BULLET_SIZE, BULLET_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BULLET_COLOR, (BULLET_SIZE // 2, BULLET_SIZE // 2), BULLET_SIZE // 2)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = direction_x * BULLET_SPEED
        self.speed_y = direction_y * BULLET_SPEED

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left < 0 or self.rect.right > WIDTH or self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.kill()


class Button:
    def __init__(self, x, y, width, height, text, action, font, text_color=BUTTON_TEXT_COLOR, color=BUTTON_COLOR,
                 hover_color=BUTTON_HOVER_COLOR):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.font = font
        self.text_color = text_color
        self.color = color
        self.hover_color = hover_color

    def draw(self, surface):
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)

        surface.fill(self.color, self.rect)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()

    def update_color(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.color = self.hover_color
        else:
            self.color = BUTTON_COLOR


class InputBox:
    def __init__(self, x, y, width, height, text='', font=None, color=WHITE, background=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = font if font else pygame.font.Font(None, BUTTON_FONT_SIZE)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False
        self.background = background

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = YELLOW if self.active else WHITE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        width = max(self.rect.w, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        screen.fill(self.background, self.rect)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


# Функция для отображения текста
def draw_text(surface, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)


def create_level(num_enemies, num_stars, num_coins, num_gems):
    global player, enemies, bullets, all_sprites, score, stars, coins, gems
    player = Player(WIDTH // 2, HEIGHT // 2)
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    stars = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    gems = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    for _ in range(num_enemies):
        x = random.randint(50, WIDTH - 50)
        y = random.randint(50, HEIGHT - 50)
        enemy = Enemy(x, y)
        enemies.add(enemy)
        all_sprites.add(enemy)
    for _ in range(num_stars):
        x = random.randint(50, WIDTH - 50)
        y = random.randint(50, HEIGHT - 50)
        star = Star(x, y)
        stars.add(star)
        all_sprites.add(star)
    for _ in range(num_coins):
        x = random.randint(50, WIDTH - 50)
        y = random.randint(50, HEIGHT - 50)
        coin = Coin(x, y)
        coins.add(coin)
        all_sprites.add(coin)
    for _ in range(num_gems):
        x = random.randint(50, WIDTH - 50)
        y = random.randint(50, HEIGHT - 50)
        gem = Gem(x, y)
        gems.add(gem)
        all_sprites.add(gem)
    score = 0


def show_settings():
    global game_state
    game_state = "settings"


def apply_settings():
    global game_state
    global game_settings
    try:
        game_settings["starting_enemies"] = int(enemies_input.text)
        game_settings["max_enemies"] = int(max_enemies_input.text)
        game_settings["starting_stars"] = int(stars_input.text)
        game_settings["max_stars"] = int(max_stars_input.text)
        game_settings["starting_coins"] = int(coins_input.text)
        game_settings["max_coins"] = int(max_coins_input.text)
        game_settings["starting_gems"] = int(gems_input.text)
        game_settings["max_gems"] = int(max_gems_input.text)
        save_settings(game_settings)
        game_state = "menu"
    except ValueError:
        print("Некорректные настройки")


# Настройки экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Космический Исследователь")
clock = pygame.time.Clock()
font = pygame.font.Font(None, FONT_SIZE)
button_font = pygame.font.Font(None, BUTTON_FONT_SIZE)

# Глобальные переменные
game_state = "menu"
player = None
enemies = None
bullets = None
stars = None
coins = None
gems = None
all_sprites = None
score = 0


# Кнопки меню
def start_game():
    global game_state
    game_state = "game"
    create_level(game_settings.get("starting_enemies", 5), game_settings.get("starting_stars", 3),
                 game_settings.get("starting_coins", 2), game_settings.get("starting_gems", 1))


menu_buttons = [
    Button(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, "Начать Игру", start_game, button_font),
    Button(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50, "Настройки", show_settings, button_font),
]
# Кнопки настроек
enemies_input = InputBox(WIDTH // 2 - 100, HEIGHT // 2 - 200, 200, 30, str(game_settings.get("starting_enemies", 5)),
                         color=WHITE)
max_enemies_input = InputBox(WIDTH // 2 - 100, HEIGHT // 2 - 150, 200, 30, str(game_settings.get("max_enemies", 10)),
                             color=WHITE)
stars_input = InputBox(WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 30, str(game_settings.get("starting_stars", 3)),
                       color=WHITE)
max_stars_input = InputBox(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 30, str(game_settings.get("max_stars", 7)),
                           color=WHITE)
coins_input = InputBox(WIDTH // 2 - 100, HEIGHT // 2 + 0, 200, 30, str(game_settings.get("starting_coins", 2)),
                       color=WHITE)
max_coins_input = InputBox(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 30, str(game_settings.get("max_coins", 5)),
                           color=WHITE)
gems_input = InputBox(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 30, str(game_settings.get("starting_gems", 1)),
                      color=WHITE)
max_gems_input = InputBox(WIDTH // 2 - 100, HEIGHT // 2 + 150, 200, 30, str(game_settings.get("max_gems", 3)),
                          color=WHITE)
apply_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 200, 200, 40, "Применить", apply_settings, button_font)
settings_items = [enemies_input, max_enemies_input, stars_input, max_stars_input, coins_input, max_coins_input,
                  gems_input, max_gems_input, apply_button]
# Игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_state == "menu":
            for button in menu_buttons:
                button.handle_event(event)
        elif game_state == "settings":
            for item in settings_items:
                if isinstance(item, Button):
                    item.handle_event(event)
                else:
                    item.handle_event(event)
        elif game_state == "game":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if player:
                        player.speed_x = -PLAYER_SPEED
                if event.key == pygame.K_RIGHT:
                    if player:
                        player.speed_x = PLAYER_SPEED
                if event.key == pygame.K_UP:
                    if player:
                        player.speed_y = -PLAYER_SPEED
                if event.key == pygame.K_DOWN:
                    if player:
                        player.speed_y = PLAYER_SPEED
                if event.key == pygame.K_SPACE:
                    if player:
                        bullet = Bullet(player.rect.centerx, player.rect.centery, 0, -1)
                        bullets.add(bullet)
                        all_sprites.add(bullet)
                        if sound_shoot:
                            sound_shoot.play()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.speed_x < 0:
                    if player:
                        player.speed_x = 0
                if event.key == pygame.K_RIGHT and player.speed_x > 0:
                    if player:
                        player.speed_x = 0
                if event.key == pygame.K_UP and player.speed_y < 0:
                    if player:
                        player.speed_y = 0
                if event.key == pygame.K_DOWN and player.speed_y > 0:
                    if player:
                        player.speed_y = 0

    if game_state == "menu":
        screen.fill(BLACK)
        for button in menu_buttons:
            button.update_color(pygame.mouse.get_pos())
            button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    elif game_state == "settings":
        screen.fill(BLACK)

        text_y = HEIGHT // 2 - 200
        line_height = 40
        label_offset = 150

        labels = [
            "Начальное количество врагов:",
            "Максимальное количество врагов:",
            "Начальное количество звезд:",
            "Максимальное количество звезд:",
            "Начальное количество монет:",
            "Максимальное количество монет:",
            "Начальное количество самоцветов:",
            "Максимальное количество самоцветов:"
        ]

        input_boxes = [
            enemies_input,
            max_enemies_input,
            stars_input,
            max_stars_input,
            coins_input,
            max_coins_input,
            gems_input,
            max_gems_input
        ]

        for label, input_box in zip(labels, input_boxes):
            draw_text(screen, label, button_font, TEXT_COLOR, WIDTH // 2 - label_offset, text_y)
            input_box.rect.topleft = (WIDTH // 2, text_y - line_height // 2 + 5)
            input_box.draw(screen)
            text_y += line_height

        apply_button.rect.topleft = (WIDTH // 2 - 100, text_y + 30)
        apply_button.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    elif game_state == "game":
        screen.fill(BLACK)
        if all_sprites:
            all_sprites.update()
            all_sprites.draw(screen)

        if bullets and enemies:
            for bullet in bullets:
                hit_enemy = pygame.sprite.spritecollideany(bullet, enemies)
                if hit_enemy:
                    if sound_hit:
                        sound_hit.play()
                    bullets.remove(bullet)
                    all_sprites.remove(bullet)
                    enemies.remove(hit_enemy)
                    all_sprites.remove(hit_enemy)
                    score += 10
        if player and stars:
            hit_star = pygame.sprite.spritecollideany(player, stars)
            if hit_star:
                if sound_star:
                    sound_star.play()
                stars.remove(hit_star)
                all_sprites.remove(hit_star)
                score += 20
        if player and coins:
            hit_coin = pygame.sprite.spritecollideany(player, coins)
            if hit_coin:
                if sound_coin:
                    sound_coin.play()
                coins.remove(hit_coin)
                all_sprites.remove(hit_coin)
                score += 30
        if player and gems:
            hit_gem = pygame.sprite.spritecollideany(player, gems)
            if hit_gem:
                if sound_gem:
                    sound_gem.play()
                gems.remove(hit_gem)
                all_sprites.remove(hit_gem)
                score += 40
        if player and enemies:
            hit_player = pygame.sprite.spritecollideany(player, enemies)
            if hit_player:
                create_level(game_settings.get("starting_enemies", 5),
                             game_settings.get("starting_stars", 3),
                             game_settings.get("starting_coins", 2),
                             game_settings.get("starting_gems", 1))

        player_size = player.original_size - score // 100
        if player_size < 10:
            player_size = 10
        player.image = pygame.Surface((player_size, player_size), pygame.SRCALPHA)
        pygame.draw.circle(player.image, PLAYER_COLOR, (player_size // 2, player_size // 2), player_size // 2)
        player.rect = player.image.get_rect(center=player.rect.center)
        player_speed = PLAYER_SPEED + score // 50
        if player_speed > 15:
            player_speed = 15
        PLAYER_SPEED = player_speed

        draw_text(screen, f"Счет: {score}", font, TEXT_COLOR, 90, 30)
        pygame.display.flip()
        clock.tick(FPS)
