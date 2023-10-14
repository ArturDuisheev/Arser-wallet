from tonsdk.contract.wallet import Wallets, WalletVersionEnum
from config import testnet


# mnemonic это пароль к кошельку который генерируется через wallets.create

mnemonics = ['learn', 'bitter', 'enter', 'carpet', 'alter', 'spin', 'vacuum', 'insane', 'relief', 'rival', 'arrange', 'kiwi', 'rifle', 'zero', 'until', 'little', 'duck', 'sad', 'evolve', 'staff', 'aware', 'lake', 'east', 'stuff']

mnemonics, pub_k, priv_k, wallet = Wallets.from_mnemonics(mnemonics=mnemonics, version=WalletVersionEnum.v3r2, workchain=0)


if __name__ == '__main__':
    print(mnemonics)
    # 4 True надо в testnet, 3 True надо в mainnet
    list_true = [True * 4 if testnet else True * 3]
    print(wallet.address.to_string(*list_true))