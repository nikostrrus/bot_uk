import logging
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram import types
from loader import dp, bot, Dispatcher
from aiogram.dispatcher import FSMContext
import keybords.inline.choice_buttons as key
import keybords.inline.callback_datas as call_datas
from bd.sql import *
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import erp
from aiogram.dispatcher.filters.state import State, StatesGroup

class pictures(StatesGroup):
    photo = State()
    name = State()
    deportament = State()
    mission = State()

class datas(StatesGroup):
    text = State()
    name = State()
    deportament = State()
    mission = State()

class quests(StatesGroup):
    type = State()
    text = State()
    point = State()

class ed_point(StatesGroup):
    name = State()
    point = State()

# Кнопка старт, аутентифицирует человека, отправляет клавиатуру
@dp.message_handler(Command('start'))
async def show_menu(message: Message):
    if message.chat.id == -1001905922253:
        await message.answer('Это админка, тут можете менять задания(добавлять, удалять), так же регулировать очки участников', reply_markup=key.main_menu_keybord)
        return ''
    text = '''🤝 Приветствуем вас в геймификации по УД в МКЖД! 
    Выполняй задания и копи баллы! 
    Обменивайбаллы на призы!'''
    await message.answer(text, reply_markup=key.menu_keyboard)
    response = await erp.get_id_erp(message.from_user.id)
    await create_profile(message.from_user.id, response[0], response[1])

# Кнопка для Приветствия
@dp.callback_query_handler(call_datas.menu_callback.filter(item_menu='next'))
async def helo_key(call: CallbackQuery, callback_data: dict):
    logging.info(f'call = {callback_data}')
    emp = (await sel_emploes(call.message.chat.id))[0][0]
    await call.message.edit_text(f'''Ты в команде, {emp} 😎\nПриступим к выполнению заданий
💎1. За каждое еженедельное задание вы получаете 100 баллов. В сумме за выполнение всех активностей можно получить максимум 1200 баллов.

💎2. За передачу контактов вы получаете 300 баллов за старшего по дому и 150 баллов за инициативного жителя.

💎3. За сбор протокола вам начисляется 2000 баллов. ''', reply_markup=key.helo_keyboard)
    await call.answer()
    
# Кнопка для помощи
@dp.callback_query_handler(call_datas.helo_callback.filter(item_helo='helo'))
async def helo_key(call: CallbackQuery, callback_data: dict):
    logging.info(f'call = {callback_data}')
    await call.message.edit_text(f'''Перед тобой список миссий за которые ты получишь 💎
Выполняй их в любом порядке, а если захочешь посмотреть количество баллов, жми кнопку «Узнать мои баллы»''', reply_markup=key.mission_keyboard)
    await call.answer()

# Кнопка миссии

@dp.callback_query_handler(call_datas.mission_callback.filter(item_mission='miss'), state=None)
async def mission_key(call: CallbackQuery, callback_data: dict):
    logging.info(f'call = {callback_data}')
    missions = (await get_random_mission())
    await set_last_mission(call.message.chat.id, missions[0][0], call.message.message_id)
    if missions[0][1] == '2':
        await pictures.photo.set()
    else:
        await datas.text.set()
    await call.message.edit_text(str(missions[0][2]).replace('"',''), reply_markup=key.back_keyboard)
    await call.answer()

# Кнопка мои баллы
@dp.callback_query_handler(call_datas.mission_callback.filter(item_mission='my_bolls'))
async def my_bolls_key(call: CallbackQuery, callback_data: dict):
    logging.info(f'call = {callback_data}')
    bal = (await check_point(call.message.chat.id))[0][0]
    await call.message.edit_text(f'У тебя сейчас {bal} 💎', reply_markup=key.back_keyboard)
    await call.answer()

# Кнопка назад
@dp.callback_query_handler(call_datas.back_callback.filter(item_back='back'))
async def back_key(call: CallbackQuery, callback_data: dict):
    logging.info(f'call = {callback_data}')
    await call.message.edit_text(f'''Перед тобой список миссий за которые ты получишь 💎
Выполняй их в любом порядке, а если захочешь посмотреть количество баллов, жми кнопку «Мои баллы»''', reply_markup=key.mission_keyboard)
    await call.answer()

# Если вдруг пришла не фото
@dp.message_handler(lambda message: not message.photo, state=pictures.photo)
async def check_photo(message: types.Message):
    await message.reply('Отправь фото')

# обробатывает пришедгее фото
@dp.message_handler(content_types=['photo'], state=pictures.photo)
async def load_photo(message: types.Message, state: FSMContext):
    person = (await get_users(message.chat.id))
    mission = (await get_mission(person[0][2]))
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        data['name'] = person[0][0]
        data['deportament'] = person[0][1]
        data["mission"] = mission[0][2]
    async with state.proxy() as data:
        await bot.send_photo(-1001905922253, data['photo'], f'''Кто прислал: {data["name"]}
Из какого отдела: {data["deportament"]}
На какое задание: {data["mission"]}
Очков за задание: {mission[0][3]}''', reply_markup=key.point_back_keyboard)
    await state.finish()
    await up_point(message.chat.id, mission[0][3])
    await message.delete()
    await bot.delete_message(message.from_user.id, person[0][3])
    await message.answer(f'Класс! Засчитываем и получи свои {mission[0][3]} 💎', reply_markup=key.back_keyboard)

