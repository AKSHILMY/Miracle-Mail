
# Commands
# Give access to third part apps in gmail security settings
# Install smtp library using 'pip install secure-smtplib' command in command prompt 
import tkinter
from tkinter import filedialog,ttk
from tkinter.constants import DISABLED, E, NW, W, X
from email.mime.multipart import MIMEMultipart
import smtplib,socket

# the message to be sent using email
msg = MIMEMultipart()       # create a message


# main window creation
height,width  = 640,420
window = tkinter.Tk()
window.geometry(str(height)+'x'+str(width))
window.resizable(0,0)
window.title("Miracle Mail")

# strings to be used throught the program
recipient_email_str = tkinter.StringVar()
sender_email_str = tkinter.StringVar()
password_str = tkinter.StringVar()

# list of attachments     
attachments_list=[]


# setting up server, authentication , creating email,attachment addition, sending email
def setup_server():
    # set up the SMTP server
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.starttls()
    return server

def login(server):
    email_address = str(sender_email_str.get())
    email_password = str(password_str.get())
    server.login(email_address,email_password)
    return email_address

def create_email(address):
    global msg
    from email.mime.text import MIMEText
    
    recipient_email = str(recipient_email_str.get())
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
    print("Successful")
    
def send_email():
    from tkinter import messagebox
    try:
        server = setup_server()
        address  = login(server)
        msg = create_email(address)
        send(server,msg)
        add_attachments(attachments_list)
        
        print(str(subject_text.get("1.0",'end-1c')))
        print(str(message_text.get("1.0",'end-1c')))
        print(str(recipient_email_str.get()))
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
        
def show_attachments(): 
    from tkinter import messagebox
    global attachments_list
    filenames=""
    if len(attachments_list)>0:
        filenames = "Following files were attached to the email: "+"\n\n"+"\n".join(attachments_list)
    else:
        filenames = "No attachments attached"
        
    tkinter.messagebox.showinfo(title = "Attachments",message=filenames)
    
def choose_attachments():
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
    if filename:
        attachments_list.append(filename)

def add_attachments(attachments): 
    from email.mime.base import MIMEBase
    from email import encoders
    import os

    # new window to show that attachments are uploading 
    uploadWindow = tkinter.Toplevel(canvas)
    uploadWindow.grab_set() # to prevent access to main window
    uploadWindow.title("Uploading")
    uploadWindow.geometry("240x50")
    uploadWindow.config(background="#000000")
    uploadWindow.resizable(0,0)

    label = tkinter.Label(uploadWindow, text="00%")
    label.pack()

    progressbar = tkinter.ttk.Progressbar(uploadWindow, orient="horizontal", length=100,  mode='determinate')
    progressbar.pack()
    for filename in attachments:
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
            filesize = os.path.getsize(filename)

            # progress bar for uploading
            with open(filename, "r", encoding='utf-8') as f:
                for i in range(os.path.getsize(filename)):
                    progressbar["value"] = progressbar["value"]+1
                    progressbar["maximum"] = filesize
                    label.config(text="Uploading "+filename+str(int(progressbar["value"]/os.path.getsize(filename)*100)) + "%")          
                    canvas.update_idletasks()
                    #time.sleep(1) 
                progressbar["value"]=0

            print("Attachment has been added")
            if filename==attachments[-1]:
                uploadWindow.destroy()
   

