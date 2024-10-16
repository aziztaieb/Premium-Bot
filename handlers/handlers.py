import json
from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove
)
import re
from telegram.ext import ContextTypes
from utilities.utils import (
    push_menu,
    is_valid_username,
    gregorian_to_solar,
    get_total_users,
    get_daily_new_users,
    get_weekly_new_users,
    format_with_commas,
    get_user_purchased,
    sanitize_username,
    get_sell_stats,
    solar_to_gregorian,
    format_solar_date,
    round_up_to_thousands,
    generate_inline_keyboard,
    get_available_months,
    get_solar_date,
    extract_number
)
from currencyapi import (
    three_m_price,
    six_m_price,
    twelve_m_price,
    last_price,
    fee_amount,
    profit_amount,
    fifty_price,
    seventy_five_price,
    hundred_price,
    # stars_fee_amount,
    # stars_profit_amount
)
from utilities.texts import (
    BUY_PREMIUM_TEXT,
    BUY_FOR_SELF_TEXT,
    FAQ_TEXT,
    FAQ_FULL_TEXT,
    MY_PURCHASES_TEXT,
    GO_BACK_TEXT,
    THREE_M_CHOICE,
    SIX_M_CHOICE,
    TWELVE_M_CHOICE,
    BUY_STARS_TEXT,
    FIFTY_STARS_CHOICE,
    SEVENTY_FIVE_STARS_CHOICE,
    HUNDRED_STARS_CHOICE,
    CUSTOM_AMOUNT,
    ENTER_CUSTOM_AMOUNT,
    STARS_HELP_TEXT,
    # THREE_M_SUB_TEXT,
    # SIX_M_SUB_TEXT,
    # TWELVE_M_SUB_TEXT,
    PENDING_APPROVAL_TEXT,
    APPROVED_TEXT,
    CANCELLED_TEXT,
    NOT_PHOTO_ERROR,
    REVIEWING_TEXT,
    CHOOSE_USERNAME_ERROR_TEXT,
    SUB_HELP_TEXT,
    WELCOME_TEXT,
    # CHOOSE_OPTION_TEXT,
    INVALID_OPTION_TEXT,
    FAILED_UPDATE_STATUS_TEXT,
    USERNAME_LIMITS_TEXT,
    STATUS_UPDATED_TEXT,
    ADMIN_PANEL_TEXT,
    cancelled_payment_text,
    cancelled_username_text,
    approved_payment,
    approved,
    sale_variables_text,
    sale_stats_text,
    users_stat_text,
    invoice_text,
    user_invoice_text,
    choose_premium_sub_option,
    choose_stars_sub_option,
    three_m_text,
    six_m_text,
    twelve_m_text,
    format_message_text,
    fifty_stars_text,
    seventy_five_stars_text,
    hundred_stars_text,
    USERS_STATS,
    SELL_STATS,
    PHOTO_SENT_SUCCESSFULLY,
    PAY_APPROVED_TEXT,
    SELL_INFO,
    NO_SUB_TEXT,
    REDIS_ERROR,
    ADMIN_LINK,
    ABOUT_US_BTN_TEXT,
    ABOUT_US_TEXT,
    CHANELL_TEXT
)
from config import ADMIN_CHAT_ID, PROFIT_AMOUNT, THREE_M_USD_PRICE, NINE_M_USD_PRICE, TWELVE_M_USD_PRICE, FEE_AMOUNT, ADMIN_USERNAME, CHANELL_ID, STARS_PROFIT
import uuid
from db.dbconn import conn, cur
from redis_conn.redis_connection import redis_conn
from redis_conn.states import set_user_state, get_user_state, BotState
from redis_conn.session import set_session, get_session, delete_session
from datetime import datetime
import jdatetime


three_m_invoice_price = float(three_m_price) + \
    float(profit_amount) + float(fee_amount)
six_m_invoice_price = float(six_m_price) + \
    float(profit_amount) + float(fee_amount)
twelve_m_invoice_price = float(twelve_m_price) + \
    float(profit_amount) + float(fee_amount)

fifty_stars_invoice_price = (50 * 0.015) * \
    (float(last_price) + float(STARS_PROFIT))
seventy_five_stars_invoice_price = (
    75 * 0.015) * (float(last_price) + float(STARS_PROFIT))
hundred_stars_invoice_price = (100 * 0.015) * \
    (float(last_price) + float(STARS_PROFIT))