# Обработка текста и проверка на то что в нутри действительно лежит текст
@dp.message_handler(content_types=types.ContentType.ANY, state=datas.text)
async def load_text(message: types.Message, state: FSMContext):
    if message.content_type != 'text':
        await message.reply('Пожалуйста, отправляйте только текстовые сообщения')
    else:
        person = (await get_users(message.chat.id))
        mission = (await get_mission(person[0][2]))
        async with state.proxy() as data:
            data['text'] = message.text
            data['name'] = person[0][0]
            data['deportament'] = person[0][1]
            data['mission'] = mission[0][2]
        async with state.proxy() as data:
            await bot.send_message(-1001905922253, f'Кто прислал: {data["name"]}\nИз какого отдела: {data["deportament"]}\nНа какое задание: {data["mission"]}\nНаписал: {message.text}\nОчков за задание: {mission[0][3]}', reply_markup=key.point_back_keyboard)
        await state.finish()
        await up_point(message.chat.id, mission[0][3])
        await message.delete()
        await bot.delete_message(message.from_user.id, person[0][3])
        await message.answer(f'Класс! Засчитываем и получи свои {mission[0][3]} 💎', reply_markup=key.back_keyboard)

# Кнопка назад
@dp.callback_query_handler(call_datas.main_back_callback.filter(item_main_bac='bac'), state=quests)
async def back_key(call: CallbackQuery, callback_data: dict, state: FSMContext):
    logging.info(f'call = {callback_data}')
    await call.message.edit_text('Тут вы можете удалить и добавить новое задание', reply_markup=key.all_mis_keyboard)
    await call.answer()
    await state.finish()

# Кнопка назад
@dp.callback_query_handler(call_datas.main_back_callbacks.filter(item_main_backs='backs'), state=ed_point)
async def back_key(call: CallbackQuery, callback_data: dict, state: FSMContext):
    logging.info(f'call = {callback_data}')
    await call.message.edit_text(f'Перед тобой список миссий за которые ты получишь 💎\nВыполняй их в любом порядке, а если захочешь посмотреть количество баллов, жми кнопку «Мои баллы»', reply_markup=key.mission_keyboard)
    await call.answer()
    await state.finish()

# Выход из машины состояния
@dp.callback_query_handler(call_datas.back_callback.filter(item_back='back'), state='*')
async def back_key(call: CallbackQuery, callback_data: dict, state: FSMContext):
    logging.info(f'call = {callback_data}')
    await call.message.edit_text(f'Перед тобой список миссий за которые ты получишь 💎\nВыполняй их в любом порядке, а если захочешь посмотреть количество баллов, жми кнопку «Мои баллы»', reply_markup=key.mission_keyboard)
    await call.answer()
    await state.finish()

# Засчитываем очки
@dp.callback_query_handler(call_datas.point_back_callback.filter(item_point_back='count'))
async def counts_point(call: CallbackQuery, callback_data: dict):
    logging.info(f'call = {callback_data}')
    if call.message.caption:
        mess = call.message.caption
        await call.message.edit_caption(mess)
    else:
        mess = call.message.text
        await call.message.edit_text(mess)
    await bot.answer_callback_query(callback_query_id=call.id, text='Балы засчитаны', show_alert=True)
    await call.answer()

# Убираем очки
@dp.callback_query_handler(call_datas.point_back_callback.filter(item_point_back='uncount'))
async def counts_point(call: CallbackQuery, callback_data: dict):
    logging.info(f'call = {callback_data}')
    if call.message.caption:
        mess = call.message.caption
        await call.message.edit_caption(mess)
    else:
        mess = call.message.text
        await call.message.edit_text(mess)
    await down_point(mess.split('\n')[0].split('Кто прислал: ')[1], mess.split('\n')[-1][-1])
    await bot.answer_callback_query(callback_query_id=call.id, text='Балы не засчитаны', show_alert=True)
    await call.answer()

# Смотрим все задания
@dp.callback_query_handler(call_datas.main_menu_callback.filter(item_main_menu='all_mission'))
async def under_menu(call: CallbackQuery, callback_data: dict):
    logging.info(f'call = {callback_data}')
    await call.message.edit_text('Тут вы можете удалить и добавить новое задание', reply_markup=key.all_mis_keyboard)
    await call.answer()

# Добавить задания
@dp.callback_query_handler(call_datas.main_menu_callback.filter(item_main_menu='add'))
async def under_menu(call: CallbackQuery, callback_data: dict, state: FSMContext):
    logging.info(f'call = {callback_data}')
    await call.message.edit_text('''Тут добавляется новое задание нужно вести 3 пункта необходимых для вноса задания в базу:
1. Выбрать что это будет фото или текст и написать цифрой, текст - 1, фото - 2
2. Текст миссии важно не использовать " кавычки
3. Необходимо написать количество очков за задание
4. Кнопка назад создана для отменения отправки задания в базу, отменяет от слова совсем\n
Удачи))''', reply_markup=key.all_mis_back_keyboard)
    await quests.type.set()

