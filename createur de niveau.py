from tkinter import *
from constante import *


class Createur_niveau:
    def __init__(self):
        self.root = Tk()
        self.root.resizable(width=False, height=False)
        self.root.title("EDITEUR DE NIVEAU")
        self.root.configure(bg='black')
        self.coef = 0.4
        self.b = 10

        self.frame0 = Frame(self.root)
        self.frame0.pack(side=LEFT, pady=10, padx=10)

        self.frame1 = Frame(self.root)
        self.frame1.pack(side=RIGHT, pady=10, padx=10)

        self.color = ''  # current color print
        self.label = Label(self.frame0, text='current color : {}'.format(self.color), font=(20))
        self.label.pack(pady=10, padx=10)

        msg = Label(self.frame0, text='Numero du niveau :', font=(20))
        msg.pack()
        self.string1 = StringVar()
        self.string1.set("Niveau : ?")
        entree = Entry(self.frame0, textvariable=self.string1, width=30, font=20)
        entree.pack()

        msg2 = Label(self.frame0, text='Taille de la grille :', font=(20))
        msg2.pack()
        self.string2 = StringVar()
        self.string2.set("Grille : ?")
        entree2 = Entry(self.frame0, textvariable=self.string2, width=30, font=20)
        entree2.pack()

        confirmer = Button(self.frame0, text='Valider', font=20, command=self.prepare, bg='green')
        confirmer.pack(pady=10, padx=10)

        self.end = Button(self.frame0, text='SAVE', font=20, command=self.save, bg='black', fg='white')
        self.end.pack(side=RIGHT, pady=10, padx=10)

        self.next = Button(self.frame0, text='SUIVANT', font=20, command=self.next, bg='grey')
        self.next.pack(side=LEFT, pady=10, padx=10)

        self.palette_couleur()
        self.root.mainloop()

    def prepare(self):
        self.init_extremites()

        self.taille = int(self.string2.get())
        self.numero_niveau = int(self.string1.get())

        self.w_case = int(100 * self.coef)
        self.w = self.h = self.taille * self.w_case + 2 * self.b

        self.frame1.destroy()
        self.dessine_quadrillage()

    def next(self):
        self.save()
        self.init_extremites()

        self.taille = int(self.string2.get())
        self.numero_niveau = int(self.string1.get()) + 1
        self.string1.set(self.numero_niveau)

        self.w_case = int(100 * self.coef)
        self.w = self.h = self.taille * self.w_case + 2 * self.b

        self.frame1.destroy()
        self.dessine_quadrillage()

    def save(self):
        nb_flux = 0
        txt = ''

        for color in self.all_colors:
            if self.extremites[color] != []:
                nb_flux += 1
                txt += color + ':' + str(self.extremites[color]) + '\n'

        entete = str(self.numero_niveau) + '-' + str(self.taille) + '-' + str(nb_flux)

        path = 'niveaux.txt'
        with open(path, 'a') as file:
            file.write(entete + '\n' + txt +'\n')

        print('\n'+entete + '\n' + txt)
        print('Niveau sauvegarder !')

    def dessine_un_rond(self, event):
        x, y = event.x, event.y
        if self.validite_coords(x, y):
            row, column = self.convert_coords(x, y)
            color = self.color

            self.dessine_case(row, column, color)  # on dessine la couleur

            self.extremites[color].append((row, column))

    def convert_coords(self, x, y):
        return ((y - self.b) // self.w_case, (x - self.b) // self.w_case)

    def init_extremites(self):
        self.extremites = {color: [] for color in self.all_colors}

    def validite_coords(self, x, y):
        not_in_grille = (x % self.w_case) != self.b and (y % self.w_case) != self.b
        dans_quadrillage = (self.b < x < self.w - self.b) and (self.b < y < self.h - self.b)
        return not_in_grille and dans_quadrillage

    def convert_row_to_coords(self, case):  # renvoie le centre (x,y) d'une case
        offset = self.b + self.w_case / 2  # pour obtenir le milieu
        return (case[1] * self.w_case) + offset, (case[0] * self.w_case) + offset

    def dessine_case(self, row, column, color):
        row_center, row_column = self.convert_row_to_coords((row, column))
        rayon = 35 * self.coef
        x0, y0 = row_center - rayon, row_column - rayon
        x1, y1 = row_center + rayon, row_column + rayon
        self.canvas.create_oval(x0, y0, x1, y1, fill=dic_couleurs[color], outline='')

    def dessine_quadrillage(self):
        self.frame1 = Frame(self.root)
        self.frame1.pack(side=RIGHT, pady=10, padx=10)

        self.canvas = Canvas(self.frame1, width=self.w, height=self.h, background='black')
        self.canvas.bind('<Button-1>', self.dessine_un_rond)
        self.canvas.pack()

        for i in range(self.taille + 1):
            x1, y1 = 10 + i * self.w_case, 10
            x2, y2 = 10 + i * self.w_case, 11 + self.taille * self.w_case
            self.canvas.create_line(x1, y1, x2, y2, fill='#a8a8a8')
            self.canvas.create_line(y1, x1, y2, x2, fill='#a8a8a8')

    def set_color(self, color):
        self.color = color
        self.label.configure(text='current color : {}'.format(self.color), bg=dic_couleurs[self.color])

    def palette_couleur(self):
        frame = Frame(self.root)
        frame.pack(side=BOTTOM)

        self.all_colors = list(dic_couleurs.keys())

        b0 = Button(frame, text='rose', bg=dic_couleurs['ro'], padx=10, font=15, command=lambda: self.set_color('ro'))
        b0.grid(row=0, column=0)

        b1 = Button(frame, text='vert', bg=dic_couleurs['ve'], padx=10, font=15, command=lambda: self.set_color('ve'))
        b1.grid(row=0, column=1)

        b2 = Button(frame, text='bordeau', bg=dic_couleurs['bo'], padx=10, font=15,
                    command=lambda: self.set_color('bo'))
        b2.grid(row=0, column=2)

        b3 = Button(frame, text='violet', bg=dic_couleurs['vi'], padx=10, font=15, command=lambda: self.set_color('vi'))
        b3.grid(row=0, column=3)

        b4 = Button(frame, text='jaune', bg=dic_couleurs['ja'], padx=10, font=15, command=lambda: self.set_color('ja'))
        b4.grid(row=0, column=4)

        b5 = Button(frame, text='orange', bg=dic_couleurs['or'], padx=10, font=15, command=lambda: self.set_color('or'))
        b5.grid(row=0, column=5)

        b6 = Button(frame, text='rouge', bg=dic_couleurs['re'], padx=10, font=15, command=lambda: self.set_color('re'))
        b6.grid(row=0, column=6)

        b7 = Button(frame, text='cyan', bg=dic_couleurs['cy'], padx=10, font=15, command=lambda: self.set_color('cy'))
        b7.grid(row=0, column=7)

        b8 = Button(frame, text='bleu', bg=dic_couleurs['bl'], padx=10, font=15, command=lambda: self.set_color('bl'))
        b8.grid(row=0, column=8)

        b8 = Button(frame, text='blanc', bg=dic_couleurs['wh'], padx=10, font=15, command=lambda: self.set_color('wh'))
        b8.grid(row=0, column=9)


Createur_niveau()
