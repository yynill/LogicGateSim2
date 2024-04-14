import pygame
from .settings import *
from .draggableObject import *
from .button import *
from .selectionBox import SelectionBox
from .cable import Cable
import numpy as np


class Loop:
    def __init__(self) -> None:
        # Initialize the main game window
        self.display_surface = pygame.display.get_surface()

        # Groups for managing sprites and draggable objects
        self.all_sprites = pygame.sprite.Group()
        self.draggable_objects = []

        # Variables for handling object dragging and selection
        self.currently_dragged_object = None
        self.selection_box = None
        self.selected_objects = []
        self.mouse_start_pos = None

        # Cable creation mode and storage
        self.cable_mode = False
        self.cables = []
        self.current_cable = None

        # Setup the interface buttons
        self.buttons = [
            # Logic gates
            Button(x=10, y=10, width=80, height=40, text='AND'),
            Button(x=100, y=10, width=80, height=40, text='OR'),
            Button(x=190, y=10, width=80, height=40, text='NOT'),
            Button(x=280, y=10, width=80, height=40, text='NAND'),
            Button(x=370, y=10, width=80, height=40, text='NOR'),
            Button(x=460, y=10, width=80, height=40, text='XOR'),
            # Utility items
            Button(x=600, y=10, width=80, height=40, text='LIGHT'),
            Button(x=690, y=10, width=80, height=40, text='LED'),
            Button(x=780, y=10, width=80, height=40, text='SWITCH'),
            Button(x=870, y=10, width=80, height=40, text='COUNTER'),
            Button(x=960, y=10, width=80, height=40, text='BOX'),
            # Cable button
            CableButton(x=1100, y=10, width=80, height=40, text='',
                        image_path='game/assets/CABLE.png'),
        ]
        # Add all buttons to the sprite group for easy rendering and updating
        for button in self.buttons:
            self.all_sprites.add(button)

    def run(self, dt, events):  # Updated every frame
        # Handle any input events
        self.handle_events(events)

        # Clear the screen and redraw all sprites
        self.display_surface.fill(BACKGROUND_COLOR)
        self.all_sprites.draw(self.display_surface)

        # If a selection box is active, draw it
        if self.selection_box and self.selection_box.visible:
            self.selection_box.draw(self.display_surface)

        for obj in self.draggable_objects:
            if isinstance(obj, (Gate, Light, Led, Counter)):
                obj.update_state()

            obj.draw_selected_outline(self.display_surface)

        # If in cable mode, draw connection points on applicable objects
        if self.cable_mode:
            for obj in self.all_sprites:
                if isinstance(obj, (Gate, Switch, Light, Led, Counter)):
                    obj.draw_slots(self.display_surface)

        # Draw all cables and the currently being drawn cable, if any
        for cable in self.cables:
            cable.update()
            cable.update_state()
            cable.draw(self.display_surface)
        if self.current_cable:
            self.current_cable.draw(self.display_surface)

    def create_draggable_object(self, object_type):
        if object_type == 'AND':
            new_object = AndGate(
                image_path='game/assets/AndGate.png', width=42, height=70)
        elif object_type == 'OR':
            new_object = OrGate(
                image_path='game/assets/OrGate.png', width=42, height=70)
        elif object_type == 'NOT':
            new_object = NotGate(
                image_path='game/assets/NotGate.png', width=42, height=70)
        elif object_type == 'NAND':
            new_object = NandGate(
                image_path='game/assets/NandGate.png', width=42, height=70)
        elif object_type == 'NOR':
            new_object = NorGate(
                image_path='game/assets/NorGate.png', width=42, height=70)
        elif object_type == 'XOR':
            new_object = XorGate(
                image_path='game/assets/XorGate.png', width=42, height=70)
        elif object_type == 'LIGHT':
            new_object = Light(
                image_path='game/assets/LIGHT_OFF.png', width=42, height=70)
        elif object_type == 'LED':
            new_object = Led(
                image_path='game/assets/LED_BLACK.png', width=46, height=64)
        elif object_type == 'SWITCH':
            new_object = Switch(
                image_path='game/assets/SWITCH_OFF.png', width=42, height=70)
        elif object_type == 'COUNTER':
            new_object = Counter(
                image_path='game/assets/Counter/0.png', width=98, height=96)
        else:
            new_object = DraggableObject(
                image_path='game/assets/DeafaultBOX.png', width=50, height=50)

        new_object.rect.x = 10
        new_object.rect.y = 60
        self.draggable_objects.append(new_object)
        self.all_sprites.add(new_object)

    def select_multiple(self, event):
        for all_obj in self.draggable_objects:
            all_obj.selected = False
        for all_cable in self.cables:
            all_cable.selected = False

        self.selected_objects = [
            obj for obj in self.draggable_objects if self.selection_box.rect.colliderect(obj.rect)]
        for selected_obj in self.selected_objects:
            selected_obj.selected = True

        for cable in self.cables:
            if cable.intersects_rect(self.selection_box.rect):
                cable.selected = True

    def button_click(self, event):
        for button in self.buttons:
            if button.is_clicked(event):
                # self.selected_objects.clear()
                if isinstance(button, CableButton):
                    button.toggle(event)
                    self.cable_mode = button.mode
                elif button.getName() != '':
                    self.create_draggable_object(button.getName())
                break

    def cable_click(self, event):
        for cable in self.cables:
            if cable.is_left_clicked(event):
                cable.selected = True
                return True
        return False

    def drag(self, event):
        interaction_occurred = False

        # Middle mouse button drag for all objects
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            self.mouse_start_pos = event.pos
            interaction_occurred = True

            # Middle mouse button held
        elif event.type == pygame.MOUSEMOTION and self.mouse_start_pos and event.buttons[1]:
            dx = event.pos[0] - self.mouse_start_pos[0]
            dy = event.pos[1] - self.mouse_start_pos[1]
            for obj in self.draggable_objects:
                obj.rect.x += dx
                obj.rect.y += dy
            self.mouse_start_pos = event.pos
            interaction_occurred = True

            # Middle mouse button lifted
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 2:
            self.mouse_start_pos = None
            interaction_occurred = True

            # drag selected obj
        if not interaction_occurred:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if any(obj.is_left_clicked(event) for obj in self.selected_objects):
                    self.mouse_start_pos = event.pos
                    interaction_occurred = True

            elif event.type == pygame.MOUSEMOTION and self.mouse_start_pos:
                dx = event.pos[0] - self.mouse_start_pos[0]
                dy = event.pos[1] - self.mouse_start_pos[1]
                for obj in self.selected_objects:
                    obj.rect.x += dx
                    obj.rect.y += dy
                self.mouse_start_pos = event.pos
                interaction_occurred = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.mouse_start_pos:
                    self.mouse_start_pos = None
                    interaction_occurred = True

            # drag single obj
        if not interaction_occurred:
            for obj in self.draggable_objects:
                if obj.dragging or (event.type == pygame.MOUSEBUTTONDOWN and obj.rect.collidepoint(event.pos)):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.currently_dragged_object = obj
                    if self.currently_dragged_object == obj:
                        obj.handle_event(event)
                        interaction_occurred = True

            # select_multiple objs
        if not interaction_occurred and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.selection_box = SelectionBox(event.pos[0], event.pos[1])
            self.selection_box.visible = True

        if event.type == pygame.MOUSEMOTION and self.selection_box and self.selection_box.visible:
            current_x, current_y = event.pos
            self.selection_box.update(current_x, current_y)

        if event.type == pygame.MOUSEBUTTONUP and self.selection_box and self.selection_box.visible:
            self.select_multiple(event)
            self.selection_box.visible = False

    def delete_selected_objects(self):
        # Delete selected cables
        for cable in self.cables[:]:  # Iterate over a copy of the cables list
            if cable.selected:
                self.cables.remove(cable)

        # Delete selected draggable objects
        for sprite in list(self.all_sprites):
            if hasattr(sprite, 'selected') and sprite.selected:
                self.draggable_objects.remove(sprite)
                self.all_sprites.remove(sprite)

    def duplicate_selected_objects(self):
        offset_x = 20
        offset_y = 20
        duplicates = []

        for obj in self.selected_objects:
            # Use the type of the current object to create a new instance
            duplicate = type(obj)(
                image_path=obj.image_path, width=obj.rect.width, height=obj.rect.height)

            if hasattr(obj, 'inputs'):
                duplicate.inputs = obj.inputs.copy()
            if hasattr(obj, 'output'):
                duplicate.output = obj.output.copy()

            duplicate.rect.x = obj.rect.x + offset_x
            duplicate.rect.y = obj.rect.y + offset_y
            duplicates.append(duplicate)

        # Clear selection of the current objects
        for obj in self.selected_objects:
            obj.selected = False

        self.selected_objects.clear()

        # Add duplicates to their respective lists and select them
        for duplicate in duplicates:
            self.draggable_objects.append(duplicate)
            self.all_sprites.add(duplicate)
            self.selected_objects.append(duplicate)  # Select the new duplicate
            duplicate.selected = True

    def find_closest_output_snap_point(self, cable_start_pos, snap_threshold=50):
        closest_point = None
        min_distance = float('inf')
        output_obj = None

        for obj in self.draggable_objects:
            if hasattr(obj, 'output') and obj.output:
                slot_pos = (
                    obj.rect.x + obj.output[0][0], obj.rect.y + obj.output[0][1])
                distance = calculate_distance(cable_start_pos, slot_pos)
                if distance < min_distance:
                    min_distance = distance
                    closest_point = slot_pos
                    output_obj = obj

        if min_distance <= snap_threshold:
            return closest_point, output_obj
        else:
            return cable_start_pos, None

    def find_closest_input_snap_point(self, cable_end_pos, snap_threshold=50):
        closest_point = None
        min_distance = float('inf')
        input_obj = None
        input_index = None  # Index of the input slot

        for obj in self.draggable_objects:
            if hasattr(obj, 'inputs') and obj.inputs:
                for idx, input_slot in enumerate(obj.inputs):
                    slot_pos = (
                        obj.rect.x + input_slot[0], obj.rect.y + input_slot[1])
                    distance = calculate_distance(cable_end_pos, slot_pos)
                    if distance < min_distance:
                        min_distance = distance
                        closest_point = slot_pos
                        input_obj = obj
                        input_index = idx

        if min_distance <= snap_threshold:
            return closest_point, input_obj, input_index
        else:
            return cable_end_pos, None, None

    def handle_cable_creation(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.mouse_start_pos = event.pos
            start_pos, output = self.find_closest_output_snap_point(
                self.mouse_start_pos)
            self.current_cable = Cable(
                start_pos,
                end_pos=self.mouse_start_pos,
                output_obj=output,
                input_obj=None
            )

        elif event.type == pygame.MOUSEMOTION and self.mouse_start_pos:
            if self.current_cable:
                self.current_cable.end_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.mouse_start_pos = None
            if self.current_cable:
                end_pos, input, input_index = self.find_closest_input_snap_point(
                    self.current_cable.end_pos, snap_threshold=50
                )
            if input:
                self.current_cable.input_obj = input
                self.current_cable.input_index = input_index

                # Check if both the start and end of the cable have successfully snapped
                if self.current_cable.input_obj is not None and self.current_cable.output_obj is not None:
                    self.current_cable.end_pos = end_pos
                    self.cables.append(self.current_cable)
                else:
                    pass

                # Regardless of whether the cable was added or discarded, clear the current cable
                self.current_cable = None

    def switch_flip(self, event):
        for obj in self.draggable_objects:
            if isinstance(obj, Switch):
                if obj.is_right_clicked(event):
                    obj.toggle_switch()

    def handle_events(self, events):
        for event in events:
            # click btn
            self.button_click(event)

            if not self.cable_mode:
                if not self.cable_click(event):
                    self.drag(event)
                    self.switch_flip(event)

                if self.selected_objects:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_d:
                            self.duplicate_selected_objects()

                        if event.key == pygame.K_BACKSPACE:
                            self.delete_selected_objects()
            else:
                self.handle_cable_creation(event)


def calculate_distance(point1, point2):
    return np.linalg.norm(np.array(point1) - np.array(point2))
