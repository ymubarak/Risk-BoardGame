import pygame
import View.Colors as Colors

# paths
GAME_PLAY_SOUND = 'media/sound/gameplay.mp3'
OPEN_SOUND = "media/sound/open.Ogg"
GAME_OVER = "media/sound/gameover.wav"

def play_sound(clip_num):
    if clip_num==0:
        pygame.mixer.music.load(GAME_PLAY_SOUND)
        pygame.mixer.music.play(-1)
    elif clip_num==1:
        pygame.mixer.music.load(OPEN_SOUND)
        pygame.mixer.music.play()
    elif clip_num==2:
        pygame.mixer.music.load(GAME_OVER)
        pygame.mixer.music.play()


def draw_text(screen, text, x, y, size=16, color=Colors.white, font_name="Cambria", center=False):
    font = pygame.font.SysFont(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.midtop = (x, y)
    
    screen.blit(text_surface, text_rect)
    return text_surface