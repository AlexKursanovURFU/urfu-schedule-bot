from telegram import Update
from telegram.ext import ContextTypes
from .config import logger
from .database.user_data import UserData
from .services.group_service import GroupService
from .services.schedule_service import ScheduleService
from .utils.formatters import (
    format_schedule_message,
    format_group_list_message,
    format_mygroup_message,
    format_error_message
)


class BotHandlers:
    """Обработчики команд бота."""

    def __init__(self):
        """Инициализирует обработчики с необходимыми сервисами."""
        self.user_data = UserData()
        self.group_service = GroupService()
        self.schedule_service = ScheduleService(days_ahead=7)

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обработчик команды /start"""
        user = update.effective_user

        message = f"""
👋 Привет, {user.first_name}!

Я — бот для расписания УрФУ.

📋 *Доступные команды:*
/schedule - 📅 показать расписание
/setgroup - 🔍 выбрать группу
/mygroup - ℹ️ информация о вашей группе
/cleargroup - 🗑 очистить группу
/days - 📊 установить количество дней для расписания
/help - ❓ справка
/about - ℹ️ о боте

💡 *Для начала работы:* используйте /setgroup
        """
        await update.message.reply_text(message, parse_mode="Markdown")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обработчик команды /help"""
        message = """
📋 *Помощь по боту*

*Основные команды:*
/schedule - показать расписание на ближайшие дни
/setgroup <название или ID> - выбрать группу
/mygroup - показать текущую группу
/cleargroup - очистить выбранную группу
/groups - 📚 показать список доступных групп

*Настройки:*
/days <число> - установить количество дней для расписания (1-30)

*Информация:*
/about - о боте
/help - эта справка

*Примеры:*
/setgroup МЕН-333009
/setgroup 63725
/days 14
        """
        await update.message.reply_text(message, parse_mode="Markdown")

    async def about_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обработчик команды /about"""
        message = """
🤖 *Бот расписания УрФУ*

*Версия:* 2.0.0
*Функционал:*
• Просмотр расписания групп
• Сохранение выбранной группы
• Настройка периода расписания

*Данные:* API УрФУ
        """
        await update.message.reply_text(message, parse_mode="Markdown")

    async def setgroup_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обработчик команды /setgroup - выбор группы"""
        user_id = update.effective_user.id
        args = context.args

        if not args:
            await update.message.reply_text(
                "❌ *Укажите группу*\n\n"
                "Примеры:\n"
                "/setgroup МЕН-333009\n"
                "/setgroup 63725\n\n"
                "Или отправьте название группы для поиска",
                parse_mode="Markdown"
            )
            return

        query = " ".join(args)
        await update.message.reply_text(f"🔍 Ищу группу '{query}'...")

        try:
            groups = self.group_service.search_groups(query)

            if not groups:
                await update.message.reply_text(f"❌ Группа '{query}' не найдена")
                return

            if len(groups) == 1:
                # Одна группа - сохраняем сразу
                group = groups[0]
                self.user_data.set_user_group(
                    user_id=user_id,
                    group_id=group.id,
                    group_title=group.title,
                    course=group.course,
                    division_id=group.divisionId
                )
                await update.message.reply_text(
                    f"✅ *Группа сохранена!*\n\n"
                    f"🎓 {group.title}\n"
                    f"📚 Курс: {group.course}\n"
                    f"🆔 ID: {group.id}\n\n"
                    f"Теперь используйте /schedule для просмотра расписания",
                    parse_mode="Markdown"
                )
            else:
                # Несколько групп - показываем список
                message = format_group_list_message(groups, query)
                await update.message.reply_text(message, parse_mode="Markdown")

        except Exception as e:
            logger.error(f"Ошибка в setgroup: {e}")
            await update.message.reply_text(format_error_message(str(e)), parse_mode="Markdown")

    async def mygroup_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обработчик команды /mygroup - информация о текущей группе"""
        user_id = update.effective_user.id
        user_info = self.user_data.get_full_user_info(user_id)

        if not user_info or not user_info.get('group_id'):
            await update.message.reply_text(
                "❌ *Группа не выбрана*\n\n"
                "Используйте /setgroup для выбора группы",
                parse_mode="Markdown"
            )
            return

        message = format_mygroup_message(
            group_title=user_info.get('group_title', 'Неизвестно'),
            group_id=user_info['group_id'],
            course=user_info.get('course', 'Неизвестно'),
            days_ahead=self.schedule_service.days_ahead
        )
        await update.message.reply_text(message, parse_mode="Markdown")

    async def cleargroup_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обработчик команды /cleargroup - удаление группы"""
        user_id = update.effective_user.id

        user_info = self.user_data.get_full_user_info(user_id)
        if not user_info or not user_info.get('group_id'):
            await update.message.reply_text("❌ У вас не выбрана группа")
            return

        self.user_data.delete_user(user_id)
        await update.message.reply_text(
            "✅ *Группа удалена!*\n\n"
            "Используйте /setgroup для выбора новой группы",
            parse_mode="Markdown"
        )

    async def days_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обработчик команды /days - установка количества дней"""
        args = context.args

        if not args:
            await update.message.reply_text(
                f"📊 *Текущее количество дней:* {self.schedule_service.days_ahead}\n\n"
                "Используйте /days <число> для изменения\n"
                "Пример: /days 14\n"
                "Доступный диапазон: 1-30 дней",
                parse_mode="Markdown"
            )
            return

        try:
            days = int(args[0])
            if days < 1 or days > 30:
                await update.message.reply_text("❌ Количество дней должно быть от 1 до 30")
                return

            self.schedule_service.set_days_ahead(days)
            await update.message.reply_text(
                f"✅ *Количество дней изменено!*\n\n"
                f"📅 Теперь расписание показывается на {days} дней\n\n"
                f"Используйте /schedule для просмотра",
                parse_mode="Markdown"
            )
        except ValueError:
            await update.message.reply_text("❌ Укажите число. Пример: /days 14")

    async def schedule_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обработчик команды /schedule - показать расписание"""
        user_id = update.effective_user.id

        # Получаем группу пользователя
        user_info = self.user_data.get_full_user_info(user_id)

        if not user_info or not user_info.get('group_id'):
            await update.message.reply_text(
                "❌ *Группа не выбрана!*\n\n"
                "Сначала выберите группу командой /setgroup\n"
                "Пример: /setgroup МЕН-333009",
                parse_mode="Markdown"
            )
            return

        group_id = user_info['group_id']
        group_title = user_info.get('group_title', 'Ваша группа')

        await update.message.reply_text(f"⏳ Загружаю расписание для группы *{group_title}*...",
                                        parse_mode="Markdown")

        try:
            schedule = self.schedule_service.get_schedule(group_id)

            message = format_schedule_message(
                schedule,
                group_title,
                self.schedule_service.days_ahead
            )

            if len(message) > 4096:
                # Если сообщение слишком длинное, отправляем по частям
                for i in range(0, len(message), 4000):
                    await update.message.reply_text(
                        message[i:i + 4000],
                        parse_mode="Markdown",
                        disable_web_page_preview=True
                    )
            else:
                await update.message.reply_text(
                    message,
                    parse_mode="Markdown",
                    disable_web_page_preview=True
                )

        except Exception as e:
            logger.error(f"Ошибка в schedule: {e}")
            await update.message.reply_text(format_error_message(str(e)), parse_mode="Markdown")

    async def groups_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обработчик команды /groups - показать список доступных групп"""
        from .utils.formatters import format_preset_groups_message

        message = format_preset_groups_message()
        await update.message.reply_text(message, parse_mode="Markdown")