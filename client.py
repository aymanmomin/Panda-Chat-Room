import socket
import threading

class PandaClient:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = input("Enter your panda name: ")
        self.buffer = b''  # Stores partial incoming data

    def start(self):
        self.client.connect((self.host, self.port))
        self.client.send(self.username.encode('utf-8'))
        threading.Thread(target=self.receive_messages).start()
        self.send_messages()

    def receive_messages(self):
        while True:
            try:
                data = self.client.recv(8192)  # Larger buffer size
                if not data:
                    print("Server closed the connection.")
                    break
                self.buffer += data
                # Attempt to decode the buffer
                while True:
                    try:
                        message = self.buffer.decode('utf-8')
                        print(message)
                        self.buffer = b''  # Clear buffer after full decode
                        break
                    except UnicodeDecodeError:
                        # Save incomplete bytes and wait for more data
                        self.buffer = self.buffer[-3:]  # Keep last 3 bytes (max UTF-8 char size)
                        break
            except Exception as e:
                print(f"Disconnected from server. Error: {e}")
                break

    def send_messages(self):
        while True:
            message = input()
            if message.lower() == '@leaves':
                self.client.send(message.encode('utf-8'))
                break
            self.client.send(message.encode('utf-8'))
        self.client.close()

if __name__ == "__main__":
    client = PandaClient()
    client.start()