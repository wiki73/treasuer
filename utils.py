import os
import sys
import pygame
def load_image(name, colorkey=None):
    fullname = os.path.join('', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        pygame.quit()
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image
def create_heart_surface(width=30, height=30, color=(255, 0, 0), empty=False):
    heart = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Цвет для пустого (серого) сердца
    gray_color = (128, 128, 128) if empty else color
    
    heart_pixels = [
        [0,0,1,1,0,0,0,1,1,0,0],
        [0,1,1,1,1,0,1,1,1,1,0],
        [1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1],
        [0,1,1,1,1,1,1,1,1,1,0],
        [0,0,1,1,1,1,1,1,1,0,0],
        [0,0,0,1,1,1,1,1,0,0,0],
        [0,0,0,0,1,1,1,0,0,0,0],
        [0,0,0,0,0,1,0,0,0,0,0]
    ]
    
    pixel_width = width // len(heart_pixels[0])
    pixel_height = height // len(heart_pixels)
    
    for y, row in enumerate(heart_pixels):
        for x, pixel in enumerate(row):
            if pixel:
                pygame.draw.rect(heart, gray_color, 
                               (x * pixel_width, y * pixel_height, 
                                pixel_width, pixel_height))
    
    return heart