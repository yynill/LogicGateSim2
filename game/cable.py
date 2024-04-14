import pygame
from .settings import *
import numpy as np


# then update state of cable, get state from input give state to output

class Cable:
    def __init__(self, start_pos, end_pos, output_obj=None, input_obj=None, input_index=None):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.active = False
        self.selected = False
        # start = output_obj
        # end = input_obj
        self.output_obj = output_obj
        self.input_obj = input_obj
        self.input_index = input_index  # Store which input it's connected to

    def update_state(self):
        x, y, state = self.output_obj.output[0]
        self.active = state
        self.input_obj.inputs[self.input_index][2] = state

    def draw(self, surface):
        if self.selected:
            pygame.draw.line(surface, WIRE_COLOR_SELECTED,
                             self.start_pos, self.end_pos, 3)
        else:
            if self.active:
                pygame.draw.line(surface, WIRE_COLOR_ACTIVE,
                                 self.start_pos, self.end_pos, 3)
            else:
                pygame.draw.line(surface, WIRE_COLOR,
                                 self.start_pos, self.end_pos, 3)

    def update(self):
        # Update the start position based on the output_obj's position
        if self.output_obj:
            self.start_pos = (
                self.output_obj.rect.x + self.output_obj.output[0][0],
                self.output_obj.rect.y + self.output_obj.output[0][1]
            )

        # Update the end position based on the input_obj's position and input_index
        if self.input_obj and self.input_index is not None:
            input_slot = self.input_obj.inputs[self.input_index]
            self.end_pos = (
                self.input_obj.rect.x + input_slot[0],
                self.input_obj.rect.y + input_slot[1]
            )

    def is_left_clicked(self, event, threshold=5):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            distance = point_line_distance(
                event.pos, self.start_pos, self.end_pos)
            return distance <= threshold
        return False

    def intersects_rect(self, rect):
        # check if either end of the cable is within (selection box)
        start_inside = rect.collidepoint(self.start_pos)
        end_inside = rect.collidepoint(self.end_pos)

        return start_inside or end_inside


def point_line_distance(point, line_start, line_end):
    # Convert points to numpy arrays for vector operations
    point = np.array(point)
    line_start = np.array(line_start)
    line_end = np.array(line_end)

    line_vec = line_end - line_start
    point_vec = point - line_start

    # Calculate the projection of point_vec onto line_vec
    line_len = np.linalg.norm(line_vec)
    line_unitvec = line_vec / line_len
    proj_length = np.dot(point_vec, line_unitvec)

    if proj_length < 0:
        # Closest point is the line start
        closest_point = line_start
    elif proj_length > line_len:
        # Closest point is the line end
        closest_point = line_end
    else:
        # Closest point is somewhere in the middle
        closest_point = line_start + line_unitvec * proj_length

    distance = np.linalg.norm(point - closest_point)

    return distance