def push_menu(user_id: str, menu_function):
    redis_conn.rpush(f"menu_stack:{user_id}", menu_function.__name__)


async def go_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    menu_stack_key = f"menu_stack:{user_id}"

    if redis_conn.llen(menu_stack_key) > 0:
        menu_function_name = redis_conn.rpop(menu_stack_key)
        if menu_function_name:
            menu_function = globals().get(menu_function_name)
            if menu_function:
                await menu_function(update, context)
    else:
        await start(update, context)


async def add_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = update.effective_user
    user_id = str(user_data.id)  # Cast to string
    user_username = user_data.username
    user_first_name = user_data.first_name
    user_last_name = user_data.last_name

    # Check if the user already exists
    cur.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    try:
        # Execute some SQL commands
        cur.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        existing_user = cur.fetchone()

        # Commit the transaction if no errors
        conn.commit()

    except Exception as e:
        # Rollback the transaction if an error occurs
        conn.rollback()
        print(f"Error executing query: {e}")
    if not existing_user:
        cur.execute(
            "INSERT INTO users (id, username, first_name, last_name) VALUES (?, ?,?,?)",
            (user_id, user_username, user_first_name, user_last_name),
        )
        conn.commit()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    push_menu(user_id, start)
    set_user_state(user_id, BotState.START)

    start_keys = [
        [
            KeyboardButton(text=BUY_PREMIUM_TEXT),
            KeyboardButton(text=BUY_STARS_TEXT),
        ],
        [
            KeyboardButton(text=MY_PURCHASES_TEXT),
        ],
        [
            KeyboardButton(text=ABOUT_US_BTN_TEXT),
            KeyboardButton(text=FAQ_TEXT),
        ]
    ]

    if user_id == ADMIN_CHAT_ID:
        start_keys = [[KeyboardButton(text=ADMIN_PANEL_TEXT)]]

    markup = ReplyKeyboardMarkup(start_keys, resize_keyboard=True)

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=WELCOME_TEXT, reply_markup=markup
    )


async def buy_sub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    buy_keys = [
        [KeyboardButton(text=BUY_FOR_SELF_TEXT)],
    ]
    markup = ReplyKeyboardMarkup(
        buy_keys, resize_keyboard=True, one_time_keyboard=True)

    if get_user_state(user_id) == BotState.BUY_PREMIUM:
        message = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=SUB_HELP_TEXT,
            reply_markup=markup,
        )
    elif get_user_state(user_id) == BotState.BUY_STARS:
        message = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=STARS_HELP_TEXT,
            reply_markup=markup,
        )

    set_session(user_id, "awaiting_username", "true")
    set_session(user_id, "last_message", message.message_id)


async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text
    user_data = update.effective_user
    user_state = get_user_state(user_id)
    last_message_id = get_session(user_id, "last_message")
    if user_state == BotState.BUY_PREMIUM:

        if get_session(user_id, "awaiting_username") == "true":
            keyboard = [
                [
                    InlineKeyboardButton(
                        text=GO_BACK_TEXT, callback_data="go_back_cancelled"
                    ),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if text == BUY_FOR_SELF_TEXT:
                if not user_data.username:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=CHOOSE_USERNAME_ERROR_TEXT,
                    )
                else:
                    username = user_data.username
                    set_session(user_id, "entered_username", username)
                    set_session(user_id, "awaiting_username", "false")
                    set_user_state(user_id, BotState.PREMIUM_SUBS_LIST)

                    # Remove the keyboard
                    # await context.bot.edit_message_text(
                    #     chat_id=update.effective_chat.id,
                    #     message_id=float(last_message_id),
                    #     text="sg",
                    #     reply_markup=ReplyKeyboardRemove()
                    # )
                    await premium_subs_list(update, context)
            else:
                if is_valid_username(sanitize_username(text)):
                    text = sanitize_username(text)
                    set_session(user_id, "entered_username", text)
                    set_session(user_id, "awaiting_username", "false")
                    set_user_state(user_id, BotState.PREMIUM_SUBS_LIST)

                    # Remove the keyboard

                    # Proceed to the subscription list
                    await premium_subs_list(update, context)
                else:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=USERNAME_LIMITS_TEXT,
                        reply_markup=reply_markup
                    )
        else:
            # Handle other text messages here
            pass
    elif user_state == BotState.BUY_STARS:
        if get_session(user_id, "awaiting_username") == "true":
            keyboard = [
                [
                    InlineKeyboardButton(
                        text=GO_BACK_TEXT, callback_data="go_back_cancelled"
                    ),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if text == BUY_FOR_SELF_TEXT:
                if not user_data.username:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=CHOOSE_USERNAME_ERROR_TEXT,
                    )
                else:
                    username = user_data.username
                    set_session(user_id, "entered_username", username)
                    set_session(user_id, "awaiting_username", "false")
                    set_user_state(user_id, BotState.STARS_SUBS_LIST)

                    # Remove the keyboard
                    # await context.bot.edit_message_text(
                    #     chat_id=update.effective_chat.id,
                    #     message_id=float(last_message_id),
                    #     text="sg",
                    #     reply_markup=ReplyKeyboardRemove()
                    # )
                    await stars_subs_list(update, context)
            else:
                if is_valid_username(sanitize_username(text)):
                    text = sanitize_username(text)
                    set_session(user_id, "entered_username", text)
                    set_session(user_id, "awaiting_username", "false")
                    set_user_state(user_id, BotState.STARS_SUBS_LIST)

                    # Remove the keyboard

                    # Proceed to the subscription list
                    await stars_subs_list(update, context)
                else:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=USERNAME_LIMITS_TEXT,
                        reply_markup=reply_markup
                    )
        else:
            # Handle other text messages here
            pass
    else:
        await start(update, context)


