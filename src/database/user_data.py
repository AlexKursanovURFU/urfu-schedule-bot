from typing import Optional, Dict, Any
from .connection import get_db_connection


class UserData:
    """Класс для работы с данными пользователей в БД."""

    def get_user_group(self, user_id: int) -> Optional[int]:
        """
        Получает ID группы пользователя.

        Args:
            user_id: ID пользователя в Telegram

        Returns:
            ID группы или None, если группа не выбрана
        """
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT group_id FROM Users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        connection.close()
        return result[0] if result else None

    def get_full_user_info(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Получает полную информацию о пользователе.

        Args:
            user_id: ID пользователя в Telegram

        Returns:
            Словарь с данными пользователя или None
        """
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
            SELECT user_id, group_id, group_title, course, division_id
            FROM Users WHERE user_id = ?
        ''', (user_id,))
        result = cursor.fetchone()
        connection.close()

        if result:
            return {
                'user_id': result[0],
                'group_id': result[1],
                'group_title': result[2],
                'course': result[3],
                'division_id': result[4]
            }
        return None

    def set_user_group(self, user_id: int, group_id: int,
                       group_title: str = None, course: int = None,
                       division_id: int = None) -> None:
        """
        Сохраняет или обновляет группу пользователя.

        Args:
            user_id: ID пользователя в Telegram
            group_id: ID группы в УрФУ
            group_title: Название группы
            course: Номер курса
            division_id: ID подразделения
        """
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute('''
            INSERT INTO Users (user_id, group_id, group_title, course, division_id)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                group_id = excluded.group_id,
                group_title = excluded.group_title,
                course = excluded.course,
                division_id = excluded.division_id
        ''', (user_id, group_id, group_title, course, division_id))

        connection.commit()
        connection.close()

    def delete_user(self, user_id: int) -> None:
        """
        Удаляет пользователя из БД (очищает его группу).

        Args:
            user_id: ID пользователя в Telegram
        """
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('DELETE FROM Users WHERE user_id = ?', (user_id,))
        connection.commit()
        connection.close()

    def user_exists(self, user_id: int) -> bool:
        """
        Проверяет, есть ли пользователь в БД.

        Args:
            user_id: ID пользователя в Telegram

        Returns:
            True если пользователь есть, иначе False
        """
        return self.get_user_group(user_id) is not None