def send_window_process():
    print(str(subject_text.get("1.0",'end-1c')))
    print(str(message_text.get("1.0",'end-1c')))
    print(str(recipient_email_str.get()))
    print()
    print("Top Level")

    # new window for login process 
    loginWindow = tkinter.Toplevel(master=canvas)
    loginWindow.grab_set() # to prevent access to main window
    loginWindow.title("Login")
    loginWindow.geometry("440x100")
    loginWindow.config(background="#000000")
    loginWindow.resizable(0,0)
    # img2=tkinter.PhotoImage(file="D:\Github\Simple-Projects\miraclemaillogo.png")
    # loginWindow.iconphoto(False,img2)
    
    sender_email_address = tkinter.Label(loginWindow,text="Email of Sender: ",bg='#000080',fg="#FFFFFF")
    sender_email_address.grid(row=1, column=0, sticky=W, pady=10,  ipadx='5px',padx=10)
    sender_email_address_entry = tkinter.Entry(loginWindow,width=40,textvariable=sender_email_str)
    sender_email_address_entry.grid(row=1,column=1,sticky=W,padx=10)

    password = tkinter.Label(loginWindow,text="Password",bg='#000080',fg="#FFFFFF")
    password.grid(row=2, column=0,sticky=W, pady=5,  ipadx='5px',padx=10) 
    password_text = tkinter.Entry(loginWindow,width=25,textvariable=password_str,show='*')
    password_text.grid(row=2,column=1,sticky=W,padx=10)

    send = tkinter.Button(loginWindow,text="Send",bg='#000080',fg="#FFFFFF",command=send_email)
    send.grid(row=3,column=2,sticky=W)



    
# GUI
if __name__ == "__main__":

   
    icon = tkinter.PhotoImage(file="D:/guiImage.png")

    canvas = tkinter.Canvas(window,width=width,height=height,background="#000000")
    canvas.pack(fill='both',expand=True)
    # canvas.create_image(0,0,image=icon,anchor=NW)

    img1=tkinter.PhotoImage(master=window,file="D:\Github\Simple-Projects\miraclemaillogo.png")
    window.iconphoto(False,img1)

    img2=tkinter.PhotoImage(master=canvas,file="D:\Github\Simple-Projects\miraclemaillogo.png")

    logo_label = tkinter.Label(canvas,image=img2)
    logo_label.grid(row=0,column=0,sticky=W,pady=10,padx=60)


    brand_label = tkinter.Label(canvas, text="MIRACLE MAIL", bg="#171717",fg='#ffffff', font='arial 20 bold')
    brand_label.grid(row=0, column=1, sticky=W, pady=2, padx='15px')

    recipient_email_label = tkinter.Label(canvas,text="Email of Recipient: ",bg='#000080',fg="#FFFFFF")
    subject_label = tkinter.Label(canvas,text="Subject",bg='#000080',fg="#FFFFFF")
    msg_label = tkinter.Label(canvas,text="Message",bg='#000080',fg="#FFFFFF")

    recipient_email_label.grid(row=1, column=0, sticky=W, pady=5,  ipadx='5px',padx=10)
    subject_label.grid(row=2, column=0,sticky=W, pady=5,  ipadx='5px',padx=10) 
    msg_label.grid(row=3,column=0,sticky=W, pady=5,  ipadx='5px',padx=10)

    email_address_entry = tkinter.Entry(canvas,width=30,textvariable=recipient_email_str)
    email_address_entry.grid(row=1,column=1,sticky=W,padx=10)

    # verify = tkinter.Button(canvas,text="Verify Email address",bg='#000080',fg="#FFFFFF",command=verify_email)
    # verify.grid(row=1,column=3,sticky=W,padx=10)

    subject_text = tkinter.Text(canvas,height=1,width=30)
    subject_text.grid(row=2,column=1,sticky=W,padx=10)

    message_text = tkinter.Text(canvas,height=10,width=44) 
    message_text.grid(row=6,columnspan=2,sticky=W,padx=10,pady=5)

    attachment_button = tkinter.Button(canvas,text="Attach File",bg='#C0C0C0',fg="#000000",command=choose_attachments)
    attachment_button.grid(row=11,column=0,sticky=W,padx=10)

    proceed_button = tkinter.Button(canvas,text="Proceed",bg='#C0C0C0',fg="#000000",command=send_window_process)
    proceed_button.grid(row=11,column=1,sticky=E)

    files_button = tkinter.Button(canvas,text="...",bg='#C0C0C0',fg="#000000",command=show_attachments,height=1,width=3)
    files_button.grid(row=12,column=0,sticky=W,padx=10)


    window.mainloop()



