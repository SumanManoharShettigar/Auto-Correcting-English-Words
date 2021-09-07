# -*- coding: utf-8 -*-
"""
Created on Sun May  9 13:27:42 2021

@author: suman
"""


from tkinter import * 
from spellchecker import SpellChecker
import tkinter as tk
import tkinter.font as tkFont
#reference for punctuations
punctuations = '''!()[]{}“”;:'"\,<>./?@#$%^&*_~'''
spell = SpellChecker()
  

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        #suggest
        self.suggest=tk.Frame()
        self.suggest.pack(side="right",fill="y")
      
        ## Main part of the GUI
       
        text_frame = tk.Frame(borderwidth=1, relief="sunken")
        self.text = tk.Text(wrap="word", background="white",
                            borderwidth=0, highlightthickness=0)
        self.vsb = tk.Scrollbar(orient="vertical", borderwidth=1,
                                command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(in_=text_frame,side="right", fill="y", expand=False)
        self.text.pack(in_=text_frame, side="left", fill="both", expand=True)
        text_frame.pack(side="left", fill="both", expand=True)
       
        # clone the text widget font and use it as a basis for some
        # tags

        self.text.tag_configure("misspelled", foreground="red", underline=True)

        # set up a binding to do simple spell check. This merely
        # checks the previous word when you type a space. 
        self.text.bind("<space>", self.Spellcheck)

        # initialize the spell checking dictionary. .
        self._words=open("./words_alpha.txt").read().split("\n")
        
        #Trying scroll
        
        Label(self.suggest, text='Suggestion :', fg='blue', bg='white').pack(side="top")  
         
       
    def Spellcheck(self, event):
        '''Spellcheck the word preceeding the insertion point'''
        # check the previous word ,\s is whitespace, r is raw string, in reverse
        index = self.text.search(r'\s', "insert", backwards=True, regexp=True)
        
        if index == "":
            index ="1.0"
            
        else:
            index = self.text.index("%s+1c" % index)
            print(index)
        #get text from index to insert
        word = self.text.get(index, "insert")
        
        #Removing punctuation marks
        no_punct = ""
        for char in word:
            if char not in punctuations:
                no_punct = no_punct + char
        #word with no punctuation
        word = no_punct
        
        
        if word.lower() in self._words:
            #remove hello  tag to word from position "index" to "index + len(word)"
            self.text.tag_remove("misspelled", index, "%s+%dc" % (index, len(word)))
            
            
        else:
            #add tag to word from position "index" to "index + len(word)"
            self.text.tag_add("misspelled", index, "%s+%dc" % (index, len(word)))
            print(spell.candidates(word))
            if word not in " ":
               
                label=Label(self.suggest, text=spell.candidates(word), fg='blue', bg='white')
                label.pack(side="top")
            def remove_text():
                label.destroy()
                button.destroy()
            if word not in " ":    
                button=Button(self.suggest, text="Delete", command=remove_text)
                button.pack(side="top")
          



if __name__ == "__main__":
    app=App()
  
    app.mainloop()