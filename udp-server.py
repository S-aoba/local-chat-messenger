import socket
import os
from faker import Faker

# socket.socket関数を使用して、新しいソケットを作成します。
# AF_UNIXはUNIXドメインソケットを表し、SOCK_DGRAMはデータグラムソケットを表します。
sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

# サーバが接続を待ち受けるUNIXドメインソケットのパスを指定します。
server_address = '127.0.0.1:8765'

try:
    # もし前回の実行でソケットファイルが残っていた場合、そのファイルを削除します。
    os.unlink(server_address)
except FileNotFoundError:
    # ファイルが存在しない場合は何もしません。
    pass

# ソケットが起動していることを表示します。
print('starting up on {}'.format(server_address))

# sockオブジェクトのbindメソッドを使って、ソケットを特定のアドレスに関連付けます。
sock.bind(server_address)

# ソケットはデータの受信を永遠に待ち続けます。
while True:
    print('\nwaiting to receive message')

    # ソケットからのデータを受信します。
    # 4096は一度に受信できる最大バイト数です。
    data, address = sock.recvfrom(4096)

    # 受信したデータのバイト数と送信元のアドレスを表示します。
    print('received {} bytes from {}'.format(len(data), address))
    print(data)

    # 受信したデータをそのまま送信元に送り返します。
    if data:
        # 'ja_JPでlocalを日本に設定'
        fake = Faker('ja_JP')
        # 入力値が文字列なのでbytesに変換して送る
        # 名前以外にもあるので下記URL参照
        # https://faker.readthedocs.io/en/master/providers.html

        sent = sock.sendto(fake.name().encode('utf-8'), address)
        # 送信したバイト数と送信先のアドレスを表示します。
        print('sent {} bytes back to {}'.format(sent, address))