async def premium_subs_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    push_menu(user_id, buy_sub)
    user_state = get_user_state(user_id)
    username = get_session(user_id, "entered_username")
    last_message_id = get_session(user_id, "last_message")

    premium_subs_list_keys = [

        [
            InlineKeyboardButton(text=three_m_text(three_m_invoice_price),
                                 callback_data="sub:3m"),
        ],
        [
            InlineKeyboardButton(text=six_m_text(
                six_m_invoice_price), callback_data="sub:6m"),
        ],
        [
            InlineKeyboardButton(text=twelve_m_text(twelve_m_invoice_price),
                                 callback_data="sub:12m"),
        ],
        [
            InlineKeyboardButton(
                text=GO_BACK_TEXT, callback_data="go_back_cancelled"
            ),
            InlineKeyboardButton(text="👤 Contact Support",
                                 url=f"https://t.me/{ADMIN_USERNAME}"),

        ],
    ]
    markup = InlineKeyboardMarkup(premium_subs_list_keys)
    msg = await context.bot.send_message(
        chat_id=update.effective_chat.id, text=choose_premium_sub_option(username=username), reply_markup=markup
    )


async def stars_subs_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    push_menu(user_id, buy_sub)
    user_state = get_user_state(user_id)
    username = get_session(user_id, "entered_username")
    last_message_id = get_session(user_id, "last_message")

    # Predefined options
    stars_subs_list_keys = [
        [
            InlineKeyboardButton(
                text=fifty_stars_text(round_up_to_thousands(fifty_stars_invoice_price)), callback_data="sub:50"),
        ],
        [
            InlineKeyboardButton(
                text=seventy_five_stars_text(round_up_to_thousands(seventy_five_stars_invoice_price)), callback_data="sub:75"
            ),
        ],
        [
            InlineKeyboardButton(
                text=hundred_stars_text(round_up_to_thousands(hundred_stars_invoice_price)), callback_data="sub:100"
            ),
        ],
    ]

    # Add "Custom Amount" button with a URL linking to a text input field
    stars_subs_list_keys.append(
        [
            InlineKeyboardButton(text=CUSTOM_AMOUNT,
                                 callback_data="sub:custom_amount"),
        ]
    )

    # Back button and support contact
    stars_subs_list_keys.append(
        [
            InlineKeyboardButton(
                text=GO_BACK_TEXT, callback_data="go_back_cancelled"),
            InlineKeyboardButton(text=ADMIN_PANEL_TEXT,
                                 url=f"https://t.me/{ADMIN_USERNAME}"),
        ]
    )

    markup = InlineKeyboardMarkup(stars_subs_list_keys)
    msg = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=choose_stars_sub_option(username=username),
        reply_markup=markup,
    )


