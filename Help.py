from tkinter import *


class Help:  # Explique le code couleur à l'utilisateur
    
    def __init__(self, list):
        self.height = 300
        self.weight = 500
        self.background = "gray90"
        self.Window = Tk()
        self.Window.title("Some guidance")
        self.Window.resizable(width=False, height=False)
        self.explanations = list  # Liste des explications et des couleurs
        self.c = Canvas(self.Window, width=self.weight, height=self.height, bg=self.background)
        self.c.pack(side=LEFT, padx=5, pady=5)
        Button(self.Window, text='Insertion Sort', command=self.sort_spec_easy).pack(side=TOP, padx=5, pady=5)
        Button(self.Window, text='Selection Sort', command=self.sort_spec_easy).pack(side=TOP, padx=5, pady=5)
        Button(self.Window, text='Quick Sort', command=self.sort_spec_quick).pack(side=TOP, padx=5, pady=5)
        Button(self.Window, text='Merge Sort', command=self.sort_spec_merge).pack(side=TOP, padx=5, pady=5)
        Button(self.Window, text='Radix Sort', command=self.radix_spec).pack(side=TOP, padx=5, pady=5)

    def clean(self):
        self.c.delete(ALL)  # efface tout le canvas pour afficher les nouvelles informations demandées
        
    def sort_spec_easy(self):  # les 2 premiers tris ont le même code couleur

        self.clean()
        size_rect = (self.weight - 50) / 4

        for i in range(4):  # les 4 couleurs que l'on utilise et leur description
            self.c.create_rectangle(size_rect * i + 10 * (i+1), 10, size_rect * (i+1) + 10 * i, 290, fill=self.explanations[i][1])
            self.c.create_text(50 + size_rect * i + 10 * (i+1), 150, width=90, font=("Times",  "15",  "bold italic"), text=self.explanations[i][0])
            
    def sort_spec_merge(self): # les explications du tri fusion

        self.clean()
        size_rect = (self.weight - 50) / 4

        for i in range(0,3):
            self.c.create_rectangle(size_rect * i + 10 * (i+1), 10, size_rect * (i+1) + 10 * i, 290, fill=self.explanations[i + 1][1])
            self.c.create_text(50 + size_rect * i + 10 * (i+1), 150, width=90, font=("Times",  "15",  "bold italic"), text=self.explanations[i + 1][0])

        self.c.create_line(size_rect * 3 + 30, self.height / 4, size_rect * 4 + 40, self.height / 4,
                           width=4, fill=self.explanations[4][1],
                           dash=(3,), arrow="both")
        self.c.create_text(size_rect*4-20, 150, width=90,
                           font=("Times", "15", "bold italic"),
                           text="The merged area") # dessine la zone que l'on trie par une double fleche

    def sort_spec_quick(self):  # les explications du tri rapide

        self.clean()
        size_rect = (self.weight - 50) / 4

        for i in range(4):
            self.c.create_rectangle(size_rect * i + 10 * (i+1), 10, size_rect * (i+1) + 10 * i, 290,
                                    fill=self.explanations[i + 1][1])
            self.c.create_text(50 + size_rect * i + 10 * (i+1), 150,
                               width=90, font=("Times",  "15",  "bold italic"), text=self.explanations[i + 1][0])

    def radix_spec(self):  # les explications du tri par base avec une couleur pour chaque unité ( 0,1,2,... )

        self.clean()
        size_rect = (self.weight - 60) / 5
        height_rect = (self.height - 10) / 2
        cpt = 0  # variable locale qui donne l'indice de l'explication et de sa couleur dans le tableau

        for i in range(2):
            for j in range(5):
                self.c.create_rectangle(size_rect * j + 10 * (j+1), i * height_rect + 10, size_rect * (j+1) + 10 * j, (i+1) * height_rect, fill=self.explanations[cpt][1])
                self.c.create_text(40+size_rect*j+10*(j+1), (1-i)*height_rect/2+i*(i+1/2)*height_rect, width=90, font=("Times",  "15",  "bold italic"), text=str(cpt))
                cpt += 1  # incrémentation pour passer à la prochaine explication
