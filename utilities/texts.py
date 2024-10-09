import jdatetime

from currencyapi import (
    three_m_price,
    six_m_price,
    twelve_m_price,
    last_price
)
from utilities.utils import format_solar_date, format_with_commas, get_solar_date, round_up_to_thousands
from config import ADMIN_USERNAME, CHANELL_ID, WEBSITE_ADDRESS, CREDIT_CARD_NUMBER, CREDIT_CARD_OWNER
import datetime

WELCOME_TEXT = "Welcome"
START_TEXT = "start"
BUY_PREMIUM_TEXT = "🛍️ Telegram Premium"
BUY_STARS_TEXT = "⭐ Buy Stars"
BUY_FOR_SELF_TEXT = "🙋‍♂️ Buy for Myself"
BUY_FOR_FRIENDS_TEXT = "🙋‍♂️🙋‍♂️🙋‍♂️ Buy for Friends"
BUY_SUCCESS_TEXT = "✅ Purchase was successful"
LOREM = "Lorem Ipsum is placeholder text used in the printing industry, and with the use of graphic designers, printers, and texts. Rather, newspapers and magazines in columns and rows as needed. It is necessary for the current conditions of technology and is used in diverse applications with the aim of improving practical tools. Many books in the past, present, and future have required extensive knowledge from society and experts, in order to create more understanding for computer designers, especially creative designers, and to establish a leading culture in the Persian language. In this case, it can be hoped that all the existing difficulties in providing solutions and the difficult conditions of typing will come to an end. The required time will include the main achievements of typography and answer the continuous questions of the people in the design world."
FAQ_FULL_TEXT = [
    ("❓ Does activating Premium require logging in?",
     "No, activating Premium does not require logging into your account."),
    ("❓ How long does it take to activate Premium?",
     "Premium will be activated within 35 minutes after your payment is confirmed."),
    ("❓ How do I activate the Telegram blue checkmark?",
     "You can activate the Telegram blue checkmark by purchasing Premium for your account."),
    ("❓ What should I do if I encounter a problem?",
     "If you encounter any issues, you can contact our team through the bot or support account. Our support team is available 24/7 to assist you."),
    ("❓ Is Telegram Premium suitable for me?",
     "Telegram Premium offers advanced features that enhance your user experience. If you're interested in additional features such as higher speed, larger file uploads, exclusive stickers, and other unique features, Telegram Premium could be the right choice for you."),
    ("❓ Can I buy a Premium subscription for my friends?",
     "Yes, you can purchase a Premium subscription for your friends. You just need to send your friend’s ID to the bot.")

]
FAQ_TEXT = "❓ Frequently Asked Questions"
MY_PURCHASES_TEXT = "❇️ My Orders"
GO_BACK_TEXT = "🔙 Go Back"
THREE_M_CHOICE = "Telegram Premium 3 months"
SIX_M_CHOICE = "Telegram Premium 6 months"
TWELVE_M_CHOICE = "Telegram Premium 12 months"
FIFTY_STARS_CHOICE = "50 Stars"
SEVENTY_FIVE_STARS_CHOICE = "75 Stars"
HUNDRED_STARS_CHOICE = "100 Stars"
PENDING_APPROVAL_TEXT = "🕰 Pending Approval"
REVIEWING_TEXT = "⌛ Reviewing"
APPROVED_TEXT = "✅ Request Completed"
CANCELLED_TEXT = "🚫 Cancelled"
PAY_APPROVED_TEXT = "💳 Transaction Approved"
CHOOSE_USERNAME_ERROR_TEXT = "⚠️ Please choose a Telegram username for your account"
SUB_HELP_TEXT = f"""
If you want to upgrade your Telegram to Premium, share the account with the bot via the menu button, or you can send another account's ID.

💡 Example Telegram ID: @{ADMIN_USERNAME}
"""

STARS_HELP_TEXT = f"""
If you want to buy Stars for your Telegram, share the account with the bot via the menu button, or you can send another account's ID.

💡 Example Telegram ID: @{ADMIN_USERNAME}
"""

