import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from github import Github

# BURAYI DÜZENLE: Kendi kodlarını tırnakların içine yapıştır
TOKEN = "8200931811:AAGNfRjoSzenGynnlWOZFHDc48UhEHcOSeQ"
GITHUB_TOKEN = "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"

bot = Bot(token=TOKEN.strip()) # strip() komutu sayesinde gizli boşluklar silinir
dp = Dispatcher()
g = Github(GITHUB_TOKEN.strip())

@dp.message(Command("start"))
async def start(m: Message):
    await m.answer("✅ **Bot Aktif!**\nBana bir HTML kodu gönder, hemen siteni kurayım.")

@dp.message()
async def build_site(m: Message):
    if not m.text or "<html>" not in m.text.lower():
        return
    
    msg = await m.answer("⏳ Site hazırlanıyor...")
    try:
        user = g.get_user()
        repo_name = f"site-{m.from_user.id}"
        
        try:
            repo = user.get_repo(repo_name)
        except:
            repo = user.create_repo(repo_name)

        try:
            contents = repo.get_contents("index.html")
            repo.update_file("index.html", "Update", m.text, contents.sha)
        except:
            repo.create_file("index.html", "Create", m.text)

        await msg.edit_text(f"🚀 **Siten Hazır!**\n🔗 https://{user.login}.github.io/{repo_name}/")
    except Exception as e:
        await msg.edit_text(f"❌ Hata: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
