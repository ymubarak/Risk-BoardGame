import pygame
import View.Colors as Colors
from View import Utility

# paths
LOGO_IMG = "media/images/logo.png"

#colors
SPLASH_BACKGROUND = Colors.dark

class SplashScreen:
    def __init__(self, master, screen_size):
        splash = pygame.Surface(screen_size)
        splash.fill(SPLASH_BACKGROUND)
        # adding logo to the splash
        logo = pygame.image.load(LOGO_IMG)
        logo_rect = logo.get_rect()
        logo_rect.center = (screen_size[0]/2, screen_size[1]/2)
        splash.blit(logo, logo_rect)
        # adding text
        txt = "AI ? Here it comes"
        font_size = 36
        Utility.draw_text(splash, txt, screen_size[0]/2, screen_size[0]/2-font_size,
         font_size, font_name="Wide Latin")
        
        # fade in
        master.blit(splash, (0, 0))
        for alpha in range(300, -1, -1):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            splash.set_alpha(alpha)
            master.fill(Colors.black)
            master.blit(splash, (0, 0))
            pygame.time.delay(2)
            pygame.display.update()