import Server 
import OwnSocket

def start_chat(client, msg):
    if msg.upper().startswith(OwnSocket.UP):
        open_chat(client, msg)
    else:
        client.send(OwnSocket.EXIT.encode(Server.ENCODING))


def open_chat(client, msg):

    chat_opened = True
    while chat_opened:
        
        msg = write_message(client)
        while not check_message_size(msg):
            print("Message Max Size {}. Try Again".format(Server.SIZE_MESSAGE_BYTES))
            msg = write_message(client)

        client.send(msg.encode(Server.ENCODING))

        if msg.upper().startswith(OwnSocket.EXIT):
            chat_opened = False
            break

        print("Waiting Server ... ('exit' to close Chat)")

        msg = client.recv(Server.SIZE_MESSAGE_BYTES).decode(Server.ENCODING)
        print("From Server: {}".format(msg))

        if msg.upper().startswith(OwnSocket.EXIT):
            chat_opened = False
            break


def write_message(client):
    return str(input("Client> "))


def check_message_size(msg):
    return True if len(msg.encode(Server.ENCODING)) <= Server.SIZE_MESSAGE_BYTES else False


def run():

    try:
        clientSocket = OwnSocket.create_client(Server.HOST, Server.PORT)
        print("Wating Server authorization ...")
        clientSocket.send(OwnSocket.OK.encode(Server.ENCODING))

        msg = clientSocket.recv(Server.SIZE_MESSAGE_BYTES).decode(Server.ENCODING)
        print("Server Chat Status: {}".format(msg))
        start_chat(clientSocket, msg)

        OwnSocket.try_close(clientSocket)

        print("Chat Closed")    
    
    except ConnectionRefusedError:
        print("Server.py is NOT running")    


if __name__=='__main__':
    run()
