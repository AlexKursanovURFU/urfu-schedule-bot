"""
Предустановленные группы УрФУ
Содержит список групп для быстрого выбора
"""

from typing import List, Dict, Optional
from ..types import Group

# Список предустановленных групп
PRESET_GROUPS: List[Dict] = [
    # МЕН группы
    {"id": 63723, "title": "МЕН-333001", "course": 3},
    {"id": 63725, "title": "МЕН-333009", "course": 3},
    {"id": 63726, "title": "МЕН-333105", "course": 3},
    {"id": 63727, "title": "МЕН-333202", "course": 3},
    {"id": 63728, "title": "МЕН-333401", "course": 3},
    {"id": 63729, "title": "МЕН-333402", "course": 3},
    # МЕН-330 группы
    {"id": 63730, "title": "МЕН-330301", "course": 3},
    {"id": 63731, "title": "МЕН-330302", "course": 3},
    {"id": 63732, "title": "МЕН-330409", "course": 3},
    {"id": 63733, "title": "МЕН-330501", "course": 3},
    {"id": 63734, "title": "МЕН-330502", "course": 3},
    {"id": 63735, "title": "МЕН-330601", "course": 3},
    {"id": 63736, "title": "МЕН-330602", "course": 3},
    {"id": 63737, "title": "МЕН-330603", "course": 3},
    {"id": 63738, "title": "МЕН-330701", "course": 3},
    {"id": 63739, "title": "МЕН-330801", "course": 3},
]


def get_preset_groups() -> List[Dict]:
    """
    Возвращает список предустановленных групп.

    Returns:
        List[Dict]: Список групп с полями id, title, course
    """
    return PRESET_GROUPS.copy()


def get_preset_group_by_title(title: str) -> Optional[Dict]:
    """
    Ищет предустановленную группу по названию.

    Args:
        title: Название группы (например, "МЕН-333009")

    Returns:
        Dict или None, если группа не найдена
    """
    for group in PRESET_GROUPS:
        if group["title"].lower() == title.lower():
            return group
    return None


def get_preset_group_by_id(group_id: int) -> Optional[Dict]:
    """
    Ищет предустановленную группу по ID.

    Args:
        group_id: ID группы

    Returns:
        Dict или None, если группа не найдена
    """
    for group in PRESET_GROUPS:
        if group["id"] == group_id:
            return group
    return None


def is_preset_group(title: str) -> bool:
    """
    Проверяет, является ли группа предустановленной.

    Args:
        title: Название группы

    Returns:
        True если группа в списке, иначе False
    """
    return get_preset_group_by_title(title) is not None


def get_all_group_titles() -> List[str]:
    """
    Возвращает список всех названий групп.

    Returns:
        List[str]: Список названий групп
    """
    return [group["title"] for group in PRESET_GROUPS]