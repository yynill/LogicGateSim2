from enum import Enum
import pygame
from .settings import *


class DraggableObject(pygame.sprite.Sprite):
    def __init__(self, image_path, width, height):
        super().__init__()
        self.image_path = image_path
        self.original_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(
            self.original_image, (width, height))
        self.rect = self.image.get_rect()
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.selected = False

    def image(self):
        return self.original_image

    def set_opacity(self, opacity):
        temp_image = self.original_image.convert_alpha()
        temp_image.fill((255, 255, 255, opacity), None, pygame.BLEND_RGBA_MULT)
        self.image = pygame.transform.scale(
            temp_image, (self.rect.width, self.rect.height))

    def draw_selected_outline(self, surface, outline_color=SELECTION_BOX_OUTLINE_COLOR, outline_width=2):
        if self.selected:
            pygame.draw.rect(surface, outline_color, self.rect, outline_width)

    def is_left_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    return True
        return False

    def is_right_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                if self.rect.collidepoint(event.pos):
                    return True
        return False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and event.button == 1:
                self.dragging = True
                mouse_x, mouse_y = event.pos
                self.offset_x = self.rect.x - mouse_x
                self.offset_y = self.rect.y - mouse_y
                self.set_opacity(128)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
            self.set_opacity(255)

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x, mouse_y = event.pos
            self.rect.x = mouse_x + self.offset_x
            self.rect.y = mouse_y + self.offset_y


class Gate(DraggableObject):
    def __init__(self, image_path, width, height):
        super().__init__(image_path, width, height)

    def draw_slots(self, surface, color=(255, 0, 0)):
        slot_radius = 5
        # Draw input slots
        for input_slot in self.inputs:
            input_pos = (self.rect.x + input_slot[0],
                         self.rect.y + input_slot[1])
            pygame.draw.circle(surface, color, input_pos, slot_radius)

        # Draw output slot
        output_pos = (self.rect.x + self.output[0][0],
                      self.rect.y + self.output[0][1])
        pygame.draw.circle(surface, color, output_pos, slot_radius)


class AndGate(Gate):
    def __init__(self, image_path, width, height):
        super().__init__(image_path, width, height)
        self.inputs = [[10, 70, False], [34, 70, False]]
        self.output = [[21, 0, False]]

    def update_state(self):
        all_inputs_true = all(input_state[2] for input_state in self.inputs)
        self.output[0][2] = all_inputs_true


class OrGate(Gate):
    def __init__(self, image_path, width, height):
        super().__init__(image_path, width, height)
        self.inputs = [[10, 70, False], [34, 70, False]]
        self.output = [[21, 0, False]]

    def update_state(self):
        any_input_true = any(input_state[2] for input_state in self.inputs)
        self.output[0][2] = any_input_true


class NotGate(Gate):
    def __init__(self, image_path, width, height):
        super().__init__(image_path, width, height)
        self.inputs = [[21, 70, False]]
        self.output = [[21, 0, False]]

    def update_state(self):
        self.output[0][2] = not self.inputs[0][2]


class NandGate(Gate):
    def __init__(self, image_path, width, height):
        super().__init__(image_path, width, height)
        self.inputs = [[10, 70, False], [34, 70, False]]
        self.output = [[21, 0, False]]

    def update_state(self):
        self.output[0][2] = not all(input_state[2]
                                    for input_state in self.inputs)


class NorGate(Gate):
    def __init__(self, image_path, width, height):
        super().__init__(image_path, width, height)
        self.inputs = [[10, 70, False], [34, 70, False]]
        self.output = [[21, 0, False]]

    def update_state(self):
        self.output[0][2] = not any(input_state[2]
                                    for input_state in self.inputs)


class XorGate(Gate):
    def __init__(self, image_path, width, height):
        super().__init__(image_path, width, height)
        self.inputs = [[10, 70, False], [34, 70, False]]
        self.output = [[21, 0, False]]

    def update_state(self):
        true_inputs = sum(input_state[2] for input_state in self.inputs)
        self.output[0][2] = true_inputs % 2 == 1


class Light(DraggableObject):
    def __init__(self, image_path, width, height):
        super().__init__(image_path, width, height)
        self.inputs = [[21, 70, False]]
        self.state = False

        self.on_image_path = 'game/assets/LIGHT_ON.png'
        self.off_image_path = 'game/assets/LIGHT_OFF.png'
        self.update_image()

    def draw_slots(self, surface, color=(255, 0, 0)):
        slot_radius = 5
        # Draw input slots
        for input_slot in self.inputs:
            input_pos = (self.rect.x + input_slot[0],
                         self.rect.y + input_slot[1])
            pygame.draw.circle(surface, color, input_pos, slot_radius)

    def update_state(self):
        self.state = self.inputs[0][2]
        self.update_image()

    def update_image(self):
        self.image_path = self.on_image_path if self.state else self.off_image_path
        self.original_image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(
            self.original_image, (self.rect.width, self.rect.height))


class Color(Enum):
    WHITE = 'game/assets/LED_WHITE.png'
    BLACK = 'game/assets/LED_BLACK.png'
    RED = 'game/assets/LED_RED.png'
    BLUE = 'game/assets/LED_BLUE.png'
    YELLOW = 'game/assets/LED_YELLOW.png'
    GREEN = 'game/assets/LED_GREEN.png'
    PURPLE = 'game/assets/LED_PURPLE.png'
    ORANGE = 'game/assets/LED_ORANGE.png'


