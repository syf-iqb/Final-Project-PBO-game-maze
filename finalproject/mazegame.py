import pygame
import sys
import os
pygame.init()

WIDTH, HEIGHT = 1000, 750
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
pygame.display.set_caption("Game Rpg")

WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
BLACK = (0, 0, 0)
CHOCLATE = (139, 69, 19)
font = pygame.font.Font(None, 36)

# === FOV & CAMERA ===
FOV_RADIUS = 80
camera_x = 0
camera_y = 0

# === LOAD SPRITE SOLDIER ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_sprite_sheet(filename, frame_width, frame_height, scale=None):
    """Memuat sprite sheet dan memotongnya menjadi list frame."""
    path = os.path.join(BASE_DIR, filename)
    sheet = pygame.image.load(path).convert_alpha()
    sheet_width = sheet.get_width()
    frames = []
    num_frames = sheet_width // frame_width
    for i in range(num_frames):
        frame = sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        if scale:
            frame = pygame.transform.scale(frame, scale)
        frames.append(frame)
    return frames

# Ukuran tile sprite soldier (sesuaikan jika berbeda)
SOLDIER_FRAME_W = 100
SOLDIER_FRAME_H = 100
SOLDIER_SCALE = (120, 120)  # ukuran render di layar

soldier_idle_frames = load_sprite_sheet("Soldier-Idle.png", SOLDIER_FRAME_W, SOLDIER_FRAME_H, SOLDIER_SCALE)
soldier_walk_frames = load_sprite_sheet("Soldier-Walk.png", SOLDIER_FRAME_W, SOLDIER_FRAME_H, SOLDIER_SCALE)

# === LOAD DUNGEON TILESET ===
# Tileset 160x160 px, grid 10x10 tile, masing-masing 16x16 px
TILE_SRC = 16        # ukuran tile asli di file PNG
TILE_SIZE = 32       # ukuran tile saat di-render di layar
MAP_W = 1920
MAP_H = 1200

def get_tile(sheet, col, row, src_size=TILE_SRC, dst_size=TILE_SIZE):
    """Ambil satu tile dari tileset berdasarkan kolom & baris (0-indexed)."""
    tile = sheet.subsurface(pygame.Rect(col * src_size, row * src_size, src_size, src_size))
    return pygame.transform.scale(tile, (dst_size, dst_size))

tileset_sheet = pygame.image.load(os.path.join(BASE_DIR, "Dungeon_Tileset.png")).convert_alpha()

# Pilih tile — sesuaikan col/row jika tampilan kurang cocok
tile_floor = get_tile(tileset_sheet, 1, 1)   # lantai tengah
tile_wall  = get_tile(tileset_sheet, 0, 0)   # dinding / batu

# Pre-render seluruh map ke satu surface besar
map_surface = pygame.Surface((MAP_W, MAP_H))
for ty in range(0, MAP_H, TILE_SIZE):
    for tx in range(0, MAP_W, TILE_SIZE):
        map_surface.blit(tile_floor, (tx, ty))

class Obstacle:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (50, 50, 50)

    def draw(self, surface, cam_x, cam_y):
        """Render obstacle dengan tile wall yang di-tile sesuai ukuran rect."""
        rx = self.rect.x - cam_x
        ry = self.rect.y - cam_y
        # Clip area agar tile tidak meluber keluar batas obstacle
        clip_rect = pygame.Rect(rx, ry, self.rect.w, self.rect.h)
        old_clip = surface.get_clip()
        surface.set_clip(clip_rect)
        for ty in range(0, self.rect.h, TILE_SIZE):
            for tx in range(0, self.rect.w, TILE_SIZE):
                surface.blit(tile_wall, (rx + tx, ry + ty))
        surface.set_clip(old_clip)

