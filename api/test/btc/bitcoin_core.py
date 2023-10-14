from bitcoin.rpc import Proxy

# Укажите настройки для вашего bitcoind RPC-сервера
rpc_user = 'ваш_пользователь'
rpc_password = 'ваш_пароль'
rpc_host = '127.0.0.1'  # IP-адрес вашего bitcoind сервера
rpc_port = 8332  # Порт вашего bitcoind RPC

# Создайте объект для взаимодействия с RPC-сервером


def get_balance_address(address, wallet_name):
    from bitcoin.wallet import CBitcoinAddress
    from bitcoin.rpc import RawProxy
    try:
    # Получение информации о кошельке
        p = RawProxy(f'http://username:password@localhost:18443/wallet/{wallet_name}')
        balance = p.getreceivedbyaddress(address)
        print(f"Баланс адреса {address}: {balance} BTC")
    except Exception as e:
        print(f'Ошибка при получении информации о кошельке {wallet_name}: {e}')


def generate_new_address(wallet_name):

    from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
    rpc_connection = AuthServiceProxy(f'http://username:password@localhost:18443/wallet/{wallet_name}')
    address = rpc_connection.getnewaddress()
    return address


def get_address_info(address, wallet_name):
    from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
    rpc_connection = AuthServiceProxy(f'http://username:password@localhost:18443/wallet/{wallet_name}')
    address = rpc_connection.getaddressinfo(address)
    print(address)
    return address

def get_address_walellet(wallet_name):
    from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
    rpc_connection = AuthServiceProxy(f'http://username:password@localhost:18443/wallet/{wallet_name}')

    try:
        address = rpc_connection.getaddressesbylabel('')
        print('Информация о кошельке', wallet_name, ':', address)
        print('адреса')
        for i in address.keys():
            print(i)
            get_balance_address(i, wallet_name)
    except Exception as e:
        print(f'Ошибка при получении информации о кошельке {wallet_name}: {e}')


def send_transaction(wallet_name, amount, address):
    from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
    rpc_connection = AuthServiceProxy(f'http://username:password@localhost:18443/wallet/{wallet_name}')
    try:
        txid = rpc_connection.sendtoaddress(address, amount)
        print(f'Отправлена транзакция {txid}')
    except Exception as e:
        print(f'Ошибка при отправке транзакции: {e}')


def generate_to_address(wallet_name, address):
    """
      'Намайнить' новую криптовалюту на выбранный адрес.
      {в нашем случае это необходмо, чтобы обновить информацию в regtest блокчейне} 
    """
    from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
    rpc_connection = AuthServiceProxy(f'http://username:password@localhost:18443/wallet/{wallet_name}')
    try:
        txid = rpc_connection.generatetoaddress(1, address)
        print(f'Отправлена транзакция {txid}')
    except Exception as e:
        print(f'Ошибка при отправке транзакции: {e}')

adress = generate_new_address('gagtain')
print(adress)
send_transaction('gagtain', 0.03, adress)
generate_to_address(1, 'bcrt1ql2n0sm650jz92h9mnf3srthppjv8qq93xqy3zw')
get_address_walellet('gagtain')



