import pygame
from pyvidplayer import Video



# class GameIntro:
#     def __init__(self):
#         self.video = Video("./video/charIntro.mp4")
#         self.video.set_size((460,330))
#         self.stay = StayScreen()
        
#     def run(self,screen):
#         while True:
#             self.video.draw(screen, (0,0))
#             pygame.display.update()
            
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT :
#                     self.playing = self.running = False
#                     pygame.quit()
#                 # if self.video.get_pos() > 24.5:
#                 #     self.stay.run(screen)

                
                
class StayScreen:
    def __init__(self):
        self.video = Video("./video/stayintro.mp4")
        self.video.set_size((460,330))
        
    def run(self,screen):
        while True:
            self.video.draw(screen, (0,0))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    self.playing = self.running = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    self.video.close()
                    return
            if self.video.get_pos() > 4.7:
                self.video.restart()
            