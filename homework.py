from typing import Dict, List, Tuple, Type


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(
            self,
            training_type: str,
            duration: float,
            distance: float,
            speed: float,
            calories: float) -> None:
        self.training_type: str = training_type
        self.duration: float = duration
        self.distance: float = distance
        self.speed: float = speed
        self.calories: float = calories

    def get_message(self) -> str:
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIES_1: int = 18
    COEFF_CALORIES_2: int = 20
    MIN_IN_HOUR: int = 60

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calor: float = (
            (self.COEFF_CALORIES_1 * self.get_mean_speed()
             - self.COEFF_CALORIES_2) * self.weight
            / self.M_IN_KM * self.duration * self.MIN_IN_HOUR
        )
        return calor


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIES_1: float = 0.035
    COEFF_CALORIES_2: float = 0.029
    MIN_IN_HOUR: int = 60

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            height: float) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calor: float = (
            (self.COEFF_CALORIES_1 * self.weight
             + (self.get_mean_speed()**2 // self.height)
             * self.COEFF_CALORIES_2 * self.weight)
            * self.duration * self.MIN_IN_HOUR
        )
        return calor


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFF_CALORIES_1: float = 1.1
    COEFF_CALORIES_2: float = 2

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            length_pool: float,
            count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calor: float = (
            (self.get_mean_speed() + self.COEFF_CALORIES_1)
            * self.COEFF_CALORIES_2 * self.weight
        )
        return calor


def read_package(workout_type: str, data: List[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    naming: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return naming[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: str = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: List[Tuple[str, List[float]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
