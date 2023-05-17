from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import mysql.connector
from tkcalendar import Calendar

root = Tk()
root.geometry('400x600') #Frame size
root.resizable(0,0)
root.title("Registration form")
# bgImg = ImageTk.PhotoImasge(file='sqlregisform\download.png')

# resized_image= bgImg.resize((300,205), Image.ANTIALIAS)
# new_image= ImageTk.PhotoImage(resized_image)


# bgLabel = Label(frame, image=resized_image)
# bgLabel.grid(row=0, column =0)
# bgLabel.place(x=0,y=0)
# bgLabel.pack(anchor='center')

#on submit check
def submit():
    global gender
    phone = phoneentry.get()
    name = nameentry.get()
    roll = rollentry.get()
    age = ageentry.get()
    # dob = dobentry.get()
    # gender = gender.get()
    # course = menu.get()

    if not checkroll(roll):
        return
    if not checkname(name):
        return
    if not checkage(age):
        return
    if not checkphone(phone):
        return
    print (dobentry.get())
    try:
        print("In try block")
        mydb = mysql.connector.connect(host='localhost', user='root', passwd='1704')
        cur = mydb.cursor()
        cur.execute('create database IF NOT EXISTS IIPSFormData')
        cur.execute('use IIPSFormData')
        # messagebox.showinfo('success', 'successfull connection')
        # cur.execute('use IIPSFormData')
        query = 'create table IF NOT EXISTS Student (RollNo int primary key not null, Name char(50) not null, Age int(2), Gender char(10), CourseID varchar(10), Phone bigint unique )'
        cur.execute(query)
        # messagebox.showinfo('Success', 'Table created')
        cur.execute('use IIPSFormData')
        query = "INSERT INTO student (RollNo, Name, Age, Gender, CourseID, Phone, DOB) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (rollentry.get(), nameentry.get(), ageentry.get(), gender.get(), menu.get(), phoneentry.get(), dobentry.get())
        cur.execute(query, values)
        print(f"Executing SQL query: {query} with data: {values}")
        
        mydb.commit()
        cur.close()
        mydb.close()
        
        messagebox.showinfo('Success', 'Field entered')
        ageentry.delete(0, END)
        rollentry.delete(0, END)
        nameentry.delete(0, END)
        gender.set(0)
        dobentry.delete(0, END)
        dobentry.insert(0, 'yyyy/mm/dd')
        menu.set('Select Course')
        phoneentry.delete(0, END)
    except mysql.connector.Error as err:
        messagebox.showerror('Error', f"Database error: {err}")
        print(f"Database error: {err}")
        mydb.rollback()
       
#callback function
def checkname(name):
    if not name.strip():
        messagebox.showerror( 'Alert!','Enter name!')
        return False
    elif not all(char.isalpha() or char.isspace() for char in name):
        messagebox.showerror( 'Alert!','Name should contain only alphabets!')
        return False
    return True

def checkage( age ):
    if not age.strip():
        messagebox.showerror('Alert!', 'Enter age!')
        return False
    elif not age.isdigit() or int(age) < 18:
        messagebox.showerror('Alert!', 'Age should be a number greater than or equal to 18!')
        return False
    elif int(age) > 50:
        messagebox.showerror('Alert!', 'Candidate above 50 not allowed!')
        return False
    return True

def checkroll(roll):
    if not roll.strip():
        messagebox.showerror('Alert!', 'Enter roll number')
        return False
    elif not roll[:2] in ['IT', 'IC', 'IM', 'IB', 'TT']:
        messagebox.showerror('Alert!', 'Roll number should begin with either IT, IC, IM, TT or IB')
        return False
    elif not len(roll) in [8,9]:
        messagebox.showerror('Alert!', 'Enter a valid roll number!')
        return False
    return True

def checkphone(phone):
    if not phone.strip():
        messagebox.showerror('Alert!','Enter phone number!')
        return False
    if phone.isdigit():
        if len(phone) == 10:
            if phone[0] in ['9','8','7','6']:
                return True
            else:
                messagebox.showerror('Alert!','Enter valid phone number!')
                return False
        else:
            messagebox.showerror('Alert!','Phone number must have 10 digits!')
            return False
    else:
        messagebox.showerror('Alert!','Phone number should contain digits only!')
        return False
    return True


def checkgender(gender):
    if not gender == " ":
        messagebox.showerror('Alert!', 'Select gender!')
        return False
    return True

