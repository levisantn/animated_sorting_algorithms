class Sort:
    
    def __init__(self):  # initialisation de notre objet 

        self.List_height = []  # liste des hauteurs des rectangles
        self.List_animation = []  # liste des echanges et comparaisons
        self.ind_swap = 0  # indice qui permet de savoir combien de comparaisons ont été faites entre 2 echanges

    def reset(self):  # on reset tout les attributs de Sort
        
        self.List_height = []
        self.List_animation = []
        self.ind_swap = 0

    def reset_swap(self):
        self.ind_swap = 0  # on reset l'indice d'échange à chaque nouvelle echange

#INSERTION SORT

    def insert_sort(self):
        
        for i in range(1, len(self.List_height)):  # pour chaque élément de la liste[1:]
            
            current = self.List_height[i]  # on désigne le rectangle à trier
            j = i  # j est une variable décroissante qui va nous permettre de comparer avec les autres rectangles
    
            while j > 0 and self.List_height[j - 1] > current:  # on cherche à placer le rectangle courant là où il faut
                # les conditions de sortie de boucle sont si current est le plus petit ( ie j=0 ) ou si un autre élément est plus petit que current
                self.List_animation.append((j - 1, j, "c"))  # si on est dans aucun de ces cas alors l'action est une comparaison
                self.List_height[j - 1], self.List_height[j] = self.List_height[j], self.List_height[j - 1]  # on inverse les éléments dans la liste car current < comparé
                j = j-1  # on décremente j

            self.List_animation.append((j, i, "e"))  # on sort de la boucle donc on fait une échange  tuple=(indice de l'endroit où le rectangle est inséré,
            #                                                                                                indice du rectangle que l'on trie,
            #                                                                                                 e pour échanges)

#SELECTION SORT

    def select_sort(self):

        tab = self.List_height  # utilisation de tab dans un simple but de clarité du code
        n = len(tab)  # taille de la liste
        
        for current in range(0, n):  # current est un indice dans la liste
            
            smaller = current  # le plus petit est désigné comme étant current
            self.List_animation.append((current, smaller, "m"))  # "m" pour animation du minimum
            
            for j in range(current+1, n):  # on regarde dans la partie droite de la liste après current
                
                if tab[j] < tab[smaller]:  # si on trouve un nouveau minimum
                    smaller = j  # smaller devient donc l'indice de ce nouveau minimum
                    self.List_animation.append((current, smaller, "m"))  # "m" pour animation du minimum
                else:
                    self.List_animation.append((smaller, j, "c")) # sinon c'est une simple comparaison
                    
            if min is not current: # a la fin du parcours de la liste si current n'est pas le minimum on l'inverse avec celui-ci
                
                stock = tab[smaller]  # on stocke la valeur du minimum dans stock
                tab[smaller] = tab[current]  # on fait l'échange
                tab[current] = stock  # on réinjecte la valeur du minimum
                self.List_animation.append((current, smaller, "e"))  # on fait une échanges en animation

            else:
                self.List_animation.append((smaller, smaller, "e"))  # on fait une "échange" avec lui-même par soucis de compréhension dans l'animation

