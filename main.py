import wikipedia
import telebot
import config
import time
wikipedia.set_lang("ru")
print('OnlineHelper is working...')
bot=telebot.TeleBot(config.TOKEN)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,'Здраствуйте! Это онлайн-помощник! Введите, то что вас интересует:')

@bot.message_handler(content_types='text')
@bot.edited_message_handler(content_types='text')
def firstrequest(message):
    global name
    name=message.text
    res = wikipedia.search(name)
    global output
    output=''
    for i, val in enumerate(res, start=1):
        output+=str(i)+' '+str(val)+'\n'
    bot.send_message(message.chat.id,output)
    bot.send_message(message.chat.id, 'Напишите номер пункта, который вас интересует: ')
    bot.register_next_step_handler(message,secondrequest)
def secondrequest(message):
    res = wikipedia.search(name)
    global firstnumber
    firstnumber = int(message.text)
    try:
        text = str(wikipedia.page(res[firstnumber - 1]).content)
    except Exception:
        bot.send_message(message.chat.id,'Извините! Произошла ошибка, попробуйте перезапустить бота /start и задать вопрос корректнее!')
    text = text.replace('====', '==')
    text = text.replace('===', '==')
    global titles
    titles=[]
    while text.count('==')>1:
        firstindex=text.index('==')
        text=text.replace('==','<-',1)
        secondindex=text.index('==')
        text = text.replace('==', '<-', 1)
        title=''
        title+=text[firstindex+3:secondindex-1]
        titles.append(title)
        secondoutput=''
    for j in range(len(titles)):
        secondoutput+=str(j+1)+' '+str(titles[j])+'\n'
    bot.send_message(message.chat.id,secondoutput)
    bot.send_message(message.chat.id,'Введите номер запроса: ')
    bot.register_next_step_handler(message,thirdrequest)
def thirdrequest(message):
    res = wikipedia.search(name)
    secondnumber= int(message.text)
    text=titles[secondnumber-1]
    thirdoutput=wikipedia.page(res[firstnumber-1]).section(text)
    bot.send_message(message.chat.id, text)
    if len(thirdoutput)<3000:
        bot.send_message(message.chat.id,thirdoutput)
    else:
        bot.send_message(message.chat.id,wikipedia.page(res[firstnumber-1]).section(text)[:3000]+'...')
    bot.send_message(message.chat.id, 'Чтобы воспользовать ботом снова, используйте команду /start')

while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15)