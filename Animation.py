from Sort import *
from Help import *
import pygame
import random

pygame.mixer.init()


class Animation:

    def __init__(self):
        # Variables utilisées
        self.song = ['a', 'b', 'c', 'd']  # ensemble des notes de musique
        self.mute = True  # variable qui controle le son actif ou pas
        for i in range(len(self.song)):  # on créer un module de son pour chaque note
            self.song[i] = pygame.mixer.Sound(
                "assets/note/%s.wav" % self.song[i])
            self.song[i].set_volume(1)
        self.ind_verif = 0  # un indice de vérification utile seulement pour certains tris
        self.memory = []
        self.ind_memory = 0
        self.unit = 0  #  variable permettant de récupérer le string indiquer de quel chiffre on parle pour le radix
        self.moving = 0
        self.tempo = []
        self.List_rectangles_memory = []
        self.help = None  # help sera notre fenêtre d'aide
        self.nbr_comp = 0  # le nbr de comparaisons
        self.ind_mini = None  # indice du rectangle le plus petit dans le selection
        self.ind_current = 0  # indice courant dans la Liste_complete
        self.ending = False  # variable qui indique si le tri est fini sur le Diagramme affiché
        self.List_rectangles = []  # Liste des identifiants de tout les rectangles
        self.stop = False  # variable qui permet de mettre en pause l'animation de tri
        self.S = Sort()  # creation d'un diagramme vide qui sera rempli après l'appui sur le bouton creation diagramme
        # nbr de comparaisons ( ici les echanges aussi sont comptés comme des comparaisons )
        self.counter_comparison = 0
        # fenetre
        self.Window = Tk()
        self.Window.resizable(width=False, height=False)
        self.Window.title("Sorting Algorithms")
        self.height = 800
        self.weight = 1300
        self.background = "PaleTurquoise3"  # couleur du fond de canvas
        self.color_current = "SpringGreen4"  # couleur du rectangle courant
        self.color_comp = "red"  # couleur du rectangle comparé
        self.color_moved = "gold"  # couleur du rectangle lors de son insertion
        self.color_ok = "dark khaki"  #  couleur du rectangle lorsqu'il est trié
        self.color_pivot = "brown4"  #  couleur du pivot
        self.nbr = IntVar()  # variable de controle du champ de saisie
        # canevas
        self.canevas = Canvas(self.Window, height=self.height,
                              width=self.weight, bg=self.background)  # Canvas principal
        # Canvas des images on et off
        self.ONOFF = Canvas(self.Window, height=65, width=150, bg="white")
        self.img_off = PhotoImage(file='assets/button/off.gif')
        self.img_on = PhotoImage(file='assets/button/on.gif')
        self.ONOFF.create_image(32, 35, image=self.img_off,  tags="image_off")
        self.ONOFF.create_image(120, 35, image=self.img_on,  tags="image_on")
        self.canevas.create_text(10, 10, anchor='nw', text=str(
            self.counter_comparison) + " comparisons", fill='black', tags="cpt")
        # Bouton pour créer un Diagramme
        self.creation_diagram = Button(
            self.Window, text='Create Diagram', command=self.creation)
        # widgets de la fenetre
        self.b1 = Button(self.Window, text="INSERTION SORT",
                         bg=self.background, command=self.button_animation_insertion_sort)
        self.b2 = Button(self.Window, text="SELECTION SORT",
                         bg=self.background, command=self.button_animation_selection_sort)
        self.b3 = Button(self.Window, text="QUICK SORT",
                         bg=self.background, command=self.button_animation_quick_sort)
        self.b4 = Button(self.Window, text="MERGE SORT",
                         bg=self.background, command=self.button_animation_merge_sort)
        self.b5 = Button(self.Window, text="RADIX SORT",
                         bg=self.background, command=self.button_animation_radix_sort)
        # champ de saisie du nbr de rectangle
        self.field = Entry(self.Window, textvariable=self.nbr)
        self.field.delete(0, END)  # on enleve le 0 par défaut
        self.field.insert(INSERT, 31)  # on l'initialise à 31 par défaut
        self.sliderspeed = Scale(self.Window, from_=500, to=10, orient=HORIZONTAL,
                                 resolution=10, length=300, showvalue=2)  # slider pour la vitesse
        # initialisation de la vitesse de tri à une vitesse moyenne permettant une compréhension suffisante
        self.sliderspeed.set(200)
        # la barre d'espace permet d'arreter ou de relancer l'animation de tri
        self.Window.bind("<space>", self.administrator)
        # permet de lancer la creation d'un nouveau diagramme
        self.Window.bind("<Return>", self.administrator)
        # Organisation sur la fenetre
        self.canevas.pack(padx=5, pady=5)
        self.field.pack(side=RIGHT, padx=5, pady=5)
        self.b1.pack(side=LEFT, padx=5, pady=5)
        self.b2.pack(side=LEFT, padx=5, pady=5)
        self.b3.pack(side=LEFT, padx=5, pady=5)
        self.b4.pack(side=LEFT, padx=5, pady=5)
        self.b5.pack(side=LEFT, padx=5, pady=5)
        self.creation_diagram.pack(side=RIGHT, padx=10, pady=5)
        Button(self.Window, relief=RAISED, bitmap='info',
               command=self.helpme).pack(side=RIGHT, padx=10)
        self.ONOFF.pack(side=RIGHT, padx=20, pady=5)
        self.sliderspeed.pack(padx=50, pady=5)

    # FUNCTIONS

    def reset(self):  # Appel de cette fonction dans creation et permet de recréer un diagramme en arretant le tri
        self.ending = False  #  variable qui permet de savoir si le tri était fini
        self.ind_verif = -1  #  réinitialisation de l'indice de vérification
        self.canevas.delete(ALL)  #  efface tout sur le Canvas
        # on cache l'image ON
        self.ONOFF.itemconfig("image_on",  state='hidden')
        #  on cache l'image OFF
        self.ONOFF.itemconfig("image_off",  state='hidden')
        self.canevas.create_text(10, 10, anchor='nw', text=str(
            self.counter_comparison) + " comparisons", tags="cpt")
        self.canevas.itemconfig("counter", fill="black")
        self.S.reset()
        self.stop = False  # Aucun tri n'est en cours donc on est réinitialise la valeur a false pour que le tri se lance des l'appui du bouton
        self.List_rectangles = []  # on réinitialise la liste de rectangles

    def too_much(self):  # on regarde si il y trop de rectangles à supporter pour le canvas
        # on récupère le nbr de rectangles saisie
        field_entry = int(self.field.get())
        if field_entry >= 500:  # si il est plus grand que 500 qui est ici le maximum accepté...
            self.field.delete(0, END)  #  on supprime la valeur du champ
            # on la remplace par une valeur par défaut
            self.field.insert(INSERT, 499)
        #  le nbr de rectangle peut maintenant récupérer la valeur du champ
        self.nbr = int(self.field.get())

    def draw(self):  # on dessine sur le canvas
        self.nbr = int(self.field.get())
        # épaisseur d'un rectangle dépendant de la largeur du canavs et du nbr de rectangles
        thickness = self.weight / self.nbr
        if self.nbr >= 300:  # à partir de 300 rectangles...
            edge = ""  #  on enleve les bords sur le canvas pour plus de lisibilité
        else:
            edge = "black"  # sinon on la laisse
        for i in range(len(self.S.List_height)):
            r = self.canevas.create_rectangle((i * thickness, self.height, (i + 1) * thickness,
                                              self.height - self.S.List_height[i]), tags="rect", outline=edge, fill='white')
            # on remplit notre Liste_rectangles de tout les identifiants de nos rectangles
            self.List_rectangles.append(r)

    def creation(self):
        self.reset()  # on reset le canvas
        self.too_much()
        self.nbr = int(self.field.get())
        # ici on créer les tailles des rectangles dans un ordre croissant et proportionel
        for i in range(1, self.nbr+1):
            size = round((self.height / self.nbr) * i - 2)
            # on les ajoute à la liste des hauteurs
            self.S.List_height.append(size)
        # on mélange aléatoirement pour que les tris soit utiles
        random.shuffle(self.S.List_height)
        self.draw()  # enfin on dessine

    def settings_speed(self):  # mise à jour de la vitesse selon le nbr de rectangles
        self.nbr = int(self.field.get())
        # la vitesse de traitement est gardé comme telle ( exprimé en ms sur le slider )
        if int(self.field.get()) < 150:
            self.turbo = self.sliderspeed.get()
        else:
            # plus on a de rectangles plus on améliore la rapidité d'éxécution
            self.turbo = self.sliderspeed.get()//((self.nbr % 100)+1)

    def administrator(self, event):  # gestionnaire d'évènements

        self.canevas.focus_set()
        if event.keysym == "space":  # pression de la barre d'espace
            # on inverse la variable à chaque nouvelle pression de la barre d'espace
            self.stop = not self.stop

            if self.stop:  # si on est en pause on cache l'image ON et on laisse image OFF
                self.ONOFF.itemconfig('image_on', state='hidden')
                self.ONOFF.itemconfig("image_off", state='normal')
            else:  # sinon on cache l'image OFF et on laisse image ON
                self.ONOFF.itemconfig("image_on", state='normal')
                self.ONOFF.itemconfig("image_off", state='hidden')

        if event.keysym == "Return":  # pression de la touche Entrée
            self.creation()  # créer un nouveau Diagramme

    def update_comp(self):  # on met à jour le nombre de comparaisons éffectuées
        self.canevas.itemconfig("cpt", text=str(
            self.counter_comparison) + " comparisons")

    def update_unit(self):  # on utilise unit pour savoir sur quel chiffre on s'intéresse
        unit = ["the unit", "the dozen", "the hundred"]
        self.canevas.itemconfig("cpt", text=unit[self.unit])

    def safety_on(self):  # on désactive tout les boutons de tri
        for b in [self.b1, self.b2, self.b3, self.b4, self.b5]:
            b.config(state='disabled')

    def safety_off(self):  # on réactive tout les boutons de tri
        for b in [self.b1, self.b2, self.b3, self.b4, self.b5]:
            b.config(state='normal')

    def reset_var(self):  # on reset toutes les variables susceptibles d'avoir été utilisées
        self.counter_comparison = 0
        self.ind_current = 0
        self.ind_verif = 0
        self.ending = not self.ending
        self.nbr_comp = 0
        self.ind_mini = 0
        self.unit = 0

    def helpme(self):
        try:
            # Si aucune fenêtre Help n'est ouvert ou si elle à été détruite manuellement on ne fait rien
            self.help.Window.destroy()
        except:  # Sinon on créer Help
            self.help = Help([("The rectangle we are sorting", self.color_current),
                              ("The rectangle we are comparing", self.color_comp),
                              ("The place where we insert the rectangle",
                               self.color_moved),
                              ("The rectangle is sorted", self.color_ok),
                              ("The pivot used", self.color_pivot),
                              ("", "purple"),
                              ("", "pink"),
                              ("", "deep sky blue"),
                              ("", "green"),
                              ("", "orange")])

