from django.core.management.base import BaseCommand
import telebot
from shop.models import Book

bot = telebot.TeleBot("6397175533:AAGhiZwqHeQSLQuNlTHqKYwOt9OQMEw8v-w")  # Замените "TOKEN" на свой токен

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello world!")

@bot.message_handler(commands=['products'])
def products(message):
    products = Book.objects.all()
    for product in products:
        bot.send_message(message.chat.id, f"{product.name} - {product.price}")


@bot.message_handler(commands=['add'])
def add_product(message):
    
    command_args = message.text.split()[1:]
    
    if len(command_args) != 2:
        bot.reply_to(message, "Неверный формат команды. Используйте: /add <product_name> <product_price>")
        return

    product_name = command_args[0]
    product_price = command_args[1]

    
    Book.objects.create(name=product_name, price=product_price)
    bot.reply_to(message, f"Товар {product_name} добавлен успешно с ценой {product_price}")



@bot.message_handler(commands=['help'])
def help_command(message):
    commands = [
        "/start - Начать",
        "/products - Показать все товары",
        "/help - Помощь",
        "/add - Добавить новый товар"
       
    ]
    help_text = "\n".join(commands)
    bot.send_message(message.chat.id, f"Available commands:\n\n{help_text}")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Starting bot...")
        bot.polling()
        print("Bot stopped")