class Entity:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.color = color
        self.speed = 4
        self.name = "Player"

        # --- Animasi sprite ---
        self.idle_frames = soldier_idle_frames
        self.walk_frames = soldier_walk_frames
        self.current_frames = self.idle_frames
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 8   # ganti frame setiap N tick
        self.is_moving = False
        self.facing_left = False   # untuk flip sprite

    def update_animation(self):
        """Pilih animasi yang tepat dan majukan frame."""
        target_frames = self.walk_frames if self.is_moving else self.idle_frames
        if target_frames is not self.current_frames:
            self.current_frames = target_frames
            self.frame_index = 0
            self.animation_timer = 0

        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.current_frames)

    def get_image(self):
        """Kembalikan frame saat ini, di-flip jika menghadap kiri."""
        img = self.current_frames[self.frame_index]
        if self.facing_left:
            img = pygame.transform.flip(img, True, False)
        return img

    def move(self, keys, obstacles):
        old_x = self.rect.x
        old_y = self.rect.y
        self.is_moving = False

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.is_moving = True
            self.facing_left = True
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.is_moving = True
            self.facing_left = False
        
        for obj in obstacles:
            if self.rect.colliderect(obj.rect):
                self.rect.x = old_x 

        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
            self.is_moving = True
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.is_moving = True
        
        for obj in obstacles:
            if self.rect.colliderect(obj.rect):
                self.rect.y = old_y 

        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > 1920: self.rect.right = 1920
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > 1200: self.rect.bottom = 1200

        self.update_animation()

class NPC(Entity):
    def __init__(self, x, y, message):
        super().__init__(x, y, (200, 200, 0))
        self.message = message

    def talk(self):
        return self.message

class Treasure(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, (220, 220, 220))
        self.is_collected = False

    def interact(self):
        self.is_collected = True
        return "Kamu mendapatkan peti"
    
class Trap(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, (255, 0, 0))
        self.is_triggered = False

    def trigger(self):
        self.is_triggered = True
        return "Terkena jebakan, Tekan SPASI. "


player = Entity(30, 1150, (0, 0, 255))
villager = NPC(70, 1990, "Ambil peti itu dan bawa kembali ke sini!")
treasure = Treasure(870, 505)
jebakan_list = [
    Trap(368, 603),
    Trap(250, 480),
    Trap(330, 277),
    Trap(235, 26),
    Trap(365, 30),
    Trap(100, 125),
    Trap(575, 70), 
    Trap(575, 340),
    Trap(525, 590),
    Trap(420, 540),
    Trap(495, 830),
    Trap(505, 880),
    Trap(510, 930),
    Trap(510, 1030),
    Trap(700, 435),
    Trap(705, 710),
    Trap(700, 970),
    Trap(625, 90),
    Trap(865, 75),
    Trap(845, 270),
    Trap(880, 880),
    Trap(930, 930),
    Trap(980, 1045),
    Trap(1120, 980),
    Trap(820, 785),
    Trap(1226, 855),
]

