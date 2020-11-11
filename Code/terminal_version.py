import datetime


def defining_input(if_list=None, type_inp=int, text=''):
    """
    Возврат числа,
    с нужным типом данных, по границе вверхнего и нижнего значений,
    с выводом текста при вводе.

    :param if_list:
    :param if_list: список условий для числа состоит из:
                    списка верней и нижней границы;
                    если условий нет -> None
    :param type_inp: необходимый тип числа
    :param text: выводимый текст перед вводом данных
    :return: ввод пользователя в соответсвтующем типе данных
    """
    if_list = [None, None] if if_list is None else if_list
    while True:
        try:
            inp = eval(input(text))
            if type(inp) == type_inp:
                if (if_list[0] is None or if_list[0] <= type_inp(inp)) and \
                        (if_list[1] is None or if_list[1] >= type_inp(inp)):
                    return type_inp(inp)
                print('Неправильный ввод')
        except Exception:
            print('Неправильный ввод')


def defining_input_list(quantity=None, if_list=None, key_split=' ', type_inp=int, text=''):
    """
    Возврат нескольких чисел списком, вводимых через разделитель,
    с нужным типом данных, по границе вверхнего и нижнего значений,
    с выводом текста при вводе.

    :param quantity: количество нужных чисел
    :param if_list: список условий для числа состоит из:
                    списка верней и нижней границы;
                    если условий нет -> None
    :param key_split: разделитель для чисел
    :param type_inp: необходимый тип чисел
    :param text: выводимый текст перед вводом данных
    :return: лист данных, в требуемом типе данных
    """
    while True:
        try:
            inp_list = [
                type_inp(eval(el))
                for el in input(text).split(key_split)
                if type(eval(el)) == type_inp
            ]
            out_list = []
            if if_list:
                for i, data in enumerate(inp_list):
                    if quantity is None:
                        if (if_list[0] is None or if_list[0] <= data) and \
                                (if_list[1] is None or if_list[1] >= data):
                            out_list.append(data)
                    else:
                        if (if_list[i][0] is None or if_list[i][0] <= data) and \
                                (if_list[i][1] is None or if_list[i][1] >= data):
                            out_list.append(data)
            if len(out_list) == quantity or quantity is None:
                return out_list
            print('Неправильный ввод')
        except Exception:
            print('Неправильный ввод')


class Armchair:
    def __init__(self, y=10, x=10):
        self.places = [['O' for _ in range(x)] for _ in range(y)]

    def __str__(self):
        text = ''
        for y in self.places:
            text += f'{"".join(y)}\n'
        return text

    def add(self, y, x):
        for x_ in x:
            if self.places[y][x_] == 'X':
                print('Место занято.')
                return False
        for x_ in x:
            self.places[y][x_] = 'X'
        print('Места забронированы.')
        return True

    def add_several(self, number_of_packages):
        for y in range(len(self.places)):
            num = 0
            for x in range(len(self.places[y])):
                if self.places[y][x] == 'O':
                    num += 1
                else:
                    num = 0
                if num == number_of_packages:
                    return y, x + 1 - number_of_packages, x
        return False


class Session:
    def __init__(self, name='', year=2020, month=1, day=1, hour=1,
                 minute=0, duration_hours=1, duration_minutes=0, armchair=Armchair()):
        self.name = name
        self.time_start = datetime.datetime(year=year, month=month, day=day,
                                            hour=hour, minute=minute)
        self.duration = datetime.time(hour=duration_hours,
                                      minute=duration_minutes)
        self.time_finish = self.time_start + datetime. \
            timedelta(days=0, seconds=duration_hours * 3600 + duration_minutes * 60)
        self.armchair = armchair

    def __eq__(self, other):
        return self.time_start == other.time_start

    def __ne__(self, other):
        return self.time_start != other.time_start

    def __lt__(self, other):
        return self.time_start < other.time_start

    def __gt__(self, other):
        return self.time_start > other.time_start

    def __le__(self, other):
        return self.time_start <= other.time_start

    def __ge__(self, other):
        return self.time_start >= other.time_start

    def print_info(self, flag=False):
        if flag:
            print(f'Места:\n{self.armchair}', end='')
        print(f'название сеанса: {self.name}\nначало: {self.time_start}\n'
              f'продолжительность: {self.duration}\nконец: {self.time_finish}')


class Hall:
    def __init__(self, sessions=None):
        self.sessions = [] if sessions is None else sessions

    def add_session(self):
        name = input('Введите название: ')
        year, month, day = defining_input_list(quantity=3,
                                               if_list=[[1895, None], [1, 12], [1, 31]],
                                               text='Введите дату (Год месяц день): ')
        hour, minute = defining_input_list(quantity=2, if_list=[[0, 23], [0, 61]],
                                           text='Введите время начала(час минута): ')
        duration_hours, duration_minutes = defining_input_list(
            quantity=2,
            if_list=[[0, 23], [0, 61]],
            text='Введите продолжительность (час минута): '
        )
        self.sessions.append(Session(name=name, year=year, month=month,
                                     day=day, hour=hour, minute=minute,
                                     duration_hours=duration_hours,
                                     duration_minutes=duration_minutes,
                                     armchair=Armchair(
                                         y=defining_input(
                                             if_list=[1, None],
                                             text='Введите количество рядов в зале: '
                                         ),
                                         x=defining_input(
                                             if_list=[1, None],
                                             text='Введите количество мест в ряде: '
                                         )
                                     )))

    def print_info(self):
        for session in range(len(self.sessions)):
            print(f'Сеанс {session + 1}.')
            self.sessions[session].print_info()
        print('-' * 60)

    def occupy(self, num):
        try:
            print(f'Зал {num + 1}.\n{self.sessions[num].armchair}')
            y = defining_input(text='Введите номер ряда: ') - 1
            x = [
                int(i) - 1
                for i in defining_input_list(
                    if_list=[1, None],
                    text='Введите номер места(если несколько, то через пробел): '
                )]
            self.sessions[num].armchair.add(y=y, x=sorted(x))
            print(self.sessions[num].armchair)
        except ValueError or IndexError:
            print('Неправильный ввод')


