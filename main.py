import os
import sys

import pygame
import requests

coords = input("Введите координаты в формате xxx yyy: ").split()
spn = input("Введите значение параметра spn(масштаб): ")
map_params = {
    "ll": ",".join([coords[1], coords[0]]),
    "spn": ",".join([spn, spn]),
    "l": "map"
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

if not response:
    print("Ошибка выполнения запроса:")
    print(response.url)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if 0 < float(spn) - 0.5 * float(spn) < 90:
                    spn = str(float(spn) - 0.5 * float(spn))
            elif event.key == pygame.K_PAGEDOWN:
                if 0 < float(spn) + 0.5 * float(spn) < 90:
                    spn = str(float(spn) + 0.5 * float(spn))

    map_params = {
        "ll": ",".join([coords[1], coords[0]]),
        "spn": ",".join([spn, spn]),
        "l": "map"
    }

    print(spn)
    response = requests.get(map_api_server, params=map_params)
    if not response:
        print("Ошибка выполнения запроса:")
        print(response.url)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()

    os.remove(map_file)

pygame.quit()
