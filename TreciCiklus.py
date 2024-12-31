import can
import time

def send_can_message():
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

    message = can.Message(arbitration_id=0x123, data=[0x11, 0x22, 0x33, 0x44], is_extended_id=False)

    try:
        bus.send(message)
        print(f"Poruka poslana: {message}")
    except can.CanError:
        print("Greška prilikom slanja poruke")

def listen_for_messages():
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')
    print("Slušam CAN poruke...")
    
    while True:
        message = bus.recv()  
        print(f"Primljena poruka: {message}")

if __name__ == "__main__":
    import threading
    listener_thread = threading.Thread(target=listen_for_messages)
    listener_thread.daemon = True  
    listener_thread.start()

    send_can_message()

    time.sleep(2)
