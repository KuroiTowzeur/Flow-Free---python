from tkinter import *
from constante import *
from gestion_utilisateur import *
from niveaux import niveaux


class menu_principal:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg='black')
        self.img = logo

        self.frame = Frame(self.root, bg='black')
        self.frame.pack(side=BOTTOM, padx=10, pady=10, expand=True, fill=BOTH)

        self.center()
        self.place_widget()

    def center(self):
        self.ws = self.root.winfo_screenwidth()
        self.hs = self.root.winfo_screenheight()
        self.w = 360
        self.h = 300
        x = (self.ws / 2) - (self.w / 2)
        y = (self.hs / 2) - (self.h / 2)
        self.root.geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))

    def place_widget(self):
        self.frame_logo = Frame(self.root, bg='black')
        self.frame_logo.pack(side=TOP, padx=20, pady=20)

        title = Label(self.frame_logo, image=self.img, borderwidth=0)
        title.pack()

        l = Label(self.frame,
                  text="Nom d'utilisateur :",
                  font=('LibreFranklin-Regular', 16),
                  fg='white',
                  bg='black',
                  borderwidth=0,
                  anchor=W)
        l.pack(side=TOP, fill=BOTH, padx=10)

        self.value = StringVar()
        self.value.set(player_defaut)
        entree = Entry(self.frame,
                       textvariable=self.value,
                       font=('LibreFranklin-Regular', 18),
                       fg='black',
                       bg='grey',
                       width=14,
                       borderwidth=0)
        entree.pack(side=LEFT, padx=10)

        b = Button(self.frame,
                   command=self.enter,
                   text='OK',
                   font=('LibreFranklin', 12),
                   fg='black',
                   bg='grey',
                   borderwidth=4)
        b.pack(side=LEFT, padx=20)

    def exit(self):
        self.frame.destroy()
        self.frame_logo.destroy()

    def enter(self):
        self.exit()
        global user
        user = self.value.get()
        grille_bouton(regularpack[0][0], regularpack[0][1], regularpack[0][2], 0, root)


# ----------------------------------------------------------------------------------------------------------------------

