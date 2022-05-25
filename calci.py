from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
import datetime
from sqlite3 import *
import pandas as pd

root = Tk()
root.title("Welcome")
root.geometry("520x290+250+200")

# bmi button on root
def f1():
	root.withdraw()
	mw.deiconify()
	
	d1 = datetime.datetime.now()
	hr = d1.hour
	msg = ""
	if hr < 12:
		msg = "Good Morning"
	elif hr < 16:
		msg = "Good Afternoon"
	else:
		msg = "Good Evening"

	res = str(d1) + "\n" + msg 
	ent_date.insert(INSERT, res)

	con = None
	try:
		
		con = connect("project.db")
		cursor = con.cursor()
		sql = "select * from bmi_info"
		cursor.execute(sql)
		ent_count.delete(0, END)
		data = cursor.fetchall()
		if len(data) == 0:
			ent_count.insert(INSERT, "Count = 0")
		else:
			res = "Count = " + str(len(data))
			ent_count.insert(INSERT, res)
	except Exception as e:
		showerror("Mistake", e)
	finally:
		if con is not None:
			con.close()

f = ("Arial", 50, "bold")
btn = Button(root, text="BMI Calci" + "\n" + "by" + "\n" + "Simran Makhija", font=f, fg="red", command=f1)
btn.pack()

# calculate button on menu window
def f2():
	mw.withdraw()
	cw.deiconify()

# view button on menu window
def f6():
	mw.withdraw()
	vw.deiconify()
	vw_data.delete(1.0, END)
	info = ""
	con = None
	try:
		con = connect("project.db")
		cursor = con.cursor()
		sql = "select * from bmi_info"
		cursor.execute(sql)
		data = cursor.fetchall()
		for d in data:
			info = info + "name = " + str(d[0]) + "\n" + "age = " + str(d[1]) + "\n" + "phone = " + str(d[2]) + "\n" + "gender = " + str(d[3]) + "\n" + "bmi = " + str(d[4]) + "\n" + "****************************" + "\n"
		vw_data.insert(INSERT, info)
	except Exception as e:	
		showerror("Mistake", e)

# export button on menu window
def f8():
	con = None
	
	d1 = datetime.datetime.now()
	filename = "patient_" + str(d1.year) + "_" + str(d1.month) + "_" + str(d1.day) + "_" + str(d1.hour) + "_" + str(d1.minute) + "_" + str(d1.second) 
	res = filename + ".csv"
	
	try:
		con = connect("project.db")
		cusror = con.cursor()
		data = pd.read_sql_query("select * from bmi_info", con)
		data.to_csv(res, index = False)
	except Exception as e:
		showerror("Mistake", e)
	finally:
		if con is not None:
			con.close()

mw = Toplevel(root)
mw.title("BMI Calculator")
mw.geometry("500x420+380+150")

fd = ("Arial", 20, "bold")
ent_date = ScrolledText(mw, width=27, height=2,font=fd)
btn_calculate_bmi = Button(mw, text="Calculate BMI", font=fd, width=15, command=f2)
btn_view_history = Button(mw, text="View History", font=fd, width=15, command=f6)
btn_export_data = Button(mw, text="Export Data", font=fd, width=15, command=f8)
ent_count = Entry(mw, font=fd, bd=2, width = 10)

y=10
ent_date.pack(pady=y)
btn_calculate_bmi.pack(pady=y)
btn_view_history.pack(pady=y)
btn_export_data.pack(pady=y)
ent_count.pack(pady=y)

mw.withdraw()

# convert on calculate window
def f3():
	cw.withdraw()
	hw.deiconify()

# calculate on calculate window
def f4():
	try:
		name = ent_name.get()
		if(len(name) == 0 or name.isdigit() or len(name) < 2):
			raise Exception
		else:
			try:
				age = int(ent_age.get())
				if age <= 0:
					raise Exception
				else:
					try:
						phone = ent_phone.get()
						if len(phone) < 10 or len(phone) > 10 or phone.isalpha():
							raise Exception
						else:
							phone = int(phone)
							try:
								gender = ""
								if s.get() == 1:
									gender = "Male"
								elif s.get() == 2:
									gender = "Female"

								if(len(gender) != 0):
									try:
										height = ent_height.get()
										if len(height) <= 0 or height.isalpha() or float(height) <= 0:
											raise Exception
										else:
											height = float(height)
											try:
												weight = ent_weight.get()
												if len(weight) <= 0 or weight.isalpha() or float(weight) < 2.5:
													raise Exception
												else:
													weight = float(weight)
													bmi = weight / (height ** 2)
													msg = ""
													if bmi < 18.5:
														msg = "Underweight"
													elif bmi >= 18.5 and bmi <= 24.9:
														msg = "Normal"
													elif bmi >= 25 and bmi <= 29.9:
														msg = "Overweight"
													else:
														msg = "Obesity"
													con = None
													try:
														con = connect("project.db")
														cursor = con.cursor()
														sql = "insert into bmi_info values('%s', '%d', '%d', '%s', '%f')"
														cursor.execute(sql % (name, age, phone, gender, bmi))
														con.commit()
							
														res = "name = " + name + "\nage = " +str(age) + "\nphone =" + str(phone) + "\ngender = " + gender +  "\nbmi = "+ str(bmi) + "\n" + msg
														showinfo("BMI",res)
																 		
													except Exception as e:
														showerror("Mistake", e)
													finally:
														if con is not None:
															con.close()
													
											except Exception as e:
												showerror("Mistake", "Invalid weight")
									except Exception as e:
										showerror("Mistake", "Invalid height")
								else:
									raise Exception
							except Exception as e:
								showerror("Mistake", "Select any one gender")
							
					except Exception as e:
						showerror("Mistake", "Phone no shud be of 10 digits")
			except Exception as e:
				showerror("Mistake", "Invalid age")
	except Exception as e:
		showerror("Mistake", "Invalid name")

