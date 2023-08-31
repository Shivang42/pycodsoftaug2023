isclip = True
from time import time
from math import factorial,floor,ceil
from random import randint,seed,shuffle
from string import digits,ascii_letters,punctuation
try:
	from pyperclip import copy
except:
	print("Please install Pyperclip first ...")
	isclip = False
from tkinter import *
from tkinter import ttk,font

seed(time())
def ncx(n,x):
    return int(factorial(n)/(factorial(n-x)*factorial(x)))
def print_hier(widg,d=0):
	filler = d*" "
	print("{}Class:{}\n{}Width:{}\n{}Height:{}\n{}Left:{}\n{}Top:{}\n".format(filler,widg.winfo_class(),filler,widg.winfo_width(),filler,widg.winfo_height(),filler,widg.winfo_x(),filler,widg.winfo_y()))
	for child in widg.winfo_children():
		print_hier(child,d+1)
def adjBut(e):
	submit.configure(font=('Impact',int(grid.winfo_width()/36)))
	reset.configure(font=('Impact',int(grid.winfo_width()/56)))
	submit.grid_configure(ipadx=int(grid.winfo_width()/360),pady=int(grid.winfo_height()/348))
def genPwd(num,complexity):
    a,b,c,d = (0,)*4
    if(num%4==0):
        a,b,c,d = (int(num/4),)*4
    elif(num%4==1):
        a = ceil(num/4)
        b,c,d = (floor(num/4),)*3
    elif(num%4==2):
        a,b = (floor(num/4),)*2
        c,d = (ceil(num/4),)*2
    elif(num%4==3):
        a,b,c = (ceil(num/4),)*3
        d = floor(num/4)
    fpwd = ''
    match complexity:
        case 'High':
            d1,d2,d3 = b+c,a,d
        case 'Medium':
            d1,d2,d3 = b+c,a+d,0
        case 'Low':
            d1,d2,d3 = a+b+c+d,0,0
    for i in range(d1):
        fpwd+=ascii_letters[randint(0,len(ascii_letters)-1)]
    for i in range(d2):
        fpwd+=digits[randint(0,len(digits)-1)]
    for i in range(d3):
        fpwd+=punctuation[randint(0,len(punctuation)-1)]
    
    perms = list(fpwd)
    shuffle(perms)
    return ''.join(perms)
def copied(e):
	global valid,isclip
	if (not valid or not isclip):
		return
	def doIt(save):
		global greet,sent
		sent.configure(image=cop,background='#272727',foreground="teal",textvariable=greet)
		greet.set(save)
	global sent,greet
	save = greet.get()
	copy(save)
	greet.set('Copied ...')
	sent.configure(background='teal',foreground="#272727",image='')
	sent.after(1600,lambda:doIt(save))
def popMess(wid,mess,x,y):
	global window,valid,poppin
	if (poppin is True or valid is False):return
	def plo():
		global poppin
		popup.destroy()
		poppin = False
		wid.bind('<Motion>',lambda e:'a')
	poppin = True
	popup = Toplevel(window,bg='white')
	popup.geometry('140x40')
	lab = Label(popup,text=mess)
	lab.configure(anchor=NW,font=font.Font(family='Segoe UI',size=10,weight='bold'),bg='white',fg='brown')
	lab.place(relx=0,rely=0)
	popup.geometry('+{}+{}'.format(x,y))
	wid.bind('<Motion>',lambda e:popup.geometry('+{}+{}'.format(e.x_root,e.y_root)))
	popup.overrideredirect(1)
	popup.wm_transient()
	window.after(3800,plo)
def errMess(mess):
	global stl,sent
	sent.configure(background='#ed4337',foreground="white")
	sent.after(3000,lambda:sent.configure(background='#272727',foreground="teal"))
	greet.set(mess)
def resetGrid():
	global leng,comp,greet,sent
	leng.set('')
	comp.set('')
	greet.set('')
	sent.configure(image='')
def genGreet():
	global stl,sent,greet,cop,leng,valid
	if(len(comp.get()) > 0):
		try:
			global valid
			if(len(leng.get())>0):
				a = int(leng.get())
				if(a<=0):
					valid = False
					sent.configure(image='')
					raise ValueError()
				pwd = genPwd(a,comp.get())
				greet.set(pwd)
				sent.configure(image=cop)
				valid = True
			else:
				valid = False
				sent.configure(image='')
				errMess("Almost there {}, just need your password length".format(comp.get()))
		except ValueError:
			valid = False
			sent.configure(image='')
			errMess("That is not a number, {}".format(comp.get()))
	else:
		valid = False
		sent.configure(image='')
		errMess("xx Please insert a valid complexity, Senor xx")


valid,poppin = (False,)*2
window = Tk()
stl = ttk.Style()

