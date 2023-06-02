from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def star_hotel() -> InlineKeyboardMarkup:
    star = '\U00002B50'
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='1' + star, callback_data='star_hotel:Одна ' + star + ':10'),
                InlineKeyboardButton(text='2' + star, callback_data='star_hotel:Две ' + star + ':20'),
                InlineKeyboardButton(text='3' + star, callback_data='star_hotel:Три ' + star + ':30'),
                InlineKeyboardButton(text='4' + star, callback_data='star_hotel:Четыре ' + star + ':40'),
                InlineKeyboardButton(text='5' + star, callback_data='star_hotel:Пять ' + star + ':50')
            ],
            [
                InlineKeyboardButton(
                    text='Не учитывать количество звезд отеля',
                    callback_data='star_hotel:Не учитывать:not'
                )],
            [
                InlineKeyboardButton(
                    text='Продолжить',
                    callback_data='star_hotel::end'
                )]
        ]
    )
    return kb
