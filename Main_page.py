# Import required Libraries
from tkinter import *
from PIL import Image, ImageTk
from tkinter.ttk import Combobox
#from Menu.settings_page import settings_windows
import cv2
from tkinter import ttk
import os.path
import json
from playsound import playsound
import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime
from weapon_detector import *

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
import io


import winsound
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 20  # Set Duration To 1000 ms == 1 second


def send_mail(fp,subject,body,strTo):
    
    print(type(fp))
    strFrom = "sender_email_address"
    

    # Create the root message 

    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot['Cc'] =strFrom
    msgRoot.preamble = 'Multi-part message in MIME format.'

    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = MIMEText('Alternative plain text message.')
    msgAlternative.attach(msgText)

    msgText = MIMEText(body, 'html')
    msgAlternative.attach(msgText)
    
    #im1 = im1.save("detect.jpg")
    msgImage = MIMEImage(fp.read())

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)

    smtp = smtplib.SMTP()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
       smtp.login(strFrom, 'sender_email_address_password')
       smtp.sendmail(strFrom, strTo, msgRoot.as_string())
       smtp.quit()






def window_shade(color_shade):
    window_main.configure(bg=color_shade)
    #status["bg"] = color_shade
    #label_widget.configure(bg=color_shade)
    labelframe_widget.configure(bg=color_shade)
    





def check_mailid(email_data):
    if(email_data[1:-1].count('@')==1) and (email_data[1:-1].count('.')>=1 and email_data[0].isalnum() and email_data[len(email_data)-1].isalnum()):
        return True
    else:
        return False

def submit():
    data = {}
    data["audio_alert"]=audio_status.get()
    data["email_alert"]=email_status.get()
    data["email_id"]=email_text.get()
    data["email_interval"]=cb.get()
    if(check_mailid(data["email_id"])):
        with open('config.json', 'w') as f:
            json.dump(data, f, indent=2)
        status["text"] ="Saved Successfully!!"
        status["bg"] = '#44DD44'

    else:
        status["text"] ="Error! Enter correct Email ID"
        status["bg"] = 'red'





def test():
    global im_buf_arr
    global test_count
    test_count=5
    status["bg"] = 'blue'
    status["text"] ="Testing configurations!"
    with open('config.json', 'r') as f:
        data=json.load(f)
    if(data["audio_alert"]):
        # for playing note.wav file
        playsound('alarm.wav')
    if(data["email_alert"]):
        img_save = im_buf_arr.save("alert.jpg")
        image_saved = open('alert.jpg', 'rb') #Read image
        
        now = datetime.now()
        subject = 'CamWatch - Test Mail'
        body = "No worries, this is just a test mail ("+now.strftime("%d/%m/%Y %H:%M:%S")+")"
        
        send_mail(image_saved,subject,body,data["email_id"])
        image_saved.close()
        #send_mail(data["email_id"])
    test_count=5
    status["text"] ="Testing - Complete!"
    

global test_count,detection_flag,email_counter,time_previous
time_previous=datetime.now()
email_counter=0
detection_flag=0
counter=0
blink_counter=5
test_count=0
#initialize weapon finder
find_weapon_init()
print("init")
#x = threading.Thread(target=thread_function, args=(1,))
#x.start()
# Create an instance of TKinter Window or frame
window_main = Tk()

# Set the size of the window

window_main.title('CamWatch')
window_main.geometry("1200x500")
window_main.resizable(False, False)


#settings button
#settings_button=Button(window_main,text = '   Settings   ', command = settings, activebackground='#44DD44', activeforeground='#FFFFFF')
#settings_button.place(x=500, y=450)


# Create a Label to capture the Video frames
label =Label(window_main)
label.place(x=80,y=20)
cap= cv2.VideoCapture(0)




if(os.path.exists("config.json") == False):
    with open('config.json', 'w') as f:
        data = {}
        data["audio_alert"]=1
        data["email_alert"]=1
        data["email_id"]="samplemail@email.com"
        data["email_interval"]="five"
        json.dump(data, f, indent=2)

        
with open('config.json', 'r') as f:
    data=json.load(f)


labelframe_widget = LabelFrame(window_main,
                                   text="CamWatch - Configuration")
label_widget=Label(labelframe_widget,
       text="",
       height=25,width=50, bg = 'grey')
#labelframe_widget.pack(padx=10, pady=10)
labelframe_widget.place(x=800,y=14)
label_widget.pack()



##audio alert
label_1=Label(window_main, text="Audio alert", fg='black', font=("Helvetica", 10))
label_1.place(x=840, y=80)
audio_status=IntVar()
audio_status.set(data["audio_alert"])
r1=Radiobutton(window_main, text="on", variable=audio_status,value=1)
r2=Radiobutton(window_main, text="off", variable=audio_status,value=0)
r1.place(x=940,y=80)
r2.place(x=1000, y=80)



