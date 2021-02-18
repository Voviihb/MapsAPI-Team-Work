import os
import sys
import pygame
import requests

from addons import Button, InputBox, get_full_address, print_text

clock = pygame.time.Clock()

map_type = "map"
#coords = input("Введите координаты в формате xxx yyy: ").split()
coords = ["-28.069396", "34.457771"]
spn = "10"
#spn = input("Введите значение параметра spn(масштаб): ")
map_params = {
        "ll": ",".join([coords[1], coords[0]]),
        "spn": ",".join([spn, spn]),
        "l": map_type
}

map_params2 = {
    "ll": ",".join([coords[1], coords[0]]),
    "spn": ",".join([spn, spn]),
    "l": map_type
}


map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

pygame.init()
screen = pygame.display.set_mode((800, 600))
background_scheme_button = Button(170, 60, screen, pygame, active_clr=(255, 0, 0))
background_sputnik_button = Button(170, 60, screen, pygame, active_clr=(255, 0, 0))
background_hybrid_button = Button(170, 60, screen, pygame, active_clr=(255, 0, 0))
search_button = Button(170, 60, screen, pygame, active_clr=(255, 255, 0))
reset_search_button = Button(170, 60, screen, pygame, active_clr=(255, 255, 0))
index_on_button = Button(170, 60, screen, pygame, active_clr=(255, 255, 0))
address_input_box = InputBox(pygame, 5, 460, 150, 32)
address_input_box_done = False

full_address = ""
running = True
x = y = 0
index = ""
index_on = False
while running:
    screen.fill("black")
    for event in pygame.event.get():
        address_input_box.handle_event(event)
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
                if abs(float(coords[0]) - 3 * float(spn)) < 90:
                    coords[0] = str(float(coords[0]) - 2 * float(spn))
            elif event.key == pygame.K_PAGEUP:
                if 0 < float(spn) - 0.5 * float(spn) < 90:
                    spn = str(float(spn) - 0.5 * float(spn))
            elif event.key == pygame.K_PAGEDOWN:
                if 0 < float(spn) + 0.5 * float(spn) < 90:
                    spn = str(float(spn) + 0.5 * float(spn))

    address_input_box.update()
    address_input_box.draw(screen)

    if index_on_button.draw((400, 500), "Индекс"):
        index_on = not index_on
    if background_scheme_button.draw((620, 20), "Схема"):
        map_type = "map"
    if background_sputnik_button.draw((620, 100), "Спутник"):
        map_type = "sat"
    if background_hybrid_button.draw((620, 180), "Гибрид"):
        map_type = "sat,skl"
    if search_button.draw((5, 500), "Искать!"):
        address = address_input_box.return_text()        if address:
            address_and_coords = get_full_address(address)
            if address_and_coords:
                r = address_and_coords[0]
                full_address = address_and_coords[1]
                index = address_and_coords[2]
                x = (float(r["lowerCorner"].split()[1]) + float(r["upperCorner"].split()[1])) / 2
                y = (float(r["lowerCorner"].split()[0]) + float(r["upperCorner"].split()[0])) / 2
                coords = [str(x), str(y)]
                map_params2 = {
                    "ll": ",".join([str(y), str(x)]),
                    "spn": ",".join([spn, spn]),
                    "l": map_type,
                    "pt": f"{y},{x},org"
                }
    if reset_search_button.draw((200, 500), "Сбросить"):
        full_address = ""
        if x:
            map_params2.pop("pt", None)
            map_params.pop("pt", None)
            response = requests.get(map_api_server, params=map_params)

        x = y = 0

    map_params2 = {
        "ll": ",".join([coords[1], coords[0]]),
        "spn": ",".join([spn, spn]),
        "l": map_type,
    }
    if x:
        map_params2["pt"] = f"{y},{x},org"
        if "pt" not in map_params or map_params["pt"] != map_params2["pt"]:
            map_params["pt"] = f"{y},{x},org"
            response = requests.get(map_api_server, params=map_params)

    if map_params != map_params2:
        map_params = map_params2
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
    print_text(full_address + (" " + index if index_on and full_address else ""), 5, 570, screen, pygame, font_size=12)

    pygame.display.flip()

    os.remove(map_file)
    clock.tick(60)

pygame.quit()