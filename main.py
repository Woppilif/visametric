from flask import Flask, request
import telepot
import urllib3
import visa
'''
proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))
'''
secret = "A_SECRET_NUMBER"
bot = telepot.Bot('')
bot.setWebhook("https://ea2e68b6.ap.ngrok.io/{}".format(secret), max_connections=1)

app = Flask(__name__)

@app.route('/{}'.format(secret), methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        if "text" in update["message"]:
            text = update["message"]["text"]

            if text == '/start':
                bot.sendMessage(chat_id, "Hello, there! This is a VISAMETRIC.COM Telegram bot. Use command /check <pass_id> <barcode> to get info about your visa status! (RUSSIA - GERMANY)\n If you need bot for other countries contact me @woppilif")
            elif '/check' in text:
                text = text.split(' ')
                if len(text) != 3:
                    bot.sendMessage(chat_id, "Sorry, feels like incorrect command!")
                    return "OK"
                try:
                    v = visa.VisaMetric(text[1],text[2])
                    answer = v.get_info()
                    bot.sendMessage(chat_id, "Dear {0}! {1}".format(answer[1],answer[0]))    
                except: 
                    bot.sendMessage(chat_id, "Error processing your data!")

        else:
            bot.sendMessage(chat_id, "From the web: sorry, I didn't understand that kind of message")
    return "OK"


if __name__ == "__main__":
    app.run()