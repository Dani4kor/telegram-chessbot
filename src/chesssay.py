from stockfishpy import *
import telebot

token = ''  # Telegram token
bot = telebot.TeleBot(token)
chessEngine = stockfishpy.Engine(
    'stockfishpath', param={'Threads': 2, 'Ponder': 'true'})


def call_stockfish_engine(message):
    chessEngine.uci()
    chessEngine.isready()
    chessEngine.ucinewgame()
    chessEngine.setposition(message)
    move = chessEngine.bestmove()
    return move['bestmove']


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, call_stockfish_engine(message.text))


if __name__ == '__main__':
    bot.polling(none_stop=True)