##email alert
label_2=Label(window_main, text="Email alert", fg='black', font=("Helvetica", 10))
label_2.place(x=840, y=130)
email_status=IntVar()
email_status.set(data["email_alert"])
r3=Radiobutton(window_main, text="on", variable=email_status,value=1)
r4=Radiobutton(window_main, text="off", variable=email_status,value=0)
r3.place(x=940,y=130)
r4.place(x=1000, y=130)

##email id
label_3=Label(window_main, text="Email ID", fg='black', font=("Helvetica", 10))
label_3.place(x=840, y=180)
email_text = StringVar()
email_text.set(data["email_id"])
textBox = Entry(window_main,textvariable = email_text, width=30)
textBox.place(x=940, y=180)


#email interval
label_4=Label(window_main, text="Email interval (in minutes)", fg='black', font=("Helvetica", 10))
label_4.place(x=840, y=230)
var = StringVar()
var.set(data["email_interval"])
email_interval=("two","four","six","eight","ten")
cb=Combobox(window_main, values=email_interval, state = "readonly", width = 8)
cb.set(data["email_interval"])
cb.place(x=1000, y=230)


#Save button
save_button=Button(window_main,text = '   Save   ', command = submit,activebackground='#44DD44', activeforeground='#FFFFFF')
save_button.place(x=900, y=295)

#test button
test_button = Button(window_main, text = '   Test   ', command = test, activebackground='blue', activeforeground='#FFFFFF')
test_button.place(x=1000, y=295)




status=Label(window_main,text="", anchor="w",width=50,height=2)
status.place(x=802, y=340)


#close button
close_button = Button(window_main, text = '      Exit CamWatch      ', command = window_main.destroy, activebackground='red', activeforeground='#FFFFFF')
close_button.place(x=600, y=450)






# Define function to show frame
def show_frames():
   global im_buf_arr
   global test_count
   global blink_counter, counter
   global time_previous,email_counter
   time_now = datetime.now()
   #print("qwe:",time_now.minute," -- ",time_previous.minute," / ",email_counter)
   
   if(email_counter!=0):
       if(time_now.minute!=time_previous.minute):
           time_previous=time_now
           email_counter-=1
   else:
       time_previous = datetime.now()
   # Get the latest frame and convert into Image
   cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_RGB2BGR)
   #weapon check
   cv2image=cv2.flip(cv2image,1)
   cv2image, detection_flag_list=find_weapon_check(cv2image,["pistol"])#.reshape((3,480,640)))
   #cv2image=cv2image.reshape((480,640,3))
   img = Image.fromarray(cv2image)
   
   detection_flag=0
   for i in detection_flag_list:
       detection_flag+=i
   img = img.resize((640, 390))
   
   
   #buf = io.BytesIO()
   #img.save(buf, format='JPEG')
   im_buf_arr = img

   #im_buf_arr = 
   #is_success, im_buf_arr = cv2.imencode(".jpg", cv2image)
   # Convert image to PhotoImage
   imgtk = ImageTk.PhotoImage(image = img)
  
   ###
   label.imgtk = imgtk
   label.configure(image=imgtk)
   if(detection_flag==0):
       if(test_count==0):
        status["bg"] ="grey"
        status["text"] =""
       else:
           test_count-=1
       blink_counter=5
       window_shade("grey")
       #window_main.configure(bg='grey')
       #print("tyu")
   else:
       with open('config.json', 'r') as f:
           data=json.load(f)
       if(data["audio_alert"]):
           winsound.Beep(frequency, duration)
       if(data["email_alert"]):
       
           if(email_counter==0):
               img_save = im_buf_arr.save("alert.jpg")
               image_saved = open('alert.jpg', 'rb') #Read image 
               now = datetime.now()
               subject = 'Weapon detected!!CamWatch - Alert!!'
               body = "Alert!! Weapon detected!! ("+now.strftime("%d/%m/%Y %H:%M:%S")+")"
               send_mail(image_saved,subject,body,data["email_id"])
               image_saved.close()
                   
               if(data["email_interval"]=='five'):
                   email_counter = 5
               else:
                   email_interval=("two","four","six","eight","ten")
                   for i in range(0,len(email_interval)):
                       if(email_interval[i] in data["email_interval"]):
                            email_counter = 2*(i+1)
           
           
       status["text"] ="Alert: Weapon Detected!"
       status["bg"] ="red"
       #playsound('alarm_trim.wav')
       #print("c:",blink_counter)
       if(blink_counter==5):
           counter=0
           window_shade("red")
           #window_main.configure(bg='red')
           #print("kl2")
       elif(blink_counter==0):
          counter=1
          window_shade("grey")
          #window_main.configure(bg='grey')
          #print("kl3")
       if counter:
           blink_counter+=1
       else:
           blink_counter-=1
   # Repeat after an interval to capture continiously
   label.after(2, show_frames)


show_frames()
#window_main.configure(bg='#8B8378')
window_main.mainloop()
#700x350
