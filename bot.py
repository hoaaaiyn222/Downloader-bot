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

    # প্ল্যাটফর্মের জন্য সঠিক লিংক যাচাই
    if platform == "🎥 youtube" and "youtube.com" not in url:
        await update.message.reply_text("⚠️ শুধুমাত্র YouTube লিঙ্ক পাঠান।")
        return
    if platform == "📱 tiktok" and "tiktok.com" not in url:
        await update.message.reply_text("⚠️ শুধুমাত্র TikTok লিঙ্ক পাঠান।")
        return
    if platform == "📘 facebook" and "facebook.com" not in url:
        await update.message.reply_text("⚠️ শুধুমাত্র Facebook লিঙ্ক পাঠান।")
        return
    if platform == "📷 instagram" and "instagram.com" not in url:
        await update.message.reply_text("⚠️ শুধুমাত্র Instagram লিঙ্ক পাঠান।")
        return
    if platform == "❌ এক্স (twitter)" and "twitter.com" not in url:
        await update.message.reply_text("⚠️ শুধুমাত্র Twitter লিঙ্ক পাঠান।")
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