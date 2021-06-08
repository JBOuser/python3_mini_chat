import threading
import OwnSocket

HOST = "127.0.0.1"
PORT = 3636
ENCODING = "utf-8"
SIZE_MESSAGE_BYTES = 1024


def allow_or_deny_comms(client, msg):
    if msg.upper().startswith(OwnSocket.OK):

        print("Client status: {}".format(msg))
        if allow_or_deny_menu():
            open_chat(client, msg)
        else:
            client.send(OwnSocket.DOWN.encode(ENCODING))
            msg = client.recv(SIZE_MESSAGE_BYTES).decode(ENCODING)
            print("Client closed ({})".format(msg))
    else:
        client.send(OwnSocket.EXIT.encode(ENCODING))    


def allow_or_deny_menu():
    print("\t\nSTART CHAT MENU")
    print("1.Yes")
    print("2.No")
    
    chosen_option = input("Choose an option: ")
    print("")

    """
    Ternary: 
    return True if chosen_option.startswith("1") is True, 
    otherwise return False
    """
    return True if chosen_option.startswith("1") else False


def open_chat(client, msg):
    client.send(OwnSocket.UP.encode(ENCODING))
    keep_chat(client, msg)


def keep_chat(client, msg):

    chat_opened = True
    while chat_opened:

        print("Waiting Client ... ('exit' to close Chat)")

        msg = client.recv(SIZE_MESSAGE_BYTES).decode(ENCODING)
        print("From Client: {}".format(msg))
        
        if msg.upper().startswith(OwnSocket.EXIT):
            chat_opened = False
            break

        msg = write_message(client)
        while not check_message_size(msg):
            print("Message Max Size {}. Try Again".format(SIZE_MESSAGE_BYTES))
            msg = write_message(client)

        client.send(msg.encode(ENCODING))

        if msg.upper().startswith(OwnSocket.EXIT):
            chat_opened = False
            break
        
        
def write_message(client):
    return str(input("Server> "))


def check_message_size(msg):
    return True if len(msg.encode(ENCODING)) <= SIZE_MESSAGE_BYTES else False


def run():
    serverSocket = OwnSocket.create_server(HOST, PORT)
    client,address = serverSocket.accept()
    
    msg = client.recv(SIZE_MESSAGE_BYTES).decode(ENCODING)
    allow_or_deny_comms(client, msg)
    
    OwnSocket.try_close(client)
    OwnSocket.try_close(serverSocket)

    print("Chat Closed")


if __name__=='__main__':
    run()
