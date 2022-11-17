import datetime as dt
from datetime import datetime
from tkinter import ttk
from tkinter.tix import *

# Simple Day Planner - Made by JJP
# Licensed under MIT Licensing for Creative Use Only
# I am fully aware that my code is 'sloppy', this was just a quick project
def checkEarlier(mystarttime, prevstarttime):
    if int(mystarttime[0]) < int(prevstarttime[0]) or (
            int(mystarttime[0]) == int(prevstarttime[0]) and int(mystarttime[1]) < int(prevstarttime[1])):
        return True
    else:
        return False

def createEvent():
    # Stands for "write in correct place"
    def wcp(myentry):
        with open(myfn, "a+") as f:
            index = 0
            f.seek(0)
            myevents = f.readlines()
            mystarttime = myentry.split(" at ")[-1].split(" until ")[0].split(":")
            for i in myevents:
                if i.strip():
                    prevstarttime = i.split(" at ")[-1].split(" until ")[0].split(":")
                    if not checkEarlier(mystarttime, prevstarttime):
                        index += 1

        myevents.insert(index, myentry)
        with open(myfn, "w") as f:
            myevents = "".join(myevents)
            f.write(myevents)

    # Command for the confirm event button
    def ceButton():
        global ne
        if v1.get() > v3.get() or (v1.get() == v3.get() and v2.get() >= v4.get()) or (len(eventname.get())==0):
            Label(cew, text="Please give valid inputs").place(anchor=N, rely=0.6, relx=0.5)
        else:
            fulltext = eventname.get() + " at " + v1.get()+":"+v2.get() + " until " + v3.get()+":"+v4.get()+"\n"
            wcp(fulltext)
            getNextFive(myfn, ne)
            cew.destroy()
    hourslist = list(range(0,24))
    for i in range(0,10):
        hourslist[i] = "0"+str(i)
    minuteslist = [str(5*a) for a in range(0,12)]
    minuteslist[0] = "00"
    minuteslist[1] = "05"
    currentdate = dt.date.today()
    myfn = str(currentdate) + "-plan.txt"
    cew = Toplevel(main)
    cew.title("Create event")
    cew.geometry("400x200")
    Label(cew, text="Event name", font=("Helvetica 12")).place(relx=0.5,rely=0,anchor=N)
    eventname = Entry(cew, bd=1, font=("Helvetica 12"))
    eventname.place(rely=0.1,relx=0.5,anchor=N, relheight=0.2, relwidth = 0.5)
    Label(cew,text="Start Time", font=("Helvetica 12")).place(rely=0.4,relx=0.25, anchor=CENTER)
    v1 = StringVar(cew)
    v1.set(hourslist[0])
    v2 = StringVar(cew)
    v2.set(minuteslist[0])
    ttk.Combobox(cew, textvariable=v1, values=hourslist).place(relx=0.19,rely=0.5,anchor=CENTER,relwidth=0.09)
    ttk.Combobox(cew, textvariable=v2, values=minuteslist).place(relx=0.31, rely=0.5, anchor=CENTER, relwidth=0.09)
    Label(cew, text=":").place(anchor=CENTER, relx=0.25,rely=0.5)

    v3 = StringVar(cew)
    v3.set(hourslist[0])
    v4 = StringVar(cew)
    v4.set(minuteslist[0])
    Label(cew, text="End Time", font=("Helvetica 12")).place(rely=0.4, relx=0.75, anchor=CENTER)
    ttk.Combobox(cew, textvariable=v3, values=hourslist).place(relx=0.69,rely=0.5,anchor=CENTER,relwidth=0.09)
    ttk.Combobox(cew, textvariable=v4, values=minuteslist).place(relx=0.81, rely=0.5, anchor=CENTER,
                                                                       relwidth=0.09)
    Label(cew, text=":").place(anchor=CENTER, relx=0.75, rely=0.5)
    Button(cew, text="Create Event", command=ceButton).place(relx = 0.5, rely = 0.7, anchor = N, relwidth = 0.4, relheight = 0.2)



def clearFile(filename):
    open(filename, 'w').close()

def conf_delete():
    todayfile = str(dt.date.today()) + "-plan.txt"
    top = Toplevel(main)
    top.title("Confirm deletion")
    top.geometry("600x200")
    Label(top,
          text="Are you sure you want to delete all events?",
          font=("Helvetica 18 bold")
    ).place(relwidth=0.9, relx=0.5, anchor=N, rely=0.1)
    Button(top,
           text="Yes",
           font=("Helvetica 18"),
           command=lambda:[clearFile(todayfile),top.destroy()]
    ).place(rely=0.7, relx=0.3, anchor=N, relwidth=0.2, relheight=0.3)
    Button(top,
           text="No!",
           font=("Helvetica 18"),
           command=top.destroy
           ).place(rely=0.7, relx=0.7, anchor=N, relwidth=0.2, relheight=0.3)

