import telebot
import deepl
import eng_to_ipa as ipa
from lingua import Language, LanguageDetectorBuilder


languages = [Language.ENGLISH, Language.RUSSIAN, Language.POLISH]
detector = LanguageDetectorBuilder.from_languages(*languages).build()

bot = telebot.TeleBot(str(input('TOKEN: ')))


class Translator:
    def __init__(self, text):
        self.text = text

    def rutoother(self):
        translate_en: str = deepl.translate(
            source_language="RU",
            target_language="EN",
            text=self.text,
            formality_tone="informal"
        )
        translate_en_ipa = ipa.convert(translate_en)
        translate_pl: str = deepl.translate(
            source_language="RU",
            target_language="PL",
            text=self.text,
            formality_tone="informal"
        )
        result = f'🇷🇺 Русский -> 🇺🇸 English and 🇵🇱 Polska\n\n🇺🇸 `{translate_en}`\nIPA: {translate_en_ipa}\n\n🇵🇱 `{translate_pl}`\n\n✂️ Нажмите на текст перевода, чтобы скопировать'

        return result

    def entoru(self):
        translate: str = deepl.translate(
            source_language="EN",
            target_language="RU",
            text=self.text,
            formality_tone="informal"
        )
        result = f'🇺🇸 English -> 🇷🇺 Русский\n\n🇷🇺 `{translate}`\n\n✂️ Click on the translation text to copy'

        return result

    def pltoru(self):
        translate: str = deepl.translate(
            source_language="PL",
            target_language="RU",
            text=self.text,
            formality_tone="informal"
        )
        result = f'🇵🇱 Polska -> 🇷🇺 Русский\n\n🇷🇺 `{translate}`\n\n✂️ Kliknij tekst tłumaczenia, aby go skopiować'

        return result


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,"Hi 👋!\nI can speak 🇺🇸English, 🇵🇱Polish, 🇷🇺Russian. Send me a message for translate!")


@bot.message_handler(content_types=['text'])
def message_translate(message):
    print(f'@{message.from_user.username}: {message.text}')
    if str(detector.detect_language_of(message.text)) == 'Language.RUSSIAN':
        result: str = Translator(message.text).rutoother()
        bot.send_message(message.chat.id, result, parse_mode="MARKDOWN")
    elif str(detector.detect_language_of(message.text)) == 'Language.ENGLISH':
        result: str = Translator(message.text).entoru()
        bot.send_message(message.chat.id, result, parse_mode="MARKDOWN")
    elif str(detector.detect_language_of(message.text)) == 'Language.POLISH':
        result: str = Translator(message.text).pltoru()
        bot.send_message(message.chat.id, result, parse_mode="MARKDOWN")


if __name__ == '__main__':
    print("TELEGRAM BOT IS WORKING")
    bot.polling()
