import sys
import re
import datetime
from project_config import *
from Players import *
from Countries import *

sys.path.append('tables')


def check_date(data):
    try:
        datetime.date.fromisoformat(data)
        return 0
    except ValueError:
        return 1


class Main:
    config = ProjectConfig()
    connection = DbConnection(config)

    def __init__(self):
        DbTable.dbconn = self.connection
        return

    def db_init(self):
        pt = PlayersTable()
        ct = CountriesTable()
        ct.create()
        pt.create()
        return

    def db_drop(self):
        ct = CountriesTable()
        pt = PlayersTable()
        pt.drop()
        ct.drop()
        return

    def read_next_step(self):
        return input("=> ").strip()

    def show_main_menu(self):
        menu = """Добро пожаловать! 
Основное меню (выберите цифру в соответствии с необходимым действием): 
    1 - просмотр стран;
    2 - просмотр игроков
    3 - сброс и инициализация таблиц;
    9 - выход."""
        print(menu)
        return

    def after_show_main_menu(self, next_step):
        while True:
            if next_step == "3":
                self.db_drop()
                self.db_init()
                print("Таблицы созданы заново!")
                return "0"
            elif next_step != "1" and next_step != "2" and next_step != "9":
                print("Выбрано неверное число! Повторите ввод!")
                return "0"
            else:
                return next_step

    def show_country(self):
        self.country_id = -1
        menu = """Просмотр списка стран!
String_number\tShort_name\tLong_name\tRegion"""
        print(menu)
        lst = CountriesTable().all()
        k = 1
        for i in lst:
            print(str(k) + "\t" + str(i[3]) + "\t" + str(i[1]) + "\t" + str(i[2]))
            k = k + 1
        menu = """Дальнейшие операции:
    0 - возврат в главное меню;
    4 - добавление новой страны;
    5 - удаление страны;
    6 - просмотр людей;
    9 - выход."""
        print(menu)
        return

    def after_show_country(self, next_step):
        while True:
            if next_step != "0" and next_step != "4" \
                    and next_step != "5" and next_step != "6" and next_step != "9":
                print("Выбрано неверное число! Повторите ввод!")
                return "1"
            else:
                return next_step

    def show_player(self):
        self.player_id = -1
        menu = """Просмотр списка игроков!
String_number\tFirst_name\tSecond_name\tBirthday\tCountry_id"""
        print(menu)
        lst = PlayersTable().all()
        k = 1
        for i in lst:
            print(str(k) + "\t" + str(i[1]) + "\t" + str(i[4])
                  + "\t" + str(i[0]) + "\t" + str(i[2]))
            k = k + 1
        menu = """Дальнейшие операции:
    0 - возврат в главное меню;
    9 - выход."""
        print(menu)
        return

    def after_show_player(self, next_step):
        while True:
            if next_step != "0" and next_step != "7" and next_step != "9":
                print("Выбрано неверное число! Повторите ввод!")
                return "2"
            else:
                return next_step

    def before_show_players_by_country(self):
        if self.country_id == -1:
            while True:
                num = input("Укажите номер строки, где находится интересующая вас страна (0 - отмена): ")
                if num == "0":
                    return "1"
                while True:
                    if not re.fullmatch('\d+', num):
                        num = input(
                            "Неверный ввод. Повторите ввод! "
                            "Укажите номер строки, где находится интересующая вас страна (0 - отмена): ")
                        if num == "0":
                            return "1"
                    elif len(num.strip()) > 6:
                        num = input(
                            "Неверный ввод. Повторите ввод! "
                            "Укажите номер строки, где находится интересующая вас страна (0 - отмена): ")
                        if num == "0":
                            return "1"
                    else:
                        break
                country = CountriesTable().find(int(num))
                if not country:
                    print("Введена страна, которая не существует!")
                else:
                    self.country_id = int(country[0])
                    self.country_obj = country
                    break
        return "61"

    def show_players_by_country(self):
        if self.country_obj[1] is None:
            print("Выбрана страна: " + self.country_obj[3] + " None " + self.country_obj[2])
        else:
            print("Выбрана страна: " + self.country_obj[3] + " "
              + self.country_obj[1] + " " + self.country_obj[2])
        lst = PlayersTable().all_by_country_id(self.country_id)
        k = 1
        for i in lst:
            print("Номер строки:" + " " + str(k) + " " + "Фамилия:" + " " + i[1] + " " + "Имя:" + " " + i[4]
                  + " " + "Дата рождения:" + " " + str(i[0]))
            k = k + 1
        menu = """Дальнейшие операции:
    0 - возврат в главное меню;
    1 - возврат в просмотр стран;
    7 - удаление игрока
    8 - добавление нового игрока;
    9 - выход."""
        print(menu)
        return

    def after_show_players_by_country(self, next_step):
        while True:
            if next_step != "0" and next_step != "1" and next_step != "7" and next_step != "8" and next_step != "9":
                print("Выбрано неверное число! Повторите ввод!")
                return "6"
            else:
                return next_step

    def add_country(self):
        data = []
        data.append(input("Введите короткое название (+ - отмена): ").strip())
        if data[0] == "+":
            return
        while True:
            while len(data[0].strip()) == 0:
                data[0] = input(
                    "Короткое название не может быть пустым! "
                    "Введите короткое название заново (+ - отмена):").strip()
                if data[0] == "+":
                    return
            short_name = CountriesTable().find_by_short_name(data[0])
            if short_name:
                data[0] = input(
                    "Такое короткое название уже существует! "
                    "Введите короткое название заново (+ - отмена):").strip()
            else:
                break
        data.append(input("Введите длинное название (+ - отмена): ").strip())
        if data[1] == "+":
            return
        while True:
            if len(data[0].strip()) == 0:
                break
            long_name = CountriesTable().find_by_long_name(data[0])
            if long_name:
                data[1] = input(
                    "Такое длинное название уже существует! "
                    "Введите длинное название заново (+ - отмена):").strip()
            else:
                break
        data.append(input("Введите регион (+ - отмена):").strip())
        if data[2] == "+":
            return
        while len(data[2].strip()) == 0:
            data[2] = input("Регион не может быть пустым! Введите регион заново (+ - отмена):").strip()
            if data[2] == "+":
                return
        CountriesTable().insert_one(data)
        return

    def add_player(self):
        data = [input("Введите фамилию (+ - отмена): ").strip()]
        if data[0] == "+":
            return
        while len(data[0].strip()) == 0:
            data[0] = input("Фамилия не может быть пустой! Введите фамилию заново (+ - отмена):").strip()
            if data[0] == "+":
                return
        data.append(input("Введите имя (+ - отмена): ").strip())
        if data[1] == "+":
            return
        while len(data[1].strip()) == 0:
            data[1] = input("Имя не может быть пустым! Введите имя заново (+ - отмена):").strip()
            if data[1] == "+":
                return
        data.append(input("Введите дату рождения (+ - отмена):").strip())
        if data[2] == "+":
            return
        while check_date(data[2]):
            data[2] = input(
                "Неверный ввод. Повторите ввод!"
                "Введите дату рождения (+ - отмена): ")
            if data[2] == "+":
                return
        data.append(self.country_id)
        PlayersTable().insert_one(data)
        return

    def delete_player(self):
        while True:
            arg = input("Введите номер интересующий вас строки (0 - отмена): ")
            if arg == "0":
                return
            while True:
                if not re.fullmatch('\d+', arg):
                    arg = input(
                        "Неверный ввод. Повторите ввод! "
                        "Введите номер интересующий вас строки (0 - отмена): ")
                    if arg == "0":
                        return
                elif len(arg.strip()) > 6:
                    arg = input(
                        "Неверный ввод. Повторите ввод! "
                        "Введите номер интересующий вас строки (0 - отмена): ")
                    if arg == "0":
                        return
                else:
                    break
            player = PlayersTable().find(self.country_id, int(arg))
            if not player:
                print("Введен игрок, который не существует!")
            else:
                break
        PlayersTable().delete_one(int(arg))
        return

    def delete_country(self):
        while True:
            arg = input("Введите номер строки, где находится интересующая вас страна (0 - отмена): ")
            if arg == "0":
                return
            while True:
                if not re.fullmatch('\d+', arg):
                    arg = input(
                        "Неверный ввод. Повторите ввод! "
                        "Введите номер строки, где находится интересующая вас страна (0 - отмена): ")
                    if arg == "0":
                        return
                elif len(arg.strip()) > 6:
                    arg = input(
                        "Неверный ввод. Повторите ввод! "
                        "Введите номер строки, где находится интересующая вас страна (0 - отмена): ")
                    if arg == "0":
                        return
                else:
                    break
            country = CountriesTable().find(int(arg))
            if not country:
                print("Введена страна, которая не существует!")
            else:
                break
        CountriesTable().delete_one(int(arg))
        return

    def main_cycle(self):
        current_menu = "0"
        while current_menu != "9":
            if current_menu == "0":
                self.show_main_menu()
                next_step = self.read_next_step()
                current_menu = self.after_show_main_menu(next_step)
            elif current_menu == "1":
                self.show_country()
                next_step = self.read_next_step()
                current_menu = self.after_show_country(next_step)
            elif current_menu == "2":
                self.show_player()
                next_step = self.read_next_step()
                current_menu = self.after_show_player(next_step)
            elif current_menu == "3":
                self.show_main_menu()
            elif current_menu == "4":
                self.add_country()
                current_menu = "1"
            elif current_menu == "5":
                self.delete_country()
                current_menu = "1"
            elif current_menu == "6":
                current_menu = self.before_show_players_by_country()
            elif current_menu == "61":
                self.show_players_by_country()
                next_step = self.read_next_step()
                current_menu = self.after_show_players_by_country(next_step)
            elif current_menu == "7":
                self.delete_player()
                current_menu = "61"
            elif current_menu == "8":
                self.add_player()
                current_menu = "61"
        print("До свидания!")
        return


m = Main()
m.main_cycle()
