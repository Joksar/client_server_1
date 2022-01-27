"""Ошибки"""


class IncorrectDataReceivedError(Exception):
    def __str__(self):
        return 'Принято некорректное сообщение от удаленного компьютера.'


class NonDictInputError(Exception):
    def __str__(self):
        return 'Аргумент функции должен быть словарем.'


class ReqFieldMissongError(Exception):
    def __init__(self, missing_field):
        self.missing_field = missing_field

    def __str__(self):
        return f'В принятом словаре отсутстсвует обязательное поле {self.missing_field}.'
