import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from github import Github

# --- GÜVENLİK İÇİN YENİ TOKENINI BURAYA YAZ ---
TOKEN = "8200931811:AAGNfRjoSzenGynnlWOZFHDc48UhEHcOSeQ"
GITHUB_TOKEN = "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"

bot = Bot(token=TOKEN)
dp = Dispatcher()
g = Github(GITHUB_TOKEN)

@dp.message(Command("start"))
async def start(m: Message):
    await m.answer("🌐 **Gerçek Site Kuran Bot**\n\nKullanım: `/kur siteadi` yazın, saniyeler içinde sitenizi yayına alayım!")

@dp.message(Command("kur"))
async def create_site(m: Message):
    args = m.text.split()
    if len(args) < 2:
        return await m.reply("❌ Lütfen bir isim yazın! Örn: `/kur harikasite`")

    site_name = args[1].lower().strip().replace(" ", "-")
    user = g.get_user()
    msg = await m.answer(f"⏳ `{site_name}` internete yükleniyor...")

    try:
        # Yeni depo oluşturma
        repo = user.create_repo(site_name)
        
        # Hazır site içeriği
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"><title>Sitem</title></head>
        <body style="text-align:center; padding:50px; font-family:sans-serif;">
            <h1>🚀 {site_name} Yayında!</h1>
            <p>Bu site bot aracılığıyla otomatik kurulmuştur.</p>
        </body>
        </html>
        """
        
        # Dosyayı yükle
        repo.create_file("index.html", "Initial commit", html_content, branch="main")
        
        # Site linki
        site_url = f"https://{user.login}.github.io/{site_name}/"
        
        await msg.edit_text(
            f"✅ **Siteniz Kuruldu!**\n\n🔗 **Link:** {site_url}\n\n"
            "⚠️ *Not: Sitenin aktifleşmesi 1-2 dakika sürebilir.*",
            disable_web_page_preview=True
        )

    except Exception as e:
        await msg.edit_text(f"❌ Hata: {str(e)}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
