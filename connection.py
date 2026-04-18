import socket
import CTkMessagebox
import sys

def check_connection() -> bool:
    try:
        # Try to connect Google DNS server
        socket.setdefaulttimeout(3) # if didn't response in 3 seconds, fail
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
        return True
    except socket.error as ex:
        return False

def show_connection_error():
    msg = CTkMessagebox.CTkMessagebox(title="Error",
                                    message="Connection error. Please check your internet connection.",
                                    option_1="Exit")
    response = msg.get()
    if response == "Exit":
        sys.exit(0)