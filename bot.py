from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import yt_dlp as youtube_dl
from urllib.parse import urlparse


# Start Command with Permanent Menu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🎥 YouTube", "📱 TikTok"],
        ["📘 Facebook", "📷 Instagram"],
        ["❌ এক্স (Twitter)"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("🔗 একটি প্ল্যাটফর্ম সিলেক্ট করুন:", reply_markup=reply_markup)

# Handle Platform Selection from Menu
async def handle_platform(update: Update, context: ContextTypes.DEFAULT_TYPE):
    platform = update.message.text.lower()
    supported_platforms = ["🎥 youtube", "📱 tiktok", "📘 facebook", "📷 instagram", "❌ এক্স (twitter)"]

    # Reset previous platform and URL
    context.user_data.clear()

    if platform in supported_platforms:
        context.user_data['platform'] = platform
        await update.message.reply_text(f"✅ {platform.upper()} সিলেক্ট করা হয়েছে। এখন ভিডিওর লিংক পাঠান।")
    else:
        await update.message.reply_text("⚠️ অনুগ্রহ করে একটি বৈধ প্ল্যাটফর্ম নির্বাচন করুন।")

# Handle Video Link
async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    platform = context.user_data.get('platform', None)
    url = update.message.text

    if not platform:
        await update.message.reply_text("⚠️ প্ল্যাটফর্ম সিলেক্ট করুন। /start দিয়ে শুরু করুন।")
        return

    # URL যাচাই করুন
    if not is_valid_url(url):
        await update.message.reply_text("⚠️ অনুগ্রহ করে একটি বৈধ URL পাঠান।")
        return

    context.user_data['url'] = url

    keyboard = [
        [InlineKeyboardButton("240p", callback_data='240'),
         InlineKeyboardButton("360p", callback_data='360')],
        [InlineKeyboardButton("720p", callback_data='720'),
         InlineKeyboardButton("অডিও (MP3)", callback_data='audio')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("📥 ভিডিও ডাউনলোডের কোয়ালিটি সিলেক্ট করুন:", reply_markup=reply_markup)

# Download Video
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    url = context.user_data['url']
    quality = query.data

    await query.edit_message_text(text=f"⏳ {quality} ডাউনলোড হচ্ছে...")

    try:
        ydl_opts = {}
        if quality == 'audio':
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{context.user_data["platform"]}_{quality}_{url.split("=")[-1]}.mp3',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            }
        else:
            ydl_opts = {
                'format': f'bestvideo[height<={quality}]+bestaudio/best',
                'outtmpl': f'{context.user_data["platform"]}_{quality}_{url.split("=")[-1]}.mp4'
            }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        file_name = f'{context.user_data["platform"]}_{quality}_{url.split("=")[-1]}.mp4' if quality != 'audio' else f'{context.user_data["platform"]}_{quality}_{url.split("=")[-1]}.mp3'
        await query.message.reply_text("✅ ডাউনলোড সম্পন্ন! পাঠানো হচ্ছে...")
        await context.bot.send_document(chat_id=query.message.chat_id, document=open(file_name, 'rb'))

    except Exception as e:
        await query.message.reply_text(f"❌ ডাউনলোড করতে সমস্যা হয়েছে: {str(e)}")

# Main Function
def main():
    application = ApplicationBuilder().token("7968874233:AAFfkYyxZzu0iDLJ_acanYMwOEYVAL-Zqgg").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_platform))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    application.add_handler(CallbackQueryHandler(download_video, pattern='^(240|360|720|audio)$'))

    application.run_polling()

if __name__ == '__main__':
    main()
