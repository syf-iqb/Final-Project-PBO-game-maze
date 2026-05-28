import pygame
import sys
pygame.init()

WIDTH, HEIGHT = 1000, 750
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
pygame.display.set_caption("Game RPG OOP")

# WARNA
pink = (255, 192, 203)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
BLACK = (0, 0, 0)
CHOCLATE = (139, 69, 19)

font = pygame.font.Font(None, 36)

# CAMERA
camera_x = 0
camera_y = 0


# =========================
# ENCAPSULATION + ABSTRACTION
# =========================
class Entity:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.color = color

        # ENCAPSULATION
        self.__speed = 4

        self.name = "Player"
        self.has_key = False

    # getter
    def get_speed(self):
        return self.__speed

    # setter
    def set_speed(self, value):
        self.__speed = value

    # ABSTRACTION
    def draw(self, screen, camera_x, camera_y):
        pygame.draw.rect(
            screen,
            self.color,
            self.rect.move(-camera_x, -camera_y)
        )

    # POLYMORPHISM DASAR
    def interact(self):
        return "Tidak ada interaksi"

    def move(self, keys, obstacles):

        old_x = self.rect.x
        old_y = self.rect.y

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.get_speed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.get_speed()

        for obj in obstacles:
            if self.rect.colliderect(obj.rect):
                self.rect.x = old_x

        if keys[pygame.K_UP]:
            self.rect.y -= self.get_speed()

        if keys[pygame.K_DOWN]:
            self.rect.y += self.get_speed()

        for obj in obstacles:
            if self.rect.colliderect(obj.rect):
                self.rect.y = old_y

        # batas map
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > 1920:
            self.rect.right = 1920

        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > 1200:
            self.rect.bottom = 1200


# =========================
# INHERITANCE
# =========================
class Obstacle:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (50, 50, 50)

    def draw(self, screen, camera_x, camera_y):
        pygame.draw.rect(
            screen,
            self.color,
            self.rect.move(-camera_x, -camera_y)
        )


class NPC(Entity):
    def __init__(self, x, y, message):
        super().__init__(x, y, (200, 200, 0))
        self.message = message

    # POLYMORPHISM
    def interact(self):
        return self.message


class Treasure(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, (220, 220, 220))
        self.is_collected = False

    # POLYMORPHISM
    def interact(self):
        self.is_collected = True
        return "Kamu mendapatkan peti"


class Trap(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, (255, 0, 0))
        self.is_triggered = False

    def trigger(self):
        self.is_triggered = True
        return "Terkena jebakan, tekan SPASI."


class Key(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, (255, 215, 0))
        self.is_collected = False

    # POLYMORPHISM
    def interact(self):
        self.is_collected = True
        return "Kamu mendapatkan kunci"


class Pintu(Entity):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, pink)
        self.rect = pygame.Rect(x, y, w, h)
        self.locked = True

    # POLYMORPHISM
    def interact(self):
        if player.has_key:
            self.locked = False
            self.color = (0, 255, 0)
            return "Pintu terbuka!"
        else:
            return "Pintu terkunci. Kamu butuh kunci."


# =========================
# OBJECT
# =========================
player = Entity(30, 1150, (0, 0, 255))

villager = NPC(
    70,
    990,
    "Ambil peti itu dan bawa kembali ke sini!"
)

treasure = Treasure(870, 505)

key_item = Key(600, 300)

jebakan_list = [
    Trap(30, 1070),
    Trap(380, 803),
    Trap(368, 603),
    Trap(250, 480),
    Trap(330, 277),
]

doors = [
    Pintu(900, 700, 20, 100),
    Pintu(400, 300, 100, 20)
]

tembok_list = [

    # batas luar
    Obstacle(0, 0, 1920, 10),
    Obstacle(50, 1070, 1870, 10),
    Obstacle(0, 0, 10, 1080),
    Obstacle(1910, 0, 10, 1080),

    # lorong
    Obstacle(200, 0, 10, 1000),
    Obstacle(400, 200, 10, 880),
    Obstacle(600, 0, 10, 400),
    Obstacle(800, 100, 10, 980),
]


active_message = ""
is_dead = False

running = True

while running:

    screen.fill(CHOCLATE)

    # =========================
    # EVENT
    # =========================
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            # INTERAKSI
            if event.key == pygame.K_SPACE:

                # mati kena trap
                if is_dead:

                    is_dead = False

                    player.rect.x = 30
                    player.rect.y = 1150

                    for jebakan in jebakan_list:
                        jebakan.is_triggered = False

                    active_message = ""

                else:

                    # POLYMORPHISM
                    interact_objects = [villager]

                    if not treasure.is_collected:
                        interact_objects.append(treasure)

                    if not key_item.is_collected:
                        interact_objects.append(key_item)

                    interact_objects += doors

                    for obj in interact_objects:

                        if player.rect.inflate(30,30).colliderect(obj.rect):

                            active_message = obj.interact()

                            # selesai game
                            if obj == villager and treasure.is_collected:

                                active_message = "Misi telah selesai!"

                                text_surf = font.render(
                                    active_message,
                                    True,
                                    WHITE
                                )

                                pygame.draw.rect(
                                    screen,
                                    BLACK,
                                    (50, 500, 700, 60)
                                )

                                screen.blit(text_surf, (70, 520))

                                pygame.display.flip()

                                pygame.time.delay(3000)

                                running = False

                            # ambil kunci
                            if obj == key_item:
                                player.has_key = True

                            break

                    else:
                        active_message = ""

    # =========================
    # MOVEMENT
    # =========================
    keys = pygame.key.get_pressed()

    current_obstacles = tembok_list + [villager]

    if not treasure.is_collected:
        current_obstacles.append(treasure)

    for door in doors:
        if door.locked:
            current_obstacles.append(door)

    player.move(keys, current_obstacles)

    # =========================
    # TRAP
    # =========================
    for jebakan in jebakan_list:

        if not jebakan.is_triggered and player.rect.colliderect(jebakan.rect):

            active_message = jebakan.trigger()

            is_dead = True

            break

    # =========================
    # CAMERA
    # =========================
    WIDTH, HEIGHT = screen.get_size()

    camera_x = player.rect.centerx - WIDTH // 2
    camera_y = player.rect.centery - HEIGHT // 2

    # =========================
    # DRAW MAP
    # =========================
    for obstacle in tembok_list:
        obstacle.draw(screen, camera_x, camera_y)

    # trap
    for jebakan in jebakan_list:
        if not jebakan.is_triggered:
            jebakan.draw(screen, camera_x, camera_y)

    # npc
    villager.draw(screen, camera_x, camera_y)

    # door
    for door in doors:
        door.draw(screen, camera_x, camera_y)

    # key
    if not key_item.is_collected:
        key_item.draw(screen, camera_x, camera_y)

    # treasure
    if not treasure.is_collected:
        treasure.draw(screen, camera_x, camera_y)

    # player
    player.draw(screen, camera_x, camera_y)

    # =========================
    # UI
    # =========================
    if active_message:

        text_surf = font.render(
            active_message,
            True,
            WHITE
        )

        pygame.draw.rect(
            screen,
            BLACK,
            (50, 500, 700, 60)
        )

        screen.blit(text_surf, (70, 520))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
