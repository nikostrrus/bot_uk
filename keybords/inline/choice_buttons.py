from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import keybords.inline.callback_datas as key

menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text='Продолжить', callback_data=key.menu_callback.new(item_menu='next')),
        ],
    ]
)

helo_keyboard = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text='Еженедельные Миссии', callback_data=key.helo_callback.new(item_helo='helo')),
        ],
        [
            InlineKeyboardButton(text='Отправить контакты старшего по дому', callback_data=key.main_menu_callback.new(item_main_menu='contactAdd')),
        ],
        [
            InlineKeyboardButton(text='Хочу собрать протокол', callback_data=key.main_menu_callback.new(item_main_menu='protocol')),
        ],
        [
            InlineKeyboardButton(text='Узнать мои баллы', callback_data=key.mission_callback.new(item_mission='my_bolls')),
        ],
    ]
)

mission_keyboard = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text='Задания', callback_data=key.user_mission_callbacks.new(item_user='user')),
        ],
        [
            InlineKeyboardButton(text='Узнать мои баллы', callback_data=key.mission_callback.new(item_mission='my_bolls')),
        ],
    ]
)

back_keyboard = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text='Назад', callback_data=key.back_callback.new(item_back='back'))
        ]
    ]
)

point_back_keyboard = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text='Засчитать очки', callback_data=key.point_back_callback.new(item_point_back='count')),
            InlineKeyboardButton(text='Не засчитать очки', callback_data=key.point_back_callback.new(item_point_back='uncount')),
        ]
    ]
)

main_menu_keybord = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text='Посмотреть все задания', callback_data=key.main_menu_callback.new(item_main_menu='all_mission')),
        ],
        [
            InlineKeyboardButton(text='Показать всех участников в exel', callback_data=key.main_menu_callback.new(item_main_menu='top_ten')),
        ],
        [
            InlineKeyboardButton(text='Изменить очки участников', callback_data=key.main_menu_callback.new(item_main_menu='write_point')),
        ],
        [
            InlineKeyboardButton(text='выгрузить ответы', callback_data=key.main_menu_callback.new(item_main_menu='phone')),
        ],
    ]
)

all_mis_keyboard = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text='Добавить задания', callback_data=key.main_menu_callback.new(item_main_menu='add')),
        ],
        [
            InlineKeyboardButton(text='Показать все задания', callback_data=key.main_menu_callback.new(item_main_menu='show_all')),
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data=key.main_menu_callback.new(item_main_menu='back')),
        ],
    ]
)

all_mis_back_keyboard = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text='Назад', callback_data=key.main_back_callback.new(item_main_bac='bac'))
        ]
    ]
)

all_mis_back_keyboards = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text='Назад', callback_data=key.main_back_callbacks.new(item_main_backs='backs'))
        ]
    ]
)

delete_mission_keyboards = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text='Удалить', callback_data=key.delete_mission_callbacks.new(item_delete='del'))
        ]
    ]
)

user_mission_keyboards = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text='Выбрать', callback_data=key.user_mission_callbacks.new(item_user='user'))
        ]
    ]
)