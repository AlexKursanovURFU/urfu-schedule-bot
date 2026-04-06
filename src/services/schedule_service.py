from datetime import datetime, timedelta
from typing import Optional

from ..api_client import UrfuAPIClient
from ..types import WeekSchedule


class ScheduleService:
    """Сервис для работы с расписанием."""

    def __init__(self, days_ahead: int = 7):
        """
        Инициализирует сервис расписания.

        Args:
            days_ahead: Количество дней для отображения расписания (по умолчанию 7)
        """
        self.days_ahead = days_ahead

    def set_days_ahead(self, days: int) -> None:
        """
        Устанавливает количество дней для отображения расписания.

        Args:
            days: Количество дней (от 1 до 30)
        """
        if 1 <= days <= 30:
            self.days_ahead = days

    def get_schedule(self, group_id: int,
                     date_from: Optional[datetime] = None,
                     days: Optional[int] = None) -> WeekSchedule:
        """
        Получает расписание группы.

        Args:
            group_id: ID группы в УрФУ
            date_from: Начальная дата (по умолчанию - сегодня)
            days: Количество дней (если не указано, используется days_ahead)

        Returns:
            Расписание на указанный период
        """
        if date_from is None:
            date_from = datetime.now()

        days_to_use = days or self.days_ahead
        date_to = date_from + timedelta(days=days_to_use - 1)

        with UrfuAPIClient() as client:
            return client.get_group_schedule(group_id, date_from, date_to)

    def get_today_schedule(self, group_id: int) -> WeekSchedule:
        """
        Получает расписание на сегодня.

        Args:
            group_id: ID группы в УрФУ

        Returns:
            Расписание на сегодня
        """
        today = datetime.now()
        return self.get_schedule(group_id, today, days=1)

    def get_tomorrow_schedule(self, group_id: int) -> WeekSchedule:
        """
        Получает расписание на завтра.

        Args:
            group_id: ID группы в УрФУ

        Returns:
            Расписание на завтра
        """
        tomorrow = datetime.now() + timedelta(days=1)
        return self.get_schedule(group_id, tomorrow, days=1)