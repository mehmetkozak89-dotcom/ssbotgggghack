import telebot
import sys
import io
import contextlib

# Buraya kendi bot tokenını yapıştır
TOKEN = "8200931811:AAGNfRjoSzenGynnlWOZFHDc48UhEHcOSeQ"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🐍 Python Kod Yürütücüye Hoş Geldiniz!\n\nÇalıştırmak istediğiniz kodu direkt mesaj olarak gönderin.")

@bot.message_handler(func=lambda message: True)
def execute_python(message):
    code = message.text
    
    # Çıktıyı yakalamak için io nesnesi kullanıyoruz
    output_buffer = io.StringIO()
    
    bot.send_chat_action(message.chat.id, 'typing')
    
    try:
        # Kodun çıktısını (print) yakalamak için redirect_stdout kullanıyoruz
        with contextlib.redirect_stdout(output_buffer):
            # Kodu yürüt
            # Not: Gerçekten çalıştırması için exec() kullanıyoruz
            exec(code, {'__builtins__': __builtins__}, {})
        
        result = output_buffer.getvalue()
        
        if result:
            bot.reply_to(message, f"📤 **Çıktı:**\n\n```python\n{result}\n```", parse_mode="Markdown")
        else:
            bot.reply_to(message, "✅ Kod başarıyla çalıştırıldı (Herhangi bir çıktı/print üretilmedi).")
            
    except Exception as e:
        # Hata oluşursa hatayı kullanıcıya gönder
        bot.reply_to(message, f"❌ **Hata Oluştu:**\n\n```text\n{str(e)}\n```", parse_mode="Markdown")

if __name__ == "__main__":
    print("Bot başlatıldı...")
    bot.polling(none_stop=True)
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
    asyncio.run(mtokenınını
