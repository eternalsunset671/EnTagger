from tkinter import *
from tkinter import filedialog
from tkinter.scrolledtext import *
import tkinter as tk
import tkinter.font as tkFont

import re

class App(tk.Tk):
    def __init__(self, **kwargs):
        tk.Tk.__init__(self, **kwargs)

        self.title('EnTagger')
        self.geometry('800x500')

        bg_color = '#f0f0f0' # Light gray
        text_bg_color = '#ffffff' # White
        button_bg_color = '#d9d9d9' # Darker gray
        button_fg_color = '#000000' # Black
        button_hover_bg_color = '#c0c0c0' # Lighter gray

        self.configure(bg=bg_color)

        self.grid_rowconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=1, weight=0)

        self.text_editor = ScrolledText(self, wrap=tk.WORD, bg=text_bg_color)
        self.text_editor.grid(column=0, row=0, sticky='nsew')

        self.text = ''
        self.file_name = ''

        #self.undo_stack = []
        #self.redo_stack = []

        self.control_frame = tk.Frame(self, relief=tk.RAISED, bd=2, bg=bg_color)
        self.control_frame.grid(column=1, row=0, sticky='ns')

        self.open_button = tk.Button(self.control_frame, text='Open file', command=self.open_file, bg=button_bg_color, fg=button_fg_color, activebackground=button_hover_bg_color)
        self.open_button.grid(column=0, row=0, sticky='ew', padx=(10, 0), pady=(10, 0))

        #self.undo_stack.append((self.text_editor.get('1.0', tk.END), self.redo_stack[:]))

        self.Questions_button = tk.Button(self.control_frame, text='Questions', command=self.Questions, bg=button_bg_color, fg=button_fg_color, activebackground=button_hover_bg_color)
        self.Questions_button.grid(column=0, row=1, sticky='ew', padx=(10, 0), pady=(10, 0))

        #self.TagQ_button = tk.Button(self.control_frame, text='TagQ', command=self.TagQ, bg=button_bg_color, fg=button_fg_color, activebackground=button_hover_bg_color)
        #self.TagQ_button.grid(column=0, row=2, sticky='ew', padx=(10, 0), pady=(10, 0))

        self.CurseWords_button = tk.Button(self.control_frame, text='Curse Words', command=self.CurseWords, bg=button_bg_color, fg=button_fg_color, activebackground=button_hover_bg_color)
        self.CurseWords_button.grid(column=0, row=3, sticky='ew', padx=(10, 0), pady=(10, 0))

        self.save_button = tk.Button(self.control_frame, text='Save file', command=self.save_file, bg=button_bg_color, fg=button_fg_color, activebackground=button_hover_bg_color)
        self.save_button.grid(column=0, row=4, sticky='ew', padx=(10, 0), pady=(10, 0))

        for button in (self.open_button, self.CurseWords_button, self.save_button, self.Questions_button):
            button.config(font=tkFont.Font(family='Helvetica', size=12))

        self.text_editor.tag_configure('TQ', background='yellow')
        self.text_editor.tag_configure('Ques', background='green')
        self.text_editor.tag_configure('CW', background='red')
        
        #self.text_editor.bind_all("<<Modified>>", self.on_text_changed)

        #self.bind_all("<Control-z>", self.undo)
        #self.bind_all("<Control-y>", self.redo)
        #keyboard.add_hotkey('ctrl+z', self.undo)
        #keyboard.add_hotkey('ctrl+y', self.redo)
        #self.bind_all("<Key>", self.on_text_changed)

        #self.previous_text = ''


    #def undo(self, event=None):
    #    if len(self.stack_of_events) != 0:
    #        self.redo_stack += [self.stack_of_events.pop()]
    #        self.text_editor.delete('1.0', END)
    #        print(*self.stack_of_events)
    #        self.text_editor.insert('1.0', self.stack_of_events[-1])
    #        self.update()
            

    #def redo(self, event=None):
    #    if len(self.redo_stack) != 0:
    #        self.text_editor.delete('1.0', END)
    #        self.text_editor.insert('1.0', self.redo_stack[-1])
    #        self.stack_of_events += [self.redo_stack.pop()]
    #        self.update()


    #def on_text_changed(self, event):
    #    #self.undo_stack.append(self.text_editor.get('1.0', tk.END))
    #    #self.redo_stack.clear()


    #def undo(self, event=None):
    #    if self.undo_stack:
    #        self.redo_stack.append(self.text_editor.get('1.0', tk.END))
    #        self.text_editor.delete('1.0', tk.END)
    #        tmp = self.undo_stack.pop()
    #        self.text_editor.insert('1.0', tmp)
    #    self.update()
    #    print('undo stack', *self.undo_stack, sep='\nж')


    #def redo(self, event=None):
    #    if self.redo_stack:
    #        self.undo_stack.append(self.text_editor.get('1.0', tk.END))
    #        self.text_editor.delete('1.0', tk.END)
    #        tmp = self.redo_stack.pop()
    #        self.text_editor.insert('1.0', tmp)
    #        self.text_editor.insert('1.0', tmp)
    #    self.update()
    #    print('redo stack', *self.redo_stack, sep='\n')


    #def on_text_changed(self, event):
    #    current_text = self.text_editor.get('1.0', tk.END)
    #    if current_text != self.previous_text:
    #        self.redo_stack = []
    #        self.text = self.text_editor.get('1.0', tk.END)
    #        self.previous_text = current_text
    

    def update(self):
        #self.highlight_tags('MR')
        self.highlight_tags('TQ')
        self.highlight_tags('CW')
        self.highlight_tags('Ques')
        

    def highlight_tags(self, tag):
        pattern = f'_{tag}_'
        index = '1.0'
        while True:
            index = self.text_editor.search(pattern, index, stopindex=END)
            if not index:
                break
            end_index = f'{index}+{len(pattern)}c'
            self.text_editor.tag_add(tag, index, end_index)
            index = end_index


    def open_file(self):
        filepath = filedialog.askopenfilename(defaultextension='txt')
        self.file_name = filepath.split('/')[-1].replace('.txt', '')
        if filepath != '':
            with open(filepath, 'r', encoding='utf-8') as file:
                self.text = file.read()
                self.text_editor.delete('1.0', END)
                self.text_editor.insert('1.0', self.text)
            #self.TagQ_button.config(state='normal')
            self.CurseWords_button.config(state='normal')
            self.Questions_button.config(state='normal')
            self.undo_stack = []
            self.redo_stack = []


    def save_file(self):
        filepath = filedialog.asksaveasfilename(
        filetypes=[('txt file', '.txt')],
        defaultextension='.txt',
        initialdir='F:\\data\\',
        initialfile=f'{self.file_name}_tagged',
        confirmoverwrite=False,
    )
        if filepath != '':
            self.text = self.text_editor.get('1.0', END)
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(self.text)
            self.text = ''


    def Questions(self):
        self.text = self.text_editor.get('1.0', tk.END)
        #self.TagQ(mode=False)
        #if self.text.find('_TQ__TQ_') != -1:
        #    self.text = self.text.replace('?', '?_Ques_')
        #    self.text = self.text.replace('_Ques__TQ_', '')
        #elif self.text.find('_TQ_') != -1:
        #    self.text = self.text.replace('?', '?_Ques_')
        #    self.text = self.text.replace('_Ques__TQ_', '')
        #else:
        self.text = re.sub(r'\?' , r'?_Ques_', self.text)
        if self.text.find('?_Ques_\'') != -1:
            self.text = self.text.replace('?_Ques_\'', '\'?_HandCheck_')
        #self.text = self.text.replace('?', '?_Ques_') #!!!!!!!!!!! pattern = r'?\s'
        self.text_editor.delete('1.0', END)
        self.text_editor.insert('1.0', self.text)
        self.Questions_button.config(state='disabled')
        self.update()
        

    def CurseWords(self):
        self.text = self.text_editor.get('1.0', tk.END)
        with open('curse words.txt') as f:
            words = f.read().split('\n')
        for x in words:
            if x not in [' ', '', '\t', '\n', '  ']:
                self.text = re.sub(r'\b' + re.escape(x) + r'\b', f'{x}_CW_', self.text)
                tmp = x[0].upper() + x[1:]
                self.text = re.sub(r'\b' + re.escape(tmp) + r'\b', f'{tmp}_CW_', self.text)
        self.text_editor.delete('1.0', END)
        self.text_editor.insert('1.0', self.text)
        self.CurseWords_button.config(state='disabled')
        self.update()


    def TagQ(self, mode=True):
        self.text = self.text_editor.get('1.0', tk.END)
        sentences = re.findall(r'(?s)([^\...\!\?\v\f]+[\...\!\?]+|[^\...\!\?\v\f]+$)', self.text)
        for sentence in sentences:
            if sentence.find('?') != -1:
                parts_of_sentence = re.split(r'([,-])', sentence)
                tmp = []
                for part in parts_of_sentence:
                    if part == '\n' or part == ',':
                        tmp[-1] += part
                    else:
                        tmp += [part]
                parts_of_sentence = tmp
                if len(parts_of_sentence) != 1: # * - сокр r - только в правой

                    #repr(sentence)     *      *                                                                                                         *     *       *
                    #grammar_right = [' is', ' are', ' does', ' do', ' has', ' did', ' have', ' had', ' can', ' could', ' should', ' must', ' would', ' will', ' wo', ' shall']


                    #' ' or '\n' or \t
                    print(parts_of_sentence)
                    grammar_dict = {
                        'a': ['are', 'am'],
                        'c': ['can', 'could'],
                        'd': ['does', 'do', 'did'],
                        'h': ['has', 'have', 'had'],
                        'i': ['is', 'innit'],
                        'm': ['must'],
                        's': ['should', 'shall', 'shan\'t'],
                        'w': ['will', 'would', 'won\'t']
                        }

                    extras = ['n\'t ', ' ', ' not ']

                    pronouns_dict = {
                        'h': ['he'],
                        'i': ['it', 'I'],
                        't': ['they'],
                        's': ['she'],
                        'w': ['we'],
                        'y': ['you']
                        }
                    
                    for i in range(-1, -3, -1):
                        part = parts_of_sentence[i]
                        gap = re.findall(r'\s', part)
                        print(gap)
                        if len(gap) == 2:
                            start = len(gap[0])
                            print(start)
                            for gram in grammar_dict[part[start]]:
                                print(gram)
                    #print(parts_of_sentence)

        #print(*sentences)
                    
                    
                #    right = ''
                #    left = ''
                #    neg_right = None
                #    for i in range(len(parts_of_sentence)-1, -1, -1):
                #        part = parts_of_sentence[i]

                #        if right == '':
                #            for gram in grammar_right:
                #                if part.find(gram) != -1:
                #                    for i in range(len(extras)):
                #                        extra = extras[i]
                #                        full = gram + extra
                #                        if part.find(full) != -1:
                #                            right = full
                #                            left = gram
                #                            print(right, left)
                #                            if i == 1:
                #                                neg_right = False
                #                            else:
                #                                neg_right = True
                #                            #if right == 'shall ':
                #                            #    left = 'Let\'s '
                #                            #elif right == 'will ':
                #                            #    pass
                #                            #elif right == 'aren\'t':
                #                            print(right)
                #                        else:
                #                            continue
                #        elif left != '':
                #            if neg_right:
                #                pass
                #            else:
                #                for ext in extras:
                #                    if ext != ' ':
                #                        tmp_left = left + extra
                #            #определяеься с окончательным видом того что нужно в правой части
                #        else:
                #            print('not found') #наверное можно пометить как обычный вопрос либо ручная проверка

                #    if left != '' and right != '':
                #        pass
                #    elif left == '' and right != '':
                #        pass
                #    else:
                #        print('error')

                #    print(parts_of_sentence)
                #else:
                #    print('hand check')

                    #учесть регуляркой что части предложения могут быть не только с пробелом и но и \n \t


                    #exceptions:
                    #will you - в правой - учитывать полностью в правой части и не проверять левую но может быть такое что справа will а слева won't
                    #am - в правой => I'm not or I am not
                    #shall - в правой => Let's - обязательно слева
                    #didn't в правой но в левой мб неправильные глаголы => вопрос не найдется (как вариант искать по местоимениям)
                    #don't в правой но в левой может не быть -s и тогда он их не определит (как вариант искать по местоимениям)


    #def MinResp(self):
    #    self.text = self.text_editor.get('1.0', tk.END)
    #    with open('minimal responses.txt') as f:
    #        words = f.read().split('\n')
    #    punc = ['.', '?', '!']
    #    for x in words:
    #        for y in punc:
    #            tmp = x + y
    #            tmp = tmp[0].upper() + tmp[1:]
    #            self.text = self.text.replace(tmp, f'{tmp} _MR_')
    #    self.text_editor.delete('1.0', END)
    #    self.text_editor.insert('1.0', self.text)
    #    self.MinResp_button.config(state='disabled')
    #    self.update()

    #def TagQ(self, mode=True):
    #    self.text = self.text_editor.get('1.0', tk.END)
    #    start = None
    #    end = None
    #    num = 14
    #    old_end = 0
    #    res = ''
    #    for i in range(len(self.text)):
    #        if self.text[i] == ',':
    #            start = i
    #        if self.text[i] == '?':
    #            end = i
    #        try:
    #            if end - start <= num and end - start > 0:
    #                #constructions = []
    #                #for x in constructions:
    #                #    if self.text[start:end].find(x) != -1: 
    #                #        pass
    #                #разделяем предложение на части и ищем батарейку
    #                res += self.text[old_end:end+1] + '_TQ_'
    #                old_end = end + 1
    #                start = None
    #                end = None
    #            else:
    #                start = None
    #                end = None
    #        except TypeError:
    #            pass
    #    if old_end < len(self.text) and old_end != 0:
    #        res += self.text[old_end:]
    #    elif old_end == 0:
    #        res += self.text[old_end:]
    #    self.text = res
    #    if mode:
    #        self.text_editor.delete('1.0', END)
    #        self.text_editor.insert('1.0', self.text)
    #        self.TagQ_button.config(state='disabled')
        
    #    self.update()


if __name__ == '__main__':
    app = App()
    app.mainloop()