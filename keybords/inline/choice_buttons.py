from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import keybords.inline.callback_datas as key

menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text='Продолжить? Любые слова))', callback_data=key.menu_callback.new(item_menu='next')),
        ],
    ]
)

helo_keyboard = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text='Миссии', callback_data=key.helo_callback.new(item_helo='helo')),
        ],
    ]
)

mission_keyboard = InlineKeyboardMarkup(
    inline_keyboard = [
        [
            InlineKeyboardButton(text='Миссия', callback_data=key.mission_callback.new(item_mission='miss')),
        ],
        [
            InlineKeyboardButton(text='Мои баллы', callback_data=key.mission_callback.new(item_mission='my_bolls')),
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