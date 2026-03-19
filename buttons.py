import pygame 
class Button():
    def __init__(self, original_image, selected_image, button_list, button_index, scale=1, select_button=pygame.K_w):
        self.scale = scale
        self.button_list = button_list
        self.button_index = button_index

        if not isinstance(original_image, str):
            self.original_image = original_image
        else:
            self.original_image = pygame.image.load(original_image).convert_alpha()

        self.original_image_size = (self.original_image.get_width(), self.original_image.get_height())
        self.original_image = pygame.transform.scale(self.original_image, (self.original_image.get_width() * self.scale, self.original_image.get_height() * self.scale))

        if not isinstance(selected_image, str):
            self.selected_image = selected_image
        else:
            self.selected_image = pygame.image.load(selected_image).convert_alpha()

        self.selected_image_size = (self.selected_image.get_width(), self.selected_image.get_height())
        self.selected_image = pygame.transform.scale(self.selected_image, (self.selected_image.get_width() * self.scale, self.selected_image.get_height() * self.scale))

        self.image = self.original_image

        if self not in self.button_list:
            self.button_list.append(self)
        
        self.select_button = select_button
    
    def button_focus(self):
        if self.button_list[self.button_index] == self:
            self.image = self.selected_image
        else:
            self.image = self.original_image
    
    def pressed(self, event_key):
        if event_key == self.select_button and self.button_list[self.button_index] == self:
            return True
        else:
            return False
    
    def update_size(self, scale):
        self.scale = scale
        self.original_image = pygame.transform.scale(self.original_image, (self.original_image_size[0] * self.scale, self.original_image_size[1] * self.scale))
        self.selected_image = pygame.transform.scale(self.selected_image, (self.selected_image_size[0] * self.scale, self.selected_image_size[1] * self.scale))
        if self.button_list[self.button_index] == self:
            self.image = self.selected_image
        else:
            self.image = self.original_image