async def handle_sub_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    query = update.callback_query
    await query.answer()
    data = query.data

    if get_user_state(user_id) == BotState.PREMIUM_SUBS_LIST:
        if data == "sub:3m":
            set_session(user_id, "sub_choice",
                        THREE_M_CHOICE)
            set_session(user_id, "sub_price", str(
                three_m_invoice_price))  # Store as string
            set_session(user_id, 'profit_amount', float(profit_amount))
        elif data == "sub:6m":
            set_session(user_id, "sub_choice", SIX_M_CHOICE)
            set_session(user_id, "sub_price", str(
                six_m_invoice_price))  # Store as string
            set_session(user_id, 'profit_amount', float(profit_amount))

        elif data == "sub:12m":
            set_session(user_id, "sub_choice",
                        TWELVE_M_CHOICE)
            set_session(user_id, "sub_price", str(
                twelve_m_invoice_price))  # Store as string
            set_session(user_id, 'profit_amount', float(profit_amount))
        else:

            return
        set_user_state(user_id, BotState.INVOICE_LIST)
        # Delete the original premium_subs_list message after state change
        await context.bot.delete_message(
            chat_id=update.effective_chat.id, message_id=query.message.message_id
        )
        await buy_for_self(update, context)

    elif get_user_state(user_id) == BotState.STARS_SUBS_LIST:
        if data == "sub:custom_amount":
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=ENTER_CUSTOM_AMOUNT
            )
            set_user_state(user_id, BotState.CUSTOM_AMOUNT)
        else:
            if data == "sub:50":
                set_session(user_id, "sub_choice",
                            FIFTY_STARS_CHOICE)
                set_session(user_id, "sub_price", str(
                    round_up_to_thousands(fifty_stars_invoice_price)))  # Store as string
                set_session(user_id, 'profit_amount',
                            (50 * 0.015) * float(STARS_PROFIT))
            elif data == "sub:75":
                set_session(user_id, "sub_choice",
                            SEVENTY_FIVE_STARS_CHOICE)
                set_session(user_id, "sub_price", str(
                    round_up_to_thousands(seventy_five_stars_invoice_price)))  # Store as string
                set_session(user_id, 'profit_amount',
                            (75 * 0.015) * float(STARS_PROFIT))
            elif data == "sub:100":
                set_session(user_id, "sub_choice",
                            HUNDRED_STARS_CHOICE)
                set_session(user_id, "sub_price", str(
                    round_up_to_thousands(hundred_stars_invoice_price)))  # Store as string
                set_session(user_id, 'profit_amount',
                            (100 * 0.015) * float(STARS_PROFIT))
            set_user_state(user_id, BotState.INVOICE_LIST)
        # Delete the original premium_subs_list message after state change
            await context.bot.delete_message(
                chat_id=update.effective_chat.id, message_id=query.message.message_id
            )
            await buy_for_self(update, context)
        # else:
        #     return

    else:
        await start(update, context)


async def handle_custom_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    custom_amount = extract_number(update.message.text)
    print(custom_amount)
    usd_price = float(custom_amount)*0.015
    irr_price = float(usd_price * (float(last_price) + 2000))

    # Validate the custom amount (e.g., check if it's a number, within a certain range)
    if get_user_state(user_id) == BotState.CUSTOM_AMOUNT:
        if not is_valid_amount(custom_amount):
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="⚠️ The entered amount is incorrect, please enter a valid number."
            )
            return

    # Store the custom amount in the user's session
    set_session(user_id, "sub_choice", f"{custom_amount} Stars")
    set_session(user_id, "sub_price", round_up_to_thousands(irr_price))
    set_session(user_id, 'profit_amount', float(profit_amount))

    # Proceed to the next step (e.g., generating an invoice)
    set_user_state(user_id, BotState.INVOICE_LIST)
    await buy_for_self(update, context)


def is_valid_amount(amount):
    # Implement your validation logic here
    if 50 <= amount <= 1000000:
        return True
    else:
        return False


async def buy_for_self(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user_state = get_user_state(user_id)
    push_menu(user_id, premium_subs_list)

    if user_state == BotState.INVOICE_LIST:

        user_data = (
            update.callback_query.from_user
            if update.callback_query
            else update.message.from_user
        )

        invoice_title = get_session(user_id, "sub_choice")
        invoice_price = get_session(user_id, "sub_price")

        if not invoice_title or not invoice_price:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="false")
            return

        # Check if the username was entered earlier; if not, use the Telegram username
        username = get_session(user_id, "entered_username")
        if not username:
            username = user_data.username
        else:
            # Clear the custom username after using it
            delete_session(user_id, "entered_username")

        invoice_username = f"@{username}"
        profit = float(STARS_PROFIT)
        # Process the invoice creation
        if "استارز" in invoice_title:
            match = re.search(r'\d+', invoice_title)
            if match:
                amount = float(match.group())
            usd_price = float(amount)*0.015
            irr_price = float(
                usd_price * (float(last_price) + profit))

            invoice_details = {
                "title": invoice_title,
                "description": invoice_username,
                "price": irr_price,
                "profit": float(usd_price * profit),
                'fee': 0
            }
        else:
            invoice_details = {
                "title": invoice_title,
                "description": invoice_username,
                "price": invoice_price,
                "profit": profit_amount,
                'fee': fee_amount
            }
        set_session(user_id, "invoice_details", json.dumps(invoice_details))
        formatted_price = format_with_commas(float(invoice_price))
        # Send the invoice or next steps here
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=user_invoice_text(
                invoice_title, formatted_price, invoice_username)
        )
    else:
        await start(update, context)


