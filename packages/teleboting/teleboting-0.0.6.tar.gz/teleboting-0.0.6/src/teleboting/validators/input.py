from functools import wraps
from typing import Callable, Optional, List, Tuple
from telebot import TeleBot
from telebot.types import Message
from functools import wraps


class FieldValidator:
    def __init__(self):
        self._rules: List[Tuple[Callable, str]] = []

    def add_rule(self, rule: Callable[[str], bool], error_msg: str) -> None:
        self._rules.append((rule, error_msg))

    def validate(self, value: str) -> Optional[str]:
        for rule, error_msg in self._rules:
            if not rule(value):
                return error_msg
        return None


class NumberValidator(FieldValidator):
    @staticmethod
    def is_integer(error_msg: str = "Требуется целое число"):
        return lambda x: x.isdigit(), error_msg

    @staticmethod
    def is_float(error_msg: str = "Требуется число"):
        return lambda x: x.replace('.', '', 1).isdigit(), error_msg

    @staticmethod
    def min_value(min_val: float, error_msg: str = "Слишком маленькое значение"):
        return lambda x: float(x) >= min_val, error_msg

    @staticmethod
    def max_value(max_val: float, error_msg: str = "Слишком большое значение"):
        return lambda x: float(x) <= max_val, error_msg

    @staticmethod
    def decimal_places(max_places: int, error_msg: str = "Некорректное количество знаков"):
        return lambda x: len(x.split('.')[-1]) <= max_places if '.' in x else True, error_msg


class TextValidator(FieldValidator):
    @staticmethod
    def min_length(min_len: int, error_msg: str = "Слишком короткий текст"):
        return lambda x: len(x) >= min_len, error_msg

    @staticmethod
    def max_length(max_len: int, error_msg: str = "Слишком длинный текст"):
        return lambda x: len(x) <= max_len, error_msg

    @staticmethod
    def allowed_chars(allowed: str, error_msg: str = "Недопустимые символы"):
        return lambda x: all(c in allowed for c in x), error_msg

    @staticmethod
    def forbidden_words(forbidden: list, error_msg: str = "Запрещённые слова"):
        return lambda x: not any(word in x.lower() for word in forbidden), error_msg


import re
from typing import Callable, Optional


class PhoneValidator:
    def __init__(self, country_code: str = '+7', min_length: int = 11, max_length: int = 15):
        self._rules = []
        self.country_code = country_code
        self.min_length = min_length
        self.max_length = max_length

        # Добавляем базовые правила
        self.add_rule(
            lambda x: self._clean_phone(x).startswith(self.country_code),
            f"Номер должен начинаться с {self.country_code}"
        )
        self.add_rule(
            lambda x: self.min_length <= len(self._clean_phone(x)) <= self.max_length,
            f"Длина номера должна быть от {self.min_length} до {self.max_length} цифр"
        )

    @staticmethod
    def _clean_phone(phone: str) -> str:
        """Очистка номера от лишних символов"""
        return re.sub(r'[^\d+]', '', phone)

    def add_rule(self, rule: Callable[[str], bool], error_msg: str) -> None:
        self._rules.append((rule, error_msg))

    def add_custom_format(self, pattern: str, error_msg: str) -> None:
        """Добавление кастомного формата с regex"""
        regex = re.compile(pattern)
        self._rules.append((lambda x: bool(regex.match(x)), error_msg))

    def validate(self, phone: str) -> Optional[str]:
        cleaned_phone = self._clean_phone(phone)

        for rule, error_msg in self._rules:
            if not rule(cleaned_phone):
                return error_msg
        return None

    @property
    def sample_format(self) -> str:
        """Пример допустимого формата"""
        return f"{self.country_code}9991234567"


def input_validation(
        field_name: str,
        validator: FieldValidator,
        success_message: str = "✅ Данные приняты!",
        retry_prompt: str = "❌ Ошибка. Попробуйте снова:"
):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(message: Message, bot: TeleBot, *args, **kwargs):
            user_id = message.from_user.id
            value = message.text

            # Проверяем валидацию
            error = validator.validate(value)
            if error:
                bot.send_message(user_id, f"{error}\n{retry_prompt}")
                return  # Прерываем выполнение

            # Сохраняем данные и вызываем основной обработчик
            bot.send_message(user_id, success_message)
            return func(message, bot, *args, **kwargs, **{field_name: value})

        return wrapper

    return decorator