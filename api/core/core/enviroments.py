from dotenv import load_dotenv, dotenv_values


def init_env():
    """ Функция инициализации переменных окружения """
    load_dotenv("example.env")
    print(dotenv_values("example.env"), 123)
    print(dotenv_values(".env"), 324)
    print('success load env')
