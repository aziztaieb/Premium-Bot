from currencyapi import (
    three_m_price,
    six_m_price,
    twelve_m_price,
    last_price
)
from utilities.utils import format_solar_date, format_with_commas
from config import ADMIN_USERNAME, CHANELL_ID, WEBSITE_ADDRESS, CREDIT_CARD_NUMBER, CREDIT_CARD_OWNER

WELCOME_TEXT = "خوش آمدید"
START_TEXT = "start"
BUY_PREMIUM_TEXT = "🛍️ تلگرام پرمیوم"
BUY_FOR_SELF_TEXT = "🙋‍♂️ خرید برای خودم"
BUY_FOR_FRIENDS_TEXT = "🙋‍♂️🙋‍♂️🙋‍♂️ خرید برای دوستان"
BUY_SUCCESS_TEXT = "✅ خرید با موفقیت انجام شد"
LOREM = "لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ، و با استفاده از طراحان گرافیک است، چاپگرها و متون بلکه روزنامه و مجله در ستون و سطرآنچنان که لازم است، و برای شرایط فعلی تکنولوژی مورد نیاز، و کاربردهای متنوع با هدف بهبود ابزارهای کاربردی می باشد، کتابهای زیادی در شصت و سه درصد گذشته حال و آینده، شناخت فراوان جامعه و متخصصان را می طلبد، تا با نرم افزارها شناخت بیشتری را برای طراحان رایانه ای علی الخصوص طراحان خلاقی، و فرهنگ پیشرو در زبان فارسی ایجاد کرد، در این صورت می توان امید داشت که تمام و دشواری موجود در ارائه راهکارها، و شرایط سخت تایپ به پایان رسد و زمان مورد نیاز شامل حروفچینی دستاوردهای اصلی، و جوابگوی سوالات پیوسته اهل دنیای موجود طراحی اساسا مورد استفاده قرار گیرد."
FAQ_FULL_TEXT = [
    ("❓ آیا فعال سازی پرمیوم نیاز به لاگین دارد",
     "خیر، برای فعال سازی پریمیوم نیازی به لاگین به حساب شما نیست"),
    ("❓ فعال سازی پرمیوم چقدر زمان میبرد",
     "تا 35 دقیقه بعد از تایید شدن پرداخت شما پریموم برای شما فعال خواهد شد"),
    ("❓ چطور تیک آبی تلگرام را فعال کنیم",
     "شما میتوانید با خرید پرمیوم برای حساب خود تیک آبی تلگرام را فعال کنید"),
    ("❓ اگر به مشکل خوردم چیکار کنم",
     "در صورت بروز هرگونه مشکل، شما می‌توانید از طریق بات یا حساب پشتیبانی با تیم ما در ارتباط باشید بگیرید. تیم پشتیبانی ما به صورت 24 ساعته آماده کمک به شماست."),
    ("❓ آیا تلگرام پرمیوم برای من مناسب است",
     "تلگرام پرمیوم امکانات و ویژگی‌های پیشرفته‌ای ارائه می‌دهد که تجربه کاربری شما را بهبود می‌بخشد. اگر به امکانات بیشتری نظیر سرعت بالاتر، آپلود فایل‌های بزرگتر، استیکرهای اختصاصی و سایر ویژگی‌های منحصر به فرد علاقه‌مند هستید، تلگرام پرمیوم می‌تواند انتخاب مناسبی برای شما باشد."),
    ("❓ آیا میتونم برای دوستانم اشتراک پرمیوم بخرم",
     "بله، شما می‌توانید برای دوستان خود هم اشتراک پرمیوم تهیه کنید. تنها کافی است آیدی دوست خود را به ربات ارسال کنید.")

]
FAQ_TEXT = "❓ سوالات پر تکرار"
MY_PURCHASES_TEXT = "❇️ سفارش های من"
GO_BACK_TEXT = "🔙 بازگشت"
THREE_M_CHOICE = "تلگرام پرمیوم 3 ماهه"
SIX_M_CHOICE = "تلگرام پرمیوم 6 ماهه"
TWELVE_M_CHOICE = "تلگرام پرمیوم 12 ماهه"
PENDING_APPROVAL_TEXT = "🕰 در انتظار تایید"
REVIEWING_TEXT = "⌛ در حال بررسی"
APPROVED_TEXT = "✅ درخواست انجام شده"
CANCELLED_TEXT = "🚫  لغو شده"
PAY_APPROVED_TEXT = "💳 تراکنش تایید شده"
CHOOSE_USERNAME_ERROR_TEXT = "⚠️ لطفاً برای حساب خود ایدی تلگرام انتخاب کنید"
SUB_HELP_TEXT = f"""
اگر میخواهید تلگرام خود را پرمیوم کنید از طریق دکمه منو اکانت را برای ربات به اشتراک بگذارید یا میتوانید آیدی اکانت دیگری را ارسال کنید

💡 نمونه ایدی تلگرام : @{ADMIN_USERNAME}
"""