class grille_bouton:
    def __init__(self, taille_grille, color, difficulté, page, root):

        self.taille_grille = taille_grille
        self.color = color
        self.difficulté = '{0}x{0} {1}'.format(taille_grille, difficulté)
        self.page = page
        self.root = root

        self.all_colors = list(dic_couleurs.keys())
        self.police = 'LibreFranklin-Regular'

        self.scores = load_score(user)
        self.nb_map_clear = cb_map_clear(self.scores)

        self.fond_valide = PhotoImage(file=fond_valide_path)
        self.fond_etoile = PhotoImage(file=fond_etoile_path)
        self.fond_noir = PhotoImage(file=fond_noir_path)

        self.zone_info()
        self.place_bouton()
        self.navigation()

        self.center()

    def center(self):
        self.ws = self.root.winfo_screenwidth()
        self.hs = self.root.winfo_screenheight()
        self.w = 420
        self.h = 620
        x = (self.ws / 2) - (self.w / 2)
        y = (self.hs / 2) - (self.h / 2)
        self.root.geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))

    def zone_info(self):
        self.frame_info = Frame(self.root, bg='black')
        self.frame_info.pack(side=TOP, fill=X, padx=25, pady=10)

        b = Button(self.frame_info,
                   image=icon_left_arrow,
                   command=self.retour_menu,
                   borderwidth=0,
                   highlightthickness=0,
                   activebackground='black')
        b.pack(side=LEFT)

        label_pack = Label(self.frame_info,
                           text='Regular Pack',
                           bg='black',
                           fg='yellow',
                           font=(self.police, 24))
        label_pack.pack(padx=10, side=LEFT)

        label_nb_map_clear = Label(self.frame_info,
                                   text='{} / 150'.format(self.nb_map_clear),
                                   bg='black',
                                   fg='grey',
                                   font=(self.police, 16))
        label_nb_map_clear.pack(side=LEFT)

        self.frame_diff = Frame(self.root, bg='black')
        self.frame_diff.pack(fill=X, padx=15)

        label = Label(self.frame_diff,
                      text=self.difficulté,
                      fg='#808080',
                      bg='black',
                      anchor=W,
                      font=(self.police, 16))
        label.pack(side=LEFT, padx=10)

    def place_bouton(self):

        self.canvas = Canvas(self.root, bg='black', width=400, height=400, highlightthickness=0)
        self.canvas.pack(pady=10)

        plateau = [n_niveau for n_niveau in range(1, 31)]

        def onclick(k):
            def click():
                self.load_niveau(k)

            return click

        for n_niveau in plateau:

            button = Button(self.canvas,
                            text=n_niveau,
                            command=onclick(n_niveau),
                            bg='black',
                            fg='white',
                            borderwidth=0,
                            activebackground=self.color,
                            font=(self.police, 12))

            # gestion fond en fonction du score (etoile, valide, rien)
            if presence(self.scores, self.taille_grille, n_niveau):
                state = self.scores[self.taille_grille][n_niveau][2]
                if state == 'perfect':
                    button.configure(image=self.fond_etoile, compound=CENTER)
                else:
                    button.configure(image=self.fond_valide, compound=CENTER)
            else:
                button.configure(image=self.fond_noir, compound=CENTER)

            r, c = (n_niveau - 1) // 5, (n_niveau - 1) % 5
            button.grid(row=r, column=c, padx=10, pady=10)

        for row in range(6):  # ajout du fond
            for column in range(5):
                offset_column = column * 74
                offset_row = row * 74

                x0, y0 = 7 + offset_column, 7 + offset_row
                x1, y1 = 66 + offset_column, 66 + offset_row
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=self.color)

    def navigation(self):
        self.frame_navigation = Frame(self.root, bg='black')
        self.frame_navigation.pack(padx=10, pady=10)

        plateau = [i for i in range(len(regularpack))]
        all_buttons = []

        def onclick(k):
            def click():
                for i, button in enumerate(all_buttons):
                    if i == k:
                        button.configure(image=round_selected)
                    else:
                        button.configure(image=round_not_selected)

                self.change_grille(k)

            return click

        for i, k in enumerate(plateau):
            button = Button(self.frame_navigation,
                            image=round_not_selected,
                            command=onclick(k),
                            borderwidth=0,
                            highlightthickness=0,
                            activebackground='black')
            if self.page == i:
                button.configure(image=round_selected)

            button.grid(row=0, column=i, padx=2)
            all_buttons.append(button)

    def exit(self):
        self.frame_info.destroy()
        self.frame_diff.destroy()

        self.canvas.destroy()

        self.frame_navigation.destroy()

    def retour_menu(self):
        self.exit()
        menu_principal(self.root)

    def change_grille(self, new_page):
        self.exit()
        grille_bouton(regularpack[new_page][0],
                      regularpack[new_page][1],
                      regularpack[new_page][2],
                      new_page,
                      self.root)

    def load_niveau(self, k):
        self.exit()
        Flowfree(self.taille_grille,
                 niveaux[self.taille_grille][int(k)],
                 int(k),
                 self.root)


# ----------------------------------------------------------------------------------------------------------------------
class notification:
    def __init__(self, id_msg, value=0):
        self.notif = Toplevel(root)
        self.notif.configure(bg='black')
        self.notif.attributes('-alpha', 0.8)
        self.notif.resizable(width=False, height=False)
        self.notif.title('')
        self.notif.focus_set()

        self.value = value

        types_msg = {0: ['Félicitations !',
                         'Vous avez atteint la fin des plateaux {0}x{0}.'.format(value),
                         'jouer {0}x{0}'.format(value + 1)],

                     1: ['Parfait !',
                         'Vous avez terminé le niveau en {} actions.'.format(value),
                         'continuer à jouer'],

                     2: ['Niveau terminé !',
                         'Vous avez terminé le niveau en {}  actions.'.format(value),
                         'continuer à jouer'],

                     3: ['Félicitations !',
                         'Vous avez atteint la fin du Pack Normal.',
                         'pack suivant'],

                     4: ['Vous y êtes presque...',
                         'Remplissez le plateau avec le tuyau pour terminer le niveau.',
                         'continuer à jouer']}

        self.type_msg = types_msg[id_msg]

        self.init_fenetre()
        self.center()
        self.notif.mainloop()

    def center(self):
        ws = self.notif.winfo_screenwidth()
        hs = self.notif.winfo_screenheight()

        w = 340
        h = 160

        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        self.notif.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def init_fenetre(self):
        self.frame = Frame(self.notif, bg='black')  # height=150, width=326)
        canvas = Canvas(self.frame, bg='white', highlightthickness=0)

        label = Label(self.frame,
                      text=self.type_msg[0],
                      font=('LibreFranklin-Regular', 16),
                      fg='white',
                      bg='black')
        label.pack(side=TOP)

        label = Label(self.frame,
                      text=self.type_msg[1],
                      font=('LibreFranklin-Regular', 12),
                      fg='white',
                      bg='black')
        label.pack(side=TOP, pady=10, padx=10)

        button = Button(canvas,
                        command=self.notif.destroy,
                        text=self.type_msg[2],
                        fg='white',
                        bg='black',
                        font=('LibreFranklin-Regular', 14),
                        borderwidth=0,
                        highlightthickness=0)
        button.pack(pady=4, padx=4, side=BOTTOM)

        canvas.pack(pady=10)
        self.frame.pack(fill=BOTH, expand=True, pady=10, padx=10)


