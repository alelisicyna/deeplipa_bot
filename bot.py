# --LIBRARIES--
# telebot: https://pypi.org/project/pyTelegramBotAPI/
# deepl-translate: https://github.com/ptrstn/deepl-translate
# eng_to_ipa: https://github.com/mphilli/English-to-IPA
# lingua-language-detector: https://github.com/pemistahl/lingua-py
# phon_polish: https://github.com/lukyjanek/phonetic-transcription


import telebot
import deepl
import eng_to_ipa as ipa
from lingua import Language, LanguageDetectorBuilder
from phon_polish import ipa_polish


languages = [Language.ENGLISH, Language.RUSSIAN, Language.POLISH]
detector = LanguageDetectorBuilder.from_languages(*languages).build()

bot = telebot.TeleBot(str(input('TOKEN: ')))


class Translator:
    def __init__(self, text):
        self.text = text

    def ru(self):
        translate_en: str = deepl.translate(
            source_language="RU",
            target_language="EN",
            text=self.text,
            formality_tone="informal"
        )
        translate_en_ipa: str = ipa.convert(translate_en)
        translate_pl: str = deepl.translate(
            source_language="RU",
            target_language="PL",
            text=self.text,
            formality_tone="informal"
        )
        translate_pl_ipa: str = ipa_polish(translate_pl)
        result: str = f'''
🇷🇺 Russian -> 🇺🇸 English and 🇵🇱 Polish\n\n
🇺🇸 `{translate_en}`
🇺🇸 IPA: {translate_en_ipa}
🇵🇱 `{translate_pl}`
🇵🇱 IPA: {translate_pl_ipa}\n\n
✂️ Click on the translation text to copy'''

        return result

    def en(self):
        IPA: str = ipa.convert(self.text)
        translate_ru: str = deepl.translate(
            source_language="EN",
            target_language="RU",
            text=self.text,
            formality_tone="informal"
        )
        translate_pl: str = deepl.translate(
            source_language="EN",
            target_language="PL",
            text=self.text,
            formality_tone="informal"
        )
        translate_pl_ipa: str = ipa_polish(translate_pl)
        result: str = f'''
🇺🇸 English -> 🇷🇺 Russian and 🇵🇱 Polish\n
🇺🇸 IPA: {IPA}\n\n
🇷🇺 `{translate_ru}`
🇵🇱 `{translate_pl}`
🇵🇱 IPA: {translate_pl_ipa}\n\n
✂️ Click on the translation text to copy'''

        return result

    def pl(self):
        IPA: str = ipa_polish(self.text)
        translate_ru: str = deepl.translate(
            source_language="PL",
            target_language="RU",
            text=self.text,
            formality_tone="informal"
        )
        translate_en: str = deepl.translate(
            source_language="PL",
            target_language="EN",
            text=self.text,
            formality_tone="informal"
        )
        translate_en_ipa: str = ipa.convert(translate_en)
        result: str = f'''
🇵🇱 Polish -> 🇷🇺 Russian and 🇺🇸 English\n
🇵🇱 IPA: {IPA}\n\n
🇷🇺 `{translate_ru}`
🇺🇸 `{translate_en}`
🇺🇸 IPA: {translate_en_ipa}\n\n
✂️ Click on the translation text to copy'''

        return result


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,"Hi 👋!\nI support: 🇺🇸🇵🇱🇷🇺\n\nSend me a message!")


@bot.message_handler(content_types=['text'])
def message_translate(message):
    result: str = None
    print(f'@{message.from_user.username}: {message.text}')
    if str(detector.detect_language_of(message.text)) == 'Language.RUSSIAN':
        result = Translator(message.text).ru()
    elif str(detector.detect_language_of(message.text)) == 'Language.ENGLISH':
        result = Translator(message.text).en()
    elif str(detector.detect_language_of(message.text)) == 'Language.POLISH':
        result = Translator(message.text).pl()
    
    bot.send_message(message.chat.id, result, parse_mode="MARKDOWN")


if __name__ == '__main__':
    print("TELEGRAM BOT IS WORKING")
    bot.polling()
