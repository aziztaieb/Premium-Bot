from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database import get_db_connection
from utils import push_menu
import requests
from currencyapi import buy_self_text
from texts import (
    BUY_PREMIUM_TEXT,
    BUY_FOR_SELF_TEXT,
    BUY_FOR_FRIENDS_TEXT,
    BUY_SUCCESS_TEXT,
    LOREM,
    FAQ_TEXT,
    MY_PURCHASES_TEXT,
    GO_BACK_TEXT,
    ONE_M_SUB_TEXT,
    THREE_M_SUB_TEXT,
)
from config import ADMIN_CHAT_ID


def push_menu(context: ContextTypes.DEFAULT_TYPE, menu_function):
    if "menu_stack" not in context.user_data:
        context.user_data["menu_stack"] = []
    context.user_data["menu_stack"].append(menu_function)


async def go_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "menu_stack" in context.user_data and context.user_data["menu_stack"]:
        menu_function = context.user_data["menu_stack"].pop()
        await menu_function(update, context)
    else:
        await start(update, context)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    push_menu(context, start)

    start_keys = [
        [
            KeyboardButton(text=BUY_PREMIUM_TEXT),
            KeyboardButton(text=MY_PURCHASES_TEXT),
        ],
        [
            KeyboardButton(text=FAQ_TEXT),
        ],
    ]
    markup = ReplyKeyboardMarkup(start_keys, resize_keyboard=True)

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="خوش آمدید", reply_markup=markup
    )


async def buy_sub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    push_menu(context, start)

    buy_keys = [
        [
            KeyboardButton(text=BUY_FOR_SELF_TEXT),
        ],
        [
            KeyboardButton(text=BUY_FOR_FRIENDS_TEXT),
        ],
        [
            KeyboardButton(text=GO_BACK_TEXT),
        ],
    ]
    markup = ReplyKeyboardMarkup(buy_keys, resize_keyboard=True)

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="انتخاب کنید :", reply_markup=markup
    )


async def buy_for_self(update: Update, context: ContextTypes.DEFAULT_TYPE):
    push_menu(context, buy_sub)
    user_data = update.message.from_user

    invoice_title = ONE_M_SUB_TEXT
    invoice_description = f"@{user_data['username']} اشتراک یک ماهه برای نام کاربری"
    invoice_price = buy_self_text  # Replace with your price

    # Format the invoice text in a clear and concise way
    invoice_text = f"""**Invoice**

Title: {invoice_title}
Description: {invoice_description}
Price: {invoice_price} ت

**Please note:** This is a text-based representation of the invoice. 
For official documentation, please refer to your payment processor's website.

Would you like to proceed with the purchase?"""

    buy_self_keys = [
        # [
        #     KeyboardButton(text=buy_self_text),
        # ],
        [
            KeyboardButton(text=GO_BACK_TEXT),
        ],
    ]
    markup = ReplyKeyboardMarkup(buy_self_keys, resize_keyboard=True)

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=invoice_text, reply_markup=markup
    )


async def buy_success(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text
    photo = update.message.photo

    if photo:

        # Handle photo message
        admin_chat_id = ADMIN_CHAT_ID  # Replace with the actual chat ID obtained

        try:
            user_data = update.message.from_user
            user_id = user_data["id"]
            user_username = user_data["username"]
            user_sub = text

            conn = get_db_connection()
            cur = conn.cursor()

            if user_username:
                cur.execute(
                    "INSERT INTO users (id, username, sub) VALUES (%s, %s, %s)",
                    (user_id, user_username, user_sub),
                )
                conn.commit()
            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="لطفا برای حساب خود یوزرنیم انتخاب کنید",
                )

            cur.close()
            conn.close()

            # Get the file ID of the largest photo (usually the last one in the list)
            file_id = photo[-1].file_id

            # Send the photo to the admin
            await context.bot.send_photo(chat_id=admin_chat_id, photo=file_id)

        except Exception as e:
            print(f"Error sending photo to admin: {e}")
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="An error occurred while sending the photo to the admin.",
            )


async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    push_menu(context, start)

    faq_keys = [
        [
            KeyboardButton(text=GO_BACK_TEXT),
        ],
    ]
    markup = ReplyKeyboardMarkup(faq_keys, resize_keyboard=True)

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=LOREM, reply_markup=markup
    )


async def my_subs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    push_menu(context, start)

    user_data = update.message.from_user
    user_id = user_data["id"]

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT username, sub, created FROM users WHERE id = %s", (str(user_id),)
    )
    user_data = cur.fetchall()
    cur.close()
    conn.close()

    if user_data:
        subs_list = "\n".join(
            [
                f"- @{username}: {sub} Premium (Created on: {created.strftime('%Y-%m-%d %H:%M:%S')})"
                for username, sub, created in user_data
            ]
        )
        response_message = f"اشتراک‌های شما:\n{subs_list}"
    else:
        response_message = "شما اشتراکی ندارید."

    my_subs_keys = [
        [
            KeyboardButton(text=GO_BACK_TEXT),
        ],
    ]
    markup = ReplyKeyboardMarkup(my_subs_keys, resize_keyboard=True)

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=response_message, reply_markup=markup
    )
