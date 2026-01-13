import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType
from aiogram.filters import Command
from github import Github

# Bilgilerini buraya tırnak içine yaz
TOKEN = "8200931811:AAGNfRjoSzenGynnlWOZFHDc48UhEHcOSeQ"
GITHUB_TOKEN = "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"

bot = Bot(token=TOKEN)
dp = Dispatcher()
g = Github(GITHUB_TOKEN)

@dp.message(Command("start"))
async def start(m: Message):
    await m.answer("🌐 **Dosyadan Site Yapan Bot Aktif!**\n\nBana bir `.html` veya `.php` dosyası gönder, anında internet sitesine dönüştüreyim!")

# HEM METİN HEM DOSYA OKUYAN FONKSİYON
@dp.message(F.document | F.text)
async def handle_content(m: Message):
    html_content = ""
    
    # Eğer dosya (document) gönderildiyse
    if m.document:
        if m.document.file_name.endswith(('.html', '.php')):
            msg = await m.answer("📥 Dosya indiriliyor ve siteye yükleniyor...")
            file = await bot.get_file(m.document.file_id)
            file_path = await bot.download_file(file.file_path)
            html_content = file_path.read().decode("utf-8")
        else:
            return await m.answer("⚠️ Lütfen sadece .html veya .php uzantılı dosya gönderin.")
    
    # Eğer metin olarak kod gönderildiyse
    elif m.text and "<html>" in m.text.lower():
        msg = await m.answer("⏳ Kodun siteye dönüştürülüyor...")
        html_content = m.text
    else:
        return

    try:
        user = g.get_user()
        repo_name = f"site-{m.from_user.id}"
        file_name = m.document.file_name if m.document else "index.html"
        
        try:
            repo = user.get_repo(repo_name)
        except:
            repo = user.create_repo(repo_name)

        try:
            contents = repo.get_contents(file_name)
            repo.update_file(file_name, "Güncelleme", html_content, contents.sha)
        except:
            repo.create_file(file_name, "İlk Kurulum", html_content)

        site_url = f"https://{user.login}.github.io/{repo_name}/"
        await msg.edit_text(f"🚀 **Siten Yayında!**\n\n🔗 **Link:** {site_url}\n📂 **Dosya:** {file_name}")

    except Exception as e:
        await msg.edit_text(f"❌ Hata oluştu: {str(e)}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