async def update_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data.split(":")
    invoice_id = data[1]
    new_status = data[2]
    ex_btn = None
    if new_status == "Canceled":
        ex_btn = data[3]

    if new_status == "Reviewing":
        persian_new_status = REVIEWING_TEXT
    elif new_status == "Pay Approved":
        persian_new_status = PAY_APPROVED_TEXT
    elif new_status == "Approved":
        persian_new_status = APPROVED_TEXT
    else:
        persian_new_status = CANCELLED_TEXT

    try:
        # Fetch the invoice to check if it exists
        cur.execute(
            "SELECT id, sub FROM invoice WHERE invoice_id = ?", (invoice_id,))
        result = cur.fetchall()
        user_chat_id, sub_name = result[0]

        if result:
            # Update the status in the db
            cur.execute(
                "UPDATE invoice SET status = ? WHERE invoice_id = ?",
                (new_status, invoice_id),
            )
            conn.commit()

            # Get the existing caption and remove any existing status update
            existing_caption = query.message.caption if query.message.caption else ""
            if STATUS_UPDATED_TEXT in existing_caption:
                existing_caption = existing_caption.split(
                    f"\n{STATUS_UPDATED_TEXT}")[0]

            updated_caption = (
                f"{existing_caption}\n\n{STATUS_UPDATED_TEXT}{persian_new_status}"
            )

            # Define the inline keyboard based on the new status
            inline_keyboard = []
            if new_status == "Pay Approved":
                cur.execute(
                    "UPDATE invoice SET is_paid = ? WHERE invoice_id = ?",
                    ("true", invoice_id),
                )
                conn.commit()
                inline_keyboard = [
                    [
                        InlineKeyboardButton(
                            text=APPROVED_TEXT,
                            callback_data=f"status:{invoice_id}:Approved",
                        ),
                        InlineKeyboardButton(
                            text=CANCELLED_TEXT,
                            callback_data=f"status:{invoice_id}:Canceled:ex_Approved",
                        ),
                    ]
                ]
                await context.bot.send_message(
                    chat_id=user_chat_id,
                    text=approved_payment(sub_name),
                )
            elif new_status == "Approved":
                await context.bot.send_message(
                    chat_id=user_chat_id,
                    text=approved(sub_name),
                )
                delete_session(user_chat_id, "invoice_details")
                inline_keyboard = []
            elif new_status == "Canceled" and ex_btn == "ex_Approved":
                in_keyboard = [
                    [
                        InlineKeyboardButton(
                            text=ADMIN_PANEL_TEXT,
                            url=ADMIN_LINK,
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text=GO_BACK_TEXT, callback_data="go_back_cancelled"
                        ),
                    ],
                ]
                reply_markup = InlineKeyboardMarkup(in_keyboard)
                await context.bot.send_message(
                    chat_id=user_chat_id,
                    text=cancelled_username_text(sub_name=sub_name),
                    reply_markup=reply_markup,
                )
                delete_session(user_chat_id, "invoice_details")
            elif new_status == "Canceled" and ex_btn == "ex_Pay Approved":
                in_keyboard = [
                    [
                        InlineKeyboardButton(
                            text="ادمین",
                            url=ADMIN_LINK,
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text=GO_BACK_TEXT, callback_data="go_back_cancelled"
                        )
                    ],
                ]
                reply_markup = InlineKeyboardMarkup(in_keyboard)
                await context.bot.send_message(
                    chat_id=user_chat_id,
                    text=cancelled_payment_text(sub_name=sub_name),
                    reply_markup=reply_markup,
                )
                delete_session(user_chat_id, "invoice_details")

            reply_markup = (
                InlineKeyboardMarkup(
                    inline_keyboard) if inline_keyboard else None
            )

            # Update the message caption and buttons
            await query.edit_message_caption(
                caption=updated_caption,
                reply_markup=reply_markup,
            )
        else:
            await query.edit_message_caption(
                caption="Invoice not found.", reply_markup=query.message.reply_markup
            )
    except Exception as e:
        await query.edit_message_caption(
            caption=f"{FAILED_UPDATE_STATUS_TEXT}\nError: {str(e)}",
            reply_markup=query.message.reply_markup,
        )


