import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
FPS = 60

# Colors (pixelated retro palette)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)

# Simple maze layout (1 = wall, 0 = path)
MAZE = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,1,0,1,1,0,1,1,1,0,1,1,1,1],
    [1,0,0,0,1,0,0,1,0,0,1,0,0,0,1,0,0,0,1,1],
    [1,1,1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
    [1,0,1,1,1,0,1,1,1,1,1,1,1,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,0,1],
    [1,1,1,1,1,0,1,1,1,1,1,1,0,1,1,1,0,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1]
]

walls = pygame.sprite.Group()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE//2, TILE_SIZE//2))
        self.image.fill((random.randint(100,255), random.randint(100,200), random.randint(100,255)))  # Random pixel color
        pygame.draw.rect(self.image, BLACK, (2,2,12,12))  # Pixel eyes
        pygame.draw.rect(self.image, BLACK, (6,14,4,4))   # Pixel mouth
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 4
        self.vel_x = 0
        self.vel_y = 0

    def update(self):
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        self.vel_y = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vel_y = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vel_y = self.speed

        # Collision with maze walls (check new rect against walls group)
        new_rect = self.rect.move(self.vel_x, 0)
        collision = any(new_rect.colliderect(w.rect) for w in walls)
        if not collision:
            self.rect = new_rect
        new_rect = self.rect.move(0, self.vel_y)
        collision = any(new_rect.colliderect(w.rect) for w in walls)
        if not collision:
            self.rect = new_rect

class Treasure(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(DARK_GRAY)
        pygame.draw.rect(self.image, ORANGE, (8,8,24,24))  # Chest body
        pygame.draw.rect(self.image, YELLOW, (12,12,16,8))  # Lid
        self.rect = self.image.get_rect(topleft=(x, y))
        self.opened = False
        self.cake_timer = 0

    def update(self):
        if self.opened:
            self.cake_timer += 1
            if self.cake_timer > 30:  # Cake pops up after delay
                self.show_cake = True

    def open_chest(self):
        self.opened = True

    def draw_cake(self, screen, font):
        if hasattr(self, 'show_cake') and self.show_cake:
            # Pixelated cake
            pygame.draw.rect(screen, PINK, (self.rect.x+8, self.rect.y+8, 24, 16))  # Cake base
            pygame.draw.rect(screen, WHITE, (self.rect.x+12, self.rect.y+4, 16, 8))  # Frosting
            pygame.draw.circle(screen, RED, (self.rect.x+16, self.rect.y+6), 3)  # Candle flame
            text = font.render("Happy Birthday!", True, YELLOW)
            screen.blit(text, (self.rect.x-20, self.rect.y-30))

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pixel Birthday Maze Adventure")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    all_sprites = pygame.sprite.Group()
    global walls
    walls = pygame.sprite.Group()
    player = Player(TILE_SIZE, TILE_SIZE)  # Start position
    treasure = Treasure(SCREEN_WIDTH - TILE_SIZE*2, SCREEN_HEIGHT - TILE_SIZE*2)
    
    all_sprites.add(player, treasure)
    
    # Create maze walls
    for row in range(len(MAZE)):
        for col in range(len(MAZE[0])):
            if MAZE[row][col] == 1:
                wall = pygame.sprite.Sprite()
                wall.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
                wall.image.fill(GRAY)
                wall.rect = wall.image.get_rect(topleft=(col*TILE_SIZE, row*TILE_SIZE))
                walls.add(wall)
                all_sprites.add(wall)
    
    running = True
    win_screen = False
    
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        all_sprites.update()
        
        # Check treasure collision
        if pygame.sprite.collide_rect(player, treasure) and not treasure.opened:
            treasure.open_chest()
        
        screen.fill(BLACK)
        
        # Draw maze background
        for row in range(len(MAZE)):
            for col in range(len(MAZE[0])):
                if MAZE[row][col] == 0:
                    pygame.draw.rect(screen, DARK_GRAY, (col*TILE_SIZE, row*TILE_SIZE, TILE_SIZE, TILE_SIZE))
        
        all_sprites.draw(screen)
        treasure.draw_cake(screen, font)
        
        # Instructions
        instr = pygame.font.Font(None, 24).render("WASD/Arrow Keys to Move | Reach the Treasure!", True, WHITE)
        screen.blit(instr, (10, 10))
        
        if treasure.opened and treasure.draw_cake:
            win_text = font.render("HAPPY BIRTHDAY! 🎉", True, YELLOW)
            screen.blit(win_text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2))
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
