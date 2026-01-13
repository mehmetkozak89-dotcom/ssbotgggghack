import asyncio
import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from github import Github

# Tokenları Render'ın 'Environment Variables' kısmından çeker
TOKEN = os.getenv("8200931811:AAGNfRjoSzenGynnlWOZFHDc48UhEHcOSeQ")
GITHUB_TOKEN = os.getenv("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")

bot = Bot(token=TOKEN)
dp = Dispatcher()
g = Github(GITHUB_TOKEN)

@dp.message(Command("start"))
async def start(m: Message):
    await m.answer("🌐 **Koddan Site Yapan Bot**\n\nBana herhangi bir HTML kodu gönder, senin için onu internete yükleyip linkini vereyim!")

@dp.message()
async def build_site(m: Message):
    # Eğer kullanıcı metin gönderdiyse (HTML kodu olduğunu varsayıyoruz)
    if not m.text or "<html>" not in m.text.lower():
        return await m.answer("⚠️ Lütfen geçerli bir HTML kodu gönderin (İçinde <html> etiketi olmalı).")

    msg = await m.answer("⏳ Kodun analiz ediliyor ve site kuruluyor...")
    
    try:
        user = g.get_user()
        # Her kullanıcı için benzersiz bir isim (Telegram ID'si ile)
        site_name = f"site-{m.from_user.id}"
        
        try:
            # Depo zaten varsa onu al, yoksa yeni oluştur
            repo = user.get_repo(site_name)
        except:
            repo = user.create_repo(site_name)

        # Kullanıcının attığı kodu index.html olarak yükle veya güncelle
        try:
            contents = repo.get_contents("index.html")
            repo.update_file("index.html", "Site güncellendi", m.text, contents.sha)
        except:
            repo.create_file("index.html", "İlk kurulum", m.text)

        site_url = f"https://{user.login}.github.io/{site_name}/"
        
        await msg.edit_text(
            f"🚀 **Siten Hazır!**\n\n🔗 **Link:** {site_url}\n\n"
            "⚠️ *Not: İlk kurulumda sitenin açılması 1-2 dakika sürebilir.*"
        )

    except Exception as e:
        await msg.edit_text(f"❌ Bir hata oluştu: {str(e)}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