async def go_back_handle(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    data = await query.answer()
    if query.data == "go_back_cancelled":
        message_id = query.message.message_id
        # await context.bot.delete_message(
        #     chat_id=update.effective_chat.id,
        #     message_id=message_id-2,
        # )
        await context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=message_id,
        )
        await start(update, context)
    elif query.data == "go_back":
        await start(update, context)


async def buy_success(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = update.effective_message.text
    chat_id = update.effective_chat.id
    photo = update.message.photo
    user_state = get_user_state(user_id)

    if photo and user_state == BotState.INVOICE_LIST:
        admin_chat_id = ADMIN_CHAT_ID

        try:
            invoice_details_str = get_session(user_id, "invoice_details")

            # Deserialize the invoice details
            invoice_details = json.loads(invoice_details_str)

            invoice_id = str(uuid.uuid4())[:8]

            user_data = update.message.from_user
            user_id = user_data.id
            user_username = user_data.username
            user_sub = invoice_details.get("title", "N/A")
            sub_price = invoice_details.get("price", "N/A")
            sub_profit = invoice_details.get("profit", "N/A")

            default_sub_status = "Reviewing"

            if user_username:
                if "استارز" in user_sub:
                    cur.execute(
                        "INSERT INTO invoice (id, username, sub, created, status, invoice_id, price, profit, fee) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (user_id, user_username, user_sub, get_solar_date(), default_sub_status,
                         invoice_id, str(sub_price), str(sub_profit), str(0))
                    )
                    conn.commit()
                else:
                    cur.execute(
                        "INSERT INTO invoice (id, username, sub, created, status, invoice_id, price, profit, fee) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (user_id, user_username, user_sub, get_solar_date(), default_sub_status,
                         invoice_id, str(sub_price), str(profit_amount), str(fee_amount))
                    )
                    conn.commit()
            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=CHOOSE_USERNAME_ERROR_TEXT,
                )
                return

            file_id = photo[-1].file_id
            user_data = update.message.from_user
            first_name = user_data.first_name
            last_name = user_data.last_name
            cur.execute(
                "SELECT profit, fee FROM invoice WHERE invoice_id = ?", (str(
                    invoice_id),)
            )
            data = cur.fetchall()
            profit_invoice = data[0][0]
            fee_invoice = data[0][1]
            invoice_text_message = invoice_text(
                invoice_details, first_name, last_name, user_id, user_username, fee_invoice, profit_invoice, invoice_id)
            inline_keyboard = [
                [
                    InlineKeyboardButton(
                        text=PAY_APPROVED_TEXT,
                        callback_data=f"status:{invoice_id}:Pay Approved",
                    ),
                    InlineKeyboardButton(
                        text=CANCELLED_TEXT,
                        callback_data=f"status:{invoice_id}:Canceled:ex_Pay Approved",
                    ),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(inline_keyboard)

            sent_keyboard = [
                [
                    InlineKeyboardButton(
                        text=GO_BACK_TEXT,
                        callback_data="go_back_cancelled",
                    ),
                ]
            ]
            sent_reply_markup = InlineKeyboardMarkup(sent_keyboard)

            await context.bot.send_photo(
                chat_id=admin_chat_id,
                photo=file_id,
                caption=invoice_text_message,
                reply_markup=reply_markup,
            )

            set_user_state(user_id, BotState.START)
            await context.bot.send_message(
                chat_id=chat_id,
                text=PHOTO_SENT_SUCCESSFULLY,
                reply_markup=sent_reply_markup,
            )

        except Exception as e:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=str(e),
            )
    elif not photo:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please send a photo.",
        )


async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top_buttons = [
        [
            InlineKeyboardButton(
                text=CHANELL_TEXT, url=f'https://t.me/{CHANELL_ID}'),
            InlineKeyboardButton(text=ADMIN_PANEL_TEXT, url=ADMIN_LINK)

        ]
    ]

    # Create the FAQ buttons
    faq_buttons = [
        [InlineKeyboardButton(q[0], callback_data=f"faq_{i}")]
        for i, q in enumerate(FAQ_FULL_TEXT)
    ]

    # Create the Go Back button
    go_back_button = [
        [InlineKeyboardButton(GO_BACK_TEXT, callback_data="go_back_cancelled")]
    ]

    # Combine all the buttons
    keyboard = top_buttons + faq_buttons + go_back_button
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(FAQ_TEXT, reply_markup=reply_markup)


