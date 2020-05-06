import socket
import pickle

header_size = 10


class Com:
    def __init__(self, cmd, msg):
        self.msg = msg
        self.cmd = cmd


class Node:
    def __init__(self, node_info, ip=socket.gethostbyname(socket.gethostname()), parent=None, nid=None):
        self.nid = nid
        self.address = ip
        self.info = node_info
        self.parent = parent
        self.req = dict()
        self.queue = dict()
        self.content = dict()
        self.req_state = dict()
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def init_tcp(self, port, nb_connect=1):
        self.tcp.bind((self.address, port))
        self.tcp.listen(nb_connect)
        cs, address = self.tcp.accept()
        com_handler(cs, address)

    def content_req(self, content):
        self.req_state[content] += 1

    def obs_req_handler(self):

        msg = pickle.dumps(self.content)
        msg = bytes(f"{len(msg):<{header_size}}", 'utf-8') + msg

    def cache_req_handler(self):
        cs, address = self.tcp.accept()
        msg_len = 0
        cache = dict()
        full_msg = b''
        new_msg = True
        receiving = True
        while receiving:
            msg = cs.recv(16)
            if new_msg:
                print("new msg len:", msg[:header_size])
                msg_len = int(msg[:header_size])
                new_msg = False

            print(f"full message length: {msg_len}")

            full_msg += msg

            print(len(full_msg))

            if len(full_msg) - header_size == msg_len:
                print("full msg received")
                print(full_msg[header_size:])
                cache = pickle.loads(full_msg[header_size:])
                new_msg = True
                full_msg = b""
                receiving = False
        print(cache)
        pass

    def obs_state(self):
        pass


class Parent(Node):
    def __init__(self, dict_info, children_dict, pid=None):
        super().__init__(dict_info)
        self.children = children_dict
        self.q_table = dict()
        self.nid = pid
        for chd in children_dict:
            chd.parent = self

    def obs_req(self, node):
        pass

    def cache_req(self, subset_info, node):
        pass


def com_handler(cs, address):
    msg_len = 0
    cache = dict()
    full_msg = b''
    new_msg = True
    receiving = True
    print("new msg from", address)
    while receiving:
        msg = cs.recv(16)
        if new_msg:
            print("new msg len:", msg[:header_size])
            msg_len = int(msg[:header_size])
            new_msg = False

        print(f"full message length: {msg_len}")

        full_msg += msg

        print(len(full_msg))

        if len(full_msg) - header_size == msg_len:
            print("full msg received")
            print(full_msg[header_size:])
            cache = pickle.loads(full_msg[header_size:])
            new_msg = True
            full_msg = b""
            receiving = False
    print(cache)

    cs.close()


if __name__ == "__main__":
    n1 = Node({"a1": 3.4})
    print(n1.parent)
    p0 = Parent({}, [n1], pid="23")
    print(n1.parent.nid)
