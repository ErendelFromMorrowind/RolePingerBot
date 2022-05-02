import json
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler        

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Этот бот умеет создавать роли и пинговать всех людей, которые добавлены к этой роли\n\nОчень рекомендуется создать роль all и добавить туда всех участников чата, чтобы бот не считал их несуществующей ролью")
    fulllist = read()
    if (str(update.effective_chat.id) in fulllist) == False:
        fulllist[str(update.effective_chat.id)] = {}
        print("started")
        writetojson(fulllist)

def read():
    with open('rolebot.json', 'r') as fp:
        fulllist = json.load(fp)
    return fulllist


def writetojson(data):
    #print(fulllist)
    #fulllist[str(chatId)] = par
    with open('rolebot.json', 'w') as fp:
        json.dump(data, fp)

def ping(update, context):
    fulllist = read()
    roles = fulllist[str(update.effective_chat.id)]
    pingtxt = ""
    ct = 0
    isInAll = False
    listofusers = []
    text = update.message.text
    #print("text read")
    if text[0] == '+':
        print("tryin' to gosvoyak")
        if "gosvoyak" in roles:
            print("gosvoyak in roles")
            listofusers = roles["gosvoyak"]
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text = "Роли gosvoyak не существует")
    elif text[0] == "@":
        text = text[1:]
        if text in roles:
            for s in roles:
                if s == text:
                    listofusers = roles[s]
        else:
            if "all" in roles:
                print("all in roles")
                for s in roles["all"]:
                    print(s)
                    if s[1:] == text:
                        isInAll = True
                        print("got")
                        break;
            if isInAll == False:
                context.bot.send_message(chat_id=update.effective_chat.id, text = "Такой роли не существует")

    for user in listofusers:
            ct += 1
            if ct < 8:
                pingtxt += user
                pingtxt += " "
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text = pingtxt)
                pingtxt = user
                pingtxt += " "
                ct = 0
    context.bot.send_message(chat_id=update.effective_chat.id, text = pingtxt)

        
def addtorole(update, context):
    fulllist = read()
    if (str(update.effective_chat.id) in fulllist) == False:
        fulllist[str(update.effective_chat.id)] = {}
    roles = fulllist[str(update.effective_chat.id)]
    text = update.message.text
    text = text[5:]
    arr = text.split()
    name = arr[0]
    role = arr[1]
    if role in roles:
        roles[role].append(name)
        fulllist[str(update.effective_chat.id)] = roles
        writetojson(fulllist)
        context.bot.send_message(chat_id=update.effective_chat.id, text = "Пользователь " + name + " добавлен к роли "+ role)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text = "Такой роли не существует")
    
def newrole(update, context):
    fulllist = read()
    if (str(update.effective_chat.id) in fulllist) == False:
        fulllist[str(update.effective_chat.id)] = {}
    roles = fulllist[str(update.effective_chat.id)]
    text = update.message.text
    text = text[9:]
    if text in roles:
        context.bot.send_message(chat_id=update.effective_chat.id, text = "Такая роль уже существует")
    else:
        roles[text] = []
        fulllist[str(update.effective_chat.id)] = roles
        writetojson(fulllist)
        context.bot.send_message(chat_id=update.effective_chat.id, text = "Pоль " + text + " добавлена")

def deletefromrole(update, context):
    fulllist = read()
    if (str(update.effective_chat.id) in fulllist) == False:
        fulllist[str(update.effective_chat.id)] = {}
    roles = fulllist[str(update.effective_chat.id)]
    text = update.message.text[8:]
    arr = text.split()
    name = arr[0]
    role = arr[1]
    roles[role].remove(name)
    print(role)
    print(name)
    fulllist[str(update.effective_chat.id)] = roles
    writetojson(fulllist)
    context.bot.send_message(chat_id=update.effective_chat.id, text = "Пользователь " + name + " удалён из роли "+ role)
    
def deleterole(update, context):
    fulllist = read()
    if (str(update.effective_chat.id) in fulllist) == False:
        fulllist[str(update.effective_chat.id)] = {}
    roles = fulllist[str(update.effective_chat.id)]
    text = update.message.text[13:]
    del roles[text]
    fulllist[str(update.effective_chat.id)] = roles
    writetojson(fulllist)
    context.bot.send_message(chat_id=update.effective_chat.id, text = "Роль "+text+ " удалена")

def listofroles(update, context):
    fulllist = read()
    if (str(update.effective_chat.id) in fulllist) == False:
        fulllist[str(update.effective_chat.id)] = {}
    roles = fulllist[str(update.effective_chat.id)]
    txt = ""
    for role in roles:
        txt += role
        txt += "\n"
    if txt == " ":
        context.bot.send_message(chat_id=update.effective_chat.id, text = "Нет ролей")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text = txt)
    
def test(update, context):
    print("Ищу")
    fulllist = read()
    if (str(update.effective_chat.id) in fulllist) == False:
        fulllist[str(update.effective_chat.id)] = {}
    roles = fulllist[str(update.effective_chat.id)]
    text = update.message.text[13:]
    print (text)
    if text in roles:
        txt = ""
        for role in roles:
            if text == role:
                users = roles[text]
        for user in users:
            txt += user[1:]
            txt += " "
            print("text+")
            print("txt = " + txt)
        if txt != "":
            context.bot.send_message(chat_id=update.effective_chat.id, text = txt)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text = "Пользователей с такой ролью не существет")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text = "Такой роли не существует")

    

def main():
    updater = Updater("5383392389:AAHbOgPgnkkL_qxBPLlvGCvM1KoOtgLy_is")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("add", addtorole))
    dp.add_handler(CommandHandler("newrole", newrole))
    dp.add_handler(CommandHandler("rolelist", listofroles))
    dp.add_handler(CommandHandler("delete", deletefromrole))
    dp.add_handler(CommandHandler("deleterole", deleterole))
    dp.add_handler(CommandHandler("usersinrole", test))
    dp.add_handler(MessageHandler(Filters.text, ping))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main() 