async def faq_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "go_back_faq":
        top_buttons = [
            [
                InlineKeyboardButton(
                    text=CHANELL_TEXT, url=f'https://t.me/{CHANELL_ID}'),
                InlineKeyboardButton(text=ADMIN_PANEL_TEXT, url=ADMIN_LINK)

            ]
        ]

        # Create the FAQ buttons
        faq_buttons = [
            [InlineKeyboardButton(q[0], callback_data=f"faq_{i}")]
            for i, q in enumerate(FAQ_FULL_TEXT)
        ]

        # Create the Go Back button
        go_back_button = [
            [InlineKeyboardButton(
                GO_BACK_TEXT, callback_data="go_back_cancelled")]
        ]

        # Combine all the buttons
        keyboard = top_buttons + faq_buttons + go_back_button
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(FAQ_TEXT, reply_markup=reply_markup)
    else:
        index = float(query.data.split("_")[1])
        question, answer = FAQ_FULL_TEXT[index]
        keyboard = [[InlineKeyboardButton(
            GO_BACK_TEXT, callback_data="go_back_faq")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"{question}\n\n{answer}", reply_markup=reply_markup
        )


async def my_subs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    push_menu(user_id, start)

    user_data = update.message.from_user
    user_id = user_data["id"]

    cur.execute(
        "SELECT username, sub, created, status FROM invoice WHERE id = ? ORDER BY created DESC",
        (str(user_id),),
    )
    user_data = cur.fetchall()

    if user_data:
        status_translation = {
            "Reviewing": REVIEWING_TEXT,
            "Pay Approved": PAY_APPROVED_TEXT,
            "Approved": APPROVED_TEXT,
            "Canceled": CANCELLED_TEXT,
            None: "Unknown",
        }
        premium_subs_list = "\n".join(
            [
                f"""
        💢 Order: {sub}
        👤 For Telegram ID: @{username}
        📅 Created on: {datetime.strptime(created, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y')}
        ⭐️ Status: {status_translation.get(status)}
                """
                for username, sub, created, status in user_data
            ]
        )
        response_message = f"Your orders:\n{premium_subs_list}"
    else:
        response_message = NO_SUB_TEXT

    my_subs_keys = [
        [
            KeyboardButton(text=GO_BACK_TEXT),
        ],
    ]
    markup = ReplyKeyboardMarkup(my_subs_keys, resize_keyboard=True)

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=response_message, reply_markup=markup
    )


async def about_us(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                text=GO_BACK_TEXT, callback_data="go_back_cancelled"
            ),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=ABOUT_US_TEXT,
        reply_markup=reply_markup,
    )


async def photo_error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                text=GO_BACK_TEXT, callback_data="go_back_cancelled"
            ),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=NOT_PHOTO_ERROR,
        reply_markup=reply_markup
    )

    # Admin handler only


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    admin_keys = [
        [
            KeyboardButton(text=USERS_STATS),
            KeyboardButton(text=SELL_STATS),
        ],
        [
            KeyboardButton(text=SELL_INFO),
        ],
    ]

    markup = ReplyKeyboardMarkup(admin_keys, resize_keyboard=True)
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID, text=WELCOME_TEXT, reply_markup=markup
    )


async def user_stats_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total_users = get_total_users()
    daily_new_users = get_daily_new_users()
    weekly_new_users = get_weekly_new_users()
    user_w_paid_invoice = get_user_purchased()

    keys = [
        [
            KeyboardButton(text=GO_BACK_TEXT),
        ]
    ]

    markup = ReplyKeyboardMarkup(keys, resize_keyboard=True)

    message_text = users_stat_text(
        total_users, daily_new_users, weekly_new_users, user_w_paid_invoice)

    await context.bot.send_message(update.effective_chat.id, message_text, reply_markup=markup)


