from stockfishpy import *
import telebot

token = ''  # Telegram token
bot = telebot.TeleBot(token)
chessEngine = stockfishpy.Engine(
    'stockfishpath', param={'Threads': 2, 'Ponder': 'true'})
chessEngine.uci()


def call_stockfish_engine(message):
    if chessEngine.isready() == 'readyok':
	    chessEngine.ucinewgame()
	    chessEngine.setposition(message)
	    move = chessEngine.bestmove()
	    return move['bestmove']
	else: return 'Chess Engine not readyok'


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
     if re.match('\s*([rnbqkpRNBQKP1-8]+\/){7}([rnbqkpRNBQKP1-8]+)\s[bw-]\s(([a-hkqA-HKQ]{1,4})|(-))\s(([a-h][36])|(-))\s\d+\s\d+\s*', message.text):
        move = call_stockfish_engine(message.text)
        bot.send_message(message.chat.id, move)
    else:
        move = 'Put right positition'
        bot.send_message(message.chat.id, move)


if __name__ == '__main__':
    bot.polling(none_stop=True)