INVALID_OPTION_TEXT = "❗️ گزینه نامعتبر لطفا دوباره تلاش کنید."
FAILED_UPDATE_STATUS_TEXT = "❗️ وضعیت به‌روزرسانی نشد."
ERROR_SENDING_PHOTO = "❗️ هنگام ارسال عکس برای ادمین خطایی رخ داد."
UNKNOWN_TEXT = "نامشخص"
NO_SUB_TEXT = "🚫 سفارشی ثبت نشده است"
# USERNAME_LIMITS_TEXT = "⚠️ لطفا یوزر نیم را به درستی وارد کنید. یک یوزر نیم درست شامل : حروف انگلیسی A تا Z ، اعداد 0 تا 9 ، آندرسکور( _ )، و ۵ تا ۳۲ حرف است"
STATUS_UPDATED_TEXT = "وضعیت تغییر کرد به : "
# change
USERNAME_LIMITS_TEXT = f"""
❗️ ایدی تلگرام وارد شده صحیح نمی باشد
نمونه ایدی تلگرام 👈 @{ADMIN_USERNAME}
"""
ITS_PAID_TEXT = "✅ مشتری گرامی تراکنش شما تایید شد"
ADMIN_PANEL_TEXT = "👤  ادمین"
USERS_STATS = "📊 آمار کاربران"
SELL_STATS = "📊 آمار فروش"
PHOTO_SENT_SUCCESSFULLY = "✅ عکس واریزی شما با موفقیت برای ادمین ما ارسال شد"
SELL_INFO = "💳 متغیر های فروش"
REDIS_ERROR = "Invoice details not found in Redis"
ADMIN_LINK = f"https://t.me/{ADMIN_USERNAME}"
ABOUT_US_BTN_TEXT = "ℹ️ درباره ما"
ABOUT_US_TEXT = f"""
با ایروپرمیوم تحریم های تلگرام رو با خیال راحت دور بزنید

 📢 کانال : @{CHANELL_ID}

 👤 ایدی ادمین : @{ADMIN_USERNAME}

 🌐 وبسایت ما : {WEBSITE_ADDRESS}

"""
NOT_PHOTO_ERROR = "❗️ خطا، لطفا فقط اسکرین شات واریزی را برای ربات ارسال نمایید"
CHANELL_TEXT = "💬 کانال ما"


def cancelled_username_text(sub_name):
    text = f"""
🔴 درخواست شما لغو شد

درخواست : {sub_name}

درخواست شما به دلیل اشتباه بودن ایدی تلگرام یا دلیلی دیگر لفو شد

❗️ در صورتی که ایدی را به درستی وارد کرده اید لطفا به پشتیبانی اطلاع دهید 👇
"""
    return text


def cancelled_payment_text(sub_name):
    text = f"""
🔴 درخواست شما لغو شد

درخواست :{sub_name}

درخواست شما به دلیل اشتباه بودن پرداخت شما لفو شد

❗️ در صورتی که پرداخت را به درستی انجام دادید لطفا به پشتیبانی اطلاع دهید 👇
"""
    return text


def approved_payment(sub_name):
    text = f"""
🟢 پرداخت شما تایید شد

درخواست :{sub_name}

✅ پرداخت شما با موفقیت تایید شد و تلگرام پرمیوم شما به زودی فعال خواهد شد
"""
    return text


def approved(sub_name):
    text = f"""
🟢 درخواست شما تایید شد

درخواست :{sub_name}

✅ درخواست شما با موفقیت انجام شد و تلگرام پرمیوم شما فعال شد
"""
    return text