async def sell_stats_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = "خالی"

    available_months = get_available_months()

    # Get current month statistics
    current_date = datetime.now()
    current_solar_date = gregorian_to_solar(current_date)
    # current_solar_year, current_solar_month, _ = map(
    #     int, current_solar_date.split('-'))
    # result, first_day, last_day = get_sell_stats(
    #     current_solar_year, current_solar_month)

    for i in available_months:
        year = int(i.split("-")[0])
        month = int(i.split("-")[1])
        result, first_day, last_day = get_sell_stats(
            year, month)

        message_text += format_message_text(result,
                                            first_day, last_day)

    keys = [
        [
            KeyboardButton(text=GO_BACK_TEXT),
        ]
    ]
    markup = ReplyKeyboardMarkup(keys, resize_keyboard=True)

    # Get previous months with invoices

    # for month in available_months:
    #     year, month_num = map(int, month.split('-'))
    #     result, first_day, last_day = get_sell_stats(year, month_num)
    #     message_text += format_message_text(result, first_day, last_day)

    await context.bot.send_message(update.effective_chat.id, message_text, reply_markup=markup)


async def sell_variables(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keys = [
        [
            KeyboardButton(text=GO_BACK_TEXT),
        ]
    ]

    markup = ReplyKeyboardMarkup(keys, resize_keyboard=True)
    message_text = sale_variables_text(
        THREE_M_USD_PRICE, NINE_M_USD_PRICE, TWELVE_M_USD_PRICE, FEE_AMOUNT, PROFIT_AMOUNT)

    await context.bot.send_message(update.effective_chat.id, message_text, reply_markup=markup)


async def handle_states(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    chat_id = update.effective_chat.id
    user_state = get_user_state(user_id)
    text = update.message.text
    photo = update.message.photo
    last_message_id = get_session(user_id, "last_message")

    if user_state == BotState.START:
        if text == BUY_PREMIUM_TEXT:
            set_user_state(user_id, BotState.BUY_PREMIUM)
            await buy_sub(update, context)
            # Call appropriate handler
        elif text == MY_PURCHASES_TEXT:
            set_user_state(user_id, BotState.PREMIUM_SUBS_LIST)
            await my_subs(update, context)
        elif text == FAQ_TEXT:
            await faq(update, context)
        elif text == ADMIN_PANEL_TEXT:
            set_user_state(user_id, BotState.ADMIN_PANEL)
            await admin_panel(update, context)
        elif text == ABOUT_US_BTN_TEXT:
            await about_us(update, context)
        elif text == BUY_STARS_TEXT:
            set_user_state(user_id, BotState.BUY_STARS)
            await buy_sub(update, context)
        else:
            await start(update, context)
    elif user_state == BotState.BUY_PREMIUM or user_state == BotState.BUY_STARS:
        await handle_text_message(update, context)
    elif user_state == BotState.FAQ:
        if text:
            await start(update, context)
    elif user_state == BotState.CUSTOM_AMOUNT:
        await handle_custom_amount(update, context)
    elif user_state == BotState.PREMIUM_SUBS_LIST:
        if text == GO_BACK_TEXT:
            await start(update, context)
        else:
            await start(update, context)
    elif user_state == BotState.ADMIN_PANEL:
        if text == USERS_STATS:
            set_user_state(user_id, BotState.USERS_STATS)
            await user_stats_handler(update, context)
        elif text == SELL_STATS:
            set_user_state(user_id, BotState.SELL_STATS)
            await sell_stats_handler(update, context)
        elif text == SELL_INFO:
            set_user_state(user_id, BotState.SELL_VARIABLES)
            await sell_variables(update, context)
        elif text == GO_BACK_TEXT:
            set_user_state(user_id, BotState.START)
            await admin_panel(update, context)
    elif user_state == BotState.USERS_STATS:
        if text == GO_BACK_TEXT:
            set_user_state(user_id, BotState.ADMIN_PANEL)
            await admin_panel(update, context)
        elif text == USERS_STATS:
            await sell_stats_handler(update, context)
    elif user_state == BotState.SELL_STATS:
        if text == GO_BACK_TEXT:
            set_user_state(user_id, BotState.ADMIN_PANEL)
            await admin_panel(update, context)
        elif text == SELL_STATS:
            await sell_stats_handler(update, context)
    elif user_state == BotState.SELL_VARIABLES:
        if text == GO_BACK_TEXT:
            set_user_state(user_id, BotState.ADMIN_PANEL)
            await admin_panel(update, context)
        elif text == SELL_INFO:
            await sell_variables(update, context)
    elif user_state == BotState.INVOICE_LIST:
        if not photo:
            await photo_error_handler(update, context)
    # elif user_state == BotState.ABOUT_US:
    #     if text == ABOUT_US_BTN_TEXT:
    #         await about_us(update, context)
