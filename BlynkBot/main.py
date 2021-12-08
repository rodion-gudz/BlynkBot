import configparser

config_path = 'BlynkBot/config.ini'
config = configparser.ConfigParser()
config.read(config_path)
bot_username = config.get('bot', 'bot_username')
bot_token = config.get('bot', 'bot_token')
mongo_url = config.get('bot', 'mongo_url')
admin_email = config.get('blynk', 'admin_email')
admin_password = config.get('blynk', 'admin_password')
blynk_url = config.get('blynk', 'blynk_url')
energy = config.get('blynk', 'energy')
