import pygame
import sys

pygame.init()

# =========================
# UKURAN DUNIA MAZE
# =========================
world_width = 1920
world_height = 1080

# =========================
# UKURAN LAYAR
# =========================
screen_width = 1280
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("MAZE")

# surface dunia
world = pygame.Surface((world_width, world_height))

# warna
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
green = (0, 255, 0)

# =========================
# CLASS
# =========================
class character:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.speed = 2
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            self.color,
            (self.x, self.y, self.width, self.height)
        )

    def get_rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

# inheritance
class pemain_class(character):
    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed

        if keys[pygame.K_RIGHT]:
            self.x += self.speed

        if keys[pygame.K_UP]:
            self.y -= self.speed

        if keys[pygame.K_DOWN]:
            self.y += self.speed


class finish_class(character):
    pass

# =========================
# PLAYER & FINISH
# =========================
pemain = pemain_class(15, 15, blue)

finish = finish_class(560, 360, green)
finish.speed = 0

# =========================
# TEMBOK MAZE
# =========================
tembok = [
    #batas luar
    pygame.Rect(0, 0, 1920, 10),
    pygame.Rect(50, 1070, 1870, 10),
    pygame.Rect(0, 0, 10, 1080),
    pygame.Rect(1910, 0, 10, 1080),

    #spawn area
    pygame.Rect(0, 1200, 450, 10),
    pygame.Rect(0, 1200, 450, 10),
    pygame.Rect(0, 0, 10, 1200),
    pygame.Rect(450, 1070, 10, 140),

    # lorong 1
    pygame.Rect(200, 0, 10, 1000),
    pygame.Rect(10, 300, 140, 10),
    pygame.Rect(60, 600, 140, 10),

    # lorong 2
    pygame.Rect(400, 200, 10, 880),
    pygame.Rect(210, 800, 140, 10),
    pygame.Rect(250, 400, 150, 10),

    #A
    pygame.Rect(350, 700, 10, 110),
    pygame.Rect(300, 650, 100, 10),
    pygame.Rect(300, 650, 10, 100),
    pygame.Rect(250, 550, 10, 200),
    pygame.Rect(250, 600, 100, 10),
    pygame.Rect(250, 550, 150, 10),
    pygame.Rect(210, 500, 140, 10),
    pygame.Rect(210, 450, 140, 10),

    #B
    pygame.Rect(210, 350, 140, 10),
    pygame.Rect(210, 300, 140, 10),
    pygame.Rect(250, 250, 150, 10),
    pygame.Rect(250, 200, 150, 10),
    pygame.Rect(250, 100, 10, 100),
    pygame.Rect(210, 50, 50, 10),
    pygame.Rect(300, 50, 10, 100),
    pygame.Rect(300, 50, 100, 10),
    pygame.Rect(400, 10, 10, 50),
    pygame.Rect(300, 150, 110, 10),
    pygame.Rect(350, 100, 100, 10),
    pygame.Rect(450, 50, 10, 150),
    pygame.Rect(500, 10, 10, 50),
    pygame.Rect(500, 50, 50, 10),
    pygame.Rect(550, 50, 10, 50),
    pygame.Rect(500, 150, 100, 10),
    pygame.Rect(500, 100, 10, 50),

    # lorong 3
    pygame.Rect(600, 0, 10, 400),
    pygame.Rect(600, 450, 10, 630),
    pygame.Rect(410, 200, 130, 10),
    pygame.Rect(500, 750, 60, 10),

    #C
    pygame.Rect(450, 250, 10, 500),
    pygame.Rect(500, 250, 10, 500),
    pygame.Rect(550, 250, 10, 700),
    pygame.Rect(550, 1000, 10, 70),
    pygame.Rect(550, 400, 60, 10),
    pygame.Rect(410, 750, 50, 10),
    pygame.Rect(450, 800, 100, 10),
    pygame.Rect(450, 850, 100, 10),
    pygame.Rect(450, 900, 100, 10),
    pygame.Rect(450, 950, 110, 10),
    pygame.Rect(450, 1000, 100, 10),
    pygame.Rect(450, 1050, 100, 10),

    # lorong 4
    pygame.Rect(800, 100, 10, 980),
    pygame.Rect(610, 450, 140, 10),
    pygame.Rect(650, 850, 150, 10),

    #E
    pygame.Rect(650, 400, 100, 10),
    pygame.Rect(750, 400, 10, 100),
    pygame.Rect(610, 350, 150, 10),
    pygame.Rect(650, 300, 100, 10),
    pygame.Rect(650, 200, 10, 100),
    pygame.Rect(650, 200, 100, 10),
    pygame.Rect(750, 100, 10, 110),
    pygame.Rect(650, 100, 100, 10),
    pygame.Rect(650, 10, 10, 100),
    pygame.Rect(600, 150, 100, 10),
    pygame.Rect(700, 250, 200, 10),
    pygame.Rect(800, 100, 150, 10),
    pygame.Rect(700, 50, 250, 10),
    pygame.Rect(950, 50, 10, 60),
    pygame.Rect(850, 150, 150, 10),
    pygame.Rect(850, 200, 100, 10),
    pygame.Rect(950, 200, 10, 400),

    # lorong 5
    pygame.Rect(1000, 0, 10, 950),
    pygame.Rect(810, 300, 150, 10),
    pygame.Rect(850, 650, 150, 10),

    #F
    pygame.Rect(900, 350, 10, 250),
    pygame.Rect(850, 350, 10, 300),

    #G
    pygame.Rect(900, 650, 10, 100),
    pygame.Rect(900, 750, 60, 10),
    pygame.Rect(940, 700, 60, 10),
    pygame.Rect(800, 750, 50, 10),
    pygame.Rect(850, 750, 10, 50),
    pygame.Rect(850, 800, 110, 10),
    pygame.Rect(850, 850, 50, 10),
    pygame.Rect(850, 850, 10, 50),
    pygame.Rect(850, 900, 100, 10),
    pygame.Rect(950, 850, 10, 60),
    pygame.Rect(900, 950, 110, 10),
    pygame.Rect(900, 900, 10, 50),
    pygame.Rect(850, 1000, 350, 10),
    pygame.Rect(1050, 950, 150, 10),

    # lorong 6
    pygame.Rect(1200, 150, 10, 250),
    pygame.Rect(1200, 450, 10, 300),
    pygame.Rect(1200, 800, 10, 280),
    pygame.Rect(1010, 850, 150, 10),

    # lorong 7
    pygame.Rect(1400, 0, 10, 750),
    pygame.Rect(1210, 200, 140, 10),
    pygame.Rect(1200, 750, 150, 10),
    pygame.Rect(1350, 750, 10, 100),
    pygame.Rect(1250, 850, 200, 10),

    # lorong 8
    pygame.Rect(1600, 200, 10, 880),
    pygame.Rect(1410, 500, 130, 10),
    pygame.Rect(1450, 800, 150, 10),
    pygame.Rect(1450, 800, 10, 60),

    # area akhir
    pygame.Rect(1610, 200, 200, 10),
    pygame.Rect(1800, 200, 10, 150),
    pygame.Rect(1610, 850, 250, 10),
    pygame.Rect(1700, 500, 210, 10),
]

