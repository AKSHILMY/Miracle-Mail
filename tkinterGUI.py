
# Commands
# Give access to third part apps in gmail security settings
# Install smtp library using 'pip install secure-smtplib' command in command prompt 
import tkinter
from tkinter import filedialog
from tkinter.constants import DISABLED, E, NW, W, X


import smtplib,socket

def setup_server():
    # set up the SMTP server
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.starttls()
    return server

def login(server):
    sender_address = str(sender.get())
    sender_password = str(password_str.get())
    server.login(sender_address,sender_password)
    return sender_address

def create_email(address):
    global msg
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    
    recipient_email = str(email.get())

    # setup the parameters of the message
    msg['From'] = address
    msg['To'] = recipient_email
    msg['Subject']=str(subject_text.get("1.0",'end-1c'))

    message = str(message_text.get("1.0",'end-1c'))
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    return msg

def send(server,msg):
    from email import message
    # send the message via the server set up earlier.
    server.send_message(msg)
    del msg
    tkinter.messagebox.showinfo(title="Successful", message="Email: "+str(str(email.get())+"\n"+"Subject: "+subject_text.get("1.0",'end-1c'))+"\n"+"Message: "+str(message_text.get("1.0",'end-1c')))
    print(str(subject_text.get("1.0",'end-1c')))
    print(str(message_text.get("1.0",'end-1c')))
    print(str(email.get()))
    print("Successful")
    

def send_email():
    from tkinter import messagebox
    try:
        server = setup_server()
        address  = login(server)
        msg = create_email(address)
        send(server,msg)
    except socket.gaierror:
        error = "No Internet Connection"
        tkinter.messagebox.showerror(title="Error", message=error)
        print(error)
    except smtplib.SMTPAuthenticationError :
        # If password or username is wrong
        # If less secure app access not granted in google account settings
        error1 = "Invalid username or password"
        error2 = "Make sure the less secure app access is granted in google account security settings"
        tkinter.messagebox.showerror(title="Error", message=error1+"\n"+error2)
        print(error1+"\n"+error2)
    except smtplib.SMTPRecipientsRefused :
        error = "Invalid Recipient Email"
        tkinter.messagebox.showerror(title="Error", message=error)
        print(error)
    except Exception:
        error = "An error occured"
        tkinter.messagebox.showerror(title="Error", message=error)
        print(error)
        

def send_window_process():
    print(str(subject_text.get("1.0",'end-1c')))
    print(str(message_text.get("1.0",'end-1c')))
    print(str(email.get()))
    print()
    print("Top Level")
    loginWindow = tkinter.Toplevel(master=canvas)
    loginWindow.grab_set() # to prevent access to main window
    loginWindow.title("Login")
    loginWindow.geometry("440x100")
    loginWindow.config(background="#000000")
    loginWindow.resizable(0,0)
    img2=tkinter.PhotoImage(file="D:\Github\Simple-Projects\miraclemaillogo.png")
    loginWindow.iconphoto(False,img2)
    
    sender_email_address = tkinter.Label(loginWindow,text="Email of Sender: ",bg='#000080',fg="#FFFFFF")
    sender_email_address.grid(row=1, column=0, sticky=W, pady=10,  ipadx='5px',padx=10)
    sender_email_address_entry = tkinter.Entry(loginWindow,width=40,textvariable=sender)
    sender_email_address_entry.grid(row=1,column=1,sticky=W,padx=10)

    password = tkinter.Label(loginWindow,text="Password",bg='#000080',fg="#FFFFFF")
    password.grid(row=2, column=0,sticky=W, pady=5,  ipadx='5px',padx=10) 
    password_text = tkinter.Entry(loginWindow,width=25,textvariable=password_str,show='*')
    password_text.grid(row=2,column=1,sticky=W,padx=10)

   
    
    send = tkinter.Button(loginWindow,text="Send",bg='#000080',fg="#FFFFFF",command=send_email)
    send.grid(row=3,column=2,sticky=W)


def add_attachment(): 
    from email.mime.base import MIMEBase
    from email import encoders

    from tkinter import filedialog

    
    filetypes = (
        ('All files', '*.*'),
        ('text files', '*.txt'),
        ('Image Files', '*.*')
    )

    filename = tkinter.filedialog.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    # open the file to be sent 
    if filename:
        file = open(filename, "rb")
        # instance of MIMEBase and named as attachment
        attachment = MIMEBase('application', 'octet-stream')
        
        # To change the payload into encoded form
        attachment.set_payload((file).read())
        
        # encode into base64
        encoders.encode_base64(attachment)
        # attachment.add_header(input("Add header to the attachment: ").strip(),"client")
        
        # attach the instance 'attachment' to instance 'msg'
        msg.attach(attachment)
        print("Attachment has been added")
    
# GUI
from email.mime.multipart import MIMEMultipart
msg = MIMEMultipart()       # create a message



height = 640
width = 360


window = tkinter.Tk()
email = tkinter.StringVar()
sender = tkinter.StringVar()
password_str = tkinter.StringVar()

window.geometry(str(height)+'x'+str(width))
window.resizable(0,0)
window.title("Miracle Mail")
icon = tkinter.PhotoImage(file="D:/guiImage.png")

canvas = tkinter.Canvas(window,width=width,height=height)
canvas.pack(fill='both',expand=True)
canvas.create_image(0,0,image=icon,anchor=NW)

img1=tkinter.PhotoImage(master=window,file="D:\Github\Simple-Projects\miraclemaillogo.png")
window.iconphoto(False,img1)

img2=tkinter.PhotoImage(master=canvas,file="D:\Github\Simple-Projects\miraclemaillogo.png")

logo = tkinter.Label(canvas,image=img2)
logo.grid(row=0,column=0,sticky=W,pady=10,padx=60)


brand = tkinter.Label(canvas, text="MIRACLE MAIL", bg="#171717",fg='#ffffff', font='arial 20 bold')
brand.grid(row=0, column=1, sticky=W, pady=2, padx='15px')

email_address = tkinter.Label(canvas,text="Email of Recipient: ",bg='#000080',fg="#FFFFFF")
subject = tkinter.Label(canvas,text="Subject",bg='#000080',fg="#FFFFFF")
message = tkinter.Label(canvas,text="Message",bg='#000080',fg="#FFFFFF")

email_address.grid(row=1, column=0, sticky=W, pady=5,  ipadx='5px',padx=10)
subject.grid(row=2, column=0,sticky=W, pady=5,  ipadx='5px',padx=10) 
message.grid(row=3,column=0,sticky=W, pady=5,  ipadx='5px',padx=10)

email_address_entry = tkinter.Entry(canvas,width=30,textvariable=email)
email_address_entry.grid(row=1,column=1,sticky=W,padx=10)

# verify = tkinter.Button(canvas,text="Verify Email address",bg='#000080',fg="#FFFFFF",command=verify_email)
# verify.grid(row=1,column=3,sticky=W,padx=10)

subject_text = tkinter.Text(canvas,height=1,width=30)
subject_text.grid(row=2,column=1,sticky=W,padx=10)

message_text = tkinter.Text(canvas,height=10,width=44) 
message_text.grid(row=6,columnspan=2,sticky=W,padx=10,pady=5)

attachment = tkinter.Button(canvas,text="Attach File",bg='#C0C0C0',fg="#000000",command=add_attachment)
attachment.grid(row=11,column=0,sticky=W,padx=10)

proceed = tkinter.Button(canvas,text="Proceed",bg='#C0C0C0',fg="#000000",command=send_window_process)
proceed.grid(row=11,column=1,sticky=E)

window.mainloop()

# To be used later


