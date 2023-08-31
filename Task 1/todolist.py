
from pickle import loads,dumps
from random import randint,seed,shuffle

from tkinter import *
from tkinter import ttk,font

def print_hier(widg,d=0):
	filler = d * " "
	print("{}Class:{}\n{}Width:{}\n{}Height:{}\n{}Left:{}\n{}Top:{}\n".format(filler,widg.winfo_class(),filler,widg.winfo_width(),filler,widg.winfo_height(),filler,widg.winfo_x(),filler,widg.winfo_y()))
	for child in widg.winfo_children():
		print_hier(child,d+1)
def addItem():
	global econt
	li1 = ListItem(econt.get())
	li1.show()
	econt.set('')

def adjBut(e):
	submit.configure(font=('Impact',int(grid.winfo_width()/36)))
	reset.configure(font=('Impact',int(grid.winfo_width()/56)))
	submit.grid_configure(ipadx=int(grid.winfo_width()/360),pady=int(grid.winfo_height()/348))

def popMess(wid,mess,x,y):
	global window,valid,poppin
	if (poppin is True or valid is False):return
	def plo():
		global poppin
		popup.destroy()
		poppin = False
		wid.bind('<Motion>',lambda e:'a')
	poppin = True
	popup = Toplevel(window,bg='#272727')
	popup.geometry('140x40')
	lab = Label(popup,text=mess)
	lab.configure(anchor=NW,font=font.Font(family='Segoe UI',size=10,weight='bold'),bg='#272727',fg='brown')
	lab.place(relx=0,rely=0)
	popup.geometry('+{}+{}'.format(x,y))
	wid.bind('<Motion>',lambda e:popup.geometry('+{}+{}'.format(e.x_root,e.y_root)))
	popup.overrideredirect(1)
	popup.wm_transient()
	window.after(3800,plo)
def errMess(mess):
	global stl,sent
	sent.configure(background='#ed4337',foreground="#272727")
	sent.after(3000,lambda:sent.configure(background='#f9f7f1',foreground="teal"))
	greet.set(mess)
def fetchdo():
	global tlist
	try:
		open('todo.pkl','rb')
	except:
		li1 = ListItem('')
		li1.show()
		return
	with open('todo.pkl','rb') as fin:
		llist = loads(fin.read())
		for li in llist:
			li1 = ListItem(li)
			li1.show()
def storedo():
	global tlist,grid
	tl = []
	if(len(grid.winfo_children())!=0):
		for litem in grid.winfo_children():
			for lchild in litem.winfo_children():
				if(lchild.winfo_class()=='Label'):
					tl.append(lchild['text'])
	with open('todo.pkl','wb') as tdl:
		tdl.write(dumps(tl))
	window.destroy()
def edit(e):
	global econt
	ttbox = e.widget.winfo_children()[0]
	def snclr():
		global addItem
		ttbox['text'] = ebox.get()
		econt.set('')
		ebut['text'] = 'Add Item'
		ebut['command'] = addItem
		ttbox.configure(highlightbackground='black',highlightcolor='black')

	econt.set(ttbox['text'])
	ttbox.configure(highlightbackground='yellow',highlightcolor='yellow')
	ebut['text'] = 'Update'
	ebut['command'] = snclr

class ListItem:
	def __init__(self,cont):
		global grid,header
		self.par = Frame(grid,highlightthickness=2,highlightbackground='#272727',height=40,width=560)
		self.par.configure(bg='#f9f7f1',bd=1)
		self.tbox = Label(self.par,text=cont)
		self.tbox.configure(font=font.Font(family='Trebuchet MS',size=14,weight='bold'),background='#f9f7f1',foreground="#272727",bd=0,anchor=CENTER)
		self.tbox.bind('<Configure>',lambda e:self.tbox.configure(wraplength=self.tbox.winfo_width()),add='+')
		self.editbut = Button(self.par,text="Edit",command=self.update,highlightthickness=4)
		self.editbut.configure(foreground="white",bd=0,highlightbackground='#272727',highlightcolor='#272727',width=14,height=2,font=('Impact',12),bg='#378805')
		self.delbut = Button(self.par,text="Delete",command=self.remove,highlightthickness=4)
		self.delbut.configure(foreground="white",bd=0,highlightbackground='#272727',highlightcolor='#272727',width=14,height=2,font=('Impact',12),bg='#cc1100')
	def show(self):
		self.par.pack(ipadx=20,ipady=20,fill=BOTH,anchor='nw',expand=True)
		self.par.pack_propagate(0)
		self.tbox.pack(side=LEFT,fill=X,expand=True)
		self.delbut.pack(padx=5,side=RIGHT,expand=False)
		self.editbut.pack(side=RIGHT,expand=False)
	def update(self):
		self.par.event_generate('<<EditMode>>')
	def remove(self):
		self.par.destroy()
		
