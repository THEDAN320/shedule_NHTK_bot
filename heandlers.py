from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional
import parser

router = Router() 

#создаем свой callback для архива
class MyCallback_archive(CallbackData, prefix="my"):
    href: Optional[str]
    
#создаем свой callback
class MyCallback_group(CallbackData, prefix="my"):
    href: Optional[int]
    archive_href: Optional[str]

# Хэндлер на /start
@router.message(Command("start"))
async def start(message: Message):
    await message.answer(f"Привет, *{message.from_user.first_name}*\!", parse_mode="MarkdownV2")
    await message.answer("Это телеграмм бот для просмотра расписания Новосибирского химико-технологического колледжа И. М. Менделеева")
    await choose_archive(message)
    
#выбор архива
async def choose_archive(message: Message):
    builder = InlineKeyboardBuilder()
    all_archives = parser.get_archives()
    
    if all_archives == "TimeOutError":  #09.07.19.html#заголовок:/.архив/29.05.2023—04.06.2023
        await message.answer("Не удается подключится к сайту колледжа, попробуйте позже!")
    else:
        for archive in all_archives:
            builder.add(types.InlineKeyboardButton(
                text=archive.text,
                callback_data=MyCallback_archive(href=archive.get("href")).pack()
            ))
            
        await message.answer(
            "Выберите архив:",
            reply_markup=builder.as_markup()
        )

#хендлер для архива
@router.callback_query(MyCallback_archive.filter())
async def my_callback_archive(query, callback_data: MyCallback_archive):
    await query.answer()
    await choose_group(query, callback_data.href)
    
#выбор группы
async def choose_group(message, choosing_archive: str):
    builder = InlineKeyboardBuilder()
    all_groups = parser.get_groups(choosing_archive)
    
    if all_groups == "TimeOutError":
        await message.message.answer("Не удается подключится к сайту колледжа, попробуйте позже!")
    else:
        count: int = 0
        for group in all_groups:
            builder.add(types.InlineKeyboardButton(
                text=group.text,
                callback_data=MyCallback_group(href=count,archive_href=choosing_archive).pack()
            ))
            count += 1
    
        builder.add(types.InlineKeyboardButton(
                text="Назад",
                callback_data=MyCallback_group(href=-1).pack()
            ))
    
        await message.message.answer(
            "Выберите группу:",
            reply_markup=builder.as_markup()
        )
    
#хендлер для группы
@router.callback_query(MyCallback_group.filter())
async def my_callback_group(query, callback_data: MyCallback_group):
    if callback_data.href == -1:
        await choose_archive()
    else:
        group = parser.get_groups(callback_data.archive_href)[callback_data.href].get("href")
        await output_shedule(query, callback_data.archive_href, group)
        
    await query.answer()
    
#вывод расписания
async def output_shedule(message, archive: str, group: str):
    current_shedule = parser.get_shedule(archive, group)
    
    if current_shedule == "TimeOutError":
        await message.message.answer("Не удается подключится к сайту колледжа, попробуйте позже!")
    else:
        await message.message.answer(current_shedule, parse_mode="HTML")
        choose_archive(message)
