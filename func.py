import tkinter as tk


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Выбор действия')
        self.bg = self.configure(bg='#292B3D')
        self.resizable(width=False, height=False)
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.width = 600
        self.height = 500
        self.protocol("WM_DELETE_WINDOW", lambda: (self.destroy(), self.quit()))
        self.geometry(f'{self.width}x{self.height}+{self.screen_width//2 - self.width//2}+{self.screen_height//2-self.height//2}')

        self.label = tk.Label(self, text="Выберите действие", font=('Consolas', 20), foreground='white', background='#292B3D')
        self.label.place(x = 180, y = 25)

        self.func_options = (
            ("Разность", ('aₙ₊₁', 'aₙ'), self.redirect_to_difference),
            ("Формула n-члена", ('a₁', 'n', 'd'), self.redirect_to_n_term),
            ("Сумма n-членов", ('a₁', 'n', 'аₙ'), self.redirect_to_summa),
            ("Свойство", ('aₙ₊₁', 'aₙ₋₁'), self.redirect_to_property),
            )
            
        self.places = ((30, 135), (30, 275), (300, 275), (300, 135))
        self.btns = []
        for btn in range(len(self.func_options)):
            self.btns.append(
                tk.Button(self, width=20, height=2, background='#352989', text=self.func_options[btn][0],
                    border=0, activebackground='#2A2263', activeforeground='white',
                    foreground='white', font=('Consolas', 16), command=self.func_options[btn][2])
            )
            self.btns[btn].place(x=self.places[btn][0], y=self.places[btn][1])

    def redirect_to_difference(self):
        app = ComputeWindow(opt=self.func_options[0][:2])
        return self.withdraw()

    def redirect_to_n_term(self):
        app = ComputeWindow(opt=self.func_options[1][:2])
        return self.withdraw()
    
    def redirect_to_summa(self):
        app = ComputeWindow(opt=self.func_options[2][:2])
        return self.withdraw()
    
    def redirect_to_property(self):
        app = ComputeWindow(opt=self.func_options[3][:2])
        return self.withdraw()


class ComputeWindow(tk.Toplevel):
    def __init__(self, opt = None):
        super().__init__()
        self.title(opt[0])
        self.bg = self.configure(bg='#292B3D')
        self.resizable(width=False, height=False)
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.width = 600
        self.height = 500
        self.protocol("WM_DELETE_WINDOW", lambda: (self.destroy(), self.quit()))
        self.geometry(f'{self.width}x{self.height}+{self.screen_width//2 - self.width//2}+{self.screen_height//2-self.height//2}')

        self.func = {
            'Разность': self.difference,
            'Формула n-члена': self.n_term,
            'Сумма n-членов': self.summ,
            'Свойство': self.property,
        }
        
        self.label = tk.Label(self, text=opt[0], font=('Consolas', 20), foreground='white', background='#292B3D')
        self.label.place(x = 180, y = 25)

        self.is_valid = (self.register(self.validate), "%P")

        self.places = [100, 175, 250]
        self.entries = []
        self.entry_labels = []
        for entry in range(len(opt[1])):
            self.entries.append(
                tk.Entry(self, foreground='white', border=0, font=('Consolas', 16), width=25,
                    background='#19182A', insertbackground='white', validate='key', validatecommand=self.is_valid)
            )
            self.entry_labels.append(
                tk.Label(self, text=opt[1][entry], font=('Consolas', 20), foreground='white', background='#292B3D')
            )
            self.entry_labels[entry].place(x = 50, y = self.places[entry])
            self.entries[entry].place(x = 150, y = self.places[entry])

        self.calculate_btn = tk.Button(self, width=15, background='#352989', text='Вычислить',
                    border=0, activebackground='#2A2263', activeforeground='white',
                    foreground='white', font=('Consolas', 16), command=self.func[opt[0]])
        self.answer = tk.Label(self, text='Ответ: ', font=('Consolas', 20), foreground='white', background='#292B3D')
        self.back_btn = tk.Button(self, background='#292B3D', text='Назад', border=0,
                                activebackground='#292B3D', activeforeground='white', foreground='white',
                                font=('Consolas', 14), command=self.return_to_main)
        self.calculate_btn.place(x=300, y = 350)
        self.answer.place(x=30, y = 350)
        self.back_btn.place(x = 30, y = 450)

    
    def return_to_main(self):
        app = MainWindow()
        return self.destroy()
    

    def validate(self, value):
        if len(value)>0:
            is_comma = (value[-1] == '.') and ('.' not in value[:-1])
            is_minus = (value[-1] == '-') and (len(value) == 1)
            if value[-1].isnumeric() or is_comma or is_minus:
                if len(value) < 17:
                    return True
                else:
                    return False
            else:
                return False
        else: 
            return True
        
    def difference(self):
        a1 = float(self.entries[0].get())
        a2 = float(self.entries[1].get())
        d = a1 - a2
        self.answer.configure(text=f'Ответ: {d}')
        return d
    
    def n_term(self):
        a1 = float(self.entries[0].get())
        n = float(self.entries[1].get())
        d = float(self.entries[2].get())
        a = a1 + (n-1)*d
        self.answer.configure(text=f'Ответ: {a}')
        return a
    
    def summ(self):
        a1 = float(self.entries[0].get())
        n = float(self.entries[1].get())
        a_n = float(self.entries[2].get())
        S = (a1 + a_n)*n/2
        self.answer.configure(text=f'Ответ: {S}')
        return S
    
    def property(self):
        a1 = float(self.entries[0].get())
        a2 = float(self.entries[1].get())
        a_n = (a1 + a2)/2
        self.answer.configure(text=f'Ответ: {a_n}')
        return a_n
    
app = MainWindow()
app.mainloop()