from aiogram import types


def button_start():
    kb = [
        [types.InlineKeyboardButton(text="👾 POC", callback_data="req_poc"),
         types.InlineKeyboardButton(text="👾 EXPLOIT", callback_data="req_exploit")],
        [
            types.InlineKeyboardButton(text="📕 History", callback_data="history"),
            types.InlineKeyboardButton(text="🔍 Scan", callback_data="scan")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard
