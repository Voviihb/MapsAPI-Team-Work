import os
import sys

import pygame
import requests

#coords = input("Введите координаты в формате xxx yyy: ").split()
coords = ["-28.069396", "34.457771"]
spn = "25"
#spn = input("Введите значение параметра spn(масштаб): ")
map_params = {
        "ll": ",".join([coords[1], coords[0]]),
        "spn": ",".join([spn, spn]),
        "l": "map"
}


map_api_server = "http://static-maps.yandex.ru/1.x/"
pygame.init()
screen = pygame.display.set_mode((600, 450))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if 0 < abs(float(coords[1]) - 2 * float(spn)) < 180:
                    coords[1] = str(float(coords[1]) - 2 * float(spn))
            elif event.key == pygame.K_RIGHT:
                if 0 < abs(float(coords[1]) + 2 * float(spn)) < 180:
                    coords[1] = str(float(coords[1]) + 2 * float(spn))
            elif event.key == pygame.K_UP:
                if abs(float(coords[0]) + 2 * float(spn)) < 90:
                    coords[0] = str(float(coords[0]) + 2 * float(spn))
            elif event.key == pygame.K_DOWN:
                if abs(float(coords[0]) - 2 * float(spn)) < 90:
                    coords[0] = str(float(coords[0]) - 2 * float(spn))
            elif event.key == pygame.K_PAGEUP:
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

    #print(coords, spn)
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



