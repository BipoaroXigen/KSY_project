from tkinter import *
import random
from PIL import ImageTk, Image
import time
# import symbols as img

class Guy:


    ### on the beggining

    def __init__(self, title):
        self.id = self.get_test_id()
        self.started = FALSE

        self.root = Tk()
        self.root.title(title)
        self.root.iconbitmap("logo.ico")
        self.root.bind("<Key>", self.key)

        self.root.geometry("600x400")

        self.initial_screen()

        self.root.mainloop()

    def initial_screen(self):        
        self.text = StringVar()
        self.text.set("test střídání úloh")

        self.banner = Label(self.root, textvariable=self.text, font=30)
        self.banner.place(relx=0.5, rely=0.1, anchor=CENTER)

        self.set = Entry()
        self.set.insert(50, "       počet úloh   (50)")
        self.set.config(fg="gray", font=16)
        self.set.place(relx=0.5, rely=0.2, anchor=CENTER)

        self.startButton = Button(self.root, text="start", command=lambda: self.begin(), font=16, width=10, height=3)
        self.startButton.place(relx=0.5, rely=0.5, anchor=CENTER)
        

    ### in time if test

    #### handlers

    def begin(self):
        "start the test"   

        # get settings
        try:
            self.repetitions = int(self.set.get())
        except:
            self.repetitions = 50

        self.results = "results/results" + self.id + ".txt"

        # prepare view
        # clear old view
        # self.clear_text()
        self.clear_input()
        self.replace_button()
        # show guide

        # run test
        self.started = TRUE
        self.run = -1
        self.initiate_task()

            # get task
            # show task text
            # initialize symbols
            # start timing


            # evaluate click
            # show evaluation
            # save evaluation
            # wait
            # repeat

    def initiate_task(self):
        "initiates choosen number of tasks"

        if self.run == self.repetitions-1:
            self.end_test()
        self.run += 1

        # retrieve symbols for task
        self.symbol1 = self.get_symbol_index()
        self.symbol2 = self.get_symbol_index()
        while self.symbol2 == self.symbol1 or (abs(self.symbol2 - self.symbol1) == 2) or (self.symbol1 == 0 and self.symbol2 == 1) or (self.symbol1 == 2 and self.symbol2 == 3) or (self.symbol1 == 1 and self.symbol2 == 0) or (self.symbol1 == 3 and self.symbol2 == 2):
            self.symbol2 = self.get_symbol_index()

        # retrieve task
        self.Task = self.get_task()
        
        if self.run == 0:
            delay = 0
        else:
            delay = 2000

        self.banner.after(delay, self.show_task_text, self.Task)
        self.banner.after(delay, self.show_symbols, self.get_symbol(self.symbol1), self.get_symbol(self.symbol2), self.run)

        # start counting answer duration time
        self.start_time = self.timer(0)

    def check_answer(self, task, answer):
        "evaluate submitted answer"
        # stop counting answer duration time
        self.end_time = self.timer(self.start_time)
        
        success = self.evaluate(task, answer)
        self.save_success(success)
        # print(success)

        # show success
        self.show_success(success)
        # time.sleep(2)
        # wait 2 seconds

        self.initiate_task()

        # # recieve click
        # timer = self.timer(timer)

        # # evaluate click
        # # show evaluation
        # # save evaluation
        # # wait
        # time.sleep(10)

    def end_test(self):
        "cancels the whole test"

        self.started = False

        # exit()

        self.root.destroy()

        # set neutral layot / results


    #### test frontend

    def show_symbols(self, symbol1, symbol2, i):
        if i == 0:
            # get symbols as img
            img1 = ImageTk.PhotoImage(Image.open(symbol1))
            img2 = ImageTk.PhotoImage(Image.open(symbol2))
            # assign images
            self.symbol_placeholder1 = Label(self.root, image=img1)
            self.symbol_placeholder2 = Label(self.root, image=img2)
            # show images
            # self.symbol_placeholder1.grid(row=2, column=2)
            # self.symbol_placeholder2.grid(row=2, column=4)
            self.symbol_placeholder1.place(relx=0.3, rely=0.45, anchor=CENTER)
            self.symbol_placeholder2.place(relx=0.7, rely=0.45, anchor=CENTER)

        # get symbols as img
        img1 = ImageTk.PhotoImage(Image.open(symbol1))
        img2 = ImageTk.PhotoImage(Image.open(symbol2))
        # assign different images
        self.symbol_placeholder1.configure(image=img1)
        self.symbol_placeholder2.configure(image=img2)
        # show newly assigned images
        self.symbol_placeholder1.image = img1
        self.symbol_placeholder2.image = img2

    def clear_input(self):
        self.set.destroy()

    def show_task_text(self, task):
        self.banner.place(relx=0.5, rely=0.1, anchor=CENTER)
        # self.text.destroy()

        taskText = ['kruh', 'čtverec', 'červená', 'modrá']
        txt = taskText[task]
        # self.text = Label(self.root, text=txt)
        # self.text.after(2000, self.show_text)
        # self.text.grid(row=1, column=3)
        self.text.set(txt)

    def replace_button(self):
        "shows answering buttons"
        # destroy start button
        self.startButton.destroy()

        # setup buttons for symbols
        vote1 = Button(self.root, text='levá', command=lambda: self.check_answer(self.Task, 0), width=10, font=16) 
        # vote1.grid(row=4, column=2)
        vote2 = Button(self.root, text='pravá', command=lambda: self.check_answer(self.Task, 1), width=10, font=16)
        # vote2.grid(row=4, column=4)

        vote1.place(relx=0.3, rely=0.8, anchor=CENTER)
        vote2.place(relx=0.7, rely=0.8, anchor=CENTER)

    def get_symbol(self, indx):
        "get random geometric symbol from index"
        symbols = ["symbols/red-cir.png", "symbols/blu-cir.png",
                   "symbols/red-sqr.png", "symbols/blu-sqr.png"]
        return symbols[indx]

    def show_success(self, success):        

        self.show_symbols("symbols/gry-sqr.png", "symbols/gry-sqr.png", 1)

        if success:
            self.text.set("Správně!")
        else:
            self.text.set("Špatně!")

    #### test backend

    def key(self, event):
        "recieve click"

        if self.started:

            if event.char == "a":
                clicked = 0
            elif event.char == "d":
                clicked = 1
            elif event.char == "s":
                clicked = 0
            elif event.char == "k":
                clicked = 1 
            elif event.char == "l":
                clicked = 1

            self.check_answer(self.Task, clicked)

        elif event.char == '\r':
            self.begin()

    def get_symbol_index(self):
        "get random geometric symbol index"
        # 0 - red + circle
        # 1 - blue + circle
        # 2 - red + square
        # 3 - blue + square

        return random.randint(0, 3)

    def get_task(self):
        "returns task for subject"
        # 0 - choose circle
        # 1 - choose square
        # 2 - choose red
        # 3 - choose blue
    
        ints = [self.symbol1, self.symbol2]
        # print(ints)
        possibleTasks = []

        # decide which tasks are possible for given symbols
        if 0 in ints:
            possibleTasks.append(0)
            possibleTasks.append(2)
        if 1 in ints:
            possibleTasks.append(0)
            possibleTasks.append(3)
        if 2 in ints:
            possibleTasks.append(1)
            possibleTasks.append(2)
        if 3 in ints:
            possibleTasks.append(1)
            possibleTasks.append(3)

        # return random possible task
        return random.choice(possibleTasks)

    def timer(self, x):
        return time.time() - x
        
    def evaluate(self, task, side):
        "decides whether task was answered correctly"

        # print("side",side)

        # match symbols with answer
        symbolLeft = self.symbol1
        symbolRight = self.symbol2

        # get which symbol was chosen as answer
        if side == 0:
            symbol = symbolLeft
        else:
            symbol = symbolRight

        # print()
        # print("odpověď")
        # print(symbol)
        # check answer
        if task == 0:
            if symbol == 0 or symbol == 1:
                return TRUE
        if task == 1:
            if symbol == 2 or symbol == 3:
                return TRUE
        if task == 2:
            if symbol == 0 or symbol == 2:
                return TRUE
        if task == 3:
            if symbol == 1 or symbol == 3:
                return TRUE

        return FALSE

    def save_success(self, success):
        f = open(self.results, "a")
        if success:
            f.write("\n" + str(self.end_time) + "_0_" + str(self.Task))
        else:
            f.write("\n" + str(self.end_time) + "_1_" + str(self.Task))

    def get_test_id(self):
        return str(time.time())
