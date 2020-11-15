# coding: utf-8
# license: GPLv3

from solar_objects import Star, Planet
from colors import *


def read_space_objects_data_from_file(input_filename):
    """Cчитывает данные о космических объектах из файла, создаёт сами объекты
    и вызывает создание их графических образов

    Параметры:

    **input_filename** — имя входного файла
    """

    objects = []
    with open(input_filename) as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue  # пустые строки и строки-комментарии пропускаем
            object_type = line.split()[0].lower()
            if object_type == "star":
                star = Star()
                parse_star_parameters(line, star)
                objects.append(star)
            elif object_type == 'planet':
                planet = Planet()
                parse_planet_parameters(line, planet)
                objects.append(planet)
            else:
                print("Unknown space object")

    return objects


def parse_star_parameters(line, star):
    """Считывает данные о звезде из строки.
    Входная строка должна иметь слеюущий формат:
    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Здесь (x, y) — координаты зведы, (Vx, Vy) — скорость.
    Пример строки:
    Star 10 red 1000 1 2 3 4

    Параметры:

    **line** — строка с описание звезды.
    **star** — объект звезды.
    """
    star_param = line.split()
    star.R = float(star_param[1])
    star.color = star_param[2]
    star.m = float(star_param[3])
    star.x = float(star_param[4])
    star.y = float(star_param[5])
    star.Vx = float(star_param[6])
    star.Vy = float(star_param[7])

def parse_planet_parameters(line, planet):
    """Считывает данные о планете из строки.
    Предполагается такая строка:
    Входная строка должна иметь слеюущий формат:
    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Здесь (x, y) — координаты планеты, (Vx, Vy) — скорость.
    Пример строки:
    Planet 10 red 1000 1 2 3 4

    Параметры:

    **line** — строка с описание планеты.
    **planet** — объект планеты.
    """
    planet_param = line.split()
    planet.R = float(planet_param[1])
    planet.color = planet_param[2]
    planet.m = float(planet_param[3])
    planet.x = float(planet_param[4])
    planet.y = float(planet_param[5])
    planet.Vx = float(planet_param[6])
    planet.Vy = float(planet_param[7])

def write_space_objects_data_to_file(output_filename, space_objects):
    """Сохраняет данные о космических объектах в файл.
    Строки должны иметь следующий формат:
    Star <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>
    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <Vx> <Vy>

    Параметры:

    **output_filename** — имя входного файла
    **space_objects** — список объектов планет и звёзд
    """
    with open(output_filename, 'w') as out_file:
        for obj in space_objects:
            obj_param_spisok = [0, 0, 0, 0, 0, 0, 0, 0]
            obj_param_spisok[0] = obj.type
            obj_param_spisok[1] = str(round(obj.R, 3))
            obj_param_spisok[2] = obj.color
            obj_param_spisok[3] = str(round(obj.m, 3))
            obj_param_spisok[4] = str(round(obj.x, 3))
            obj_param_spisok[5] = str(round(obj.y, 3))
            obj_param_spisok[6] = str(round(obj.Vx, 3))
            obj_param_spisok[7] = str(round(obj.Vy, 3))
            obj_param = ' '.join(obj_param_spisok)
            print(out_file, obj_param)
            out_file.write(obj_param + "\n")
        out_file.close()

if __name__ == "__main__":
    print("This module is not for direct call!")
