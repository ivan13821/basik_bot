from aiogram.fsm.state import StatesGroup, State
from aiogram import F, Router, Bot, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from datetime import datetime

from config import get_tg_api_token, get_feedback_chat_id



#database
from game_for_economists.postgres.psql_main import Database

db = Database()


#импорт клавиатуры
from other.other_keyboard import OtherKeyboardFactory

router = Router()

bot = Bot(token=get_tg_api_token())



class OtherStates(StatesGroup):

    send_message_from_created = State()


@router.message(StateFilter(None), F.text == '/start')
async def start_game(message: types.Message):
    
    """ Пользователоь первый раз заходит в игру """

    await message.answer("Добро пожаловать в бота для развития предпринимательского дела", reply_markup=OtherKeyboardFactory.menu())








@router.message(StateFilter(None), F.text == 'Еще')
async def start_game(message: types.Message):
    
    """ Дополнительные возможности """

    await message.answer("Выберете какое действие вам нужно: ", reply_markup=OtherKeyboardFactory.other_func())











#вкладка "Еще" --------------------------------------------------------------------------------------

messages_id = {}


@router.callback_query(StateFilter(None), F.data == "send_from_created")
async def start_game(call: types.CallbackQuery, state: FSMContext):

    """ Отправка сообщения разработчику """

    await call.answer("Напишите ваше сообщение")

    messages_id[call.message.chat.id] = call.message.message_id

    await state.set_state(OtherStates.send_message_from_created)









@router.message(OtherStates.send_message_from_created)
async def start_game(message: types.Message, state: FSMContext):

    """ Получение сообщения и отправка разработчику """

    if message.text == "Назад":

        await message.answer("Вы вышли в основное меню", reply_markup=OtherKeyboardFactory.menu())
        state.clear()
    
    else:

        markup = OtherKeyboardFactory.menu()

        feedback_chat_id = get_feedback_chat_id()

        await bot.delete_message(message.chat.id, messages_id[message.chat.id])

        del messages_id[message.chat.id]

        await bot.send_message(feedback_chat_id, "Сообщение от @" + str(message.chat.username)
                            + " (ид чата: " + str(message.chat.id) + ")")
        
        await bot.forward_message(feedback_chat_id, message.chat.id, message.message_id)

        await message.answer("Ваше сообщение успешно отправленно", reply_markup=markup,
                            disable_notification=True)
        await state.clear()
    





@router.callback_query(StateFilter(None), F.data == "back")
async def start_game(call: types.CallbackQuery, state: FSMContext):

    """ Пользователь передумал что-либо делать во вкладке Еще (нажал Назад)"""

    await state.clear()

    await call.answer("Вы вышли в основное меню", reply_markup=OtherKeyboardFactory.menu())

    await bot.delete_message(call.message.chat.id, call.message.message_id)


















#Помощь --------------------------------------------------------------------------------------------------------------


@router.message(F.text == "/help")
async def help_users(message: types.Message, state: FSMContext):

    """ Пользователь выбирает в чем именно ему нужна помощь """

    await message.answer("Выберете в чем вам нужна помощь:", reply_markup=OtherKeyboardFactory.help())










@router.callback_query(F.data == "help_bye_cold_swep")
async def help_with_bye_cold_swep(call: types.CallbackQuery, state: FSMContext):

    """ Помощь пользователю с покупкой продажей (на биржу или другому пользователю) или обменом ресурсов"""

    await bot.delete_message(call.message.chat.id, call.message.message_id)

    await bot.send_message(call.message.chat.id, "Чтобы совершить действие связанное с ресурсами (продажа, покупка, обмен) вам нужно ввести:\n"
                        "1 2 3 4 5\n"
                        "1 - выбрать действие (купить, продать обменять)\n"
                        "2 - тот с кем вы хотете торовать (биржа или пользователь)\n"
                        "3 - название ресурса (здание, рабочие...)\n"
                        "4 - количество ресурсов\n"
                        "5 - если вы торгуете с игроком ввести цену ресурсов")









@router.callback_query(F.data == "help_with_credit")
async def help_with_credit(call: types.CallbackQuery, state: FSMContext):

    """ Помощь пользователю с кредитом """


    await bot.send_message(call.message.chat.id, "Кредит выдается в самом начале игры и составляет 4000 д.ед.\n"
                      "Кредит выданый в первый год выдается под 25% годовых, в последующие года под 50%\n"
                      "Не забывайте выплачивать кредит, а то проиграете ;)")

    await bot.delete_message(call.message.chat.id, call.message.message_id)