#QUICK SORT

    def quick_sort(self, start, end):  # tri rapide entre 2 indices de liste
        
        if start < end: # tant qu'on a pas décomposé par récursivité toute la liste en liste de 1 élément
            pivot = self.quick_sort_partition(start, end)  # on cherche le pivot qui va séparer notre liste en 2
            self.quick_sort(start, pivot)  # on repète l'opération sur la partie gauche
            self.quick_sort(pivot + 1, end)  # on repète l'opération sur la partie droite

    def research_pivot(self, start, end):  # recherche du pivot entre start et end

        maxi = self.List_height[start]  # on initialise maxi a la valeur de départ
        mini = self.List_height[start]  # on intialise aussi mini à la valeur de départ

        for m in range(start, end):  # ici on cherche le plus grand et le plus petit
            if self.List_height[m] > maxi:
                maxi = self.List_height[m]
            if self.List_height[m] < mini:
                mini = self.List_height[m]

        mid = (maxi + mini) / 2  # le milieu est alors défini comme la moyenne des 2

        x = abs(mid - self.List_height[start])  # approximation du pivot
        pivot = start

        for m in range(start, end):  # on cherche la hauteur la plus proche du pivot pour la désigner comme celui-ci
            if abs(mid - self.List_height[m]) < x:
                pivot = m  # m est l'indice de la hauteur la plus moyenne pour obtenir le meilleur pivot
                x = abs(mid - self.List_height[m])  # x prend la nouvelle approximation plus précise

        return pivot  # renvoi l'indice du pivot

    def quick_sort_partition(self, start, end):
        
        ind_pivot = self.research_pivot(start, end)  # on recupère l'indice du pivot
        self.List_height[ind_pivot], self.List_height[start] = self.List_height[start], self.List_height[ind_pivot]  # on l'échange avec le premier élément de la portion
        pivot = start  # après cet échange pivot est donc le premier élément de la liste
        self.List_animation.append((start, ind_pivot, "p"))  # "p" pour l'animation du Pivot
        
        for i in range(start + 1, end):  # on va comparer le pivot avec tout les éléments de la liste
            if self.List_height[i] <= self.List_height[pivot]:  # si c'est plus petit que le pivot
                self.List_animation.append((pivot, i, "small"))  # on l'animera avec le mot "small" pour petit
                stock = self.List_height[pivot]  # on stocke le pivot
                self.List_height[pivot] = self.List_height[i]  # le plus petit prend la place du pivot
                for j in range(0, i-pivot-1):
                    self.List_height[i - j] = self.List_height[i - j - 1]  # on décale vers la droite tout les éléments
                pivot += 1  # on incrémente l'indice du pivot qui c'est forcément décalé de 1
                self.List_height[pivot] = stock  # on réinjecte le pivot à l'indice i
            else:  # si c'est plus grand que le pivot
                self.List_animation.append((pivot, i, "big"))  # on l'animera avec le mot "big" pour grand

        return pivot  # on renvoi le nouveau pivot pour la récursivité

