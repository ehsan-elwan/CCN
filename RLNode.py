import socket
import pickle

nb_children = 10


class Com:
    def __init__(self, cmd, data, recipient, port):
        """
        Class Com: is used to represent an exchange object common between Parent and the different nodes
        :param cmd: The command type {observation request, cache request, observed state, etc..}
        :param data: the content to communicate for i.e: sensor values
        :param recipient: The ip address of the recipient
        :param port: RDV port, its used for listening only,
        new port number will be assigned once the connection is established
        """
        self.data = {"cmd": cmd, "data": data}
        self.recipient = recipient
        self.port = port
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, header_size=10):
        """
        This method convert the content to be sent to bytes by serializing the data
        Add a header containing the full size of the message in order for the reciver to detect End-of-Msg
        :param header_size:
        """
        msg = pickle.dumps(self.data)
        msg = bytes(f"{len(msg):<{header_size}}", 'utf-8') + msg
        self.tcp.connect((self.recipient, self.port))
        self.tcp.send(msg)
        print(self.tcp.recv(1024))
        self.tcp.close()


class Node:
    def __init__(self, node_info, ip=socket.gethostbyname(socket.gethostname()), parent=None, nid=None):
        self.nid = nid
        self.ip = ip
        self.parent = parent
        self.info = dict() # sensors information
        self.queue = dict()
        self.req_state = dict() # keep track of requested data coming from outside users
        self.info[nid] = node_info

    def content_req(self, content):
        self.req_state[content] += 1

    def obs_req_handler(self):
        pass

    def obs_state(self):
        pass


class Parent(Node):
    def __init__(self, dict_info, children_dict, pid=None):
        super().__init__(dict_info)
        self.children = children_dict
        self.q_table = dict()  # Q-Table of parent
        self.nid = pid
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for chd in children_dict:
            chd.parent = self

    def init_tcp(self, port, nb_connect=nb_children):
        self.tcp.bind((self.ip, port))
        self.tcp.listen(nb_connect)
        while True:
            # Establish connection with client.
            cs, address = self.tcp.accept()
            print("Got connection from", address)

            # send an acknowledgment to the client.
            cs.send("ACK from parent".encode('utf-8'))
            # Close the connection with the client
            com_handler(cs, address)

    def obs_req(self, node):
        pass

    def cache_req(self, subset_info, node):
        pass


def com_handler(cs, address, header_size=10):
    """
    This function will rebuild the received message from bytes and convert it back to python object/ dictionary
    :param cs:
    :param address:
    :param header_size:
    """
    print("Hello from node, msg from", address)
    msg_len = 0
    cache = dict()
    full_msg = b''
    new_msg = True
    receiving = True
    while receiving:
        msg = cs.recv(16)
        if new_msg:
            msg_len = int(msg[:header_size])
            new_msg = False

        full_msg += msg

        if len(full_msg) - header_size == msg_len:
            cache = pickle.loads(full_msg[header_size:])
            new_msg = True
            full_msg = b""
            receiving = False
    print(cache)

    cs.close()


if __name__ == "__main__":
    pass