class Led(DraggableObject):
    def __init__(self, image_path, width, height):
        super().__init__(image_path, width, height)
        # yellow - blue - red
        self.inputs = [[7, 64, False], [23, 64, False], [40, 64, False]]

        self.state = Color.BLACK.value
        self.update_image()

    def draw_slots(self, surface, color=(255, 0, 0)):
        slot_radius = 5
        # Draw input slots
        for input_slot in self.inputs:
            input_pos = (self.rect.x + input_slot[0],
                         self.rect.y + input_slot[1])
            pygame.draw.circle(surface, color, input_pos, slot_radius)

    def update_state(self):
        if self.inputs[0][2] and self.inputs[1][2] and self.inputs[2][2]:
            self.state = Color.WHITE.value
        elif self.inputs[0][2] and self.inputs[1][2]:
            self.state = Color.GREEN.value
        elif self.inputs[2][2] and self.inputs[1][2]:
            self.state = Color.PURPLE.value
        elif self.inputs[2][2] and self.inputs[0][2]:
            self.state = Color.ORANGE.value
        elif self.inputs[2][2]:
            self.state = Color.RED.value
        elif self.inputs[1][2]:
            self.state = Color.BLUE.value
        elif self.inputs[0][2]:
            self.state = Color.YELLOW.value
        else:
            self.state = Color.BLACK.value
        self.update_image()

    def update_image(self):
        self.image_path = self.state
        self.original_image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(
            self.original_image, (self.rect.width, self.rect.height))


class Numbers(Enum):
    N_0 = 'game/assets/Counter/0.png'
    N_1 = 'game/assets/Counter/1.png'
    N_2 = 'game/assets/Counter/2.png'
    N_3 = 'game/assets/Counter/3.png'
    N_4 = 'game/assets/Counter/4.png'
    N_5 = 'game/assets/Counter/5.png'
    N_6 = 'game/assets/Counter/6.png'
    N_7 = 'game/assets/Counter/7.png'
    N_8 = 'game/assets/Counter/8.png'
    N_9 = 'game/assets/Counter/9.png'
    N_10 = 'game/assets/Counter/10.png'
    N_11 = 'game/assets/Counter/11.png'
    N_12 = 'game/assets/Counter/12.png'
    N_13 = 'game/assets/Counter/13.png'
    N_14 = 'game/assets/Counter/14.png'
    N_15 = 'game/assets/Counter/15.png'
    N_16 = 'game/assets/Counter/16.png'
    N_17 = 'game/assets/Counter/17.png'
    N_18 = 'game/assets/Counter/18.png'
    N_19 = 'game/assets/Counter/19.png'
    N_20 = 'game/assets/Counter/20.png'
    N_21 = 'game/assets/Counter/21.png'
    N_22 = 'game/assets/Counter/22.png'
    N_23 = 'game/assets/Counter/23.png'
    N_24 = 'game/assets/Counter/24.png'
    N_25 = 'game/assets/Counter/25.png'
    N_26 = 'game/assets/Counter/26.png'
    N_27 = 'game/assets/Counter/27.png'
    N_28 = 'game/assets/Counter/28.png'
    N_29 = 'game/assets/Counter/29.png'
    N_30 = 'game/assets/Counter/30.png'
    N_31 = 'game/assets/Counter/31.png'


class Counter(DraggableObject):
    def __init__(self, image_path, width, height):
        super().__init__(image_path, width, height)
        self.inputs = [
            [14, 96, False],  # Represents 1
            [32, 96, False],  # Represents 2
            [50, 96, False],  # Represents 4
            [68, 96, False],  # Represents 8
            [86, 96, False]]  # Represents 16
        self.state = Numbers.N_0.value

    def draw_slots(self, surface, color=(255, 0, 0)):
        slot_radius = 5
        # Draw input slots
        for input_slot in self.inputs:
            input_pos = (self.rect.x + input_slot[0],
                         self.rect.y + input_slot[1])
            pygame.draw.circle(surface, color, input_pos, slot_radius)

    def update_state(self):
        binary_state = [input[2]
                        for input in self.inputs]  # Extract the boolean values
        decimal_value = binary_state[4] * 16 + binary_state[3] * 8 + \
            binary_state[2] * 4 + binary_state[1] * 2 + binary_state[0] * 1

        self.state = getattr(Numbers, f'N_{decimal_value}').value

        self.update_image()

        self.update_image()

    def update_image(self):
        self.image_path = self.state
        self.original_image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(
            self.original_image, (self.rect.width, self.rect.height))


class Switch(DraggableObject):
    def __init__(self, image_path, width, height):
        super().__init__(image_path, width, height)
        self.output = [[21, 0, False]]

        self.on_image_path = 'game/assets/SWITCH_ON.png'
        self.off_image_path = 'game/assets/SWITCH_OFF.png'
        self.update_image()

    def draw_slots(self, surface, color=(255, 0, 0)):
        slot_radius = 5
        # Draw output slot
        output_pos = (self.rect.x + self.output[0][0],
                      self.rect.y + self.output[0][1])
        pygame.draw.circle(surface, color, output_pos, slot_radius)

    def update_image(self):
        self.image_path = self.on_image_path if self.output[0][2] else self.off_image_path
        self.original_image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(
            self.original_image, (self.rect.width, self.rect.height))

    def toggle_switch(self):
        self.output[0][2] = not self.output[0][2]
        self.update_image()
