import telebot
from telebot import types
import random

TOKEN = "8690617110:AAGmJ-HsmLSX-fSBy6JEduxvk-Ol3TWadBA"

bot = telebot.TeleBot(TOKEN)

choices = ["Rock", "Paper", "Scissors"]
scores = {}
winStreak = {}

ranNumber = {}

solsItems = (
    ("lemon", 2),
    ("cherry", 4),
    ("clover", 8),
    ("bell", 16),
    ("diamond", 32),
    ("treasure chest", 64),
    ("seven", 128),
    ("triple seven", 256),
    ("golden clover", 512),
    ("jackpot", 1024),
)
totalRolls = {}
rarestItem = {}

duelRoom = {
    "players": [],
    "choices": {}
}

def rpsKeyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Rock", "Paper", "Scissors")
    keyboard.add("score", "menu")
    return keyboard

def startKeyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("rock paper scissors", "number guess")
    keyboard.add("chance roll", "math quiz")
    return keyboard

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    bot.send_message(
        message.chat.id,
        "Welcome! Choose a game to play",
        reply_markup=startKeyboard()
    )
@bot.message_handler(func= lambda message: message.text == "menu")
def start(message):
    user_id = message.from_user.id
    bot.send_message(
        message.chat.id,
        "Welcome! Choose a game to play",
        reply_markup=startKeyboard()
    )

@bot.message_handler(func= lambda message: message.text == "math quiz")
def secret(message):
    bot.send_message(message.chat.id, "work in progress", reply_markup=startKeyboard())

@bot.message_handler(func= lambda message: message.text == "rock paper scissors")
def rpsStart(message):
    user_id = message.from_user.id

    if user_id not in scores:
        scores[user_id] = {"user": 0, "bot": 0}
        winStreak[user_id] = 0
    bot.send_message(
        message.chat.id,
        "Rock paper scissors!\nChoose an action to play:",
        reply_markup=rpsKeyboard()
    )

@bot.message_handler(func = lambda message: message.text == "score")
def showScore(message):
    user_id = message.from_user.id
    if user_id in scores:
        user_score = scores[user_id]["user"]
        bot_score = scores[user_id]["bot"]
        streak = winStreak[user_id]

        bot.send_message(
            message.chat.id,
            f"SCORES:\n"
            f"you: {user_score}\n"
            f"bot: {bot_score}\n"
            f"win streak: {streak}"

        )

@bot.message_handler(func=lambda message: message.text in choices)
def rpsPlay(message):

    user_id = message.from_user.id
    chat_id = message.chat.id
    user_choice = message.text
    bot_choice = random.choice(choices)

    if user_id in duelRoom["players"]:
        duelRoom["choices"][user_id] = message.text
        bot.send_message(
            chat_id,
            "duel initiated, waiting for player 2.")

        if len(duelRoom["choices"]) == 2:
            p1,p2 = duelRoom["players"]
            choice1 = duelRoom["choices"][p1]
            choice2 = duelRoom["choices"][p2]

            result = getResult(choice1, choice2)

            bot.send_message(
                chat_id,
                f"player 1: {choice1}\n"
                f"player 2: {choice2}\n\n"
                f"{result}",
            )
            duelRoom["players"].clear()
            duelRoom["choices"].clear()
        return


    if user_choice == bot_choice:
        result = "TIE"
        winStreak[user_id] = 0

    elif (user_choice == "Rock" and bot_choice == "Scissors") or \
         (user_choice == "Scissors" and bot_choice == "Paper") or \
         (user_choice == "Paper" and bot_choice == "Rock"):
        result = "YOU WON"
        scores[user_id]["user"] += 1
        winStreak[user_id] += 1
    else:
        result = "BOT WON"
        winStreak[user_id] = 0
        scores[user_id]["bot"] += 1

    bot.send_message(
        message.chat.id,
        f"you chose: {user_choice}\n"
        f"bot chose: {bot_choice}\n\n"
        f"{result}",
        reply_markup=rpsKeyboard()
    )