# ----------------------------------------------------------------------------------------------------------------------

class Flowfree:
    def __init__(self, taille_grille, grille_niveau, numero_niveau, root):

        self.taille_grille = taille_grille
        self.grille_niveau = grille_niveau
        self.numero_niveau = numero_niveau
        self.nb_flux = len(self.grille_niveau)
        self.root = root

        self.consigne = False  # permet d'afficher 1 unique fois la consigne
        self.fin = False  # permet d'addicher qu'une seul fois le msg de win

        self.niveau_autour()
        self.state = None

        self.coef = 0.8
        self.b = 10  # bordure
        self.w_case = int(100 * self.coef)
        self.police = 'LibreFranklin-Regular'

        self.l_canvas = self.taille_grille * self.w_case + (2 * self.b)

        #
        self.init_score()

        self.zone_niveau()
        self.init_zone_info()
        self.dessine_quadrillage()
        self.zone_action()

        self.init_game()
        self.center()

    def center(self):
        self.ws = self.root.winfo_screenwidth()
        self.hs = self.root.winfo_screenheight()

        self.w = self.l_canvas
        self.h = (self.zone_info.winfo_reqheight()) + self.l_canvas + 114

        x = (self.ws - self.w) / 2
        y = ((self.hs - self.h) / 2) - 40
        self.root.geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))

    def zone_niveau(self):
        self.zone_niveau = Frame(self.root,
                                 borderwidth=0,
                                 bg='black',
                                 height=42,
                                 width=self.l_canvas - 2 * self.b)

        bouton_menu = Button(self.zone_niveau,
                             image=icon_left_arrow,
                             command=self.menu,
                             borderwidth=0,
                             highlightthickness=0,
                             activebackground='black')
        bouton_menu.place(anchor=W, relx=0, rely=0.5)

        label0 = Label(self.zone_niveau,
                       text='niveau {0}'.format(self.numero_niveau),
                       bg='black',
                       fg="#EEED00",
                       font=(self.police, int(26 * self.coef)))
        label0.place(anchor=W, x=42, rely=0.5)

        label1 = Label(self.zone_niveau,
                       text='{0}x{0}'.format(self.taille_grille),
                       bg='black',
                       fg="#A6A6A6",
                       font=(self.police, int(22 * self.coef)))
        label1.place(anchor=W, x=52 + label0.winfo_reqwidth(), rely=0.5)

        if self.state == 'perfect':
            txt2 = '★'
        elif self.state == 'completed':
            txt2 = '✔'
        else:
            txt2 = ''

        label2 = Label(self.zone_niveau,
                       text=txt2,
                       bg='black',
                       fg="white",
                       font=(self.police, int(22 * self.coef)))
        label2.place(anchor=E, relx=1, rely=0.5)

        self.zone_niveau.pack(pady=10)

    def init_zone_info(self):
        self.action = 0
        taille_police = str(int(18 * self.coef))

        self.zone_info = Frame(self.root,
                               borderwidth=0,
                               bg='black',
                               width=self.l_canvas - 2 * self.b)

        self.inf_flux0 = Label(self.zone_info,
                               text='flux : {}/{}'.format(0, self.nb_flux),
                               bg='black',
                               fg="white",
                               font=(self.police, taille_police))
        self.inf_flux0.place(anchor=W, relx=0, rely=0.5)

        self.inf_flux1 = Label(self.zone_info,
                               text='actions : {} record : {}'.format(0, self.record),
                               bg='black',
                               fg='white',
                               font=(self.police, taille_police))
        self.inf_flux1.place(anchor=CENTER, relx=0.5, rely=0.5)

        self.inf_flux2 = Label(self.zone_info,
                               text='tuyau : {}%'.format(0),
                               bg='black',
                               fg="white",
                               font=(self.police, taille_police))
        self.inf_flux2.place(anchor=E, relx=1, rely=0.5)

        self.zone_info.configure(height=self.inf_flux2.winfo_reqheight())

        self.zone_info.pack()

    def refresh_zone_info(self):
        self.cb_chemins_finis()

        self.inf_flux0.configure(text='flux : {}/{}'.format(self.nb_chemins_finis, self.nb_flux))

        c = 'orange' if self.action > self.nb_flux else 'white'
        self.inf_flux1.configure(text='actions : {} record : {}'.format(self.action, self.record), fg=c)

        self.inf_flux2.configure(text='tuyau : {}%'.format(self.nb_tuyau()))

    def dessine_quadrillage(self):  # '#151515'
        self.canvas = Canvas(self.root,
                             width=self.l_canvas,
                             height=self.l_canvas,
                             background='black',
                             borderwidth=0,
                             highlightthickness=0)

        self.canvas.bind('<Button-1>', self.change_current_couleur)
        self.canvas.bind('<B1-Motion>', self.get_case)

        for i in range(self.taille_grille + 1):
            x1, y1 = self.b + i * self.w_case, self.b
            x2, y2 = self.b + i * self.w_case, self.b + 1 + self.taille_grille * self.w_case

            self.canvas.create_line(x1, y1, x2, y2, fill='#a8a8a8')
            self.canvas.create_line(y1, x1, y2, x2, fill='#a8a8a8')

        self.canvas.pack()

    def zone_action(self):
        self.zone_action = Frame(self.root,
                                 borderwidth=0,
                                 bg='black')

        state0 = 'normal' if self.numero_niveau_précédent else 'disabled'

        b0 = Button(self.zone_action,
                    image=icon_left_arrow,
                    command=self.back,
                    borderwidth=0,
                    state=state0,
                    highlightthickness=0,
                    activebackground='black')
        b0.pack(side=LEFT)

        b1 = Button(self.zone_action,
                    image=icon_restart,
                    command=self.restart,
                    borderwidth=0,
                    highlightthickness=0,
                    activebackground='black')
        b1.pack(side=LEFT, padx=40)

        state2 = 'normal' if self.numero_niveau_suivant else 'disabled'

        b2 = Button(self.zone_action,
                    image=icon_right_arrow,
                    command=self.next,
                    borderwidth=0,
                    state=state2,
                    highlightthickness=0,
                    activebackground='black')
        b2.pack(side=LEFT)

        self.zone_action.pack(pady=5)

    def change_current_couleur(self, event):  # change la couleur quand on clique

        if self.validite_coords(event.x, event.y):

            self.convert_coords(event.x, event.y)
            row, column = self.current_case

            if self.grille[row][column] != '':  # si on est pas sur une case vide

                self.current_color = self.grille[row][column]  # on change la couleur courante

                if self.color_precedente != self.current_color:
                    self.action += 1

                if not (self.grille_jouable[row][column]):  # si on est sur un rond du niveau

                    self.reset_liens(self.current_color)  # on enlève les liens précédent
                    self.chemins[self.grille[row][column]] = [(row, column)]  # init du chemin

                    self.reset_glow(self.current_color)  # on reset le glowing

                    self.glowing(row, column, self.current_color)
                    self.dessine_case(row, column, self.current_color)

                else:  # on est sur un lien
                    self.efface_partie_lien(self.current_color, row, column)
                    self.efface_partie_glow(self.current_color, row, column)

                self.color_precedente = self.current_color

    def niveau_autour(self):
        if (self.numero_niveau - 1) > 0:
            self.numero_niveau_précédent, self.taille_grille_précédent = (self.numero_niveau - 1), self.taille_grille
        elif (self.taille_grille - 1) > 4:
            self.numero_niveau_précédent, self.taille_grille_précédent = 30, self.taille_grille - 1
        else:
            self.numero_niveau_précédent, self.taille_grille_précédent = False, False

        if (self.numero_niveau + 1) < 31:
            self.numero_niveau_suivant, self.taille_grille_suivant = self.numero_niveau + 1, self.taille_grille
        elif (self.taille_grille + 1) < 10:
            self.numero_niveau_suivant, self.taille_grille_suivant = 1, self.taille_grille + 1
        else:
            self.numero_niveau_suivant, self.taille_grille_suivant = False, False

    def get_case(self, event):
        if self.validite_coords(event.x, event.y):
            self.convert_coords(event.x, event.y)
            self.actualise()

    def case_coté(self, r, c):
        l = self.taille_grille - 1
        cases_cote = [(r, c - 1), (r, c + 1), (r - 1, c), (r + 1, c)]
        return [(r, c) for (r, c) in cases_cote if (0 <= r <= l) and (0 <= c <= l)]

    def validite_coords(self, x, y):
        not_in_grille = (x % self.w_case) != self.b and (y % self.w_case) != self.b
        dans_quadrillage = (self.b < x < self.l_canvas - self.b) and (self.b < y < self.l_canvas - self.b)
        return not_in_grille and dans_quadrillage

    def convert_coords(self, x, y):
        self.current_case = (y - self.b) // self.w_case, (x - self.b) // self.w_case

    def convert_row_to_coords(self, case):  # renvoie le centre (x,y) d'une case
        offset = self.b + self.w_case / 2  # pour obtenir le milieu
        return (case[1] * self.w_case) + offset, (case[0] * self.w_case) + offset

    def manage_notification(self):

        tous_chemins_fini = self.tous_les_chemins_finis()
        tout_rempli = self.rempli()

        if self.fin_jeu() and not (self.fin):  # si on a fini le jeu
            self.fin = True

            if self.action == self.nb_flux:  # parfait
                state = 'perfect'
                idx = 1

            else:  # completé
                state = 'completed'
                idx = 2

            save_score(user, self.taille_grille, self.numero_niveau, self.action, state)

            if self.numero_niveau_suivant != False:  # si il y a un niveau suivant
                self.next()
                if self.numero_niveau_suivant == 1:  # si on change de plateaux
                    notification(0, self.taille_grille)
                else:
                    notification(idx, self.action)

            else:  # il ny a pas de niveau suivant
                notification(3)

        elif tous_chemins_fini and not (tout_rempli) and not (self.consigne):  # si il manque des tuyaux
            self.consigne = True
            notification(4)

    def actualise(self):
        row, column = self.current_case
        color = self.current_color
        tous_chemins_fini = self.tous_les_chemins_finis()
        tout_rempli = self.rempli()

        self.refresh_zone_info()
        self.manage_notification()

        fin_chemin = self.chemin_fini(color)  # si le chemin de la couleur actuel est déjà fini
        if self.chemins[color]:  # si on a au moins un element du chemin
            adjacent = (row, column) in self.case_coté(*(self.chemins[color][-1]))  # si on est sur une case adjacente
        else:
            adjacent = False
        case_jouable = self.grille_jouable[row][column]  # si on est pas sur une case du niveau
        extremité = (row, column) in self.extremites[color]  # si on est sur une case du niveau de couleur

        if not (fin_chemin) and adjacent and (case_jouable or extremité):  # domaine de validité

            if self.grille[row][column] == '' or (extremité and (row, column) != self.chemins[color][0]):
                # si c'est une case vide ou si c'est l'extrémité manquante

                self.dessine_lien(self.chemins[self.current_color][-1], self.current_case)
                self.grille[row][column] = self.current_color

                if not ((row, column) in self.chemins[self.current_color]):
                    self.chemins[self.current_color].append((row, column))

            elif (row, column) in self.chemins[color]:  # 'queue de poisson'

                self.efface_partie_lien(color, row, column)
                self.efface_partie_glow(color, row, column)

            else:  # on passe par le chemin d'une autre couleur
                couleur_coupée = self.grille[row][column]
                chemin_coupé = self.chemins[couleur_coupée]

                index = chemin_coupé.index((row, column)) - 1
                r, c = chemin_coupé[index]

                self.efface_partie_lien(couleur_coupée, r, c)
                self.efface_partie_glow(couleur_coupée, r, c)

    def dessine_case(self, row, column, color):
        row_center, row_column = self.convert_row_to_coords((row, column))
        rayon = 35 * self.coef
        x0, y0 = row_center - rayon, row_column - rayon
        x1, y1 = row_center + rayon, row_column + rayon
        self.canvas.create_oval(x0, y0, x1, y1, fill=dic_couleurs[color], outline='')

    def dessine_lien(self, case0, case1):
        color = self.current_color
        color_hexa = dic_couleurs[color]

        self.glowing(case1[0], case1[1], self.current_color)
        if case1 in self.extremites[color]:  # on remet le rond si la case est une extremité
            self.dessine_case(case1[0], case1[1], color)

        x0, y0 = self.convert_row_to_coords(case0)
        x1, y1 = self.convert_row_to_coords(case1)

        item = self.canvas.create_line(x0, y0, x1, y1, fill=color_hexa, width=35 * self.coef, capstyle=ROUND)
        self.liens[color].append(item)

    def glowing(self, row, column, color):
        hexa_color = dic_couleurs_glow[color]
        k = self.coef

        center = self.convert_row_to_coords((row, column))

        offset = (self.w_case // 2) - 1

        x0, y0 = center[0] - offset, center[1] - offset
        x1, y1 = center[0] + offset, center[1] + offset

        item = self.canvas.create_rectangle(x0, y0, x1, y1, fill=hexa_color, outline=hexa_color)

        self.glow[color].append((row, column))
        self.grille_glow[row][column] = item

    def nb_tuyau(self):
        nb_tuyaux_totaux = self.taille_grille ** 2 - self.nb_flux
        nb_tuyaux_posé = sum([len(self.liens[color]) for color in self.colors])
        return int((nb_tuyaux_posé / nb_tuyaux_totaux) * 100)

    def chemin_fini(self, couleur):
        if self.chemins[couleur]:  # si la liste est pas vide
            longueur = len(self.chemins[couleur]) > 1
            extremité = self.chemins[couleur][-1] in self.extremites[couleur]
            return (longueur and extremité)
        return False

    def cb_chemins_finis(self):
        self.nb_chemins_finis = 0
        for color in self.colors:
            self.nb_chemins_finis += self.chemin_fini(color)

    def tous_les_chemins_finis(self):
        return not (False in [self.chemin_fini(color) for color in self.colors])

    def rempli(self):
        return not (True in ['' in row for row in self.grille])

    def fin_jeu(self):
        return self.tous_les_chemins_finis() and self.rempli()

    def reset_glow(self, color):  # suprimer le glow d'une couleur

        for row, column in self.glow[color]:
            item = self.grille_glow[row][column]

            if item:
                self.canvas.delete(item)
                self.grille_glow[row][column] = ''

        self.glow[color] = []

    def reset_liens(self, couleur):  # fonction qui efface les liens d'une couleur
        for item in self.liens[couleur]:  # suppression des liens dans le canvas
            self.canvas.delete(item)
        self.liens[couleur] = []

        for r, c in self.chemins[couleur]:  # on netoie la grille
            if not ((r, c) in self.extremites[couleur]):  # si on est pas dans une case de depart
                self.grille[r][c] = ''

    def efface_partie_lien(self, couleur, row, column):
        chemin = self.chemins[couleur]
        intersection = row, column
        indice_max = chemin.index(intersection)

        elt_enlever = chemin[indice_max + 1:]
        elt_garder = chemin[:indice_max + 1]

        lien = self.liens[couleur]
        lien_garder = self.liens[couleur][:indice_max]
        lien_enlever = self.liens[couleur][indice_max:]

        for item in lien_enlever:
            self.canvas.delete(item)

        self.liens[couleur] = lien_garder
        self.chemins[couleur] = elt_garder

        for r, c in elt_enlever:
            if not ((r, c) in self.extremites[couleur]):
                self.grille[r][c] = ''

    def efface_partie_glow(self, couleur, row, column):
        glowing = self.glow[couleur]
        intersection = row, column
        indice_max = glowing.index(intersection)

        elt_enlever = glowing[indice_max + 1:]
        elt_garder = glowing[:indice_max + 1]

        for row, column in elt_enlever:
            item = self.grille_glow[row][column]
            self.canvas.delete(item)
            self.grille_glow[row][column] = ''

        self.glow[couleur] = elt_garder

    def init_game(self):
        self.init_grille_jouable()
        self.init_grille()

        self.init_colors()
        self.init_extremites()
        self.init_liens()
        self.init_chemins()
        self.init_glow()
        self.init_grille_glow()

        self.current_color = self.colors[0]  # fixe au hasard pour eviter que ça plante
        self.color_precedente = ''

        self.dessine_niveau()

    def init_score(self):
        self.scores = load_score(user)

        if presence(self.scores, self.taille_grille, self.numero_niveau):
            self.record = self.scores[self.taille_grille][self.numero_niveau][1]
            self.state = self.scores[self.taille_grille][self.numero_niveau][2]
        else:
            self.record, self.state = '-', ''

    def init_grille_jouable(self):
        self.grille_jouable = [[True for i in range(self.taille_grille)] for i in range(self.taille_grille)]
        for color, coords in self.grille_niveau.items():
            for (row, column) in coords:
                self.grille_jouable[row][column] = False

    def init_grille(self):
        self.grille = [['' for i in range(self.taille_grille)] for i in range(self.taille_grille)]
        for color, coords in self.grille_niveau.items():
            for (row, column) in coords:
                self.grille[row][column] = color

    def init_colors(self):
        self.colors = [color for color in self.grille_niveau.keys()]

    def init_extremites(self):
        self.extremites = {}
        for color, coords in self.grille_niveau.items():
            self.extremites[color] = coords

    def init_liens(self):
        self.liens = {color: [] for color in self.colors}

    def init_chemins(self):
        self.chemins = {color: [] for color in self.colors}

    def init_glow(self):
        self.glow = {color: [] for color in self.colors}

    def init_grille_glow(self):
        self.grille_glow = [['' for i in range(self.taille_grille)] for i in range(self.taille_grille)]

    def dessine_niveau(self):  # dessine le niveau
        for color, coords in self.grille_niveau.items():
            for row, column in coords:
                self.dessine_case(row, column, color)

    def restart(self):
        self.exit()
        Flowfree(self.taille_grille, self.grille_niveau, self.numero_niveau, self.root)

    def exit(self):
        self.zone_niveau.destroy()
        self.zone_info.destroy()
        self.canvas.destroy()
        self.zone_action.destroy()

    def back(self):
        taille = self.taille_grille_précédent
        numero = self.numero_niveau_précédent
        grille_niveau = niveaux[taille][numero]
        root = self.root

        self.exit()

        Flowfree(taille, grille_niveau, numero, root)

    def next(self):

        numero = self.numero_niveau_suivant
        taille = self.taille_grille_suivant
        grille_niveau = niveaux[taille][numero]
        root = self.root

        self.exit()

        Flowfree(taille, grille_niveau, numero, root)

    def menu(self):
        self.exit()
        idx = [infos[0] for infos in regularpack].index(self.taille_grille)
        grille_bouton(self.taille_grille, regularpack[idx][1], regularpack[idx][2], idx, self.root)


# ----------------------------------------------------------------------------------------------------------------------

root = Tk()
root.resizable(width=False, height=False)
root.title("Flow Free")
root.configure(bg='black')

#
root.iconbitmap(icon_path)
icon_left_arrow = PhotoImage(file=icon_left_arrow_path)
icon_restart = PhotoImage(file=icon_icon_restart_path)
icon_right_arrow = PhotoImage(file=icon_right_arrow_path)

icon_left_arrow_false = PhotoImage(file=icon_left_arrow_false_path)
icon_right_arrow_false = PhotoImage(file=icon_right_arrow_false_path)

round_selected = PhotoImage(file=round_selected_path)
round_not_selected = PhotoImage(file=round_not_selected_path)

logo = PhotoImage(file=logo_path)
#

menu_principal(root)
root.mainloop()