tembok_list = [
#batas luar
    Obstacle(0, 0, 1920, 20),
    Obstacle(50, 1070, 1870, 20),
    Obstacle(0, 0, 20, 1080),
    Obstacle(1910, 0, 20, 1080),

    #spawn area
    Obstacle(0, 1200, 450, 10),
    Obstacle(0, 1200, 450, 10),
    Obstacle(0, 0, 10, 1200),
    Obstacle(450, 1070, 10, 140),

    # lorong 1
    Obstacle(200, 0, 10, 1000),
    Obstacle(10, 300, 140, 10),
    Obstacle(60, 600, 140, 10),

    # lorong 2
    Obstacle(400, 200, 10, 880),
    Obstacle(210, 800, 140, 10),
    Obstacle(250, 400, 150, 10),

    #A
    Obstacle(350, 700, 10, 110),
    Obstacle(300, 650, 100, 10),
    Obstacle(300, 650, 10, 100),
    Obstacle(250, 550, 10, 200),
    Obstacle(250, 600, 100, 10),
    Obstacle(250, 550, 150, 10),
    Obstacle(210, 500, 140, 10),
    Obstacle(210, 450, 140, 10),

    #B
    Obstacle(210, 350, 140, 10),
    Obstacle(210, 300, 140, 10),
    Obstacle(250, 250, 150, 10),
    Obstacle(250, 200, 150, 10),
    Obstacle(250, 100, 10, 100),
    Obstacle(210, 50, 50, 10),
    Obstacle(300, 50, 10, 100),
    Obstacle(300, 50, 100, 10),
    Obstacle(400, 10, 10, 50),
    Obstacle(300, 150, 110, 10),
    Obstacle(350, 100, 100, 10),
    Obstacle(450, 50, 10, 150),
    Obstacle(500, 10, 10, 50),
    Obstacle(500, 50, 50, 10),
    Obstacle(550, 50, 10, 50),
    Obstacle(500, 150, 100, 10),
    Obstacle(500, 100, 10, 50),

    # lorong 3
    Obstacle(600, 0, 10, 400),
    Obstacle(600, 450, 10, 630),
    Obstacle(410, 200, 130, 10),
    Obstacle(500, 750, 60, 10),

    #C
    Obstacle(450, 250, 10, 500),
    Obstacle(500, 250, 10, 500),
    Obstacle(550, 250, 10, 700),
    Obstacle(550, 1000, 10, 70),
    Obstacle(550, 400, 60, 10),
    Obstacle(410, 750, 50, 10),
    Obstacle(450, 800, 100, 10),
    Obstacle(450, 850, 100, 10),
    Obstacle(450, 900, 100, 10),
    Obstacle(450, 950, 110, 10),
    Obstacle(450, 1000, 100, 10),
    Obstacle(450, 1050, 100, 10),

    # lorong 4
    Obstacle(800, 100, 10, 980),
    Obstacle(610, 450, 140, 10),
    Obstacle(650, 850, 150, 10),

    #E
    Obstacle(650, 400, 100, 10),
    Obstacle(750, 400, 10, 100),
    Obstacle(610, 350, 150, 10),
    Obstacle(650, 300, 100, 10),
    Obstacle(650, 200, 10, 100),
    Obstacle(650, 200, 100, 10),
    Obstacle(750, 100, 10, 110),
    Obstacle(650, 100, 100, 10),
    Obstacle(650, 10, 10, 100),
    Obstacle(600, 150, 100, 10),
    Obstacle(700, 250, 200, 10),
    Obstacle(800, 100, 150, 10),
    Obstacle(700, 50, 250, 10),
    Obstacle(950, 50, 10, 60),
    Obstacle(850, 150, 150, 10),
    Obstacle(850, 200, 100, 10),
    Obstacle(950, 200, 10, 400),

    # lorong 5
    Obstacle(1000, 0, 10, 950),
    Obstacle(810, 300, 150, 10),
    Obstacle(850, 650, 150, 10),

    #F
    Obstacle(900, 350, 10, 250),
    Obstacle(850, 350, 10, 300),

    #G
    Obstacle(900, 650, 10, 100),
    Obstacle(900, 750, 60, 10),
    Obstacle(940, 700, 60, 10),
    Obstacle(800, 750, 50, 10),
    Obstacle(850, 750, 10, 50),
    Obstacle(850, 800, 110, 10),
    Obstacle(850, 850, 50, 10),
    Obstacle(850, 850, 10, 50),
    Obstacle(850, 900, 100, 10),
    Obstacle(950, 850, 10, 60),
    Obstacle(900, 950, 110, 10),
    Obstacle(900, 900, 10, 50),
    Obstacle(850, 1000, 350, 10),
    Obstacle(1050, 950, 150, 10),

    # lorong 6
    Obstacle(1200, 150, 10, 250),
    Obstacle(1200, 450, 10, 300),
    Obstacle(1200, 800, 10, 280),
    Obstacle(1010, 850, 150, 10),

    # lorong 7
    Obstacle(1400, 0, 10, 750),
    Obstacle(1210, 200, 140, 10),
    Obstacle(1200, 750, 150, 10),
    Obstacle(1350, 750, 10, 100),
    Obstacle(1250, 850, 200, 10),

    # lorong 8
    Obstacle(1600, 200, 10, 880),
    Obstacle(1410, 500, 130, 10),
    Obstacle(1450, 800, 150, 10),
    Obstacle(1450, 800, 10, 60),

    # area akhir
    Obstacle(1610, 200, 200, 10),
    Obstacle(1800, 200, 10, 150),
    Obstacle(1610, 850, 250, 10),
    Obstacle(1700, 500, 210, 10),
]