INVALID_OPTION_TEXT = "❗️ Invalid option, please try again."
FAILED_UPDATE_STATUS_TEXT = "❗️ Status update failed."
ERROR_SENDING_PHOTO = "❗️ There was an error sending the photo to the admin."
UNKNOWN_TEXT = "Unknown"
CUSTOM_AMOUNT = "✍️ Enter a Custom Amount"
ENTER_CUSTOM_AMOUNT = """⭐ Please send the desired amount of Stars to buy for the bot (from 50 to 1,000,000)
"""
NO_SUB_TEXT = "🚫 No order has been placed"
# USERNAME_LIMITS_TEXT = "⚠️ Please enter a correct username. A valid username includes: English letters A to Z, numbers 0 to 9, underscore (_), and 5 to 32 characters."
STATUS_UPDATED_TEXT = "Status changed to: "
# change
USERNAME_LIMITS_TEXT = f"""
❗️ The entered Telegram ID is incorrect.
Example Telegram ID 👈 @{ADMIN_USERNAME}
"""
ITS_PAID_TEXT = "✅ Dear customer, your transaction has been confirmed"
ADMIN_PANEL_TEXT = "👤 Admin"
USERS_STATS = "📊 User Statistics"
SELL_STATS = "📊 Sales Statistics"
PHOTO_SENT_SUCCESSFULLY = "✅ Your payment screenshot has been successfully sent to our admin"
SELL_INFO = "💳 Sales Variables"
REDIS_ERROR = "Invoice details not found in Redis"
ADMIN_LINK = f"https://t.me/{ADMIN_USERNAME}"
ABOUT_US_BTN_TEXT = "ℹ️ About Us"
ABOUT_US_TEXT = f"""
With AeroPremium, bypass Telegram sanctions with peace of mind.

 📢 Channel: @{CHANELL_ID}

 👤 Admin ID: @{ADMIN_USERNAME}

 🌐 Our website: {WEBSITE_ADDRESS}

"""
NOT_PHOTO_ERROR = "❗️ Error, please send only the payment screenshot to the bot"
CHANELL_TEXT = "💬 Our Channel"

def cancelled_username_text(sub_name):
    text = f"""
🔴 Your request was cancelled

Request: {sub_name}

Your request was cancelled due to an incorrect Telegram ID or another reason.

❗️ If you have entered the ID correctly, please notify support 👇
"""
    return text


def cancelled_payment_text(sub_name):
    text = f"""
🔴 Your request was cancelled

Request: {sub_name}

Your request was cancelled due to an issue with your payment.

❗️ If you have made the payment correctly, please notify support 👇
"""
    return text


def approved_payment(sub_name):
    text = f"""
🟢 Your payment has been approved

Request: {sub_name}

✅ Your payment has been successfully confirmed, and your Telegram Premium will be activated soon.
"""
    return text


def approved(sub_name):
    text = f"""
🟢 Your request has been approved

Request: {sub_name}

✅ Your request has been successfully completed, and your Telegram Premium is now active.
"""
    return text


def sale_variables_text(three_m, six_m, tweleve_m, fee, profit):
    text = f"""
📊 Sales Variables

Three-month subscription price: ${three_m}

Six-month subscription price: ${six_m}

Twelve-month subscription price: ${tweleve_m}

Fee: ${fee}

Profit: ${profit}

"""
    return text


def sale_stats_text(first_day, last_day, total_paid_invoices, formatted_sales, profit):
    text = f"""
📊 Sales Statistics

From {format_solar_date(first_day)} to {format_solar_date(last_day)}

Total purchases: {total_paid_invoices}

Total sales amount: {formatted_sales}

Total profit: {profit}

"""
    return text