def getResult(choice1, choice2):

    if choice1 == choice2:
        return "Draw"
    elif (choice1 == "Rock" and choice2 == "Scissors") or \
            (choice1 == "Scissors" and choice2 == "Paper") or \
            (choice1 == "Paper" and choice2 == "Rock"):
        return "player 1 won!"
    else:
        return "player 2 won!"


@bot.message_handler(commands=['duel'])
def startDuel(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if user_id in duelRoom["players"]:
        bot.send_message(
            chat_id,
            "youre already in a lobby!"

        )
        return
    duelRoom["players"].append(user_id)

    if len(duelRoom["players"]) == 1:
        bot.send_message(
            chat_id,
        "waiting for the second player...")
    elif len(duelRoom["players"]) == 2:
        bot.send_message(
            chat_id,
            "player found, game starting now!",
            reply_markup=rpsKeyboard()
        )

#NUMBER GUESS --------------------------------------------------

def guessKeyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("number guess", "menu")
    return keyboard

variants = ["new number", "menu"]
guessWinFlag = False

@bot.message_handler(func= lambda message: message.text == "number guess")
def guessStart(message):
    userID = message.from_user.id
    ranNumber[userID] = random.randint(1, 100)
    bot.send_message(message.chat.id, "guess the random number from 1 to 100", reply_markup=startKeyboard())

@bot.message_handler(func= lambda message: message.from_user.id in ranNumber)
def guessPlay(message):

    if message.text == "number guess" and guessWinFlag == True:
        return "number guess"
    elif message.text == "number guess" and guessWinFlag == False:
        return
    if message.text == "menu":
        return 
    userID = message.from_user.id
    secret = ranNumber[userID]

    try:
        guess = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "enter whole numbers!", reply_markup=startKeyboard())
        return

    if guess > secret:
        bot.send_message(message.chat.id, "less!", reply_markup=startKeyboard())
    elif guess < secret:
        bot.send_message(message.chat.id, "more!", reply_markup=startKeyboard())
    else:
        bot.send_message(message.chat.id, f"you won! The number was {secret}", reply_markup=startKeyboard())
        del ranNumber[userID]
        guessWinFlag = True

# SOLS RNG -----------------------------------------

def solsKeyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("roll")
    keyboard.add("stats", "menu")
    return keyboard

@bot.message_handler(func= lambda message: message.text == "chance roll")
def solsStart(message):
    bot.send_message(message.chat.id, "Press 'Roll' to spin for an item with a set rarity, the rarer the better!", reply_markup=solsKeyboard())

@bot.message_handler(func= lambda message: message.text == "roll")
def rolling(message):
    userID = message.from_user.id
    roll = random.randint(1, 1024)
    if userID not in totalRolls:
        totalRolls[userID] = 0
    itemID = 0
    rarities = [512,256,128,64,32,16,8,4,2,1]
    cumulative = 0
    for i, r in enumerate(rarities):
        cumulative += r
        if roll <= cumulative:
            itemID = i
            break
    lastRoll = solsItems[itemID]
    if userID not in rarestItem:
        rarestItem[userID] = lastRoll
    elif lastRoll[1] > rarestItem[userID][1]:
        rarestItem[userID] = lastRoll
    totalRolls[userID] += 1
    bot.send_message(message.chat.id, f"You rolled {lastRoll[0]}, 1 in {lastRoll[1]}", reply_markup=solsKeyboard())

@bot.message_handler(func= lambda message: message.text == "stats")
def solsStats(message):
    userID = message.from_user.id
    bot.send_message(message.chat.id, f"total rolls: {totalRolls[userID]}\nrarest item: {rarestItem[userID][0]}, 1 in {rarestItem[userID][1]}", reply_markup=solsKeyboard())

bot.infinity_polling()