@router.callback_query(F.data == "help_with_level")
async def help_with_level(call: types.CallbackQuery, state: FSMContext):

    """ Помощь пользователю с повышением уровня поизводства """


    await bot.send_message(call.message.chat.id, "Для повышения прозводства нужно выполнить одно из двух условий:\n"
                      "1 - купить нужные для этого ресурсы (посмотреть -> Справка/Ресурсы для повышения производства)\n"
                      "2 - накопить достаточное количество денег, для повышения производства, тогда ресурсы будут купленны автоматически по ценам на бирже и отданы на повышение производства")

    await bot.delete_message(call.message.chat.id, call.message.message_id)

























# Правила игры ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@router.message(F.text == "/rules")
async def rules(message: types.Message, state: FSMContext):

    """ Рассказывает о правилах игры в несколько уровней """

    # первый уровень - Рассказываем о главной задаче игры и условиях победы.
    # даем выбор какие правила он хочет узнать глубже: (кредиты, торговля, объединения, уровень производства)

    await message.answer("Главная цель - накопить как можно больше денег)\nУсловия победы в этой игре простые у кого после вычитания его кредитов останется больше денег тот и победил", reply_markup=OtherKeyboardFactory.rules())








@router.callback_query(F.data == "rules_bye_cold_swep")
async def ruleswith_bye_cold_swep(call: types.CallbackQuery, state: FSMContext):

    """ Правила торговли """

    await bot.delete_message(call.message.chat.id, call.message.message_id)

    await bot.send_message(call.message.chat.id, "Торговля может осуществляться между пользователями или между пользователем и биржей\nПодробнее /help")









@router.callback_query(F.data == "rules_with_credit")
async def ruleswith_credit(call: types.CallbackQuery, state: FSMContext):

    """ Правила кредита """


    await bot.send_message(call.message.chat.id, "Кредит дается в самом начале игры 4000 ден.ед. Кредиты выданые в 1 год выдается под 25% годовых, в последующие под 50%.\nВы можете брать в кредит суммы до 1 000 000 ден.ед."
                           "Также не стоит забывать что ваш кредит с каждым годом становиться больше.")

    await bot.delete_message(call.message.chat.id, call.message.message_id)











@router.callback_query(F.data == "rules_with_level")
async def ruleswith_level(call: types.CallbackQuery, state: FSMContext):

    """ Правила повышения уровня поизводства """


    await bot.send_message(call.message.chat.id, "Для повышения прозводства нужно выполнить одно из двух условий:\n"
                      "1 - купить нужные для этого ресурсы (посмотреть -> Справка/Ресурсы для повышения производства)\n"
                      "2 - накопить достаточное количество денег, для повышения производства, тогда ресурсы будут купленны автоматически по ценам на бирже и отданы на повышение производства")

    await bot.delete_message(call.message.chat.id, call.message.message_id)











@router.callback_query(F.data == "rules_group")
async def rules_group(call: types.CallbackQuery, state: FSMContext):

    """ Правила объединений """


    await bot.send_message(call.message.chat.id, "Пользователи могут объединяться в группы, тогда их ресурсы добавятся к ресурсам группы, и каждый член группы будет иметь доступ к общим ресурсам, но никто из участников группы не будет иметь личных ресурсов.\n"
                           "Так же если полльзователь выходит из группы он забирает в личное пользование часть ресурсов группы в соотношение к количествам участников например:\n"
                           "В группе было 5 человек, из них 1 вышел, он получает 1/5 ресурсов т.е 20% от всех ресурсов")

    await bot.delete_message(call.message.chat.id, call.message.message_id)





# Подсказки ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



@router.message(F.text == "/clue")
async def rules(message: types.Message, state: FSMContext):

    """ Отправляет пользователю подсказки """

    clues = [
        "Если в основном меню игры ввести <Продать все> то все ваши ресурсы, или ресурсы вашей группы будут проданы",
        "Если вы хотите повысить производство, не обязательно покупать все ресурсы бот сделает это за вас, если у вас достаточно денег"
    ]

    await message.answer(text = "Вот интересные команды для вас)")
    for clue in clues:

        await message.answer(clue)





# лучшие игроки -----------------------------------------------------------------------------------------------------------------------------

@router.message(F.text == "/best_players")
async def rules(message: types.Message, state: FSMContext):

    """ Выводит список 5 лучших игроков"""

    sel = db.chow_five_winners()

    sel.reverse()

    result = '🏆 Лучшие результаты на конец 5 года 🏆\n'

    for i in range(len(sel)):

        chat_id, when, name, check = sel[i]

        when = when.strftime('%d.%m.%Y')

        check = int(check)

        check = f"{check:,}"

        if i == 0: result += f"🥇 @{name} {check} ден.ед   ({when})\n"
        elif i == 1: result += f"🥈 @{name}  {check} ден.ед   ({when})\n"
        elif i == 2: result += f"🥉 @{name} {check} ден.ед   ({when})\n"
        else: result += f"@{name} {check} ден.ед   ({when})\n"
        
    
    await bot.send_message(message.chat.id, result)

    
