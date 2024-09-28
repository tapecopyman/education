import pygame
import sys
import random

#https://chatgpt.com/share/66f7a2ee-7100-8006-b99e-8f0cfb2ec2f5
# pygame을 사용하여 "다람쥐 찾기"라는 게임을 만들어 보세요.
#- 당신은 화살표 키를 사용하여 빠르게 움직일 수 있는 코알라 아이콘입니다. 아이콘 이미지는 koala.png입니다.
#- 딸기가 매초 무작위로 생성되어 튕겨 다닙니다. 아이콘 이미지는 strawberry.png입니다.
#- 딸기에 닿으면 죽습니다.
#- 3초 후에 다람쥐 아이콘이 생성되어 튕겨 다닙니다. 아이콘 이미지는 squirrel.png입니다. 만지면 이깁니다.
#- strawberry.png 등 이미지파일은 images 폴더에 저장됩니다
#- 모든 아이콘이 40픽셀 x 40픽셀인지 확인하세요.
#- 복고풍 색상과 어두운 배경을 사용하세요.
#- 게임 화면에 "WARM-LAB"을 넣고 모서리에 타이머를 넣으세요.
#- 게임을 시작하기 전에 지침을 표시합니다.
#- 이기거나 졌을 때 자동으로 게임을 다시 시작합니다.
# By ChatGPT o1-mini



# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Find the Squirrel")

# Colors
DARK_BG = (10, 10, 30)
RETRO_COLORS = {
    "text": (255, 165, 0),      # Orange
    "timer": (0, 255, 255),     # Cyan
}

# Fonts
FONT_TITLE = pygame.font.SysFont('Arial', 50, bold=True)
FONT_TEXT = pygame.font.SysFont('Arial', 24)

# Load and scale images
def load_image(name):
    image = pygame.image.load(f'images/{name}').convert_alpha()
    return pygame.transform.scale(image, (40, 40))

KOALA_IMG = load_image('koala.png')
STRAWBERRY_IMG = load_image('strawberry.png')
SQUIRREL_IMG = load_image('squirrel.png')

# Game Clock
clock = pygame.time.Clock()
FPS = 60

# Custom Events
ADD_STRAWBERRY = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_STRAWBERRY, 1000)  # Every second

# Game States
STATE_INSTRUCTIONS = 'instructions'
STATE_PLAYING = 'playing'
STATE_WIN = 'win'
STATE_LOSE = 'lose'

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = KOALA_IMG
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.speed = 5

    def update(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys_pressed[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys_pressed[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Keep within screen
        self.rect.clamp_ip(SCREEN.get_rect())

class MovingSprite(pygame.sprite.Sprite):
    def __init__(self, image, speed=None):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(
            center=(random.randint(40, WIDTH - 40), random.randint(40, HEIGHT - 40))
        )
        if speed:
            self.speed_x, self.speed_y = speed
        else:
            self.speed_x = random.choice([-3, -2, -1, 1, 2, 3])
            self.speed_y = random.choice([-3, -2, -1, 1, 2, 3])

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce off walls
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed_x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

def display_text(text, font, color, center):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=center)
    SCREEN.blit(text_surface, rect)

def main():
    # Initialize game variables
    game_state = STATE_INSTRUCTIONS
    player = Player()
    player_group = pygame.sprite.GroupSingle(player)
    strawberries = pygame.sprite.Group()
    squirrel = None
    squirrel_group = pygame.sprite.Group()
    start_time = pygame.time.get_ticks()
    win_lose_time = None

    # Timer
    def get_elapsed_time():
        elapsed_ms = pygame.time.get_ticks() - start_time
        return elapsed_ms // 1000  # in seconds

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_state == STATE_INSTRUCTIONS:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_state = STATE_PLAYING
                    start_time = pygame.time.get_ticks()
                    # Reset groups
                    strawberries.empty()
                    squirrel_group.empty()
                    squirrel = None

            elif game_state == STATE_PLAYING:
                if event.type == ADD_STRAWBERRY:
                    strawberry = MovingSprite(STRAWBERRY_IMG)
                    strawberries.add(strawberry)

        keys_pressed = pygame.key.get_pressed()

        if game_state == STATE_PLAYING:
            # Update player
            player_group.update(keys_pressed)

            # Update strawberries
            strawberries.update()

            # Check for collisions with strawberries
            if pygame.sprite.spritecollideany(player, strawberries):
                game_state = STATE_LOSE
                win_lose_time = pygame.time.get_ticks()

            # Generate squirrel after 3 seconds
            if get_elapsed_time() >= 3 and not squirrel:
                squirrel = MovingSprite(SQUIRREL_IMG)
                squirrel_group.add(squirrel)

            # Update squirrel
            if squirrel:
                squirrel_group.update()
                # Check collision with squirrel
                if pygame.sprite.spritecollideany(player, squirrel_group):
                    game_state = STATE_WIN
                    win_lose_time = pygame.time.get_ticks()

        elif game_state in [STATE_WIN, STATE_LOSE]:
            # Wait for 2 seconds then restart
            if pygame.time.get_ticks() - win_lose_time > 2000:
                game_state = STATE_INSTRUCTIONS

        # Drawing
        SCREEN.fill(DARK_BG)

        if game_state == STATE_INSTRUCTIONS:
            display_text("Find the Squirrel", FONT_TITLE, RETRO_COLORS["text"], (WIDTH//2, HEIGHT//2 - 50))
            instructions = [
                "Use arrow keys to move the koala.",
                "Avoid touching the strawberries.",
                "Find and touch the squirrel to win.",
                "Press SPACE to start."
            ]
            for i, line in enumerate(instructions):
                display_text(line, FONT_TEXT, RETRO_COLORS["text"], (WIDTH//2, HEIGHT//2 + i * 30))
        else:
            # Draw all sprites
            player_group.draw(SCREEN)
            strawberries.draw(SCREEN)
            squirrel_group.draw(SCREEN)

            # Display WARM-LAB
            display_text("WARM-LAB", FONT_TEXT, RETRO_COLORS["text"], (70, 30))

            # Display timer
            elapsed = get_elapsed_time()
            timer_text = f"Time: {elapsed}s"
            timer_surface = FONT_TEXT.render(timer_text, True, RETRO_COLORS["timer"])
            SCREEN.blit(timer_surface, (WIDTH - 150, 10))

            if game_state == STATE_WIN:
                display_text("You Win!", FONT_TITLE, RETRO_COLORS["text"], (WIDTH//2, HEIGHT//2))
            elif game_state == STATE_LOSE:
                display_text("You Died!", FONT_TITLE, RETRO_COLORS["text"], (WIDTH//2, HEIGHT//2))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
