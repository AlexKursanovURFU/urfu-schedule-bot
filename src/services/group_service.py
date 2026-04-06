from typing import List, Optional
from ..api_client import UrfuAPIClient
from ..types import Group


class GroupService:
    """Сервис для работы с группами."""

    @staticmethod
    def search_groups(query: str) -> List[Group]:
        """
        Поиск групп по названию.

        Args:
            query: Название или часть названия группы

        Returns:
            Список найденных групп
        """
        with UrfuAPIClient() as client:
            return client.search_groups(query)

    @staticmethod
    def get_group_by_id(group_id: int) -> Optional[Group]:
        """
        Получает информацию о группе по ID.

        Args:
            group_id: ID группы в УрФУ

        Returns:
            Объект Group или None, если группа не найдена
        """
        # Ищем группы, содержащие ID
        groups = GroupService.search_groups(str(group_id))

        # Ищем точное совпадение по ID
        for group in groups:
            if group.id == group_id:
                return group
        return None

    @staticmethod
    def get_group_by_title(title: str) -> Optional[Group]:
        """
        Получает информацию о группе по точному названию.

        Args:
            title: Точное название группы

        Returns:
            Объект Group или None, если группа не найдена
        """
        groups = GroupService.search_groups(title)

        for group in groups:
            if group.title.lower() == title.lower():
                return group
        return groups[0] if groups else None