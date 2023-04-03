import pygame
import config as cg
from pause import Buttons

class Buttons(pygame.sprite.Sprite):
    def __init__(self, width, height, xoff, yoff):
        super().__init__()
        self.buttons_only_surf = pygame.transform.scale(pygame.image.load('graphics/endbuttonsonly.png').convert_alpha(), (width, height))
        self.buttons_mask = pygame.mask.from_surface(self.buttons_only_surf)
        self.xoff = xoff
        self.yoff = yoff

    def check_collision(self, mask):
        if self.buttons_mask.overlap(mask, (pygame.mouse.get_pos()[0] - self.xoff, pygame.mouse.get_pos()[1] - self.yoff)):
            # print(True)
            return True        
        # print(False)
        return False


def calculateScore(list):
    total = 0
    pointsPer = 100.0 / len(list)
    for x in list:
        if x:
            total += pointsPer
    return int(total)

class EndScreen:
    def __init__(self, cursor_width, cursor_height):        

        # adjustable options
        SIZE_MULTIPLIER = 7
        self.WIDTH = 50 * SIZE_MULTIPLIER
        self.HEIGHT = 33 * SIZE_MULTIPLIER
        self.pause_text_top_offset = 38
        self.smalltext_spacing_from_mid = 40
        self.smalltext_bottom_offset = 39
        self.scoretime_center_x = (cg.SCREEN_WIDTH/4 ) - 80

        # critical variables        
        self.show_end = False
        self.end_surf = pygame.transform.scale(pygame.image.load('graphics/endscreen.png').convert_alpha(), (self.WIDTH, self.HEIGHT))
        self.end_surf_rect = self.end_surf.get_rect(center = (cg.SCREEN_WIDTH/2, cg.SCREEN_HEIGHT/2))
        # self.retry_highlight_surf = pygame.transform.scale(pygame.image.load('graphics/retryhighlight.png').convert_alpha(), (self.WIDTH, self.HEIGHT))
        # self.retry_highlight_surf_rect = self.retry_highlight_surf.get_rect(center = (cg.SCREEN_WIDTH/2, cg.SCREEN_HEIGHT/2))
        self.resume_highlight_surf = pygame.transform.scale(pygame.image.load('graphics/resumehighlight.png').convert_alpha(), (self.WIDTH, self.HEIGHT))
        self.resume_highlight_surf_rect = self.resume_highlight_surf.get_rect(center = (cg.SCREEN_WIDTH/2, cg.SCREEN_HEIGHT/2))
        self.font = pygame.font.Font('graphics/5x5.ttf', 70)
        self.smfont = pygame.font.Font('graphics/5x5.ttf', 20)

        self.retry_bool = False

        self.buttons = Buttons(self.WIDTH, self.HEIGHT, self.end_surf_rect.left + (cursor_width/2.0), self.end_surf_rect.top + (cursor_height/2.0))

        self.display_surface = pygame.display.get_surface()
        self.button_pressed = False        
        self.mouse1_clicked = False
        self.highlight = False

    def run(self, mask, taskCompletions, mins, sec):            
        if self.show_end == True:    
            score = calculateScore(taskCompletions)
            self.display(self.display_surface, score, mins, sec)        
            self.cursor_collision(mask)            
        else:            
            return   

    def display(self, screen, score, mins, sec):
        bg_surf = pygame.Surface((cg.SCREEN_WIDTH, cg.SCREEN_HEIGHT))
        bg_surf.set_alpha(150)
        bg_surf.fill((0, 0, 0))

        self.end_surf = pygame.transform.scale(pygame.image.load('graphics/endscreen.png').convert_alpha(), (self.WIDTH, self.HEIGHT))

        paused_text = self.font.render('End', False, 'White')
        paused_text_rect = paused_text.get_rect(center = (self.end_surf.get_width() / 2 + 3, self.pause_text_top_offset))
        self.end_surf.blit(paused_text, paused_text_rect)

        resume_text = self.smfont.render('Retry', False, 'Black')
        resume_text_rect = resume_text.get_rect(midleft = (self.end_surf.get_width() / 2 + self.smalltext_spacing_from_mid, self.end_surf.get_height() - self.smalltext_bottom_offset))
        self.end_surf.blit(resume_text, resume_text_rect)

        # draw points and time
        # score procesing
        score_str = str(score)
        # while len(score_str) < 3:              add 0s to end of score
        #     score_str = '0' + score_str
        score_text = self.smfont.render('Score: ' + score_str, False, 'Black')
        score_text_rect = score_text.get_rect(midleft = ( self.scoretime_center_x, (cg.SCREEN_HEIGHT/2 - 60) ))
        self.end_surf.blit(score_text, score_text_rect)

        reaction_file_name = "indifferent"
        match round(score / 20.0):
            case 5:
                reaction_file_name = "overjoyed"
            case 4:
                reaction_file_name = "happy"
            case 3:
                reaction_file_name = "indifferent"
            case 2:
                reaction_file_name = "sad"
            case 1:
                reaction_file_name = "angry"
            case 0:
                reaction_file_name = "angry"

        # time processing
        mins_str = ""
        sec_str = ""
        if mins == 0:
            mins_str = '00'
        elif mins < 10:
            mins_str = '0' + str(mins)
        else:
            mins_str = str(mins)
        if sec == 0:
            sec_str = '00'
        elif sec < 10:
            sec_str = '0' + str(sec)
        else:
            sec_str = str(sec)
        time_text = self.smfont.render('Time: ' + mins_str + ":" + sec_str, False, 'Black')
        time_text_rect = time_text.get_rect(midleft = ( self.scoretime_center_x, (cg.SCREEN_HEIGHT/2 - 40) ))
        self.end_surf.blit(time_text, time_text_rect)

        # mom reaction drawing
        mom = pygame.image.load('graphics/character/mom/mom.png').convert_alpha()
        mom_rect = mom.get_rect(center = (cg.SCREEN_WIDTH/4 - 30, (cg.SCREEN_HEIGHT/2 + 22)))
        self.end_surf.blit(mom, mom_rect)

        reaction = pygame.image.load('graphics/character/reactions/' + reaction_file_name + '.png').convert_alpha()
        reaction_rect = reaction.get_rect(bottomleft = (mom_rect.right - 8, mom_rect.top + 20))
        self.end_surf.blit(reaction, reaction_rect)

        screen.blit(bg_surf, (0,0))
        if self.highlight:
            self.end_surf.blit(self.resume_highlight_surf, (0,0))        
        screen.blit(self.end_surf, self.end_surf_rect)


    def cursor_collision(self, mask):
        if self.buttons.check_collision(mask):
            self.highlight = True

            if pygame.mouse.get_pressed()[0] and not self.mouse1_clicked:            
                self.mouse1_clicked = True                
                self.retry_bool = True                
        else:
            self.highlight = False
        if not pygame.mouse.get_pressed()[0]:
            self.mouse1_clicked = False