#MERGE SORT

    def merge_sort(self, start, end):  # cette fonction décompose en 2 une liste

        if start < end:  # le cas de base est une liste à un élément qui ne peut plus être décomposée
            mid = (start + end - 1) // 2

            self.merge_sort(start, mid)  # nouvelle décomposition partie gauche
            self.merge_sort(mid + 1, end)  # nouvelle décomposition partie droite
            self.merge(start, mid, end)  # on fusionne l'ensemble

    def merge(self, start, mid, end):  # la fusion

        self.List_animation.append((start, end, "edge"))  # "edge" pour bord pour animer la zone de la liste que l'on traite

        l_init = self.List_height[:]  # copie de notre liste ( représente la mémoire externe )
        
        size_left = mid - start + 1  # la taille de la partie de gauche est définie par l'intervalle (milieu inclus)
        size_right = end - mid  # la taille de la partie de droite est définie par l'intervalle
        
        left = [0]*size_left  # on créer une liste gauche dont tout les éléments sont initier à 0
        pos_left = [0]*size_left  # pos_left est une liste en parallèle de la liste gauche aussi initialisé à 0
        
        right = [0]*size_right  # idem pour la droite
        pos_right = [0]*size_right  # idem pour pos_right
        
        for i in range(0, size_left):
            left[i] = l_init[start + i]  # on range tout les éléments de gauche dans gauche
            pos_left[i] = start + i  # on récupère tout leur indice dans la vrai liste
        for i in range(0, size_right):
            right[i] = l_init[mid+1+i]  # idem pour la droite
            pos_right[i] = mid+1+i  # idem pour la droite
            
        index_left,  index_right = 0, 0  # ces 2 indices vont nous permettre de circuler dans left et right
        index = start  # index est la variable qui permet de circuler dans l_init
        
        while index_left < size_left and index_right < size_right:  # tant qu'on a pas placé tout les éléments d'une des 2 listes
            '''
            Ici on va reclasser dans une seule et unique liste la fusion 
            de la liste de gauche et de celle de droite dans l'ordre croissant.
            Grâce à la récursivité de ce tri, ces 2 parties sont déjà triée séparément.
            On peut donc comparer les éléments les uns aux autres dans l'ordre.
            '''
            if left[index_left] <= right[index_right]:  # si l'élément de la liste de droite est plus grand que celui de gauche
                l_init[index] = left[index_left]  # on place l'élément de gauche à la position index dans la liste qui se fusionne
                self.List_animation.append((index, pos_left[index_left], "org"))  # animation de l'organisation des éléments de fusion
                index_left += 1  # incrémentation de l'indice de gauche
            else:  # Symétriquement si l'élément de la liste de gauche est plus grand que celui de droite
                l_init[index] = right[index_right]
                self.List_animation.append((index, pos_right[index_right], "org"))
                index_right += 1
            index += 1  # incrémentation de l'indice permettant de circuler dans la fusion

        while index_left < size_left:  # si la liste de droite est totalement fusionner alors on y ajoute tout les éléments de la liste de gauche 1 par 1
            l_init[index] = left[index_left]
            self.List_animation.append((index, pos_left[index_left], "org"))
            index_left += 1
            index += 1
        
        while index_right < size_right:  # si la liste de gauche est totalement fusionner alors on y ajoute tout les éléments de la liste de droite 1 par 1
            l_init[index] = right[index_right]
            self.List_animation.append((index, pos_right[index_right], "org"))
            index_right += 1
            index += 1

        self.List_height[:] = l_init  # notre liste initiale devient la liste fusionnée
        self.List_animation.append(("", "", "reorg"))  # reorg permet d'animer la réorganisation de cette nouvelle liste fusionnée


#RADIX SORT

    def radix_sort(self):

        div = 1  # permet de sélectionner le reste du chiffre
        modulo = 10  # permet de sélectionner la valeur de l'unité, dizaine ou centaine
        new_list = []  # la mémoire externe
        final = sorted(self.List_height)  # on stocke la liste triée pour la comparer en condition de boucle
        
        while self.List_height != final:  # tant que la liste n'est pas triée
            
            ind_memory = [[],  [],  [],  [],  [],  [],  [],  [],  [],  []]  # notre tableau de rangement des 0,1,2,3,4,...
            
            for ind_value in range(len(self.List_height)):
                
                least_digit = self.List_height[ind_value] % modulo  # least_digit est la valeur de l'unité
                least_digit = int(least_digit / div)  # récupère la valeur entière de la division
                ind_memory[least_digit].append(ind_value)  # on ajoute cette valeur à la liste à l'indice de liste correspondant à least_digit
                
                self.List_animation.append((ind_value, "fill", least_digit))  # fill pour coloriage du rectangle
                
            new_list[:] = []
            
            for i in range(len(ind_memory)):  # on parcours ind_memory et on reclasse les éléments dans l'ordre dans lequel on les lie
                
                for j in range(len(ind_memory[i])):

                    new_list.append(self.List_height[ind_memory[i][j]])  # new_list reçoit toutes les valeurs dans le nouvel ordre
                    self.List_animation.append((ind_memory[i][j], "move", None))  # move permet d'animer le reclassement des rectangles

            self.List_height[:] = new_list  # la liste actuelle prend la valeur de cette liste de mémoire externe
            
            self.List_animation.append((0, -1))  #  ce tuple est spécial et il sert uniquement à repréparer le nouveau passage

            modulo = modulo * 10  # on s'interesse au prochain chiffre
            div = div * 10  # on s'interesse au prochain chiffre