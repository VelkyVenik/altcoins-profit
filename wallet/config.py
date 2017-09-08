import configparser

_config = configparser.ConfigParser()
_config.read(['config.ini', '../config.ini'])


def get(section, option):
    return _config.get(section, option)


if __name__ == '__main__':
    print(get('CoinBase', 'API_KEY'))
