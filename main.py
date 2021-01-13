import guy as guy
import evaluator as evaluator
# import random
# from tkinter import *
# from PIL import ImageTk, Image
# import symbols as img

G = guy.Guy('střídání úloh: test')
id = G.id
try:
    Eval = evaluator.Evaluator(id)
    Eval.print()
except:
    pass