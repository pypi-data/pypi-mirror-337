import kognic.studio.proto.messages_pb2 as PB
from websockets.sync.client import connect


def hello():
    with connect("ws://localhost:8765", max_size=2**32) as websocket:
        message = websocket.recv()
        proto_message = PB.Message()
        proto_message.ParseFromString(message)

        init_scene_message = PB.Message(
            initialize_scene=PB.InitializeScene(scene="be3c8585-3e33-4a88-a28f-35f81fa26a73")
        )
        websocket.send(init_scene_message.SerializeToString())

        num_messages = 0
        while True:
            message = websocket.recv()
            num_messages = num_messages + 1
            proto_message = PB.Message()
            proto_message.ParseFromString(message)
            fields = proto_message.ListFields()
            fields = [field[0].name for field in fields]
            print(num_messages)
            print(f"Received: {fields}")
            if num_messages == 24:
                request_message = PB.RequestFramesAmount(amount=5)
                message = PB.Message(request_frame_amount=request_message)
                # request_message = PB.RequestFramesRange(from_frame_id="18", to_frame_id="27")
                # message = message = PB.Message(request_frame_range=request_message)
                websocket.send(message.SerializeToString())
            if num_messages == 40:
                request_message = PB.RequestFramesAmount(amount=99)
                message = PB.Message(request_frame_amount=request_message)
                # request_message = PB.RequestFramesRange(from_frame_id="18", to_frame_id="tjabba")
                # message = message = PB.Message(request_frame_range=request_message)
                websocket.send(message.SerializeToString())


hello()
