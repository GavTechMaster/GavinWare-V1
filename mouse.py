import pygame

class Mouse(pygame.sprite.Sprite):
    def __init__(self, image_path, selected_image_path, screen, move_mappings=(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN), speed=5, scale=1):
        pygame.sprite.Sprite.__init__(self)
        if isinstance(image_path, str):
            self.image = pygame.image.load(image_path).convert_alpha()
        else:
            self.image = image_path
        if isinstance(selected_image_path, str):
            self.selected_image = pygame.image.load(selected_image_path).convert_alpha()
        else:
            self.selected_image = selected_image_path
        self.scale = scale
        self.image = pygame.transform.scale_by(self.image, self.scale)
        self.selected_image = pygame.transform.scale_by(self.selected_image, self.scale)
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.speed = speed
        self.left_move = move_mappings[0]
        self.right_move = move_mappings[1]
        self.up_move = move_mappings[2]
        self.down_move = move_mappings[3]
        self.screen = screen
        try:
            self.rect.x = round(self.screen[0] / 2) - round(self.image.get_width() / 2)
            self.rect.y = round(self.screen[1] / 2) - round(self.image.get_height() / 2)
        except:
            self.rect.x = 0
            self.rect.y = 0

    def mouse_move(self):
        keys = pygame.key.get_pressed()
        if keys[self.left_move]:
            if self.rect.x > 0:
                self.rect.x -= self.speed
        if keys[self.right_move]:
            if (self.rect.x + self.image.get_width()) < self.screen[0]:
                self.rect.x += self.speed
        if keys[self.up_move]:
            if self.rect.y > 0:
                self.rect.y -= self.speed
        if keys[self.down_move]:
            if (self.rect.y + self.image.get_height()) < self.screen[1]:
                self.rect.y += self.speed