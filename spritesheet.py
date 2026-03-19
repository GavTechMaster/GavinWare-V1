import pygame
import numpy as np

class SpriteSheet:
    def __init__(self, spritesheet_path, sprite_sizes, sprite_amount, scale=1, exact_size=False):
        self.spritesheet = pygame.image.load(spritesheet_path).convert_alpha()
        self.sprites = []
        self.scale = scale
        self.sprite_sizes = sprite_sizes
        self.sprite_amount = sprite_amount
        self.sprite_index_x = 0
        self.sprite_index_y = 0
        for y in range(sprite_amount[1]):
            if y != 0:
                self.sprite_index_y += sprite_sizes[1]
            self.sprite_index_x = 0
            for x in range(sprite_amount[0]):
                if x != 0:
                    self.sprite_index_x += sprite_sizes[0]
                sprite_rect = (self.sprite_index_x, self.sprite_index_y, sprite_sizes[0], sprite_sizes[1])
                sprite_rect = self.spritesheet.subsurface(sprite_rect)
                alpha_array = pygame.surfarray.pixels_alpha(sprite_rect)
                if np.any(alpha_array > 0):
                    if not exact_size:
                        if not isinstance(self.scale, tuple):
                            sprite_rect = pygame.transform.scale(sprite_rect, (sprite_rect.get_width() * self.scale, sprite_rect.get_height() * self.scale))
                        else:
                            sprite_rect = pygame.transform.scale(sprite_rect, (sprite_rect.get_width() * self.scale[0], sprite_rect.get_height() * self.scale[1]))
                    else:
                        if not isinstance(self.scale, tuple):
                            sprite_rect = pygame.transform.scale(sprite_rect, (self.scale, self.scale))
                        else:
                            sprite_rect = pygame.transform.scale(sprite_rect, (self.scale[0], self.scale[1]))
                    self.sprites.append(sprite_rect)
                else:
                    continue
        self.current_frame = 0
        self.image = self.sprites[self.current_frame]
        self.last_update = pygame.time.get_ticks()
        self.original_sprites = self.sprites

    def play(self, fps, start_index=0, end_index="END"):
        self.fps = fps

        frame_delay = 1000 / self.fps

        if end_index in ("end", "END"):
            end_index = len(self.sprites)

        current_spritesheet = self.sprites[start_index:end_index]

        now = pygame.time.get_ticks()

        if now - self.last_update > frame_delay:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(current_spritesheet)
            self.image = current_spritesheet[self.current_frame]

    def update_size(self, scale):
        self.scale = scale
        new_sprites = []
        for sprite in self.original_sprites:
            scaled_surf = pygame.transform.scale(sprite, (self.sprite_sizes[0] * self.scale, self.sprite_sizes[1] * self.scale))
            new_sprites.append(scaled_surf)
        self.sprites = new_sprites
        self.image = self.sprites[self.current_frame]