# Отлавливаем не правильную передачу типа миссии 
@dp.message_handler(lambda message: not message.text.isdigit() and 0 < int(message.text) < 3, state=quests.type)
async def check_photo(message: Message, state: FSMContext):
    await message.reply('Отправь верное число')

# Отлавливаем правильную передачу числа
@dp.message_handler(state=quests.type)
async def load_type(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['type'] = message.text
    await message.answer('Хорошо, отправьте текст задания')
    await quests.next()

# Отлавливаем текст мессии
@dp.message_handler(state=quests.text)
async def load_text(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
    await message.answer('Хорошо, ведите зачисляемые очки числом следующим сообщением')
    await quests.next()

# Отлавливаем не правильную передачу очков за миссию
@dp.message_handler(lambda message: not message.text.isdigit(), state=quests.point)
async def check_photo(message: Message, state: FSMContext):
    await message.reply('Отправь число')

# Отлавливаем текст мессии
@dp.message_handler(state=quests.point)
async def load_point(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['point'] = int(message.text)
    async with state.proxy() as data:
        await add_mission(data['type'], data['text'], int(data['point']))
    await message.answer('Мисссия была добавлена')
    await state.finish()

# Показать все миссии
@dp.callback_query_handler(call_datas.main_menu_callback.filter(item_main_menu='show_all'))
async def all_mission(call: CallbackQuery, callback_data: dict):
    logging.info(f'call = {callback_data}')
    all_mis = (await get_all_mission())
    for item in all_mis:
        await bot.send_message(-1001905922253, f'{item[0]}', reply_markup=key.delete_mission_keyboards)
    await call.answer()

# Кнопка назад
@dp.callback_query_handler(call_datas.main_menu_callback.filter(item_main_menu='back'))
async def back_key(call: CallbackQuery, callback_data: dict):
    logging.info(f'call = {callback_data}')
    await call.message.edit_text('Это админка, тут вы можете менять задания(добавлять, удалять), так же изменять очки участников', reply_markup=key.main_menu_keybord)
    await call.answer()

# топ 10 участников
@dp.callback_query_handler(call_datas.main_menu_callback.filter(item_main_menu='top_ten'))
async def top_ten(call: CallbackQuery, callback_data: dict):
    logging.info(f'call = {callback_data}')
    await unloading_from_database()
    await bot.send_document(-1001905922253, open('result.xlsx', 'rb'))
    await call.answer()

@dp.callback_query_handler(call_datas.main_menu_callback.filter(item_main_menu='phone'))
async def phone(call: CallbackQuery, callback_data: dict):
    logging.info(f'call = {callback_data}')
    await unloading_from_database_answer()
    await bot.send_document(-1001905922253, open('nomera.xlsx', 'rb'))
    await call.answer()    

# Изменяем количество очков
@dp.callback_query_handler(call_datas.main_menu_callback.filter(item_main_menu='write_point'))
async def write_point(call: CallbackQuery, callback_data: dict):
    logging.info(f'call{callback_data}')
    await call.message.edit_text('''Тут необходимо:
1сообщение от вас: Полное ФИО участника, у которого необходимо изменить колличество очков 
2сообщение от вас: Ввести число на которое изменятся его текущие очки''', reply_markup=key.all_mis_back_keyboards)
    await ed_point.name.set()
    await call.answer()
    
# Отлавливаем имя и проверяем на наличие его в бд
@dp.message_handler(state=ed_point.name)
async def load_name_for_edit_point(message: Message, state: FSMContext):
    if (await search_employs(message.text)):
        async with state.proxy() as data:
            data['name'] = message.text
        await ed_point.next()
        await bot.send_message(-1001905922253, f'Отлично теперь пришли количество очков')
    else:
        await message.answer('Вы велли не правильное имя сотрудника, повторите ввод')

@dp.message_handler(lambda message: not message.text.isdigit(), state=ed_point.point)
async def check_photo(message: Message, state: FSMContext):
    await message.reply('Отправь число очков')

# Отлавливаем текст мессии
@dp.message_handler(state=ed_point.point)
async def load_point_for_edit_point(message: Message, state: FSMContext):
    async with state.proxy() as data:
        await edit_point(data['name'], message.text)
        await bot.send_message(-1001905922253, f'{data["name"]} было установлино количество очков {message.text}')
    await state.finish()

# Удаление миссий
@dp.callback_query_handler(call_datas.delete_mission_callbacks.filter(item_delete='del'))
async def del_mis(call: CallbackQuery, callback_data: dict):
    logging.info(f'call{callback_data}')
    await del_mission(call.message.text)
    await call.message.edit_text(f'Задание удалено: {call.message.text}')
    await call.answer()


