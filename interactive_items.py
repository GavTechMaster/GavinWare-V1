import pygame

class Interactive_Item(pygame.sprite.Sprite):
    def __init__(self, image_path, interaction, position=(0, 0), scale=1):
        pygame.sprite.Sprite.__init__(self)
        if isinstance(image_path, str):
            self.image = pygame.image.load(image_path).convert_alpha()
        else:
            self.image = self.image
        self.scale = scale
        self.original_image = self.image
        self.image = pygame.transform.scale_by(self.image, self.scale)
        self.interaction = interaction
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
    def interacted(self, interaction_argument):
        if interaction_argument == None:
            self.interaction()
        else:
            self.interaction(interaction_argument)
    def update_size(self, scale):
        self.scale = scale
        self.image = pygame.transform.scale_by(self.original_image, self.scale)