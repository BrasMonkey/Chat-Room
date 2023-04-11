from threading import Thread
import tkinter
import socket



window = tkinter.Tk()
window.title("Chat Room App")
window.configure(bg="white")

msg = tkinter.StringVar()
msg.set("")

def send():
    new_msg = msg.get()
    s.send(bytes(new_msg, "utf8"))
    msg.set("")
    if new_msg == "/quit":
        s.close()
        window.destroy()
    
def quit_chat():
    msg.set("/quit")
    send()

def receive():
    while True:
        try:
            msg = s.recv(1024).decode("utf8")
            msg_zone.insert(tkinter.END, msg)
        except:
            print("Ups...something went wrong")
            break


msg_frame = tkinter.Frame(window, width = 100, height = 100, bg = "white")
msg_frame.grid()

scroll_bar = tkinter.Scrollbar(msg_frame)
scroll_bar.grid(row=0, column=1, sticky="ns")

msg_zone = tkinter.Listbox(msg_frame, height = 15, width = 100, bg = "white", yscrollcommand = scroll_bar.set)
msg_zone.grid(row=0,column=0,sticky="nsew")

send_zone = tkinter.Frame(window, width = 100, height= 15)
send_zone.grid()

label = tkinter.Label(send_zone, text="Message: ")
label.grid(row=0)
entry = tkinter.Entry(send_zone, textvariable = msg, width="50")
entry.grid(row=0, column=1)

send_button = tkinter.Button(send_zone, text = "Send", font = "Aerial", fg="black", command = send)
send_button.grid(row=0, column=2)

quit_button = tkinter.Button(send_zone, text = "Quit", font = "Aerial", fg="white", bg="black", command = quit_chat)
quit_button.grid(row=0, column=3)

host = "localhost"
port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

receive_thrd = Thread(target=receive)
receive_thrd.start()

tkinter.mainloop()