stl.configure('Header.TLabel',font=('Impact',24),background='#272727',foreground="teal",underline=1,bd=4)
stl.configure('Question.TLabel',font=font.Font(family='Segoe UI',size=16,weight='bold'),background='#272727',foreground="white",bd=2)
stl.configure('Focus.TLabel',background="red")

logo = PhotoImage(file='pwdgen.png')
window.title('Password Generator')
window.columnconfigure(0,weight=1)
window.rowconfigure(0,weight=1)
window.iconphoto(False,logo)

grid = Frame(window,bg="#272727")
grid['relief'] = 'raise'
grid['borderwidth'] = 0
grid['height'],grid['width'] = [i*0.5 for i in (1080,1920)]
grid['highlightthickness'] = 3
grid.configure(highlightcolor='#fad35e',highlightbackground='white')
grid.grid(column=0,row=0,sticky=(N,W,S,E))

header = ttk.Label(grid,style='Header.TLabel',text="Password Generator")
header.grid(column=1,row=0,sticky=(W))

levels=['Low','Medium','High']
comp,leng,greet = (StringVar(),StringVar(),StringVar())
q1 = ttk.Label(grid,style='Question.TLabel',text="Enter length")
q1.grid(column=0,row=2,sticky=(W,E))
a1 = Spinbox(grid,textvariable=leng,from_=1,to_=64,bg='#272727',fg='white',justify=CENTER,wrap=True)
q2 = ttk.Label(grid,style='Question.TLabel',text="Enter complexity")
q2.grid(column=0,row=4,sticky=(W,E))
a2 = OptionMenu(grid,comp,*levels)
a2.grid(column=2,row=4,sticky=(N,S,W,E))
a1.grid(column=2,row=2,sticky=(N,S,W,E))
a1.configure(font=('Impact',32),foreground="#272727",width=18)
a2.configure(font=('Impact',32),foreground="#272727",width=18)
a1.bind('<FocusIn>',lambda e:a1.configure(bg='white',fg='#272727'))
a1.bind('<FocusOut>',lambda e:a1.configure(fg='white',bg='#272727'))
a2.bind('<FocusIn>',lambda e:a2.configure(bg='white',fg='#272727'))
a2.bind('<FocusOut>',lambda e:a2.configure(fg='white',bg='#272727'))
a2['menu'].configure(font=('Impact',22),foreground="white",bg='#272727')


submit = Button(grid,text="Generate",command=genGreet,highlightthickness=4)
submit.configure(foreground="white",bd=0,highlightbackground='white',highlightcolor='white',font=('Impact',12),bg='#fad35e')
submit.grid(column=1,row=6,padx=105,pady=45,sticky=(N,S,W,E))
reset = Button(grid,text="Reset",command=resetGrid,highlightthickness=4)
reset.configure(foreground="white",bd=0,highlightbackground='white',highlightcolor='white',font=('Impact',12),bg='#cc1100')
reset.grid(column=1,row=7,ipady=1,ipadx=5)

cop = PhotoImage(file='copico.png')
footer = Frame(grid,bg="#272727",highlightthickness=3)
footer.config(highlightcolor='yellow',highlightbackground='white',relief='flat',bd=0)
footer.grid(column=0,row=8,sticky=(N,S,W,E),pady=10,ipady=10,columnspan=3,rowspan=2)
sent = Label(footer,textvariable=greet,image='',compound=RIGHT)
sent.configure(font=('Impact',14),background='#272727',foreground="teal",anchor=CENTER,bd=4,width=40,wraplength=sent.winfo_width())
sent.place(relx=0,rely=0,relwidth=1,relheight=1.5)
sent.bind('<Configure>',lambda e:sent.configure(wraplength=e.width))
sent.bind('<Button-1>',lambda e:copied(e))
sent.bind('<Enter>',lambda e:popMess(e.widget,"Click to copy{}".format('' if isclip else '\n(install pyperclip first)'),e.x_root,e.y_root))

for child in grid.winfo_children():
	if(child.winfo_class()=='TLabel'):
		if(child['style']=='Header.TLabel'):
			child.bind('<Configure>',lambda e:stl.configure('Header.TLabel',font=('Impact',int(grid.winfo_width()/24))))
		elif(child['style']=='Question.TLabel'):
			child.bind('<Configure>',lambda e:stl.configure('Question.TLabel',font=('Impact',int(grid.winfo_width()/36))))
a1.bind('<Configure>',lambda e:a1.configure(font=('Impact',int(grid.winfo_width()/56))))
a2.bind('<Configure>',lambda e:a2.configure(font=('Impact',int(grid.winfo_width()/56))))

submit.bind('<Configure>',lambda e:adjBut(e))
sent.bind('<Configure>',lambda e:sent.configure(font=('Impact',int(grid.winfo_width()/56)),wraplength=sent.winfo_width()))

for i in range(10):
	grid.rowconfigure(i,weight=1)
for j in range(3):
	grid.columnconfigure(j,weight=1)
#print_hier(grid)


window.mainloop()