def getNextFive(file, labels):
    now = datetime.now()
    currenttime = [now.hour, now.minute]
    myindex = 0
    with open(file, "r") as f:
        global ne
        mylines = f.readlines()
        linenum = len(mylines)
        f.seek(0)
        for i, x in enumerate(mylines):
            if x.strip():
                myst = x.split(" at ")[-1].split(" until ")[0].split(":")
                if checkEarlier(currenttime, myst):
                    myindex = i
                    break
    if(len(mylines)!=0):
        finalev = mylines[-1]
        finaltime = finalev.split(" at ")[-1].split(" until ")[0].split(":")
        if checkEarlier(currenttime, finaltime):
            for j in range(myindex, min(5+myindex,linenum)):
                labels[j-myindex].config(text=mylines[j], fg="black")
        else:
            labels[0].config(text="All tasks done for today!", fg="green")
    else:
        labels[0].config(text="All tasks done for today!", fg="green")

def showAllEvents():
    def clearLabel():
        noevents['text'] = ''
    allEvents = Toplevel(main)
    allEvents.title("List of Events")
    file = str(dt.date.today()) + "-plan.txt"
    scrollbar = Scrollbar(allEvents)
    scrollbar.pack(side=RIGHT, fill=Y)
    mylist = Listbox(allEvents, yscrollcommand = scrollbar.set, bd=0, relief="flat", font=("Ariel 13"),selectmode=SINGLE)
    with open(file, "r") as f:
        allevents = f.readlines()
        if allevents == []:
            noevents = Label(main, text="No events to be found", fg="red")
            noevents.place(anchor=S, relx=0.25, rely=0.3)
            allEvents.destroy()
            main.after(5000, clearLabel)
            return
    for event in allevents:
        mylist.insert(END, "- "+event)
    mylist.config(width=0)
    if(len(allevents) < 8):
        newheight = 8
    else:
        newheight = 0
    mylist.config(height=newheight)
    mylist.pack()
    scrollbar.config(command=mylist.yview)

def deleteEvent():
    def clearLabel():
        noevents['text'] = ''
    def getSelection():
        with open(file, "r") as f:
            allevents = f.readlines()
        for i in mylist.curselection():
            allevents.pop(i)
            mylist.delete(i)
        with open(file, "w") as f:
            allevents = ''.join(allevents)
            f.write(allevents)

    file = str(dt.date.today()) + "-plan.txt"
    de = Toplevel(main)
    Label(de, text="Please select the event you would like to delete",font=("Ariel 13")).pack(expand=TRUE)
    scrollbar = Scrollbar(de)
    scrollbar.pack(side=RIGHT, fill=Y)
    mylist = Listbox(de, yscrollcommand=scrollbar.set, bd=0, relief="flat", font=("Ariel 13"), selectmode=SINGLE)
    with open(file, "r") as f:
        allevents=f.readlines()
        if allevents == []:
            noevents = Label(main, text="No events to be found", fg="red")
            noevents.place(anchor=S, relx=0.25, rely=0.55)
            de.destroy()
            main.after(5000, clearLabel)
            return
    for event in allevents:
        mylist.insert(END, "- " + event)
    mylist.config(width=0)
    mylist.config(height=10)
    mylist.pack()
    Button(de, text="Delete", command=getSelection).pack()
    scrollbar.config(command=mylist.yview)
if __name__ == '__main__':
    myfn = str(dt.date.today()) + "-plan.txt"
    with open(myfn, "a+") as f:
        f.seek(0)
        mydata = f.readlines()
    main = Tk()
    main.geometry("600x300")
    main.title("Day Planner")
    main.columnconfigure(0, weight=1)
    main.columnconfigure(1, weight=1)
    sepstyle = ttk.Style()
    sepstyle.configure('red.TSeparator', background="#eb3841")
    event = Button(main, text="Create New Event", command=createEvent).place(relx=0.25,rely=0.05, relheight=0.15, relwidth=0.3,anchor=N)
    seeEvents = Button(main, text="See All Events", command=showAllEvents).place(relx=0.25, rely=0.3, relheight=0.15, relwidth=0.3,
                                                              anchor=N)
    deleteEvent = Button(main, text="Delete Event", command=deleteEvent).place(relx=0.25, rely=0.55, relheight=0.15, relwidth=0.3,
                                                                anchor=N)
    deleteAllEvents = Button(main, text="Delete all events", bg="red", command=conf_delete).place(relx=0.25, rely=0.8, relheight=0.15, relwidth=0.3,
                                                                anchor=N)
    uc = Label(main, text="Upcoming Tasks", font=("Helvetica 18 underline")).place(anchor=N, relx=0.75,rely=0, relheight=0.1)
    ne = []
    ne.append(Label(main, text="No Task", borderwidth=1, relief="solid", font=("Arial 13")))
    ne.append(Label(main, text="No Task", borderwidth=1, relief="solid", font=("Arial 13")))
    ne.append(Label(main, text="No Task", borderwidth=1, relief="solid", font=("Arial 13")))
    ne.append(Label(main, text="No Task", borderwidth=1, relief="solid", font=("Arial 13")))
    ne.append(Label(main, text="No Task", borderwidth=1, relief="solid", font=("Arial 13")))
    ne[4].place(anchor=N, relx=0.75,rely=0.84, relwidth=0.5, relheight=0.16)
    for i,_ in enumerate(ne):
        ne[i].place(anchor=N,relx=0.75,rely=(0.2+0.16*i), relwidth=0.5, relheight=0.16)
    linebet = ttk.Separator(main, orient=VERTICAL, style="red.TSeparator").place(relx=0.5, relheight = 1, rely=0)
    getNextFive(myfn, ne)
    main.mainloop()
