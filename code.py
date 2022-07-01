import pygame
import random

class Batman(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.batmobile = False
        self.mobile_timer = 0
        self.play_sound = False

        self.frames = []
        frame_count = 13
        for i in range(frame_count):
            path = f"Files/Batman/{i}.png"
            surf = pygame.image.load(path)
            surf = pygame.transform.rotozoom(surf, 0, 1.12)
            self.frames.append(surf)

        self.frame_index = 0
        self.y_pos = 481
        self.batman = self.frames[int(self.frame_index)]
        self.batman_rect = self.batman.get_rect(midbottom=(150, self.y_pos))
        self.image = self.batman
        self.rect = self.batman_rect
        self.gravity = 0

        self.bt_surf = pygame.image.load("Files/Batman/bm.png")
        self.bt_surf =  pygame.transform.rotozoom(self.bt_surf, 0, 1.1)
        self.bt_rect = self.bt_surf.get_rect(midbottom=(155, 300))

    def user_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == self.y_pos:
            self.gravity = -25

    def apply_gravity(self):
        if self.batmobile:
            self.gravity += 0.7
        else:
            self.gravity += 1
        self.rect.bottom += self.gravity
        if self.rect.bottom >= self.y_pos:
            self.rect.bottom = self.y_pos

    def animate(self):
        if self.batmobile:
            if not self.play_sound:
                pygame.mixer.Sound('Files/mobile.ogg').play()
                self.play_sound = True
            self.image = self.bt_surf
            self.rect = self.bt_rect
            self.mobile_timer += 0.01
            if self.mobile_timer >= 5: 
                pygame.mixer.Sound('Files/mobile_off.ogg').play()
                self.mobile_timer = 0
                self.batmobile = False
                self.play_sound = False
                self.image, self.rect = self.batman, self.batman_rect
                self.rect.y = self.y_pos
                self.bt_rect.y = 350
                self.gravity = 0
        else:
            if self.rect.bottom >= self.y_pos:
                self.frame_index += 0.25
                if self.frame_index >= len(self.frames): self.frame_index = 0
                self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()
        self.apply_gravity()
        self.user_input()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type
        self.frames = []

        if type == "joker":
            frame_count = 31
            self.frame_speed = 0.25
            self.y_pos = 478
            for i in range(frame_count):
                path = f"Files/Joker/joker-{i}.png"
                surf = pygame.image.load(path)
                surf = pygame.transform.rotozoom(surf, 0, 0.6)
                self.frames.append(surf)

        elif type == "bomb":
            frame_count = 2
            self.frame_speed = 0.1
            self.y_pos = 220
            for i in range(frame_count):
                path = f"Files/Bomb/bomb-{i}.png"
                surf = pygame.image.load(path)
                self.frames.append(surf)

        elif type == "power":
            frame_count = 39
            self.frame_speed = 0.25
            self.y_pos = 220
            for i in range(frame_count):
                path = f"Files/Power/logo-{i}.png"
                surf = pygame.image.load(path)
                self.frames.append(surf)

        self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        pos = [x for x in range(1200, 1600, 60)]
        self.rect = self.image.get_rect(midbottom=(random.choice(pos), self.y_pos))
        self.gravity = 0
    
    def animate(self):
        self.frame_index += self.frame_speed
        if self.frame_index >= len(self.frames): self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()
        self.destroy()
        self.rect.x -= 6

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def check_collisions():
    global obstacles, player, batman
    player_rect = player.sprite.rect
    (x1, y1), (x2, y2) = player_rect.topleft, player_rect.bottomright
    x1 += 100
    for obstacle in obstacles:
        obstacle_center = obstacle.rect.center
        if x2 >= obstacle_center[0] >= x1 and y2 >= obstacle_center[1] >= y1:
            if obstacle.type == "power":
                obstacle.kill()
                if batman.batmobile:
                    batman.mobile_timer = 0
                else:
                    batman.batmobile = True
            else:
                obstacles.empty()
                batman.kill()
                return True
    return False

pygame.init()
pygame.display.set_caption("Batman Runner")
screen = pygame.display.set_mode((1100, 600))

clock = pygame.time.Clock()
font = pygame.font.Font("Files/font.ttf", 40)
game_active = False
song = pygame.mixer.Sound("Files/game.wav")
song.set_volume(0.3)
song_playing = False
score = 0

pygame.mixer.music.load("Files/main.wav")
pygame.mixer.music.set_volume(0.5)

sky = pygame.Surface((1100, 475))
sky.fill((240, 240, 240))
sky_rect = sky.get_rect(topleft=(0,0))
ground = pygame.image.load("Files/Bg/ground.png")
ground_rect = ground.get_rect(topleft=(0,475))

player = pygame.sprite.GroupSingle()
batman = Batman()
player.add(batman)
obstacles = pygame.sprite.Group()

game_over = pygame.Surface((1100, 600))
game_over.fill((200, 200, 200))
batman_still = pygame.image.load("Files/batman.png")
batman_still_rect = batman_still.get_rect(bottomleft=(360, 600))

obstacle_event = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_event, 2000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_event:
                e = random.choice([0, 1, 2])
                if e == 0:
                    obstacles.add(Obstacle("bomb"))
                elif e == 1:
                    obstacles.add(Obstacle("joker"))
                else:
                    obstacles.add(Obstacle("power"))
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    game_active = True
                    score = 0
                    batman = Batman()
                    player.add(batman)

    if game_active:
            if not song_playing:
                song.play(loops=-1)
                song_playing = True

            screen.blit(sky, sky_rect)
            screen.blit(ground, ground_rect)

            player.draw(screen)
            player.update()
            obstacles.draw(screen)
            obstacles.update()

            score += 0.02
            score_text = font.render(f"Score: {int(score)}", "Black", True)
            score_text_rect = score_text.get_rect(center=(550, 50))
            pygame.draw.rect(screen, (230, 230, 230), score_text_rect, width=10)
            pygame.draw.rect(screen, (230, 230, 230), score_text_rect, width=0)
            screen.blit(score_text, score_text_rect)

            game_active = not check_collisions()
    else:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
        if song_playing:
            song.stop()
            song_playing = False
        screen.blit(game_over, (0, 0))
        screen.blit(batman_still, batman_still_rect)
        
        if score:
            text = f"Your Score: {int(score)}"
        else:
            text = "Press Enter to play"

        text_surf = font.render(text, True, "Black")
        text_rect = text_surf.get_rect(center=(550, 150))
        pygame.draw.rect(screen, (230, 230, 230), text_rect, width=10)
        pygame.draw.rect(screen, (230, 230, 230), text_rect, width=0)
        screen.blit(text_surf, text_rect)

    pygame.display.update()
    clock.tick(60)