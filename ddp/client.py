import websocket
import ddp
import sys

class Client(object):
    def __init__(self, url):
        self.url = url
        self.ws = websocket.create_connection(url)

    def send(self, message):
        self.ws.send(ddp.serialize(message))
    
    def recv(self):
        return ddp.deserialize(self.ws.recv())

    def send_recv(self, message):
        self.send(message)
        return self.recv()

    def connect(self, session=None, protocol="1"):
        self.protocol = protocol
        return self.send_recv(ddp.Connect(session, protocol, [protocol]))

if __name__ == "__main__":
    client = Client("ws://sys-colin-zerp6:9999/ddp")
    rcvd_obj = client.connect()
    print rcvd_obj

    # Hope we connected ok    
    if rcvd_obj.msg != "connected":
        sys.exit()

    # Send a ping
    print client.send_recv(ddp.Ping("yummy"))

    # subscribe to product.product
    params = {
        "model": "product.product",
        "domain": [('default_code', 'ilike', '%LSM%')],
        "fields": ["id", "default_code"]
    }
    print client.send(ddp.Sub(1, "someProducts", params))

    # execute a method
    ddp_id = '1'
    params = ["product.product", "price_get", [[6443]], {}] 
    print client.send_recv(ddp.Method("execute", ddp_id, params))
    params = ["product.product", "write", [[6443], {"notes": "Touched by DDP!"}], {}] 
    print client.send_recv(ddp.Method("execute", ddp_id, params))

