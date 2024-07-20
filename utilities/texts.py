from currencyapi import (
    three_m_price,
    six_m_price,
    twelve_m_price,
)
from utilities.utils import format_solar_date, format_with_commas
from config import ADMIN_USERNAME, CHANELL_ID, WEBSITE_ADDRESS, CREDIT_CARD_NUMBER, CREDIT_CARD_OWNER

WELCOME_TEXT = "خوش آمدید"
START_TEXT = "start"
BUY_PREMIUM_TEXT = "🛍️ خرید پرمیوم تلگرام"
BUY_FOR_SELF_TEXT = "🙋‍♂️ خرید برای خودم"
BUY_FOR_FRIENDS_TEXT = "🙋‍♂️🙋‍♂️🙋‍♂️ خرید برای دوستان"
BUY_SUCCESS_TEXT = "✅ خرید با موفقیت انجام شد"
LOREM = "لورم ایپسوم متن ساختگی با تولید سادگی نامفهوم از صنعت چاپ، و با استفاده از طراحان گرافیک است، چاپگرها و متون بلکه روزنامه و مجله در ستون و سطرآنچنان که لازم است، و برای شرایط فعلی تکنولوژی مورد نیاز، و کاربردهای متنوع با هدف بهبود ابزارهای کاربردی می باشد، کتابهای زیادی در شصت و سه درصد گذشته حال و آینده، شناخت فراوان جامعه و متخصصان را می طلبد، تا با نرم افزارها شناخت بیشتری را برای طراحان رایانه ای علی الخصوص طراحان خلاقی، و فرهنگ پیشرو در زبان فارسی ایجاد کرد، در این صورت می توان امید داشت که تمام و دشواری موجود در ارائه راهکارها، و شرایط سخت تایپ به پایان رسد و زمان مورد نیاز شامل حروفچینی دستاوردهای اصلی، و جوابگوی سوالات پیوسته اهل دنیای موجود طراحی اساسا مورد استفاده قرار گیرد."
FAQ_FULL_TEXT = [
    ("❓ تلگرام پرمیوم چیست", "تلگرام پرمیوم یک سرویس اشتراکی است که امکانات بیشتری را نسبت به نسخه رایگان تلگرام ارائه می‌دهد. این امکانات شامل امکانات اضافی، سفارشی‌سازی بیشتر، فضای ذخیره‌سازی بزرگتر و عدم نمایش تبلیغات می‌شود."),
    ("❓ چرا باید تلگرام پرمیوم را بخرم", "با خرید تلگرام پرمیوم، شما می‌توانید از امکانات ویژه‌ای مانند ارسال فایل‌های بزرگتر، سرعت دانلود بالاتر، استیکرهای انحصاری، و گزینه‌های سفارشی‌سازی بیشتر بهره‌مند شوید. این امکانات تجربه کاربری شما را بهبود می‌بخشند."),
    ("❓ چطوری تلگرام پرمیوم را بخرم",
     "برای خرید اشتراک تلگرام پرمیوم، کافی است با بات ما ارتباط برقرار کنید و مراحل ساده‌ای را دنبال کنید. بات شما را راهنمایی می‌کند تا اشتراک خود را انتخاب و پرداخت را انجام دهید."),
    ("❓ اگر به مشکل خوردم چیکار کنم",
     "در صورت بروز هرگونه مشکل، شما می‌توانید از طریق بات یا حساب پشتیبانی با تیم ما در ارتباط باشید بگیرید. تیم پشتیبانی ما به صورت ۲۴/۷ آماده کمک به شماست."),
    ("❓ آیا میتونم به یکی دیگه اشتراک هدیه بدم",
     "بله، شما می‌توانید اشتراک تلگرام پرمیوم را به عنوان هدیه به دوستان یا خانواده خود ارائه دهید. برای این کار کافی است در قسمت خرید اشتراک یوز نیم شخص مورد نظر را وارد کنید."),
    ("❓ آیا تلگرام پرمیوم روی همه دستگاه ها کار میکنه",
     "بله، با خرید اشتراک تلگرام پرمیوم، می‌توانید از امکانات آن در تمام دستگاه‌هایی که تلگرام بر روی آن‌ها نصب شده است، استفاده کنید."),
]
FAQ_TEXT = "❓ پرسش‌ های متداول"
MY_PURCHASES_TEXT = "❇️ درخواست های من"
GO_BACK_TEXT = "🔙 بازگشت"
THREE_M_SUB_TEXT = "تلگرام پرمیوم سه ماهه"
SIX_M_SUB_TEXT = "تلگرام پرمیوم شش ماهه"
TWELVE_M_SUB_TEXT = "تلگرام پرمیوم دوازده ماهه"
PENDING_APPROVAL_TEXT = "🕰 در انتظار تایید"
REVIEWING_TEXT = "⌛ در حال بررسی"
APPROVED_TEXT = "✅ درخواست انجام شده"
CANCELLED_TEXT = "🚫  لغو شده"
PAY_APPROVED_TEXT = "💳 تراکنش تایید شده"
CHOOSE_USERNAME_ERROR_TEXT = "⚠️ لطفاً برای حساب خود ایدی تلگرام انتخاب کنید"
SUB_HELP_TEXT = """⭐️ لطفا ایدی تلگرام مورد نظر برای خرید پرمیوم ارسال کنید"""
CHOOSE_OPTION_TEXT = "⭐️ لطفا نوع اشتراک تلگرام پریموم خود را انتخاب کنید"
INVALID_OPTION_TEXT = "❗️ گزینه نامعتبر لطفا دوباره تلاش کنید."
FAILED_UPDATE_STATUS_TEXT = "❗️ وضعیت به‌روزرسانی نشد."
ERROR_SENDING_PHOTO = "❗️ هنگام ارسال عکس برای ادمین خطایی رخ داد."
UNKNOWN_TEXT = "نامشخص"
NO_SUB_TEXT = "🚫 شما اشتراکی ندارید."
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

 📢ادرس کانال ما : @{CHANELL_ID}

 👤ادرس ادمین ما : @{ADMIN_USERNAME}

 🌐ادرس وبسایت ما : {WEBSITE_ADDRESS}

"""
NOT_PHOTO_ERROR = "❗️ خطا، لطفا فقط اسکرین شات واریزی را برای ربات ارسال نمایید"


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


def invoice_text(invoice_details, first_name, last_name, user_id, user_username, last_price, fee_amount, profit_amount, invoice_id):
    text = f"""**فاکتور**

درخواست : {invoice_details.get('title', 'N/A')}
نام : {first_name}
نام خانوادگی : {last_name}
ایدی کاربر : {user_id}
ایدی تلگرام اصلی : @{user_username}
ایدی تلگرام وارد شده : {invoice_details.get('description', 'N/A')}
قیمت تتر : {format_with_commas(int(float(last_price)))}
قیمت فاکتور : {invoice_details.get('price', 'N/A')} ت
کارمزد فاکتور : {format_with_commas(fee_amount)}
سود فاکتور : {format_with_commas(profit_amount)}
شماره فاکتور : {invoice_id}"""
    return text


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
