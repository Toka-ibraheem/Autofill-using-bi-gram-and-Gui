import re
import tkinter as tk
from tkinter import *
from tkinter import messagebox


ngramsNum = 2
ngrams_list = {}
probabilities = {}
count = 0
nPredictions = 100
options = []


def prepareData():
    file = open(
       "C:\\Users\\dell\\Desktop\\dataset.txt",
        "r", encoding="UTF-8")
    dataset = file.read()
    file.close()
    return dataset


# preparing data for generating ngrams
def tokenizeText(text):
    text = text.lower()
    # tokenizing text to work on arabic and english words and numbers
    text = re.sub('[^\sa-zA-Z0-9ء-ي]', '', text)
    return text.split()

def calculateProb(sentence, counter=0):
    if sentence not in ngrams_list.keys():
        ngrams_list[sentence] = 1
    else:
        ngrams_list[sentence] += 1
    counter += 1
    probabilities[sentence] = ngrams_list[sentence] / counter
  
#print(prob.keys())
#print(prob.values())
def generateNGrams(words_list, n, counter=0):#bigram
    nGrams = []
    for num in range(0, len(words_list)):
        sentence = ' '.join(words_list[num:num + n])
        calculateProb(sentence, counter)

def splitSequence(seq):
    return seq.split(" ")


def getPredictions(sequence):
    predicted = []
    nPred = nPredictions
    inputSequence = splitSequence(sequence)
    for sentence in probabilities.keys():
        if sequence in sentence:
            outputSequence = splitSequence(sentence)
            cont = False
            for i in range(0, len(inputSequence)):
                if outputSequence[i] != inputSequence[i]:
                    cont = True
                    break
            if cont:
                continue
            predicted.append((sentence, probabilities[sentence]))
    predicted.sort(key=lambda x: x[1], reverse=True)

    noPrediction = False
    if len(predicted) == 0:
        noPrediction = True
    else:
        if len(predicted) < nPredictions:
            nPred = len(predicted)
        for i in range(0, nPred):
            outputSequence = predicted[i][0].split(" ")
            options.append(outputSequence[len(inputSequence)])
    return options, noPrediction, nPred


def popup():
    messagebox.showinfo("Autofill Alert", "No predicted words")


def showChoice():
    userInput_var.set(str(choiceVar.get()))

# defining a function that will get the words and print them on the screen
def searchToken():
    userInput = userInput_var.get()
    generateNGrams(words, len(splitSequence(userInput)) + 1, count)
    output_options, noPredictions, nPred = getPredictions(userInput.lower())
    mb = Menubutton(root, text="Autofill ", relief=RAISED, font=('AR CENA', 14, 'bold'))
    mb.grid(row=3, column=1)
    mb.menu = Menu(mb, tearoff=0, font=12)
    mb["menu"] = mb.menu
    mb.menu.delete(0, nPred)
    if noPredictions:
        popup()
    else:
        for i in range(0, nPred):
            mb.menu.add_radiobutton(label=userInput + " " + str(output_options[i]),
                                    variable=choiceVar, command=showChoice)
    words_entry.delete(0, 'end')
    ngrams_list.clear()
    probabilities.clear()
    options.clear()

dataset = prepareData()
words = tokenizeText(dataset)

root = tk.Tk()
root.geometry("1000x600")
root.title("AutoFill Arabic ")

output_options = []
userInput_var = tk.StringVar()
choiceVar = tk.StringVar()


words_label = tk.Label(root, text=('search here: '), fg=('indigo'), font=('AR CENA', 14, 'bold'))
words_entry = tk.Entry(root, textvariable=userInput_var, font=('AR CENA', 20, 'normal'), width=30)
searchButton = tk.Button(root, text='Go ', command=searchToken, font=('AR CENA', 12, 'bold'))

# placing the label and entry in the required position using grid method
words_label.grid(row=0, column=0)
words_entry.grid(row=0, column=1)
searchButton.grid(row=2, column=1)
# performing an infinite loop for the window to display
root.mainloop()




















