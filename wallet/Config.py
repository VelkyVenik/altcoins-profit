import configparser


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(['config.ini', '../config.ini'])

    def get(self, section, option):
        return self.config.get(section, option)

config = Config()

if __name__ == '__main__':
    print(config.get('CoinBase', 'API_KEY'))