def checkcourse(course):
    if not course == " ":
        messagebox.showerror('Alert!', 'Select course!')
        return False
    return True

def checkdob(dob):
    if not dob == " ":
        messagebox.showerror('Alert!', 'Enter DOB!')
        return False
    return True



#frame
color = 'black'
font = ('sans-serif', '15', 'bold')
efont = ('sans-serif', '15')
frame = Frame(root, width=400, height=600,bg=color, bd=0)
frame.place(x=0,y=0)
# root.config(bg = color)

#heading
heading = Label(frame, text = 'IIPS Student Record', bg = color, font = ('Poopins', '20', 'bold'), fg='red')
heading.place(y=20, x=75)
# heading.pack(anchor='center')

#roll number
roll = Label(frame, text= 'Enroll Number',bg = color, font = font, fg='white')
roll.place(y=80,x=12)
rollentry = Entry(frame, width=16, font= efont, bd=0, fg='black')
rollentry.place(x=182 , y=80)

#name
name = Label(frame, text= 'Name: ',bg = color, font = font, fg='white')
name.place(y=120,x=12)
nameentry = Entry(frame, width=16, font= efont, bd=0, fg='black')
nameentry.place(x=182 , y=120)
# validatename = win.register(checkname) #callback
# nameentry.config(validate='key', validatecommand= (validatename, "%P")) #bind

#age
age = Label(frame, text= 'Age: ',bg = color, font = font, fg='white')
age.place(y=160,x=12)
ageentry = Entry(frame, width=16, font= efont, bd=0, fg='black')
ageentry.place(x=182 , y=160)


#Get the selected date when the user closes the calender
def pickdate(event):
    global cal, date_window

    date_window = Toplevel()
    date_window.grab_set()
    date_window.title('Choose Date of Birth')
    date_window.geometry('250x220')
    cal = Calendar(date_window, selectmode='day', date_pattern='y/mm/dd')
    cal.place(x=0,y=0)

    submit = Button(date_window, text= 'Submit', command= grab_date)
    submit.place(x=80,y=190)

def grab_date():
    dobentry.delete(0, END)
    dobentry.insert(0, cal.get_date())
    date_window.destroy()

#dob
dob = Label(frame, text='Date of Birth:', bg= color, font =font, fg='white' )
dob.place(x=12, y=200)
dobentry = Entry(frame, bg='white', font = efont)
dobentry.place(x=182, y=200, width=170)
dobentry.insert(0, 'yyyy/mm/dd')
dobentry.bind('<1>', pickdate)


# #gender
genderlabel =  Label(frame, text= 'Gender: ',bg = color, font = font, fg='white')
genderlabel.place(y=240,x=12)
gender = StringVar()
gender.set('None')
genderradio1 = Radiobutton(frame,text='Male', variable=gender, value='Male', font= efont, bd=0, fg='black')
genderradio1.place(x=182 , y=240)
# genderradio1.pack()

genderradio2 = Radiobutton(frame,text='Female', variable=gender, value='Female', font= efont, bd=0, fg='black')
genderradio2.place(x=262 , y=240)
# genderradio2.pack(anchor=W)

genderradio3 = Radiobutton(frame,text='Other', variable=gender, value='Other', font= efont, bd=0, fg='black')
genderradio3.place(x=182 , y=280)
# genderradio3.pack(anchor=W)


# gender_label = Label(frame, text="Gender:")
# gender_var = StringVar()
# male_radio = Radiobutton(frame, text="Male", variable=gender_var, value="Male")
# female_radio = Radiobutton(frame, text="Female", variable=gender_var, value="Female")



#course id
course = Label(frame, text= 'Course ID: ',bg = color, font = font, fg='white')
course.place(y = 320, x = 12) 

course = ['IT101', 'IC102', 'IB101', 'MS101', 'TT102', 'MR103','ER104']
menu = StringVar()
menu.set('Select Course')
coursedropdown = OptionMenu(frame,menu, *course)
coursedropdown.place( x=182 , y=320)
coursedropdown.config(width=12, font = efont , bg='white')

#phone
phone = Label(frame, text= 'Phone Number:',bg = color, font = font, fg='white')
phone.place(y=390,x=12)
phoneentry = Entry(frame, width=16, font= efont, bd=0, fg='black')
phoneentry.place(x=182 , y=390)

#submit
submit = Button(frame,font=efont, text='Submit',command=submit ,width=19, borderwidth=1, height=1, activebackground=color, activeforeground='white')
submit.place(x=100, y= 430)


root.mainloop()