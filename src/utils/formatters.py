from typing import List
from ..types import WeekSchedule, Lesson, Group


def format_schedule_message(schedule: WeekSchedule,
                            group_title: str = None,
                            days_ahead: int = 7) -> str:
    """
    Форматирует расписание в красивое сообщение для Telegram.

    Args:
        schedule: Объект WeekSchedule с расписанием
        group_title: Название группы (опционально)
        days_ahead: Количество дней в расписании

    Returns:
        Отформатированное сообщение в Markdown
    """
    if not schedule.days:
        return "📭 На ближайшие дни занятий нет"

    # Заголовок
    message = "📚 *РАСПИСАНИЕ*\n"
    if group_title:
        message += f"🎓 *Группа:* {group_title}\n"
    message += f"📅 *Период:* {days_ahead} дней\n"
    message += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

    day_count = 0

    for day in schedule.days:
        if not day.lessons:
            continue

        day_count += 1
        # Заголовок дня
        weekday_ru = _translate_weekday(day.weekday)
        date_short = day.date[5:].replace('-', '.')
        message += f"*📌 {weekday_ru} ({date_short})*\n"
        message += "────────────────────────────────────\n"

        for lesson in day.lessons:
            message += _format_lesson(lesson)

        message += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"

    if day_count == 0:
        return "📭 На ближайшие дни занятий нет"

    return message


def _format_lesson(lesson: Lesson) -> str:
    """Форматирует одно занятие."""
    # Время
    time_start = lesson.timeBegin[:5] if lesson.timeBegin else "??:??"
    time_end = lesson.timeEnd[:5] if lesson.timeEnd else "??:??"
    pair_info = f"[{lesson.pairNumber} пара]" if lesson.pairNumber > 0 else ""

    message = f"🕐 *{time_start}*–{time_end} {pair_info}\n"
    message += f"📖 {lesson.title}\n"
    message += f"📚 *Тип:* {lesson.loadType}\n"

    # Преподаватель
    if lesson.teacherName:
        message += f"👨‍🏫 *Преподаватель:* {lesson.teacherName}\n"

    # Аудитория
    if lesson.auditoryTitle:
        message += f"🏛 *Аудитория:* {lesson.auditoryTitle}\n"
        if lesson.auditoryLocation:
            # Сокращаем длинное название локации
            location = lesson.auditoryLocation[:60] + "..." if len(
                lesson.auditoryLocation) > 60 else lesson.auditoryLocation
            message += f"📍 {location}\n"

    # Комментарий или ссылка
    if lesson.comment:
        if lesson.comment.startswith('http'):
            message += f"🔗 [Ссылка на занятие]({lesson.comment})\n"
        else:
            comment = lesson.comment[:80] + "..." if len(lesson.comment) > 80 else lesson.comment
            message += f"💬 {comment}\n"

    return message + "\n"


def format_group_list_message(groups: List[Group], query: str) -> str:
    """
    Форматирует список найденных групп.

    Args:
        groups: Список групп
        query: Поисковый запрос

    Returns:
        Отформатированное сообщение
    """
    if not groups:
        return f"❌ По запросу '{query}' группы не найдены"

    message = f"🔍 *Результаты поиска групп:*\n"
    message += f"📝 *Запрос:* '{query}'\n"
    message += f"📊 *Найдено:* {len(groups)} групп\n\n"

    for i, group in enumerate(groups[:10], 1):
        message += f"{i}. *{group.title}*\n"
        message += f"   🆔 ID: `{group.id}`\n"
        message += f"   📚 Курс: {group.course}\n\n"

    if len(groups) > 10:
        message += f"*...и еще {len(groups) - 10} групп*\n\n"

    message += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    message += "💡 *Как выбрать группу:*\n"
    message += "Отправьте `/setgroup ID`\n"
    message += f"Например: `/setgroup {groups[0].id if groups else 63725}`\n\n"
    message += "Или повторите поиск с более точным названием"

    return message


def format_mygroup_message(group_title: str, group_id: int, course: int, days_ahead: int) -> str:
    """
    Форматирует сообщение с информацией о текущей группе.

    Args:
        group_title: Название группы
        group_id: ID группы
        course: Номер курса
        days_ahead: Текущая настройка количества дней

    Returns:
        Отформатированное сообщение
    """
    message = f"""
ℹ️ *Ваша текущая группа*

🎓 *Название:* {group_title}
🆔 *ID:* `{group_id}`
📚 *Курс:* {course}

📊 *Настройки:*
📅 *Дней для расписания:* {days_ahead}

💡 *Команды:*
/schedule - показать расписание
/cleargroup - удалить группу
/days <число> - изменить количество дней
"""
    return message


def _translate_weekday(weekday: str) -> str:
    """
    Переводит название дня недели на русский с заглавной буквы.

    Args:
        weekday: Название дня на русском (может быть с маленькой буквы)

    Returns:
        День недели с заглавной буквы
    """
    return weekday.capitalize()


def format_error_message(error: str) -> str:
    """
    Форматирует сообщение об ошибке.

    Args:
        error: Текст ошибки

    Returns:
        Отформатированное сообщение об ошибке
    """
    return f"❌ *Ошибка:* {error}\n\nПопробуйте позже или обратитесь к администратору."


def format_preset_groups_message() -> str:
    """
    Форматирует список предустановленных групп для вывода в Telegram.

    Returns:
        Отформатированное сообщение со списком групп
    """
    from ..data.preset_groups import get_preset_groups

    groups = get_preset_groups()

    message = "📚 *Доступные группы УрФУ*\n\n"

    # Группируем по префиксу
    men_333 = [g for g in groups if g["title"].startswith("МЕН-333")]
    men_330 = [g for g in groups if g["title"].startswith("МЕН-330")]

    message += "*МЕН-333:*\n"
    for group in men_333:
        message += f"  • `{group['title']}` (ID: {group['id']})\n"

    message += "\n*МЕН-330:*\n"
    for group in men_330:
        message += f"  • `{group['title']}` (ID: {group['id']})\n"

    message += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    message += "💡 *Как выбрать группу:*\n"
    message += "Отправьте `/setgroup МЕН-333009`\n"
    message += "Или `/setgroup 63725`\n\n"
    message += "📌 *Совет:* Используйте `/search` для поиска других групп"

    return message