import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import subprocess
import os
from telegram.ext import filters



BOT_TOKEN = "YOUR TOKEN HERE"  # Replace with your bot token
API_URL = "http://localhost:8000/transcribe/"  # Adjust if needed

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = (
        update.message.voice or
        update.message.audio or
        update.message.video_note or
        update.message.video
    )

    telegram_file = await context.bot.get_file(file.file_id)
    input_path = f"{file.file_id}.mp4" if update.message.video or update.message.video_note else f"{file.file_id}.ogg"
    output_path = input_path.replace(".mp4", ".wav").replace(".ogg", ".wav")

    await telegram_file.download_to_drive(input_path)

    # Convert to .wav (for compatibility)
    subprocess.run([
        "ffmpeg", "-i", input_path,
        "-ar", "16000",  # sample rate
        "-ac", "1",      # mono channel
        "-f", "wav",
        output_path
    ], check=True)

    with open(output_path, 'rb') as f:
        response = requests.post("http://localhost:8000/transcribe/", files={"file": f})

    if response.status_code == 200:
        transcription = response.json().get("transcription", "[no result]")
        await update.message.reply_text(f"🗣 {transcription}")
    else:
        await update.message.reply_text("⚠️ Transcription failed.")

    # Optional: Clean up
    os.remove(input_path)
    os.remove(output_path)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO | filters.VIDEO | filters.VIDEO_NOTE, handle_voice))
    print("Bot is running...")
    app.run_polling()