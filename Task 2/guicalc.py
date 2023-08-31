
from math import sqrt
from string import digits
from functools import partial

from tkinter import *
from tkinter import ttk,font

def print_hier(widg,d=0):
	filler = d * " "
	print("{}Class:{}\n{}Width:{}\n{}Height:{}\n{}Left:{}\n{}Top:{}\n".format(filler,widg.winfo_class(),filler,widg.winfo_width(),filler,widg.winfo_height(),filler,widg.winfo_x(),filler,widg.winfo_y()))
	for child in widg.winfo_children():
		print_hier(child,d+1)
def errMess(mess):
	global stack,ebox
	def do():
		ebox.configure(background='white',foreground="black")
		stack.set('')
	ebox.configure(background='#ed4337',foreground="#272727")
	stack.set(mess)
	ebox.after(3000,do)
def parseSqr(expstr):
    global keys
    flag,ind=False,0
    exp = expstr
    while('√' in exp):
        leng = len(exp)
        i = 0 
        while(i < leng):
            if(exp[i]=='√'):
                ind = i
                flag = True
            elif(flag==True and i==leng-1):
                exp = exp[:ind]+str(sqrt(float(exp[ind+1:])))
                flag = False
                ind = 0
                leng = len(exp)
            elif(flag==True and (exp[i] in keys[4:])):
                exp = exp[:ind]+str(sqrt(float(exp[ind+1:i])))+exp[i:]
                flag = False
                ind = 0
                leng = len(exp)
            i+=1
    return exp	
def pushSym(char,isOp=False):
	global stack,keys
	cexp = stack.get()
	if(isOp==True):
		if(len(cexp)!=0):
			if(cexp[-1] in keys and char not in ['!','√']):	
				stack.set(cexp[:-1]+char)
			elif(char not in ['!','√'] or cexp[-1] in keys):
				stack.set(cexp+char)
			else:
				return
		else:	
			if(char in ['!','√']):
				stack.set(cexp+char)
			else:
				return
	else:
		stack.set(cexp+char)
def doCalc():
	global stack
	try:
		expression = stack.get()
		expression = expression.replace('^','**')
		expression = expression.replace('!','-')
		expression = parseSqr(expression)
		stack.set(eval(expression))
	except ZeroDivisionError:
		errMess("Division by zero not allowed")
	except (NameError,SyntaxError):
		errMess("Syntax error ...")


window = Tk()

logo = PhotoImage(file='guicalc.png')
window.title('Funky Calculator')
window.geometry('576x324')
window.iconphoto(False,logo)

window.configure(bg='#272727')
window.columnconfigure(0,weight=1)
window.rowconfigure(0,weight=1)

keys = ['C','√','!','CE','/','*','-','+']
digs = list(digits[len(digits)::-1]+".=")
stack,bl = (StringVar(),StringVar())

keypad = Frame(window,bg='#272727')
ebox = Entry(window,textvariable=stack)
ebox.configure(font=('Segoe UI',20),bg='white',fg='#272727',width=40,relief='sunken',justify=RIGHT)
ebox.pack(side="top",pady=10)
keypad.pack(side="top")
m,n = (0,)*2
for i in range(5):
	for j in range(4):
		if(j==3):
			wid = keys[n]
			col='#d6d7d7'
			n+=1
		elif(i==0):
			wid = keys[n]
			col='#d6d7d7'
			n+=1
		else:
			wid = digs[m]
			m+=1
		ebut = Button(keypad,text=wid)
		if(wid=='='):
			col = '#f7444e'
			ebut['command'] = doCalc
		elif(wid=='CE'):
			ebut['command'] = lambda:stack.set(stack.get()[:-1])
		elif(wid=='C'):
			ebut['command'] = lambda:stack.set('')
		elif(wid in keys):
			ebut['command'] = partial(pushSym,wid,isOp=True)
		else:
			ebut['command'] = partial(pushSym,wid)
		ebut.configure(foreground="black",bd=0,highlightbackground='#272727',highlightcolor='#272727',font=('Impact',24),bg=col,relief='raised')
		ebut.grid(row=i,column=j,padx=5,pady=5,ipadx=40,ipady=10,sticky=(N,W,E,S))

for i in range(5):
	keypad.rowconfigure(i,weight=0)
for j in range(4):
	keypad.columnconfigure(j,weight=2)

#print_hier(grid)
window.mainloop()