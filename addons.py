import requests


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


class InputBox:

    def __init__(self, pygame, x, y, w, h, text=''):
        self.pg = pygame
        self.rect = pygame.Rect(x, y, w, h)
        self.COLOR_INACTIVE = pygame.Color('lightskyblue3')
        self.COLOR_ACTIVE = pygame.Color('dodgerblue2')
        self.FONT = pygame.font.Font(None, 32)
        self.color = self.COLOR_INACTIVE
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == self.pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        if event.type == self.pg.KEYDOWN:
            if self.active:
                if event.key == self.pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == self.pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        self.pg.draw.rect(screen, self.color, self.rect, 2)

    def return_text(self):
        t = self.text
        self.text = ""
        return t


def get_full_address(text):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={text}&format=json"

    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_index = \
        toponym["boundedBy"]["Envelope"]
        return toponym_index

    else:
        print("Ошибка выполнения запроса:")
        print(geocoder_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return 0
