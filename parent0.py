from RLNode import *

p = Parent({}, [], pid="23")
print("Waiting for connection...")
p.init_tcp(12345)