# =========================
# COLLISION
# =========================
def collide(obj, walls):
    obj_rect = obj.get_rect()

    for wall in walls:
        if obj_rect.colliderect(wall):
            return True

    return False

# =========================
# GAME LOOP
# =========================
running = True
game_over = False

clock = pygame.time.Clock()

while running:

    clock.tick(144)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    prev_x = pemain.x
    prev_y = pemain.y

    # =========================
    # GAMBAR KE WORLD
    # =========================
    world.fill(white)

    if not game_over:

        pemain.move(keys)

        # collision
        if collide(pemain, tembok):
            pemain.x = prev_x
            pemain.y = prev_y

        # menang
        if pemain.get_rect().colliderect(finish.get_rect()):
            game_over = True

    # gambar tembok
    for wall in tembok:
        pygame.draw.rect(world, black, wall)

    # game over
    if game_over:

        font = pygame.font.SysFont(None, 70)

        text = font.render(
            "ANDA MENANG",
            True,
            green
        )

        world.blit(text, (700, 500))

        pemain.speed = 0

    # gambar objek
    pemain.draw(world)
    finish.draw(world)

    # =========================
    # SCALE WORLD KE SCREEN
    # =========================
    scaled_world = pygame.transform.scale(
        world,
        (screen_width, screen_height)
    )
    screen.blit(scaled_world, (0, 0))
    pygame.display.update()

pygame.quit()
sys.exit()
