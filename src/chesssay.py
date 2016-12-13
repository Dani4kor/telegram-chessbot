from stockfishpy import *
import telebot
import re

token = ''  # Telegram token
bot = telebot.TeleBot(token)
chessEngine = stockfishpy.Engine(
    'stockfishPATH', param={'Threads': 2, 'Ponder': 'true'})
chessEngine.uci()


def fenPass(fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
    regexMatch = re.match('\s*^(((?:[rnbqkpRNBQKP1-8]+\/){7})[rnbqkpRNBQKP1-8]+)\s([b|w])\s([K|Q|k|q]{1,4})\s(-|[a-h][1-8])\s(\d+\s\d+)$', fen)
    if  regexMatch:
        regexList = regexMatch.groups()
        fen = regexList[0].split("/")
        if len(fen) != 8:
            raise ValueError("expected 8 rows in position part of fen: {0}".format(repr(fen)))

        for fenPart in fen:
            field_sum = 0
            previous_was_digit, previous_was_piece = False,False

            for c in fenPart:
                if c in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                    if previous_was_digit:
                        raise ValueError("two subsequent digits in position part of fen: {0}".format(repr(fen)))
                    field_sum += int(c)
                    previous_was_digit = True
                    previous_was_piece = False
                elif c == "~":
                    if not previous_was_piece:
                        raise ValueError("~ not after piece in position part of fen: {0}".format(repr(fen)))
                    previous_was_digit, previous_was_piece = False,False
                elif c.lower() in ["p", "n", "b", "r", "q", "k"]:
                    field_sum += 1
                    previous_was_digit = False
                    previous_was_piece = True
                else:
                    raise ValueError("invalid character in position part of fen: {0}".format(repr(fen)))

            if field_sum != 8:
                raise ValueError("expected 8 columns per row in position part of fen: {0}".format(repr(fen)))  

    else: raise ValueError("fen doesn`t match follow this example: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 ")  


def call_stockfish_engine(message):
    if chessEngine.isready() == 'readyok':
        chessEngine.ucinewgame()
        chessEngine.setposition(message)
        move = chessEngine.bestmove()
        return move['bestmove']
    else: return 'Chess Engine not readyok'




if __name__ == '__main__':
    bot.polling(none_stop=True)
