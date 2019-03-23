#!/usr/bin/python
# Telegram Remote-Shell
from datetime import datetime
now = datetime.now()
import telepot,time,os
import qrtools,zbar
inqr = qrtools.QR()
# Telegram senders id
# authorized_senders = "614572543"

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    sender = msg['from']['id']
    f = open('trsh.log', 'a')
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    f.write("Chat-id - "+str(chat_id)+", content_type - "+str(content_type)+", Sender - "+str(sender)+", "+date_time+"\n")
    f.close()
    if (content_type == 'photo') and (os.path.isfile("/tmp/zsyqr")):
        bot.download_file(msg['photo'][-1]['file_id'], '/tmp/file.png')
        output = "Scanning ..."
        inqr.decode("/tmp/file.png")
        bot.sendMessage(chat_id, output)
        bot.sendMessage(chat_id, inqr.data)
        stn = inqr.data.find("/",7)
        zsyinfo = os.popen("head -1 /tmp/zsyqr.info").read()
        os.popen("sed -i '1d' /tmp/zsyqr.info").read()
        zsyinfo = zsyinfo.strip('\n')
        newzsy = "http://"+zsyinfo+inqr.data[stn:]
        bot.sendMessage(chat_id, "New : "+newzsy)
        os.popen("/root/qr.py "+newzsy).read()
        photo = open('/tmp/photo.png', 'rb')
        bot.sendPhoto(chat_id, photo)
        output = os.popen("cat /tmp/zsyqr.info|wc -l").read()
        output = output.strip('\n')
        bot.sendMessage(chat_id, newzsy)
        bot.sendMessage(chat_id,"The domain also has : "+output)
        os.popen("rm -rf /tmp/zsyqr").read()
    elif content_type == 'text':
        text = msg['text']
        args=text.split()
        command = args[0]
        if command == '/zsy':
            os.popen("rm -rf /tmp/zsyqr").read()
            os.popen("touch /tmp/zsyqr").read()
            bot.sendMessage(chat_id, "Please sent image")
        else:
            bot.sendMessage(chat_id, "Error input wait for 10 Seconds")
            time.sleep(10)
            os.popen("cd /root;kill `ps -ef |grep zsyqr.py|grep -v grep|awk '{print $2}'`;python zsyqr.py &").read()
    else:
        bot.sendMessage(chat_id, "Error input wait for 10 Seconds")
        time.sleep(10)
        os.popen("cd /root;kill `ps -ef |grep zsyqr.py|grep -v grep|awk '{print $2}'`;python zsyqr.py &").read()
bot = telepot.Bot('643xxxxxx:AAEBUnNwbywOxxxxxxxxxxx')
bot.message_loop(handle)
while 1:
    time.sleep(10)