def sale_variables_text(three_m, six_m, tweleve_m, fee, profit):
    text = f"""
📊  متغیر های فروش

قیمت اشتراک سه ماهه : ${three_m}

قیمت اشتراک شش ماه : ${six_m}

قیمت اشتراک دوازده ماهه : ${tweleve_m}

قیمت کارمزد : ${fee}

قیمت سود : ${profit}

"""
    return text


def sale_stats_text(first_day, last_day, total_paid_invoices, formatted_sales, profit):
    text = f"""
📊 آمار فروش

از تاریخ {format_solar_date(first_day)} تا تاریخ {format_solar_date(last_day)}

تعداد کل خرید ها : {total_paid_invoices}

مقدار فروش کل : {formatted_sales}

مقدار سود کل : {profit}

"""
    return text


def users_stat_text(total_users, daily_new_users, weekly_new_users, user_w_paid_invoice):
    text = f"""
📊 آمار کاربران

تعداد کل کاربران : {total_users}

تعداد کاربران جدید امروز : {daily_new_users}

تعداد کاربران جدید این هفته : {weekly_new_users}

تعداد کاربرانی که حداقل یک خرید انجام دادند : {user_w_paid_invoice}

"""
    return text


def invoice_text(invoice_details, first_name, last_name, user_id, user_username, fee_amount, profit_amount, invoice_id):

    text = f"""📰 فاکتور جدید

🧾 شماره فاکتور : {invoice_id}
📋 درخواست : {invoice_details.get('title', 'N/A')}
👤 نام : {first_name}
👥 نام خانوادگی : {last_name}
🆔 ایدی کاربر : {user_id}
🔗 ایدی تلگرام اصلی : @{user_username}
🔍 ایدی تلگرام وارد شده : {invoice_details.get('description', 'N/A')}

💲 قیمت تتر : {format_with_commas(int(float(last_price)))}
💰 قیمت فاکتور : {invoice_details.get('price', 'N/A')} ت
💸 کارمزد فاکتور : {format_with_commas(int(fee_amount))}
📈 سود فاکتور : {format_with_commas(int(profit_amount))}

"""

    rtl_text = f"""\u200F📰 فاکتور جدید

\u200F🧾 شماره فاکتور : {invoice_id}
\u200F📋 درخواست : {invoice_details.get('title', 'N/A')}
\u200F👤 نام : {first_name}
\u200F👥 نام خانوادگی : {last_name}
\u200F🆔 ایدی کاربر : {user_id}
\u200F🔗 ایدی تلگرام اصلی : @{user_username}
\u200F🔍 ایدی تلگرام وارد شده : {invoice_details.get('description', 'N/A')}

\u200F💲 قیمت تتر : {format_with_commas(int(float(last_price)))}
\u200F💰 قیمت فاکتور : {invoice_details.get('price', 'N/A')} ت
\u200F💸 کارمزد فاکتور : {format_with_commas(int(fee_amount))}
\u200F📈 سود فاکتور : {format_with_commas(int(profit_amount))}

"""
    return rtl_text


def user_invoice_text(invoice_title, formatted_price, invoice_username):
    text = f"""🧾 فاکتور شما ایجاد شد.

💢 درخواست: {invoice_title}
👤 برای ایدی: {invoice_username}

🛍 مبلغ جهت پرداخت: {formatted_price} تومان

🔸 شماره کارت:
{CREDIT_CARD_NUMBER}

🔸به نام:   {CREDIT_CARD_OWNER}

📌 لطفا اسکرین شات واریزی را برای ربات ارسال نمایید 👇"""
    return text


def choose_sub_option(username):
    CHOOSE_OPTION_TEXT = f"""
⭐️ لطفا نوع اشتراک تلگرام پریموم خود را انتخاب کنید

آیدی تلگرام انتخاب شده: @{username}
"""

    return CHOOSE_OPTION_TEXT


def three_m_text(price):
    text = f"3 ماهه - {format_with_commas(price)} ت"
    return text


def six_m_text(price):
    text = f"6 ماهه - {format_with_commas(price)} ت"
    return text


def twelve_m_text(price):
    text = f"12 ماهه - {format_with_commas(price)} ت"
    return text
