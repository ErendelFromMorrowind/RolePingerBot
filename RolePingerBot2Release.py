import json
import time
import threading
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler







def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Этот бот умеет создавать роли и пинговать всех людей, которые добавлены к этой роли\n\nОчень рекомендуется создать роль all и добавить туда всех участников чата, чтобы бот не считал их несуществующей ролью.\nЧтобы вызывать людей по + для игры в свою игру, создайте роль \"gosvoyak\"")
    fulllist = read()
    if (str(update.effective_chat.id) in fulllist) == False:
        fulllist[str(update.effective_chat.id)] = {}
        fulllist[str(update.effective_chat.id)]["svoyak"] = True
        writetojson(fulllist)

def read():
    with open('rolebot.json', 'r') as fp:
        fulllist = json.load(fp)
    return fulllist

def turnsvoyak(update, context):
    fulllist = read()
    chatinfo = fulllist[str(update.effective_chat.id)]
    if "svoyak?" in chatinfo:
        if chatinfo["svoyak?"] == True:
            chatinfo["svoyak?"] = False
            fulllist[str(update.effective_chat.id)] = chatinfo
            writetojson(fulllist)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Пинг роли gosvoyak по плюсу выключен")
        else:
            chatinfo["svoyak?"] = True
            fulllist[str(update.effective_chat.id)] = chatinfo
            writetojson(fulllist)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Пинг роли gosvoyak по плюсу включён")
    else:
        chatinfo["svoyak?"] = True
        context.bot.send_message(chat_id=update.effective_chat.id, text="Пинг роли gosvoyak по плюсу включён")
        fulllist[str(update.effective_chat.id)] = chatinfo
        writetojson(fulllist)

def turnSvoyakNoMsg(chatinfo):
    if "svoyak?" in chatinfo:
        if chatinfo["svoyak?"] == True:
            chatinfo["svoyak?"] = False
            return chatinfo
        else:
            chatinfo["svoyak?"] = True
            return chatinfo
    else:
        chatinfo["svoyak?"] = True
        return chatinfo

def writetojson(data):
    with open('rolebot.json', 'w') as fp:
        json.dump(data, fp)

def pingSvoyak(update, context, text):
    listofusers = []
    fulllist = read()
    ct = 0
    pingtxt = ''
    roles = fulllist[str(update.effective_chat.id)]
    svoyak = roles["svoyak?"]
    if svoyak == True and "gosvoyak" in roles:
        listofusers = roles["gosvoyak"]
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

def getRole(text):
    startnum = text.find('@')
    #print(text)
    text = text[startnum+1:]
    #print(text)
    rolename = ''
    for symb in text:
        if checkAllowed(symb) == True:
            rolename += symb
    return rolename
    

def ping(update, context):
    text = update.message.text
    if text == '+':
        pingSvoyak(update, context, text)
        return
    if '@' in text:
        rolename = getRole(text)
        fulllist = read()
        roles = fulllist[str(update.effective_chat.id)]
        pingtxt = ""
        ct = 0
        listofusers = []
        if rolename in roles:
            for s in roles:
                if s == rolename:
                    listofusers = roles[s]
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

def massGetNames(text):
    names = text.split()
    names.pop(len(names)-1)
    names[0] = names[0][1:]
    names[len(names)-1] = names[len(names)-1][0:-1]
    return names
    
def addtorole(update, context):
    fulllist = read()
    if (str(update.effective_chat.id) in fulllist) == False:
        fulllist[str(update.effective_chat.id)] = {}
    roles = fulllist[str(update.effective_chat.id)]
    text = update.message.text
    text = text[5:]
    arr = text.split()
    name = arr[0]
    role = arr[len(arr)-1]
    #print(role)
    if role in roles:
        if name[0] != "(":
            roles[role].append(name)
            fulllist[str(update.effective_chat.id)] = roles
            writetojson(fulllist)
            context.bot.send_message(chat_id=update.effective_chat.id, text = "Пользователь " + name + " добавлен к роли "+ role)
        else:
            names = massGetNames(text)
            #print(names)
            for name in names:
                roles[role].append(name)
                #print(name)
                context.bot.send_message(chat_id=update.effective_chat.id, text = "Пользователь " + name + " добавлен к роли "+ role)
            fulllist[str(update.effective_chat.id)] = roles
            writetojson(fulllist)
    else:
            context.bot.send_message(chat_id=update.effective_chat.id, text = "Такой роли не существует")

#def silentadd(update, context):
    

def checkAllowed(text):
    allowedlist = ['_', '@', '+', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', 'ё', '1','2','3','4','5','6','7','8','9','0']
    for symb in text:
        if (not symb in allowedlist):
            if not symb.lower() in allowedlist:
                return False
    return True

def newrole(update, context):
    fulllist = read()
    if (str(update.effective_chat.id) in fulllist) == False:
        fulllist[str(update.effective_chat.id)] = {}
    roles = fulllist[str(update.effective_chat.id)]
    text = update.message.text
    text = text[9:]
    if checkAllowed(text) == True:
        if text in roles:
            context.bot.send_message(chat_id=update.effective_chat.id, text = "Такая роль уже существует")
        else:
            roles[text] = []
            fulllist[str(update.effective_chat.id)] = roles
            writetojson(fulllist)
            context.bot.send_message(chat_id=update.effective_chat.id, text = "Pоль " + text + " добавлена")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text = "Роль содержит недопустимые символы")

def deletefromrole(update, context):
    fulllist = read()
    if (str(update.effective_chat.id) in fulllist) == False:
        fulllist[str(update.effective_chat.id)] = {}
    roles = fulllist[str(update.effective_chat.id)]
    text = update.message.text[8:]
    arr = text.split()
    name = arr[0]
    role = arr[len(arr)-1]
    if role in roles:
        if name[0] != '(':
            if name in roles[role]:
                roles[role].remove(name)
                fulllist[str(update.effective_chat.id)] = roles
                writetojson(fulllist)
                context.bot.send_message(chat_id=update.effective_chat.id, text = "Пользователь " + name + " удалён из роли "+ role)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text = "Пользователь " + name + " отсутствеут в роли "+ role)
        else:
            names = massGetNames(text)
            for name in names:
                if name in roles[role]:
                    roles[role].remove(name)
                    context.bot.send_message(chat_id=update.effective_chat.id, text = "Пользователь " + name + " удалён из роли "+ role)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text = "Пользователь " + name + " отсутствеут в роли "+ role)
            fulllist[str(update.effective_chat.id)] = roles
            writetojson(fulllist)
            
                
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
    fulllist = read()
    if (str(update.effective_chat.id) in fulllist) == False:
        fulllist[str(update.effective_chat.id)] = {}
    roles = fulllist[str(update.effective_chat.id)]
    text = update.message.text[13:]
    if text in roles:
        txt = ""
        for role in roles:
            if text == role:
                users = roles[text]
        for user in users:
            if user[0] == '@':
                txt += user[1:]
            else:
                txt += user
            txt += " "
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
    dp.add_handler(CommandHandler("turnsvoyak", turnsvoyak))
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
