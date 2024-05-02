from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
import tkinter as tk
import tkinter.font as tkFont

import re

#форматировать под один стиль пунктуацию и непечатные символы а также пересмотреть регулярку и проверить как она отрабавтывает на реальном корпусе
#ключи в словарях содержат пробелы но не учитывают других символов

class EnTagger(tk.Tk):
    def __init__(self, **kwargs):
        tk.Tk.__init__(self, **kwargs)
        
        self.title('EnTagger')
        self.geometry('900x500')

        bg_color = '#f0f0f0'  # Light gray
        text_bg_color = '#ffffff'  # White
        button_bg_color = '#d9d9d9'  # Darker gray
        button_fg_color = '#000000'  # Black
        button_hover_bg_color = '#c0c0c0'  # Lighter gray

        frame = tk.Frame(self, bg=bg_color)
        frame.grid(row=0, column=0, sticky='nsew')
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        text_frame = tk.Frame(frame, bg=bg_color)
        text_frame.grid(row=0, column=0, sticky='nsew')
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

        self.text_editor = scrolledtext.ScrolledText(
            text_frame,
            width=69,
            height=22,
            font=('Helvetica', 14),
            selectbackground='light blue',
            selectforeground='black',
            undo=True,
            wrap='none',
            bg=text_bg_color
        )
        self.text_editor.grid(row=0, column=0, sticky='nsew')

        menu = tk.Menu(self, bg=bg_color, fg=button_fg_color)
        self.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=False, bg=bg_color, fg=button_fg_color)
        menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='New', command=self.new_file)
        file_menu.add_command(label='Open', command=self.open_file)
        file_menu.add_command(label='Save', command=self.save_file)
        file_menu.add_command(label='Save As', command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.quit)

        edit_menu = tk.Menu(menu, tearoff=False, bg=bg_color, fg=button_fg_color)
        menu.add_cascade(label='Edit', menu=edit_menu)
        edit_menu.add_command(label='Cut', command=lambda: self.cut(False), accelerator='(Ctrl+X)')
        edit_menu.add_command(label='Copy', command=lambda: self.copy(False), accelerator='(Ctrl+C)')
        edit_menu.add_command(label='Paste', command=lambda: self.paste(False), accelerator='(Ctrl+V)')
        edit_menu.add_separator()
        edit_menu.add_command(label='Undo', command=self.undo, accelerator='(Ctrl+Z)')
        edit_menu.add_command(label='Redo', command=self.redo, accelerator='(Ctrl+Y)')

        self.text = ''

        self.open_status_name = False
        self.selected = False

        self.bind('<Control-Key-x>', self.cut)
        self.bind('<Control-Key-c>', self.copy)
        self.bind('<Control-Key-v>', self.paste)

        self.configure(bg=bg_color)

        self.control_frame = tk.Frame(self, relief=tk.RAISED, bd=2, bg=bg_color)
        self.control_frame.grid(row=0, column=1, sticky='ns')

        self.Questions_button = tk.Button(self.control_frame, text='Questions', command=self.Questions, bg=button_bg_color, fg=button_fg_color, activebackground=button_hover_bg_color)
        self.Questions_button.grid(row=0, column=0, sticky='ew', padx=(10, 0), pady=(10, 0))

        self.TagQ_button = tk.Button(self.control_frame, text='TagQ', command=self.TagQ, bg=button_bg_color, fg=button_fg_color, activebackground=button_hover_bg_color)
        self.TagQ_button.grid(row=1, column=0, sticky='ew', padx=(10, 0), pady=(10, 0))

        self.CurseWords_button = tk.Button(self.control_frame, text='Curse Words', command=self.CurseWords, bg=button_bg_color, fg=button_fg_color, activebackground=button_hover_bg_color)
        self.CurseWords_button.grid(row=2, column=0, sticky='ew', padx=(10, 0), pady=(10, 0))

        for button in (self.TagQ_button, self.CurseWords_button, self.Questions_button):
            button.config(font=tkFont.Font(family='Helvetica', size=12))
            button.grid_columnconfigure(0, weight=1)

        self.text_editor.tag_configure('TQ', background='yellow')
        self.text_editor.tag_configure('Ques', background='green')
        self.text_editor.tag_configure('HandCheck', background='red')
        self.text_editor.tag_configure('CW', background='blue')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)


    def update(self, mode=True):
        if mode:
            self.text_editor.delete('1.0', END)
            self.text_editor.insert('1.0', self.text)
        self.highlight_tags('TQ')
        self.highlight_tags('CW')
        self.highlight_tags('Ques')
        self.highlight_tags('HandCheck')


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


    def undo(self):
        self.text_editor.edit_undo()
        self.update(False)

    def redo(self):
        self.text_editor.edit_redo()
        self.update(False)

    def cut(self, e):
        if e:
            self.selected = self.clipboard_get()
        else:
            if self.text_editor.selection_get():
                self.selected = self.text_editor.selection_get()
                self.text_editor.delete('sel.first', 'sel.last')
                self.clipboard_clear()
                self.clipboard_append(self.selected)


    def copy(self, e):
        if e:
            self.selected = self.clipboard_get()

        if self.text_editor.selection_get():
            self.selected = self.text_editor.selection_get()
            self.clipboard_clear()
            self.clipboard_append(self.selected)


    def paste(self, e):
        if e:
            self.selected = self.clipboard_get()
        else:
            if self.selected:
                position = self.text_editor.index(INSERT)
                self.text_editor.insert(position, self.selected)


    def new_file(self):
        self.text = ''
        self.text_editor.delete('1.0', END)
        self.title(f'EnTagger ### New file')
        self.open_status_name = False


    def open_file(self):
        filepath = filedialog.askopenfilename(defaultextension='txt')
        if filepath:
            with open(filepath, 'r', encoding='utf-8') as file:
                self.text = file.read()
                self.file_name = filepath.split('/')[-1].replace('.txt', '')
                self.open_status_name = filepath
            self.title(f'EnTagger ### {self.file_name}') #  ⃰
            self.update()
            

    def save_file(self):
        if self.open_status_name:
            with open(self.open_status_name, 'w') as f:
                f.write(self.text)
            self.title(f'EnTagger ### {self.file_name}')
        else:
            self.save_as_file()


    def save_as_file(self):
        filepath = filedialog.asksaveasfilename(
            filetypes=[('txt file', '.txt')],
            defaultextension='.txt',
            initialdir='F:\\data\\',
            initialfile=f'{self.file_name}_tagged',
            confirmoverwrite=False,
        )
        if filepath:
            self.text = self.text_editor.get('1.0', END)
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(self.text)
            self.title(f'EnTagger ### {self.file_name}')


    def Questions(self):
        self.text = self.text_editor.get('1.0', tk.END)
        if self.text.find('_Ques_') == -1:
            if self.text.find('_TQ_') != -1:
                self.text = re.sub(r'(\?)(?!_TQ_)', '?_Ques_', self.text)
            else:
                self.TagQ(mode=False)
                self.text = re.sub(r'(\?)(?!_TQ_)', '?_Ques_', self.text)
                self.text = self.text.replace('_TQ_', '')

            if self.text.find('?_Ques_\'') != -1:
                self.text = self.text.replace('?_Ques_\'', '\'?_HandCheck_')
            self.update()
        else:
            self.text = self.text.replace('_Ques_', '')
            self.update()


    def CurseWords(self):
        self.text = self.text_editor.get('1.0', tk.END)
        if self.text.find('_CW_') == -1:
            with open('curse words.txt') as f:
                words = f.read().split('\n')
            for x in words:
                if x not in [' ', '', '\t', '\n', '  ']:
                    self.text = re.sub(r'\b' + re.escape(x) + r'\b', f'{x}_CW_', self.text)
                    tmp = x[0].upper() + x[1:]
                    self.text = re.sub(r'\b' + re.escape(tmp) + r'\b', f'{tmp}_CW_', self.text)
            self.update()
        else:
            self.text = self.text.replace('_CW_', '')
            self.update()


    def TagQ(self, mode=True):
        self.text_editor.edit_separator()
        self.text = self.text_editor.get('1.0', tk.END)

        if self.text.find('_TQ_') == -1:
            sentences = re.findall(r'(?s)([^\...\!\?\v\f]+[\...\!\?]+|[^\...\!\?\v\f]+$)', self.text)
            for sentence in sentences:
                if sentence.find('?') != -1:
                    parts_of_sentence = re.split(r'([,-])', sentence) #!!!!!
                    print(parts_of_sentence)
                    tmp = []
                    for part in parts_of_sentence:
                        if part == '\n' or part == ',':
                            tmp[-1] += part
                        else:
                            tmp += [part]
                    parts_of_sentence = tmp
                    if len(parts_of_sentence) != 1: 

                        grammar_dict = {
                            'a': ['are', 'am'],
                            'c': ['can', 'could'],
                            'd': ['does', 'do', 'did'],
                            'h': ['has', 'have', 'had'],
                            'i': ['is', 'innit'],
                            'm': ['must', 'may'],
                            's': ['should', 'shall', 'shan\'t'],
                            'w': ['was', 'were', 'will', 'would', 'won\'t']
                            }

                        extras_dict = {
                            ' ': [r'\s'], #!!!!
                            'n': [r'n\'t\s'] 
                            }

                        not_dict = {
                            ' ': [r'\snot\s'] #!!!!
                            }

                        pronouns_dict = {
                            'h': ['he'],
                            'i': ['I', 'it'],
                            't': ['they'],
                            's': ['she'],
                            'w': ['we'],
                            'y': ['you']
                            }

                        def check_tail(part, pattern, grammars):
                            try:
                                end = re.search(pattern, part).end()
                                for i in range(len(grammars)):
                                    grammar = grammars[i]
                                    for part_grammar in grammar[part[end].lower()]:
                                        extra = r'[\?\,]' if i == 2 else  ''
                                        if re.search(pattern + part_grammar + extra, part):
                                            pattern += part_grammar + extra
                                            end = re.search(pattern, part).end()
                                            if i == 2:
                                                return True
                            except KeyError:
                                return False    

                        for i in range(-1, -3, -1):
                            part = parts_of_sentence[i]
                            gap = re.findall(r'\s', part)
                            start = len(gap[0])
                            pattern = gap[0]
                            if len(gap) == 2:
                                if check_tail(part, pattern, [grammar_dict, extras_dict, pronouns_dict]):
                                    self.text = self.text.replace(sentence, sentence + '_TQ_')
                                    break
                                else:
                                    try:
                                        for pronoun in pronouns_dict[part[start]]:
                                            if re.search(r'\s' + pronoun + r'\s', part) and re.search(r'[\?\,]', part):
                                                self.text = self.text.replace(sentence, sentence + '_TQ_')
                                                break
                                        break
                                    except KeyError:
                                        pass

                            elif len(gap) == 3:
                                if check_tail(part, pattern, [grammar_dict, not_dict, pronouns_dict]):
                                    self.text = self.text.replace(sentence, sentence + '_TQ_')
                                    break
                                else:
                                    pass

                            elif len(gap) == 1:
                                if re.search(r'\sOK?', part):
                                    self.text = self.text.replace(sentence, sentence + '_TQ_')
                                    break
                                elif not re.search(r'[A-Z]', part) and re.search(r'[\?\,]', part):
                                    self.text = self.text.replace(sentence, sentence + '_TQ_')
                                    break
            self.text = re.sub(r'(_TQ_)+', '_TQ_', self.text)
            if mode:
                self.update()
        else:
            self.text = self.text.replace('_TQ_', '')
            self.update()

if __name__ == '__main__':
    app = EnTagger()
    app.mainloop()