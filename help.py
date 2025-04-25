from tkinter import Tk, Label, PhotoImage, Canvas
def help():
    inter = Tk()
    inter.geometry("1080x720")
    text1 = Label(inter,text="CHINESE CHECKERS GAME",fg='#66B2FF',font=("Comic Sans MS",25))
    text2 = Label(inter,text="Game Rules :",fg='#404040',font=("Comic Sans MS",20))
    text3 = Label(inter,text= "The aim is to race all one's pieces into the star corner on the opposite side of the board"
                              "before the opponents do the same.\n Each player starts with 10 colored pieces on one of the six corners.\n"
                              " Players take turns moving a single piece, either by moving one step in any direction to an empty space,\n"
                              " or by jumping in one or any number of available consecutive hops over other single pieces.",
                  font=("Comic Sans MS",14))
    image = PhotoImage(file="helppic.png").zoom(20).subsample(35)
    canvas = Canvas(inter,width=1080,height=400)
    canvas.create_image(500,200,image=image)
    canvas.place(x=30,y=220)
    text1.pack()
    text2.pack()
    text3.pack()
    inter.mainloop()
