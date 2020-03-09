from tkinter import *
from tkinter import messagebox

window = Tk()

window.title("JFET Amp Components Calculation")

window.geometry('250x400')

required_vals = ['Rin', 'Rout', 'Vdd', 'fco', 'Avo', 'Vpo', 'Idss', 'Vdsq', 'beta',
                    'lambda', 'Rsig', 'k', 'Rl']

rows = 0
objects = []

for i in required_vals:
    temp = Entry(window, width = 10)
    temp.grid(column = 1, row=rows)
    temp_lbl = Label(window, text = i)
    temp_lbl.grid(column=0, row=rows)

    objects.append(temp)
    rows += 1

def parallel(*args):
    """
    Takes an array of parallel resistances and returns the equivalent resistance.

    --------
    Arguments: R1,R2,R3,...,Rn

    Returns: 1/(1/R1 + 1/R2 + ...)
    """
    return 1/sum([1/i for i in args])

def clicked():
    Rin = float(objects[0].get())
    Rout = float(objects[1].get())
    Vdd = float(objects[2].get())
    fco = float(objects[3].get())
    Avo = float(objects[4].get())
    Vpo = float(objects[5].get())
    Idss = float(objects[6].get())
    Vdsq = float(objects[7].get())
    beta = float(objects[8].get())
    lambdaa = float(objects[9].get())
    Rsig = float(objects[10].get())
    k = float(objects[11].get())
    Rl = float(objects[12].get())

    Rg = Rin
    gm = - Avo/Rout
    Rds = 1/gm
    Vgs = lambda Vpo, lambdaa, Idss, Vdsq, gm : 0.5*Vpo*(Vpo/Idss)*(1/(1+lambdaa*Vdsq))*gm + Vpo
    Vgsq = Vgs(Vpo, lambdaa, Idss, Vdsq, gm)
    Id = lambda Idss, Vgsq, Vpo, lambdaa, Vdsq : Idss*(1+lambdaa*Vdsq)*(1-Vgsq/Vpo)**2
    Idq = Id(Idss, Vgsq, Vpo, lambdaa, Vdsq)
    Rs = -Vgsq/Idq
    gds = Idq/((1/lambdaa)+Vdsq)
    rds = 1/gds
    Rd = 1/((1/Rout)-gds)
    Vd = Rd*Idq+Vdsq+Rs*Idq
    Rgeq = Rg+Rsig
    Rdeq = Rl + parallel(rds,Rd)
    Rseqp = (rds+parallel(Rd,Rl))/(1+ gm*rds)
    Rseq = parallel(Rs,Rseqp)
    fCap = lambda k, Req, fco : k/(Req*fco)

    Cg = fCap(k,Rgeq, fco)
    Cd = fCap(k,Rdeq,fco)
    Cs = fCap(k,Rseq,fco)

    text = "Rs = " + str(Rs) + "\n" + "Rg = " + str(Rg) + "\n" +"Rd = " + str(Rd) + "\n" + "Cs = " + str(Cs) + "\n" +"Cg = " + str(Cg) + "\n" + "Cd = " + str(Cd)
    messagebox.showinfo('BJT',text)

btn = Button(window, text='Run Calculations', command=clicked)

btn.grid(column=4,row=15)

window.mainloop()
