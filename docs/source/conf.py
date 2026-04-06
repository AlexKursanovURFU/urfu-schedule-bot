import os
import sys

# Добавляем путь к папке src (правильный способ)
sys.path.insert(0, os.path.abspath('../../'))

# Или так, если не работает:
# sys.path.insert(0, 'C:/Users/Gregory/PycharmProjects/urfu-schedule-bot/src')

project = 'urfu-schedule-bot'
author = 'АННА'
copyright = '2026, АННА'
release = '2.0.0'
language = 'ru'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Создаем папку _static если её нет
if not os.path.exists('_static'):
    os.makedirs('_static')

autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'undoc-members': True,
}

# Отключаем проверку импортов для неподдерживаемых модулей
autodoc_mock_imports = ['telegram', 'httpx', 'loguru', 'dotenv']