import pygame
import sys
pygame.init()

WIDTH, HEIGHT = 1000, 750
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
pygame.display.set_caption("Game Rpg")

pink = (255, 192, 203)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
BLACK = (0, 0, 0)
CHOCLATE = (139, 69, 19)
font = pygame.font.Font(None, 36)

# === FOV & CAMERA ===
FOV_RADIUS = 80
camera_x = 0
camera_y = 0

class Obstacle:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (50, 50, 50)

class Entity:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.color = color
        self.speed = 4
        self.name = "Player"
        self.has_key = False 

    def move(self, keys, obstacles):
        old_x = self.rect.x
        old_y = self.rect.y

        if keys[pygame.K_LEFT]:  self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]: self.rect.x += self.speed
        
        for obj in obstacles:
            if self.rect.colliderect(obj.rect):
                self.rect.x = old_x 

        if keys[pygame.K_UP]:    self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:  self.rect.y += self.speed
        
        for obj in obstacles:
            if self.rect.colliderect(obj.rect):
                self.rect.y = old_y 

        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > 1920: self.rect.right = 1920
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > 1200: self.rect.bottom = 1200

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
    
class Key(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, (255, 215, 0))
        self.is_collected = False

    def interact(self):
        self.is_collected = True
        return "Kamu mendapatkan kunci"
    
class Pintu(Entity):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, pink)
        self.rect = pygame.Rect(x, y, w, h)
        self.locked = True

    def interact(self):
        if player.has_key:
            self.locked = False
            self.color = (0, 255, 0)
            return "Pintu terbuka!"
        else:
            return "Pintu terkunci. Kamu butuh kunci."

    def interact(self):
        if player.has_key:
            self.locked = False
            self.color = (0, 255, 0)
            return "Pintu terbuka!"
            
        else:
            return "Pintu terkunci. Kamu butuh kunci."


player = Entity(30, 1150, (0, 0, 255))
villager = NPC(70, 1990, "Ambil peti itu dan bawa kembali ke sini!")
treasure = Treasure(870, 505)
key_item = Key(600, 300)

jebakan_list = [
    Trap(30, 1070),
    Trap(380, 803),
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

doors = [
    Pintu(1500, 500, 80, 20),
    Pintu(900, 700, 20, 100),
    Pintu(400, 300, 100, 20)
]

tembok_list = [
#batas luar
    Obstacle(0, 0, 1920, 10),
    Obstacle(50, 1070, 1870, 10),
    Obstacle(0, 0, 10, 1080),
    Obstacle(1910, 0, 10, 1080),

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
    screen.fill(CHOCLATE)
    
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

                elif not key_item.is_collected and player.rect.inflate(30, 30).colliderect(key_item.rect):
                    active_message = key_item.interact()
                    player.has_key = True

                for door in doors:
                    if player.rect.inflate(30, 30).colliderect(door.rect):
                        active_message = door.interact()
                        break
                
                else:
                    active_message = ""

    keys = pygame.key.get_pressed()

    if not is_dead:
        current_obstacles = tembok_list + [villager]

    if not treasure.is_collected:
        current_obstacles.append(treasure)

    for door in doors:
        if door.locked:
            current_obstacles.append(door)

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

    # map render
    for obstacle in tembok_list:
        pygame.draw.rect(screen, obstacle.color, obstacle.rect.move(-camera_x, -camera_y))
        
    for jebakan in jebakan_list:
            if not jebakan.is_triggered:
                pygame.draw.rect(screen, jebakan.color, jebakan.rect.move(-camera_x, -camera_y))
    
    pygame.draw.rect(screen, villager.color, villager.rect.move(-camera_x, -camera_y))

    pygame.draw.rect(screen, villager.color, villager.rect.move(-camera_x, -camera_y))

    for door in doors:
        pygame.draw.rect(screen, door.color, door.rect.move(-camera_x, -camera_y))

    if not key_item.is_collected:
        pygame.draw.rect(
            screen,
            key_item.color,
            key_item.rect.move(-camera_x, -camera_y)
        )
    
    if not treasure.is_collected:
        pygame.draw.rect(screen, treasure.color, treasure.rect.move(-camera_x, -camera_y))
        
    pygame.draw.rect(screen, player.color, player.rect.move(-camera_x, -camera_y))

    # fov luar
#    fog = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
#    fog.fill((0, 0, 0, 255))  # hitam FULL

    player_screen = (
        player.rect.centerx - camera_x,
        player.rect.centery - camera_y
)
   

# fov dalam
#    pygame.draw.circle(fog, (0, 0, 0, 0), player_screen, FOV_RADIUS)

#    screen.blit(fog, (0, 0))

    # UI Dialog
    if active_message:
        text_surf = font.render(active_message, True, WHITE)
        pygame.draw.rect(screen, (0, 0, 0), (50, 500, 700, 60))
        screen.blit(text_surf, (70, 520))

    
    pygame.display.flip()
    clock.tick(60) 

pygame.quit()
sys.exit()