# ANIMATION INSERTION

    def verif(self):  # verifie le bon tri des éléments et valide en les coloriant graduellement
        if -1 < self.ind_verif < len(self.S.List_height)-1:
            if self.S.List_height[self.ind_verif] <= self.S.List_height[self.ind_verif + 1]:
                self.canevas.itemconfig(
                    self.List_rectangles[self.ind_verif], fill=self.color_ok)
            self.ind_verif += 1  # on passe à la vérification suivante
            # elle est en accéléré car ce n'est qu'une vérification
            self.Window.after(self.turbo//2, self.verif)
        elif -1 < self.ind_verif == len(self.S.List_height)-1:
            self.canevas.itemconfig(
                self.List_rectangles[self.ind_verif], fill=self.color_ok)
            self.ind_verif += 1  #  on passe à la vérification suivante
            self.Window.after(self.turbo//2, self.verif)  # bis
        else:
            self.ind_verif = 1  # réinitialise l'indice de vérification
            self.safety_off()  # on désécurise les boutons

    def button_animation_insertion_sort(self):
        self.settings_speed()  # on met à jour la vitesse
        self.reset_var()  # on réinitialise les variables
        # si le tri est fini et qu'on veut refaire le tri sur une liste dèjà triée ...
        if not self.ending:
            self.creation()  # ... on ne peut pas ! A la place on créer un nouveau Diagramme
        else:
            self.safety_on()  # on désactive tout les boutons
            self.S.insert_sort()  # on trie...
            self.conductor_insertion_sort()  # ...puis on anime

    # chef d'orchestre qui choisit le type d'animation
    def conductor_insertion_sort(self):
        # si on a fini de tout trier...
        if self.ind_current >= len(self.S.List_animation):
            # s'il rester un rectangle colorié on le rend blanc
            self.canevas.itemconfig("ok", fill="white")
            self.canevas.dtag("ok", "ok")  # on le dtag
            self.verif()  # Fonction de vérification
        else:
            self.update_comp()  # on met à jour sur le canevas le nombre de comparaisons
            self.settings_speed()  #  on met à jour la vitesse
            if not self.stop:  # si le pgrm n'est pas en pause
                # "e" = echanges
                if str(self.S.List_animation[self.ind_current][2]) == "e":
                    nbr_move = self.S.ind_swap  # le nbr de rectangles à décaler sur le canvas
                    self.S.reset_swap()  # indice_echange = 0 pour recommencer à partir d'un nouveau rectangle
                    # le rectangle que l'on veut trié
                    rect_courant = self.S.List_animation[self.ind_current][1]
                    self.animation_swap_insertion(nbr_move, rect_courant)
                # "c" = comparaisons
                elif str(self.S.List_animation[self.ind_current][2]) == "c":
                    self.counter_comparison += 1  # et d'une comparaisons de plus
                    # un décalage supplémentaire sera nécéssaire pour l'animation de l'échange
                    self.S.ind_swap += 1
                    self.animation_comparisons_insertion()
            else:
                # on boucle sur lui-même si on est en pause
                self.Window.after(self.turbo, self.conductor_insertion_sort)

    def animation_swap_insertion(self, place, current):  # anime une echange
        # on efface les traces de la derniere action
        self.canevas.itemconfig("ok", fill="white")
        self.canevas.itemconfig("comp", fill="white")  # idem
        self.canevas.dtag("ok", "ok")  # idem
        # on cherche l'epaisseur du rectangle qui va permettre le depl sur le canvas
        thickness = self.weight / self.nbr
        # on stocke le rectangle que l'on veut trier
        stock = self.List_rectangles[current]
        for i in range(1, place + 1):  # on decale tous jusqu'à l'endroit où il doit être inséré
            # on decale vers la droite les elements
            self.List_rectangles[current - i +
                                 1] = self.List_rectangles[current - i]
            # on decale vers la droite d'une largeur de rectangle
            self.canevas.move(self.List_rectangles[current - i], thickness, 0)
        # on reinsere le rectangle courant à sa place
        self.List_rectangles[self.S.List_animation[self.ind_current][0]] = stock
        # on deplace le rectangle courant à sa place sur le canvas
        self.canevas.move(stock, -place * thickness, 0)
        # le rectangle est trié on le tag "ok"
        self.canevas.itemconfig(
            self.List_rectangles[self.S.List_animation[self.ind_current][0]], tags="ok")
        # le rectangle est colorié en jaune où il est inséré
        self.canevas.itemconfig("ok", fill=self.color_moved)
        self.ind_current += 1  # on passe au prochaine tuple de la liste d'animation
        # on reprend l'animation de la liste complete
        self.Window.after(self.turbo, self.conductor_insertion_sort)

    def animation_comparisons_insertion(self):  # anime une comparaison

        # on efface les traces de la derniere action
        self.canevas.itemconfig("comp", fill="white")
        # on efface les traces de la derniere action
        self.canevas.itemconfig("ok", fill="white")
        # on efface les traces de la derniere action
        self.canevas.dtag("comp", "comp")
        # on efface les traces de la derniere action
        self.canevas.dtag("ok", "ok")

        # le rectangle que l'on compare
        rect_compare = self.List_rectangles[self.S.List_animation[self.ind_current][0]]
        #  le rectangle que l'on veut trier
        rect_courant = self.List_rectangles[self.S.List_animation[self.ind_current][1]]

        if self.S.ind_swap == 1:  # si c'est la première echange faire...
            self.canevas.itemconfig(rect_courant, tags="courant")

        # on tag le rectangle que l'on compare pour le reconnaîre
        self.canevas.itemconfig(rect_compare, tags="comp")
        # on colorie en vert le rect que l'on veut trier
        self.canevas.itemconfig("courant", fill=self.color_current)
        # on colorie en rouge le rect avec lequel on le compare
        self.canevas.itemconfig("comp", fill=self.color_comp)
        self.ind_current += 1  # on passe au prochain tuple dans la liste d'animation
        # on reprend l'animation de la liste complete
        self.Window.after(self.turbo, self.conductor_insertion_sort)


# ANIMATION SELECTION


    def button_animation_selection_sort(self):
        self.settings_speed()  # on met à jour la vitesse
        self.reset_var()  # on réinitialise les variables
        # si le tri est fini et qu'on veut refaire le tri sur une liste dèjà triée ...
        if not self.ending:
            self.creation()  # ... on ne peut pas ! A la place on créer un nouveau Diagramme
        else:
            self.safety_on()   # on désactive tout les boutons
            self.S.select_sort()  # on trie...
            self.conductor_selection_sort()  # ... puis on anime

    # chef d'orchestre qui choisit le type d'animation
    def conductor_selection_sort(self):

        # si on a fini de tout trier...
        if self.ind_current >= len(self.S.List_animation):
            self.canevas.itemconfig("ok", fill=self.color_ok)
            self.canevas.dtag("ok", "ok")
            self.canevas.dtag("comp", "comp")
            self.canevas.dtag("comp", "comp")
            self.safety_off()
        else:
            # c'est le signal pour stopper le son joué précédemment si il est encore en train de jouer
            self.update_comp()
            self.settings_speed()
            if not self.stop:
                # "m"= nouveau minimum trouvé
                if str(self.S.List_animation[self.ind_current][2]) == "m":
                    self.nbr_comp = self.S.ind_swap
                    # on recupere l'indice du plus petit
                    self.ind_mini = self.S.List_animation[self.ind_current][1]
                    self.S.ind_swap += 1
                    self.animation_minimum(self.ind_mini)
                # "e" = echanges
                elif str(self.S.List_animation[self.ind_current][2]) == "e":
                    nb_comp = self.nbr_comp
                    self.nbr_comp = 0
                    self.S.reset_swap()  # indice_echange = 0 pour recommencer à partir d'un nouveau rectangle
                    self.animation_swap_selection(nb_comp, self.ind_mini)
                # "c" = comparaisons
                elif str(self.S.List_animation[self.ind_current][2]) == "c":
                    self.counter_comparison += 1  # et d'une comparaisons de plus
                    self.S.ind_swap += 1  # un décalage supplémentaire sera nécéssaire
                    self.animation_comparisons_selection()
            else:
                # on boucle tant qu'on est en pause
                self.Window.after(self.turbo, self.conductor_selection_sort)

    def animation_minimum(self, ind_minimum):  # anime le plus petit rectangle
        # on efface les traces de la dernière action
        self.canevas.itemconfig("mini", fill="white")
        # on efface les traces de la dernière action
        self.canevas.dtag("mini", "mini")
        # on tag le plus petit en mini
        self.canevas.itemconfig(self.List_rectangles[ind_minimum], tags="mini")
        # on le colorie en vert
        self.canevas.itemconfig("mini", fill=self.color_current)
        # on colorie ceux qui sont tag ok avec la couleur pour trier
        self.canevas.itemconfig("ok", fill=self.color_ok)
        self.ind_current += 1  # on passe au prochain tuple
        # on reprend l'animation de la liste d'animation
        self.Window.after(self.turbo, self.conductor_selection_sort)

    def animation_swap_selection(self, gap, mini):  # anime une echange
        # on colorie ceux qui sont tag ok, ceux qui sont déjà trié
        self.canevas.itemconfig("ok", fill=self.color_ok)
        self.canevas.dtag("ok", "ok")  # on supprime le tag ok
        # déplace le mini au début
        self.canevas.move(
            self.List_rectangles[mini], -gap * (self.weight / self.nbr), 0)
        self.canevas.move(self.List_rectangles[self.S.List_animation[self.ind_current][0]], gap * (
            self.weight / self.nbr), 0)  # déplace le rectangle à l'ancienne position de mini
        self.List_rectangles[mini], self.List_rectangles[self.S.List_animation[self.ind_current][0]
                                                         # on échange les rectangles de place dans la liste
                                                         ] = self.List_rectangles[self.S.List_animation[self.ind_current][0]], self.List_rectangles[mini]
        # on tag le rectangle mini
        self.canevas.itemconfig(
            self.List_rectangles[self.S.List_animation[self.ind_current][0]], tags="ok")
        # on colorie l'item avec le tag ok
        self.canevas.itemconfig("ok", fill=self.color_moved)
        # ajoute le tag ok à tout les items qui sont tag mini
        self.canevas.addtag_withtag("mini", "ok")
        self.ind_current += 1  # on passe au prochain tuple
        # on reprend l'animation de la liste d'animation
        self.Window.after(2 * self.turbo, self.conductor_selection_sort)

    def animation_comparisons_selection(self):  # anime une comparaison
        # colorie en blanc les items ayant le tag comp
        self.canevas.itemconfig("comp", fill="white")
        self.canevas.itemconfig("ok", fill=self.color_ok)
        self.canevas.dtag("comp", "comp")  # supprime le tag comp
        self.canevas.dtag("ok", "ok")
        # ajoute le tag comp au rectangle à l'indice current
        self.canevas.itemconfig(
            self.List_rectangles[self.S.List_animation[self.ind_current][1]], tags="comp")
        self.canevas.itemconfig("comp", fill=self.color_comp)
        self.ind_current += 1  # on passe au prochaon tuple
        # on reprend l'animation de la liste d'animation
        self.Window.after(self.turbo, self.conductor_selection_sort)


# ANIMATION QUICK

    # commenté sur le animation_selection_sort

    def button_animation_quick_sort(self):
        self.settings_speed()
        self.reset_var()
        if not self.ending:
            self.creation()
        else:
            self.safety_on()
            self.S.quick_sort(0, len(self.S.List_height))  # on trie...
            self.conductor_quick_sort()  # ... puis on anime

    def conductor_quick_sort(self):  #
        if self.ind_current >= len(self.S.List_animation):
            self.canevas.itemconfig("pivot", fill=self.color_ok)
            self.canevas.dtag("pivot", "pivot")
            self.canevas.dtag("bigger", "bigger")
            self.canevas.dtag("smaller", "smaller")
            self.safety_off()
        else:
            self.update_comp()
            self.settings_speed()
            if not self.stop:
                # si c'est le pivot
                if str(self.S.List_animation[self.ind_current][2]) == "p":
                    self.animation_pivot()  # lance l'animation du pivot
                # si c'est un rectangle "smaller" ou "bigger"
                elif str(self.S.List_animation[self.ind_current][2]) == "big" or str(self.S.List_animation[self.ind_current][2]) == "small":
                    self.counter_comparison += 1  # on passe à la prochaine comparaison
                    # lance l'animation du "smaller" ou "bigger"
                    self.animation_routing_smaller_bigger()
            else:
                self.Window.after(self.turbo, self.conductor_quick_sort)

    # Trouve le pivot et le place au debut de la portion du diagramme qu'on traite
    def animation_pivot(self):

        self.canevas.itemconfig("pivot", fill=self.color_ok)
        self.canevas.itemconfig("bigger", fill=self.color_moved)
        self.canevas.dtag("pivot", "pivot")

        ind_rect1 = self.S.List_animation[self.ind_current][0]
        ind_rect2 = self.S.List_animation[self.ind_current][1]

        self.canevas.move(
            self.List_rectangles[ind_rect2], (-ind_rect2 + ind_rect1) * (self.weight / self.nbr), 0)
        self.canevas.move(
            self.List_rectangles[ind_rect1], (ind_rect2 - ind_rect1) * (self.weight / self.nbr), 0)
        self.List_rectangles[ind_rect1], self.List_rectangles[ind_rect2] = self.List_rectangles[ind_rect2], self.List_rectangles[ind_rect1]

        self.canevas.itemconfig(self.List_rectangles[ind_rect1], tags="pivot")
        self.canevas.itemconfig("pivot", fill=self.color_pivot)
        self.ind_current += 1

        self.Window.after(self.turbo, self.conductor_quick_sort)

    # si le rectangle est plus petit que le pivot on le place juste avant le pivot
    def animation_smaller(self):
        # si le rectangle est plus grand on le laisse là où il est
        self.canevas.itemconfig("pivot", fill="white")
        self.canevas.dtag("pivot", "pivot")

        # indice du rectangle pivot
        ind_rect1 = self.S.List_animation[self.ind_current][0]
        # indice du plus petit que pivot
        ind_rect2 = self.S.List_animation[self.ind_current][1]

        stock = self.List_rectangles[ind_rect1]  # le rectangle pivot
        self.List_rectangles[ind_rect1] = self.List_rectangles[ind_rect2]
        self.canevas.move(
            self.List_rectangles[ind_rect2], (-ind_rect2 + ind_rect1) * (self.weight / self.nbr), 0)

        # on deplace d'une largeur tout les rectangles compris entre le pivot et le rectangle plus petit
        for j in range(0, ind_rect2-ind_rect1-1):
            self.canevas.move(
                self.List_rectangles[ind_rect2 - j - 1], (self.weight / self.nbr), 0)
            self.List_rectangles[ind_rect2 -
                                 j] = self.List_rectangles[ind_rect2 - j - 1]
        self.canevas.move(stock, (self.weight / self.nbr), 0)
        self.List_rectangles[ind_rect1 + 1] = stock

        self.canevas.itemconfig("smaller", fill=self.color_moved)
        self.canevas.itemconfig(
            self.List_rectangles[ind_rect1 + 1], tags="pivot")
        self.canevas.itemconfig(
            self.List_rectangles[ind_rect1 + 1], fill=self.color_pivot)
        self.ind_current += 1
        self.Window.after(self.turbo, self.conductor_quick_sort)

    # ajoute le tag "bigger" ou "smaller" au rectangle courant puis lance respectivement animation_smaller ou animation_bigger
    def animation_routing_smaller_bigger(self):

        self.canevas.itemconfig("bigger", fill="white")
        self.canevas.itemconfig("smaller", fill="white")
        self.canevas.dtag("bigger", "bigger")
        self.canevas.dtag("smaller", "smaller")

        if str(self.S.List_animation[self.ind_current][2]) == "big":
            self.canevas.itemconfig(
                self.List_rectangles[self.S.List_animation[self.ind_current][1]], tags="bigger")
            self.canevas.itemconfig("bigger", fill=self.color_comp)
            self.ind_current += 1
            self.Window.after(self.turbo, self.conductor_quick_sort)
        else:
            self.canevas.itemconfig(
                self.List_rectangles[self.S.List_animation[self.ind_current][1]], tags="smaller")
            self.canevas.itemconfig("smaller", fill=self.color_comp)
            self.Window.after(self.turbo, self.animation_smaller)


# ANIMATION MERGE

    # commenté sur le animation_selection_sort

    def button_animation_merge_sort(self):
        self.settings_speed()
        self.reset_var()
        if not self.ending:
            self.creation()
        else:
            self.safety_on()
            self.S.merge_sort(0, len(self.S.List_height) - 1)
            self.conductor_merge_sort()  # ... puis on anime

    def conductor_merge_sort(self):

        # si on fini de tout trié on lance verif() qui colorie toute la liste trié
        if self.ind_current >= len(self.S.List_animation):
            self.verif()
        else:
            self.update_comp()
            self.settings_speed()

            if not self.stop:
                # si "edge" on trace une ligne de pointillé sur la portion qu'on traite
                if str(self.S.List_animation[self.ind_current][2]) == "edge":
                    self.tempo = self.List_rectangles[:]
                    self.animation_edge()
                    self.ind_memory = 0
                    self.memory.clear()

                # si "org" on colorie en rouge toutes les comparaisons qu"on effectue au fur et à mesure
                elif str(self.S.List_animation[self.ind_current][2]) == "org":
                    self.counter_comparison += 1
                    self.animation_organisation()

                # si "reorg" on redessine les rectangles triés sur la portion qu'on traite
                elif str(self.S.List_animation[self.ind_current][2]) == "reorg":
                    self.animation_memory()

            else:
                self.Window.after(self.turbo, self.conductor_merge_sort)

    def animation_edge(self):  # trace une ligne de pointillés entre composante1 et composante2 qui sont les 2 rectangles qui délimitent la ligne de pointillés, càd la portion qu'on traite actuellement

        self.canevas.delete("area")
        thickness = self.weight / self.nbr
        composante1 = self.S.List_animation[self.ind_current][0]
        composante2 = self.S.List_animation[self.ind_current][1]

        self.canevas.create_line(composante1 * thickness, self.height / 2, (composante2 + 1) * thickness, self.height / 2,
                                 width=4, fill=self.color_pivot, dash=(3,), arrow="both", tags="area")

        self.ind_current += 1

        self.Window.after(self.turbo, self.conductor_merge_sort)

    def animation_organisation(self):

        self.canevas.itemconfig("r", fill="white")
        self.canevas.itemconfig("b", fill=self.color_pivot)
        self.canevas.dtag("r", "r")

        # les 2 indices des rectangles où on effectue les comparaisons
        composante1 = self.S.List_animation[self.ind_current][0]
        composante2 = self.S.List_animation[self.ind_current][1]

        # le rectangle courant est celui d'indice composante2
        rect_courant = self.List_rectangles[composante2]

        self.canevas.itemconfig(rect_courant, tags="r")
        # colorie en rouge le rectangle courant
        self.canevas.itemconfig("r", fill="red")

        # remplissage de la liste memory qui va contenir des tuples utiles pour animation_memory() dans la suite
        self.memory.append((composante1, composante2))

        self.ind_current += 1

        self.Window.after(self.turbo, self.conductor_merge_sort)

    def animation_memory(self):

        self.canevas.itemconfig("ok", fill="white")
        self.canevas.itemconfig("r", fill="white")
        self.canevas.dtag("r", "r")

        if self.ind_memory < len(self.memory):

            # l'endrois ou on place le rectangle
            place = self.memory[self.ind_memory][0]
            # indice du rectangle qu'on va placer
            ind_rect = self.memory[self.ind_memory][1]

            rect_to_move = self.tempo[ind_rect]  # rectangle qu'on va placer

            start = list(self.canevas.coords(rect_to_move))[1]
            # on conserve les coordonnées y0,y1 du rectangle qu on va placer (utilise pour la redéfinition des coordonnées du rectangle qu'on bouge ci-dessous)
            end = list(self.canevas.coords(rect_to_move))[3]

            self.canevas.coords(rect_to_move, place * (self.weight / self.nbr), start, (place + 1) * (
                self.weight / self.nbr), end)  # nouvelle coordonnées de rect_to_move

            # change la position de rect_to_move dans la liste de rectangles
            self.List_rectangles[place] = rect_to_move
            self.canevas.itemconfig(
                self.List_rectangles[place], fill=self.color_moved)
            # colorie le rectangle rect_to_move
            self.canevas.itemconfig(self.List_rectangles[place], tags="ok")
            self.ind_memory += 1

        else:
            self.ind_current += 1

        self.Window.after(self.turbo, self.conductor_merge_sort)


# ANIMATION RADIX


    def button_animation_radix_sort(self):
        self.settings_speed()
        self.reset_var()
        if not self.ending:
            self.creation()
        else:
            self.safety_on()
            self.S.radix_sort()  # on trie...
            self.conductor_radix_sort()  # ... puis on anime

    def conductor_radix_sort(self):
        if self.ind_current >= len(self.S.List_animation):
            self.verif()
            self.List_rectangles_memory = []
            self.moving = 0
        else:
            self.update_unit()
            self.settings_speed()
            if not self.stop:
                # Si "fill" on colorie le rectangle en fonction de son chiffre
                if str(self.S.List_animation[self.ind_current][1]) == "fill":
                    self.animation_tracking()
                # Si "move" on déplacer le rectangle et on le place à sa nouvelle position
                elif str(self.S.List_animation[self.ind_current][1]) == "move":
                    self.animation_order()
                # Colorie tout le diagramme en blanc, indique un passage à la prochaine unité
                elif self.S.List_animation[self.ind_current][1] == -1:
                    self.animation_preparation()
            else:
                self.Window.after(self.turbo, self.conductor_radix_sort)

    # Si "fill" on colorie le rectangle en fonction de son chiffre
    def animation_tracking(self):

        coloring = [self.color_current, self.color_comp, self.color_ok, self.color_moved, self.color_pivot,
                    "purple", "pink", "deep sky blue", "green", "orange"]  # liste de toute les couleurs
        current_rect = self.List_rectangles[self.S.List_animation[self.ind_current][0]]
        # le chiffre que le traitre qui servira d'indice pour choisir la couleur
        color_unit = self.S.List_animation[self.ind_current][2]

        self.canevas.itemconfig(current_rect, fill=coloring[color_unit])

        self.ind_current += 1

        self.Window.after(self.turbo, self.conductor_radix_sort)

    # Si "move" on déplacer le rectangle et on le place à sa nouvelle position
    def animation_order(self):

        ind_memory = self.S.List_animation[self.ind_current][0]
        current_rect = self.List_rectangles[ind_memory]

        start = list(self.canevas.coords(current_rect))[1]
        end = list(self.canevas.coords(current_rect))[3]

        self.List_rectangles_memory.append(ind_memory)

        self.canevas.coords(current_rect, self.moving * (self.weight / self.nbr), start,
                            (self.moving + 1) * (self.weight / self.nbr), end)

        # tag_raise pour placer le rectangle au dessus du rectangle déja en place (sinon il se place derrière)
        self.canevas.tag_raise(current_rect)

        self.ind_current += 1
        self.moving += 1

        self.Window.after(self.turbo, self.conductor_radix_sort)

    # Colorie tout le diagramme en blanc, indique un passage à la prochaine unité et réinitialise les variables utilisées
    def animation_preparation(self):
        new_list = []
        for i in range(len(self.List_rectangles_memory)):
            new_list.append(
                self.List_rectangles[self.List_rectangles_memory[i]])
        # on recupère la nouvelle liste après la réorganisation
        self.List_rectangles[:] = new_list
        for i in range(len(self.List_rectangles)):
            self.canevas.itemconfig(self.List_rectangles[i], fill="white")
        self.List_rectangles_memory[:] = []
        self.moving = 0
        self.ind_current += 1
        self.unit += 1
        self.Window.after(self.turbo, self.conductor_radix_sort)


A = Animation()
A.creation()
A.Window.mainloop()
