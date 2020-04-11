import logging
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters, CommandHandler

updater = Updater(token='', use_context=True)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

players_results = {}
number_of_rounds = 0
number_of_players = 0

initialized = False

dispatcher = updater.dispatcher


def play(update, context):
    if initialized:
        user_message = update.message.from_user.id
        save_dice_result(user_message, update.message.dice.value)
        if game_finished():
            print_podium()


def print_podium():
    max_sum_player = {}
    for player in players_results:
        max_sum_player[player] = sum(players_results[player])
    print(max_sum_player)


def game_finished():
    global  initialized
    if (len(players_results) < number_of_players):
        return False
    for player in players_results:
        if (len(players_results[player]) < number_of_rounds):
            return False
    initialized = False
    return True


def save_dice_result(player, value):
    global  players_results
    if player not in players_results:
       players_results[player] = []
    print("rounds")
    print(number_of_rounds)
    if check_turn_validity(player):
        players_results[player].append(value)


def check_turn_validity(player):
    global number_of_rounds
    global players_results
    print(str(player) + " played")
    print(len(players_results[player]))
    return len(players_results[player]) <= number_of_rounds -1


def init(update, context):
    print("init")
    if context.args[0].isdigit() and context.args[1].isdigit():
        global number_of_players
        number_of_players = int(context.args[0]) + 1
        global number_of_rounds
        number_of_rounds = int(context.args[1])
        global initialized
        initialized = True

        for i in range(0, number_of_rounds):
            message = context.bot.send_dice(chat_id=update.effective_chat.id)
            save_dice_result("bot", message.dice.value)

    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Usage:  /play {numbers_of_players} {numbers_of_rounds}")


players_results["bot"] = []

init_handler = CommandHandler("play", init)
play_handler = MessageHandler(Filters.dice, play)

dispatcher.add_handler(init_handler)
dispatcher.add_handler(play_handler)

updater.start_polling();
