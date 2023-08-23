import socket
import os


# UNIXドメインソケットとデータグラム（非接続）ソケットを作成します
sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

# サーバのアドレスを定義します。
# サーバはこのアドレスでメッセージを待ち受けます
server_address = '127.0.0.1:8765'

# このクライアントのアドレスを定義します。
# サーバはこのアドレスにメッセージを返します
address = '127.0.0.1:3000'

try:
    # もし前回の実行でソケットファイルが残っていた場合、そのファイルを削除します。
    os.unlink(address)
except FileNotFoundError:
    # ファイルが存在しない場合は何もしません。
    pass
# サーバに送信するメッセージを定義します
input = input("> ")

# このクライアントのアドレスをソケットに紐付けます。
# これはUNIXドメインソケットの場合に限ります。
# このアドレスは、サーバによって送信元アドレスとして受け取られます。
sock.bind(address)

try:
    # サーバにメッセージを送信します
    print('sending {!r}'.format(input))
    # 入力値が文字列なのでbytesに変換して送る
    sent = sock.sendto(input.encode('utf-8'), server_address)

    # サーバからの応答を待ち受けます
    print('waiting to receive')
    # 最大4096バイトのデータを受け取ります
    data, server = sock.recvfrom(4096)

    # サーバから受け取ったメッセージを表示します
    # 受け取る値がbytesなので文字列の変換する
    print('received {!r}'.format(data.decode('utf-8')))

finally:
    # 最後にソケットを閉じてリソースを解放します
    print('closing socket')
    sock.close()
