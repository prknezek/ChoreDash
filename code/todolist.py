import pygame
import config as cg

class todoList:

    def __init__(self):

        # adjustable options
        self.WIDTH = 100
        self.HEIGHT = 100
        self.box_top_offset = 8
        self.left_offset = 5
        self.top_offset = 5
        self.spacing = 15
        self.font_size = 10

        # critical variables
        self.taskStrings = ["TODO List:",
                            "TAKE OUT TRASH",
                            "LAUNDRY",
                            "CLEAN ROOM",
                            "DISHES"]
        self.taskCompletions = [1,0,1,0]
        self.todo_surf = pygame.transform.scale(pygame.image.load('graphics/todolist.png').convert_alpha(), (self.WIDTH, self.HEIGHT))
        # self.todo_surf = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)

        # mundane variables
        self.font = pygame.font.Font('graphics/5x5.ttf', self.font_size)


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
        

    def run(self, displayScreen):
        condition = True
        if condition:
            self.display(displayScreen)
        else:
            return