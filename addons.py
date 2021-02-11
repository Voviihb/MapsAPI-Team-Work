def print_text_from_center(message, x, y, screen, pygame, font_size=30):
    font = pygame.font.Font(None, font_size)
    string_rendered = font.render(message, 1, pygame.Color('black'))
    TextW = string_rendered.get_width()
    TextH = string_rendered.get_height()
    TextRect = string_rendered.get_rect()
    TextRect.x = x - TextW // 2
    TextRect.top = y - TextH // 2
    screen.blit(string_rendered, TextRect)


class Button:
    def __init__(self, width, height, screen, pygame=None, inactive_clr=(13, 162, 58), active_clr=(23, 204, 58)):
        self.screen = screen
        self.pygame = pygame
        self.pygame.init()
        self.width = width
        self.height = height
        self.current_clr = list(inactive_clr)
        self.inactive_clr = inactive_clr
        self.active_clr = active_clr
        self.diff_clr = [(i - k) // 8 for i, k in zip(active_clr, inactive_clr)]
        self.last_ret = False

    def SetSize(self, width, height):
        self.width = width
        self.height = height

    def draw(self, pos: tuple, message="", image=None, action=None, font_size=50, cmd=None, args=None):
        mouse = self.pygame.mouse.get_pos()
        click = self.pygame.mouse.get_pressed()

        x, y = pos[0], pos[1]

        rh = self.height // 3
        MiddleRectSize = (self.width, self.height - rh * 2)
        topleft = (x + rh, y + rh)
        RectsSize = (self.width - rh * 2, self.height - rh * 2)
        self.pygame.draw.circle(self.screen, self.current_clr, topleft, rh, draw_top_left=True)
        self.pygame.draw.circle(self.screen, self.current_clr, (x + rh, y + self.height - rh), rh,
                                draw_bottom_left=True)
        self.pygame.draw.circle(self.screen, self.current_clr, (x + self.width - rh, y + rh), rh, draw_top_right=True)
        self.pygame.draw.circle(self.screen, self.current_clr, (x + self.width - rh, y + self.height - rh), rh,
                                draw_bottom_right=True)

        self.pygame.draw.rect(self.screen, self.current_clr, (x + rh, y) + RectsSize)  # Top rectangle
        self.pygame.draw.rect(self.screen, self.current_clr, (x, y + rh) + MiddleRectSize)  # Middle rectangle
        self.pygame.draw.rect(self.screen, self.current_clr, (x + rh, y + self.height - rh) + RectsSize)  # Bottom rect

        if message:
            print_text_from_center(message, x + self.width // 2, y + self.height // 2, self.screen, self.pygame,
                                   font_size=font_size)
        elif image:
            ImageW = self.width - self.width // 2
            ImageH = self.height - self.height // 2
            rect = image.get_rect()
            CurrentW = rect.height
            CurrentH = rect.width
            if CurrentW != ImageW or CurrentH != ImageH:
                image = self.pygame.transform.smoothscale(image, (ImageW, ImageH))
            Center = x + self.width // 2, y + self.height // 2
            DrawX, DrawY = Center[0] - ImageW // 2, Center[1] - ImageH // 2
            self.screen.blit(image, (DrawX, DrawY))

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            for i in range(len(self.current_clr)):
                if self.diff_clr[i] >= 0:
                    self.current_clr[i] = min(self.active_clr[i], self.current_clr[i] + self.diff_clr[i])
                else:
                    self.current_clr[i] = max(self.active_clr[i], self.current_clr[i] + self.diff_clr[i])
            if click[0] == 1:
                return True
            else:
                self.last_ret = False
        else:
            for i in range(len(self.current_clr)):
                if self.diff_clr[i] >= 0:
                    self.current_clr[i] = max(self.inactive_clr[i], self.current_clr[i] - self.diff_clr[i])
                else:
                    self.current_clr[i] = min(self.inactive_clr[i], self.current_clr[i] - self.diff_clr[i])