# back on calculate window
def f5():
	cw.withdraw()
	mw.deiconify()
	con = None
	try:
		con = connect("project.db")
		cursor = con.cursor()
		sql = "select * from bmi_info"
		cursor.execute(sql)
		ent_count.delete(0, END)
		data = cursor.fetchall()
		if len(data) == 0:
			ent_count.insert(INSERT, "Count = 0")
		else:
			res = "Count = " + str(len(data))
			ent_count.insert(INSERT, res)
	except Exception as e:
		showerror("Mistake", e)
	finally:
		if con is not None:
			con.close()


cw = Toplevel(root)
cw.title("Calculate")
cw.geometry("800x500+150+100")

s= IntVar()
s.set(20)

lab_name = Label(cw, text="Enter name", font=fd)
ent_name = Entry(cw, font=fd, bd=2)
lab_age = Label(cw, text="Enter age", font=fd)
ent_age = Entry(cw, font=fd, bd=2)
lab_phone = Label(cw, text="Enter phone", font=fd)
ent_phone = Entry(cw, font=fd, bd=2)
lab_gender = Label(cw, text="Gender", font=fd)
rb_male = Radiobutton(cw, text="Male", font=fd, variable=s, value=1)
rb_female = Radiobutton(cw, text="Female", font=fd, variable=s, value=2)
lab_height= Label(cw, text="Enter height in mtr", font=fd)
ent_height= Entry(cw, font=fd, bd=2)
lab_weight= Label(cw, text="Enter weight in mtr", font=fd)
ent_weight= Entry(cw, font=fd, bd=2)
btn_convert = Button(cw, text="Convert", font=fd, command=f3)
btn_calculate = Button(cw, text="Calculate", font=fd, command=f4)
btn_back = Button(cw, text="Back", font=fd, command=f5)

lab_name.place(x=10, y=20)
ent_name.place(x=300, y=20)
lab_age.place(x=10, y=70)
ent_age.place(x=300, y=70)
lab_phone.place(x=10, y=120)
ent_phone.place(x=300, y=120)
lab_gender.place(x=10, y=170)
rb_male.place(x=300, y=170)
rb_female.place(x=400, y=170)
lab_height.place(x=10, y=220)
ent_height.place(x=300, y=220)
btn_convert.place(x=650, y=220)
lab_weight.place(x=10, y=270)
ent_weight.place(x=300, y=270)
btn_calculate.place(x=100, y=350, width=150)
btn_back.place(x=300, y=350, width=150)


cw.withdraw()

# convert on height converter window
def f6():
	try:
		feet = float(ent_feet.get())
		inches = float(ent_inches.get())
		if feet <=0 or feet > 7 or inches < 0 or inches > 11:
			raise Exception
	
	except Exception as e:
		showwarning("Mistake", "Enter valid details")

	else:
		r1 = feet * 0.3048
		r2 = inches * 0.0254
		res = r1 + r2
		showinfo("Meters", res)

	finally:
		ent_feet.delete(0, END)
		ent_inches.delete(0, END)
			
def f9():
	hw.withdraw()
	cw.deiconify()		

hw = Toplevel(root)
hw.title("Height Converter")
hw.geometry("500x500+250+100")

lab_height = Label(hw, text="Enter your height", font=fd)
lab_feet = Label(hw, text="Feet", font=fd)
ent_feet = Entry(hw, font=fd, bd=2)
lab_inches = Label(hw, text="Inches", font=fd)
ent_inches = Entry(hw, font=fd, bd=2)
btn_convert = Button(hw, text="Convert", font=fd, command=f6)
btn_back = Button(hw, text="Back", font=fd, command=f9)

y=10
lab_height.pack(pady=y)
lab_feet.pack(pady=y)
ent_feet.pack(pady=y)
lab_inches.pack(pady=y)
ent_inches.pack(pady=y)
btn_convert.pack(pady=y)
btn_back.pack(pady=y)

hw.withdraw()

def f7():
	vw.withdraw()
	mw.deiconify()
	

vw = Toplevel(root)
vw.title("View")
vw.geometry("500x400+200+100")

y=10
vw_data = ScrolledText(vw, width=30, height=10, font=fd)
btn_back = Button(vw, text="Back", font=fd, command=f7)
vw_data.pack(pady=y)
btn_back.pack(pady=y)

vw.withdraw()

root.mainloop()