valid,poppin = (False,)*2
window = Tk()
stl = ttk.Style()

stl.configure('Header.TLabel',font=('Impact',36),background='#f9f7f1',foreground="#002c3e",underline=1,bd=4,anchor=CENTER)
stl.configure('Question.TLabel',font=font.Font(family='Segoe UI',size=16,weight='bold'),background='#f9f7f1',foreground="#272727",bd=2)
stl.configure('Focus.TLabel',background="red")

logo = PhotoImage(file='todolist.png')
window.title('Todo List')
window.geometry('{}x{}'.format(int(1920*0.33),int(1080*0.33)))
window.iconphoto(False,logo)

window.configure(bg='#272727')
window.columnconfigure(0,weight=1)
window.rowconfigure(0,weight=1)
window.bind('<<EditMode>>',lambda e:edit(e))
window.protocol('WM_DELETE_WINDOW',storedo)


levels,econt,greet = (StringVar(),StringVar(),StringVar())
eframe = Frame(window)
header = ttk.Label(window,style='Header.TLabel',text="To-Do List")
header.pack(side="top",fill=X)
# header.grid(column=0,row=0,columnspan=4,rowspan=2,sticky=(N,W,E,S))
ebox = Entry(eframe,textvariable=econt)
ebox.configure(font=('Segoe UI',16),bg='#f3ecdb',fg='#272727',width=40,relief='sunken')
ebox.pack(side="left")
# ebox.grid(column=0,row=3,columnspan=2,sticky=(N,S))
ebut = Button(eframe,text="Add item",command=addItem)
ebut.configure(foreground="white",bd=0,highlightbackground='#272727',highlightcolor='#272727',font=('Impact',24),bg='#f7444e')
ebut.pack(side="left",padx=15)
eframe.pack(side="top",padx=15)

tlist = Canvas(window)

scrollbar = Scrollbar(window,orient='vertical')
scrollbar.config(command=tlist.yview)
scrollbar.pack(side="right",fill=Y)

tlist['yscrollcommand']=scrollbar.set
grid = Frame(tlist,bg="#f9f7f1",relief='raise',borderwidth=0,height=500,width=600)
grid['highlightthickness'] = 3
# grid.configure(highlightcolor='yellow',highlightbackground='yellow')
tlist['height'],tlist['width'] = 540,grid['width']
tlist.configure(bg='#f9f7f1',scrollregion=grid.bbox("all"))
nwin = tlist.create_window((0,0),window=grid,anchor="nw")
tlist.pack(side='top',pady=30)

window.after_idle(fetchdo)

for i in range(0,10):
	window.rowconfigure(i,weight=0)

def scaleWigs(e):
	global grid,tlist,nwin
	if(len(grid.winfo_children())!=0):
		for litem in grid.winfo_children():
			litem['width'] = int(e.width * 0.78) - 40
	if(grid.winfo_reqheight()!=tlist.winfo_height()):
		#THis is not required
		tlist.config(height=grid.winfo_reqheight())
	if(grid.winfo_reqwidth()!=tlist.winfo_width()):
		tlist.config(width=grid.winfo_reqwidth())

tlist.bind('<Configure>',lambda e:tlist.configure(scrollregion=tlist.bbox("all")))
window.bind('<Configure>',lambda e:stl.configure('Header.TLabel',font=('Impact',int(grid.winfo_width()/24))),add='+')
window.bind('<Configure>',lambda e:stl.configure('Question.TLabel',font=('Impact',int(grid.winfo_width()/48))),add='+')

header.bind('<Configure>',lambda e:scaleWigs(e),add='+')
window.bind('<MouseWheel>',lambda e:tlist.yview_scroll(int(e.delta/60),'units'))
#print_hier(grid)
window.mainloop()