active_message = ""
is_dead = False

running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #tempat cari koordinat
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            map_x = mouse_x + camera_x
            map_y = mouse_y + camera_y
            print(f"Koordinat Klik -> X: {map_x}, y: {map_y}")

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            
            if event.key == pygame.K_SPACE:
                
                if is_dead:
                    is_dead = False
                    player.rect.x = 30
                    player.rect.y = 1150
                    for jebakan in jebakan_list:
                        jebakan.is_triggered = False
                    active_message = ""
                    
                elif player.rect.inflate(30, 30).colliderect(villager.rect):
                    if treasure.is_collected:
                        active_message = "Misi telah selesai!"
                        
                        text_surf = font.render(active_message, True, WHITE)
                        pygame.draw.rect(screen, (0, 0, 0), (50, 500, 700, 60))
                        screen.blit(text_surf, (70, 520))
                        pygame.display.flip()
                        
                        pygame.time.delay(3000)
                        running = False
                    else:
                        active_message = villager.talk()
                
                elif not treasure.is_collected and player.rect.inflate(30, 30).colliderect(treasure.rect):
                    active_message = treasure.interact()
                
                else:
                    active_message = ""

    keys = pygame.key.get_pressed()

    if not is_dead:
        current_obstacles = tembok_list + [villager]
        if not treasure.is_collected:
            current_obstacles.append(treasure)
        
        player.move(keys, current_obstacles)

    for jebakan in jebakan_list:
        if not jebakan.is_triggered and player.rect.colliderect(jebakan.rect):
            active_message = jebakan.trigger()
            is_dead = True
            break

    WIDTH, HEIGHT = screen.get_size()

    # kamera tenggah
    camera_x = player.rect.centerx - WIDTH // 2
    camera_y = player.rect.centery - HEIGHT // 2

    # Render background dungeon tileset
    screen.fill((20, 20, 20))  # area luar map gelap
    screen.blit(map_surface, (-camera_x, -camera_y))
    
    # map render (dinding dengan tile wall)
    for obstacle in tembok_list:
        obstacle.draw(screen, camera_x, camera_y)
        
    for jebakan in jebakan_list:
            if not jebakan.is_triggered:
                pygame.draw.rect(screen, jebakan.color, jebakan.rect.move(-camera_x, -camera_y))
    
    pygame.draw.rect(screen, villager.color, villager.rect.move(-camera_x, -camera_y))
    
    if not treasure.is_collected:
        pygame.draw.rect(screen, treasure.color, treasure.rect.move(-camera_x, -camera_y))

    # Render player dengan sprite animasi
    player_img = player.get_image()
    img_w, img_h = player_img.get_size()
    draw_x = player.rect.centerx - camera_x - img_w // 2
    draw_y = player.rect.centery - camera_y - img_h // 2
    screen.blit(player_img, (draw_x, draw_y))

    # fov luar
    #fog = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    #fog.fill((0, 0, 0, 255))  # hitam FULL

    player_screen = (
        player.rect.centerx - camera_x,
        player.rect.centery - camera_y
)
   

# fov dalam
    #pygame.draw.circle(fog, (0, 0, 0, 0), player_screen, FOV_RADIUS)

    #screen.blit(fog, (0, 0))

    # UI Dialog
    if active_message:
        text_surf = font.render(active_message, True, WHITE)
        pygame.draw.rect(screen, (0, 0, 0), (50, 500, 700, 60))
        screen.blit(text_surf, (70, 520))

    
    pygame.display.flip()
    clock.tick(60) 

pygame.quit()
sys.exit()
