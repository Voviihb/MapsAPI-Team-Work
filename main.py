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
                coords[1] = str(float(coords[1]) - 2 * float(spn))
            elif event.key == pygame.K_RIGHT:
                coords[1] = str(float(coords[1]) + 2 * float(spn))
            elif event.key == pygame.K_UP:
                coords[0] = str(float(coords[0]) + 2 * float(spn))
            elif event.key == pygame.K_DOWN:
                coords[0] = str(float(coords[0]) - 2 * float(spn))

    map_params = {
        "ll": ",".join([coords[1], coords[0]]),
        "spn": ",".join([spn, spn]),
        "l": "map"
    }

    print(coords)
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



