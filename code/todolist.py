import pygame
import config as cg
from enum import Enum

class TaskIndex(Enum):
    TRASH = 0
    LAUNDRY = 1
    TOYS = 2
    DISHES = 3
    CLEAN_FLOORS = 4
    CLEAR_COUNTER = 5
    TOILET = 6

class todoList:

    def __init__(self):

        # adjustable options
        self.WIDTH = 112
        self.HEIGHT = 112
        self.box_top_offset = 8
        self.left_offset = 5
        self.top_offset = 5
        self.spacing = 14
        self.font_size = 10

        # critical variables
        self.allTasksCompleted = False                      ### turns true when all tasks are completed
        self.taskStrings = ["TODO List:",
                            f"TAKE OUT TRASH ()",
                            "LAUNDRY",
                            "CLEAN ROOM",
                            "DISHES",
                            "SWEEP FLOORS",
                            "CLEAR COUNTER",
                            "CLEAN TOILET"]
        self.taskCompletions = [False, False, False, False, False, False, False]
        
        self.todo_surf = pygame.transform.scale(pygame.image.load('graphics/todolist.png').convert_alpha(), (self.WIDTH, self.HEIGHT))
        # self.todo_surf = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)

        # mundane variables
        self.font = pygame.font.Font('graphics/5x5.ttf', self.font_size)

    def complete(self, taskToMark:str):
        match taskToMark.lower():
            case "trash":
                self.taskCompletions[TaskIndex.TRASH.value] = True
            case "laundry":
                self.taskCompletions[TaskIndex.LAUNDRY.value] = True
            case "toys":
                self.taskCompletions[TaskIndex.TOYS.value] = True
            case "dishes":
                self.taskCompletions[TaskIndex.DISHES.value] = True

    def updateCompleted(self, updatedArr):
        self.taskCompletions = updatedArr

    def display(self, display_surf):
        # draw to custom surface
        # pygame.draw.rect(self.todo_surf, (243, 231, 121), (0, 0, self.WIDTH, self.HEIGHT))

        for index, string in enumerate(self.taskStrings):            
            # render text
            string_surf = self.font.render(string, True, 'Black')

            # render strikethrough
            if index != 0 and self.taskCompletions[index-1] == 1:
                pygame.draw.line(string_surf, 'Black', (string_surf.get_rect().left, string_surf.get_rect().centery+1), (string_surf.get_rect().right, string_surf.get_rect().centery+1))
            string_surf_rect = string_surf.get_rect(midleft = (self.left_offset, self.top_offset + (index * self.spacing)))
            self.todo_surf.blit(string_surf, string_surf_rect)

        # draw to screen
        todo_surf_rect = self.todo_surf.get_rect(topright = (cg.SCREEN_WIDTH - 31, self.box_top_offset))
        display_surf.blit(self.todo_surf, todo_surf_rect)

    def checkCompletion(self):
        for x in self.taskCompletions:
            if not x:
                self.allTasksCompleted = False
                return
        self.allTasksCompleted = True

    def run(self, displayScreen, showToDoList, updatedArr):
        self.updateCompleted(updatedArr)
        self.checkCompletion()
        if showToDoList:
            self.display(displayScreen)
        else:
            return        