def format_message_text(result, first_day, last_day, is_current=False):
    total_paid_invoices = result[0]
    total_sales = result[1]
    total_profit = result[2]
    if total_sales and total_profit:
        formatted_sales = format_with_commas(total_sales)
        formatted_profit = format_with_commas(total_profit)
    else:
        formatted_sales = 0
        formatted_profit = 0

    year = first_day.year
    month = first_day.month

    now_month = jdatetime.datetime.now().month

    # Create a list for Persian month names
    persian_month_names = [
        'Farvardin', 'Ordibehesht', 'Khordad', 'Tir', 'Mordad', 'Shahrivar',
        'Mehr', 'Aban', 'Azar', 'Dey', 'Bahman', 'Esfand'
    ]

    # Format the Persian date
    persian_date_str = f'{persian_month_names[month - 1]} {year}'
    if month == now_month:
        period = f"{persian_date_str} (Current Month)"
    else:
        period = f"{persian_date_str}"
    message_text = f"""
    
    Sales Statistics for {period}:
    Number of paid invoices: {total_paid_invoices}
    Total sales: {formatted_sales}
    Total profit: {formatted_profit}
    """
    return message_text


def users_stat_text(total_users, daily_new_users, weekly_new_users, user_w_paid_invoice):
    text = f"""
📊 User Statistics

Total users: {total_users}

New users today: {daily_new_users}

New users this week: {weekly_new_users}

Users with at least one purchase: {user_w_paid_invoice}

"""
    return text


def invoice_text(invoice_details, first_name, last_name, user_id, user_username, fee_amount, profit_amount, invoice_id):

    text = f"""📰 New Invoice

🧾 Invoice number: {invoice_id}
📋 Request: {invoice_details.get('title', 'N/A')}
👤 First name: {first_name}
👥 Last name: {last_name}
🆔 User ID: {user_id}
🔗 Main Telegram ID: @{user_username}
🔍 Entered Telegram ID: {invoice_details.get('description', 'N/A')}

💲 Tether price: {format_with_commas(float(last_price))}
💰 Invoice price: {round_up_to_thousands(float(invoice_details.get('price', 'N/A')))} T
💸 Invoice fee: {format_with_commas(float(fee_amount))}
📈 Invoice profit: {format_with_commas(float(profit_amount))}

"""

    rtl_text = f"""\u200F📰 New Invoice

\u200F🧾 Invoice number: {invoice_id}
\u200F📋 Request: {invoice_details.get('title', 'N/A')}
\u200F👤 First name: {first_name}
\u200F👥 Last name: {last_name}
\u200F🆔 User ID: {user_id}
\u200F🔗 Main Telegram ID: @{user_username}
\u200F🔍 Entered Telegram ID: {invoice_details.get('description', 'N/A')}

\u200F💲 Tether price: {format_with_commas(float(float(last_price)))}
\u200F💰 Invoice price: {invoice_details.get('price', 'N/A')} T
\u200F💸 Invoice fee: {format_with_commas(float(fee_amount))}
\u200F📈 Invoice profit: {format_with_commas(float(profit_amount))}

"""
    return rtl_text


def user_invoice_text(invoice_title, formatted_price, invoice_username):
    text = f"""🧾 Your invoice has been created.

💢 Request: {invoice_title}
👤 For username: {invoice_username}

🛍 Amount to pay: {formatted_price} Tomans

🔸 Card number:
{CREDIT_CARD_NUMBER}

🔸In the name of: {CREDIT_CARD_OWNER}

📌 Please send the payment screenshot to the bot 👇"""
    return text


def choose_premium_sub_option(username):
    CHOOSE_OPTION_TEXT = f"""
⭐️ Please select your Telegram Premium subscription type

Selected Telegram ID: @{username}
"""

    return CHOOSE_OPTION_TEXT


def three_m_text(price):
    text = f"3 months - {format_with_commas(price)} T"
    return text


def six_m_text(price):
    text = f"6 months - {format_with_commas(price)} T"
    return text


def twelve_m_text(price):
    text = f"12 months - {format_with_commas(price)} T"
    return text


def choose_stars_sub_option(username):
    CHOOSE_OPTION_TEXT = f"""
⭐️ Please select the number of Stars you want

Selected Telegram ID: @{username}
"""

    return CHOOSE_OPTION_TEXT


def fifty_stars_text(price):
    text = f"50 Stars - {format_with_commas(price)} T"
    return text


def seventy_five_stars_text(price):
    text = f"75 Stars - {format_with_commas(price)} T"
    return text


def hundred_stars_text(price):
    text = f"100 Stars - {format_with_commas(price)} T"
    return text