class Cinema:
    def __init__(self, halls=None):
        self.halls = [] if halls is None else halls

    def add_halls(self):
        hall = Hall()
        for session in range(defining_input(
                if_list=[1, None],
                text='Введите количество сеансов: '
        )):
            print(f'Сеанс {session + 1}.')
            hall.add_session()
        self.halls.append(hall)

    def print_info(self):
        for hall in range(len(self.halls)):
            print(f'Зал {hall + 1}.')
            self.halls[hall].print_info()

    def occupy(self, num):
        while True:
            try:
                self.halls[num].occupy(defining_input(
                    if_list=[1, None],
                    text='Введите номер сеанса: '
                ) - 1)
                break
            except ValueError or IndexError:
                pass

    def several(self, number_of_packages):
        data = []
        for hall in self.halls:
            for session in hall.sessions:
                coord = session.armchair.add_several(number_of_packages)
                if coord:
                    data.append([session.time_start, session, coord])
        if data:
            data.sort()
            data[0][1].armchair.add(data[0][2][0], data[0][2][1:])
            data[0][1].print_info(True)
        else:
            print('Нет подходящих сеансов.')


class Cinemas:
    def __init__(self, cinemas=None):
        self.cinemas = [] if cinemas is None else cinemas

    def add_cinema(self):
        cin = Cinema()
        for index in range(defining_input(
                if_list=[1, None],
                text='Введите количество залов: '
        )):
            cin.add_halls()
        self.cinemas.append(cin)

    def get(self, num):
        while True:
            print('1-Информация о всех залах.')
            print('2-Информация о зале.')
            print('3-Вывод мест сеанса.')
            print('4-Забронировать места.')
            print('5-Ближайший сеанс на несколько человек.')
            print('6-Добавить зал.')
            print('7-Добавить сеанс.')
            print('0-Назад.')
            command = defining_input(if_list=[0, 7], text='Введите команду: ')
            if command == 1:
                self.cinemas[num].print_info()
            elif command == 2:
                h = defining_input(if_list=[1, None], text='Введите номер зала: ') - 1
                try:
                    self.cinemas[num].hall[h].print_info()
                except ValueError or IndexError:
                    print('Неправильный ввод')
            elif command == 3:
                h = defining_input(if_list=[1, None], text='Введите номер зала: ') - 1
                s = defining_input(if_list=[1, None], text='Введите номер сеанса: ') - 1
                try:
                    self.cinemas[num].halls[h].sessions[s].print_info(True)
                except ValueError or IndexError:
                    print('Неправильный ввод')
            elif command == 4:
                self.cinemas[num].print_info()
                h = defining_input(if_list=[1, None], text='Введите номер зала: ') - 1
                try:
                    self.cinemas[num].occupy(h)
                except ValueError or IndexError:
                    print('Неправильный ввод')
            elif command == 5:
                quantity = defining_input(
                    if_list=[1, None],
                    text='Введите требуемое количество мест: '
                )
                self.cinemas[num].several(quantity)
            elif command == 6:
                self.cinemas[num].add_halls()
            elif command == 7:
                h = defining_input(if_list=[1, None], text='Введите номер зала: ') - 1
                try:
                    self.cinemas[num].halls[h].add_session()
                except ValueError or IndexError:
                    print('Неправильный ввод')
            elif command == 0:
                return

    def __str__(self):
        return f'Кинотеатров всего: {len(self.cinemas)}'


if __name__ == '__main__':
    cinemas = Cinemas()
    print('Обусловимся, что:\n'
          'Время сеансов кино не пересекается, за этим пристально следят!\n'
          'Вся нумерация начинается с 1.\n'
          'Места в зале образуют прямоугольник.\n'
          'Места в зале нумеруются:\n'
          '\tряд сверху вниз от 1 до n соответственно\n'
          '\tместо слева направо от 1 до n соответственно\n'
          'В одной сети кинотеатров может быть от 1 до n кинотеатров\n'
          'В одном кинотеатре может быть от 1 до n кинозалов\n'
          'В одном кинозале за день может пройти от 1 до n сеансов\n'
          'В данный момент времени в кинозале может идти только 1 сеанс\n'
          )
    while True:
        print(cinemas)
        print('1-Добавить кинотеатр.')
        if cinemas.cinemas:
            print('2-Управление кинотеатром.')
        command = defining_input(
            if_list=[1, 2 if cinemas.cinemas else 1], text='Введите номер комамнды: '
        )
        if command == 1:
            cinemas.add_cinema()
        elif command == 2:
            cinemas.get(defining_input(
                if_list=[1, len(cinemas.cinemas)],
                text='Введите номер кинотеатра: '
            ) - 1)
