from RLNode import *

n1 = Node({"a1": 3.4, "a2": 12}, nid="A1")

print("Node sensors & values:", n1.info)

c1 = Com("obs_state", n1.info, n1.ip, 12345)
print("sending sensor values to parent...")
c1.send()
