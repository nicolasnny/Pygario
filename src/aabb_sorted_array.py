from constant import MAP_DIMENTION, ROBOTS_ENTITY_PREF, PLAYER_ENTITY_NAME

class AABB_sorted_array(list):
    """Une methode qui prend la forme d'une liste de quadrants
    qui ont les objets du niveau, trie par leur plus petite position des cotes
    Args:
        list (_type_): une liste de liste d'objets
    """
    
    def __init__(self):
        super().__init__()
        
        self.xMilieu = (MAP_DIMENTION["abscisses"][0] + MAP_DIMENTION["abscisses"][1]) / 2 
        self.yMilieu = (MAP_DIMENTION["ordonnees"][0] + MAP_DIMENTION["ordonnees"][1]) / 2
        
        # creation des 4 quadrants
        self.append([]); self.append([]); self.append([]); self.append([])
        
    def insert(self, obj) -> None:
        """Insere un objet dans le AABB_sorted_array, en le triant selon sa
        plus petite position.
        Preconditions: 
            - les quadrants sont tries
            - obj.oldPos = obj.position
        Args:
            obj (ArgBall): L'objet a inserer
        """
        
        minY = obj.oldPos.y - obj.oldSize
        maxY = obj.oldPos.y + obj.oldSize
        
        # decision du/des quadrants d'insertion
        if obj.oldPos.x - obj.oldSize <= self.xMilieu:
            if minY <= self.yMilieu: self[0].insert(self.sInsert_index(obj, 0), obj)
            if maxY >= self.yMilieu: self[1].insert(self.sInsert_index(obj, 1), obj)
        if obj.oldPos.x + obj.oldSize >= self.xMilieu: 
            if minY <= self.yMilieu: self[2].insert(self.sInsert_index(obj, 2), obj)
            if maxY >= self.yMilieu: self[3].insert(self.sInsert_index(obj, 3), obj)

    def sInsert_index(self, obj, quadrantIndex) -> None:
        """Donne la position d'insertion d'un objet dans le quadrant,
        en le triant selon sa plus petite position. 
        L'insertion se fait grace a l'algorithme de Dichotomie
        Preconditions: 
            - les quadrants sont tries
            - obj.oldPos = obj.position
        
        Args:
            obj (ArgBall): l'objet a inserer
            quadrantIndex (int): l'index du quadrant dans lequel l'objet seras insere
        Returns:
            (int) l'index ou il faut l'inserer
        """
        quadrant = self[quadrantIndex]
        
        m = 0
        inf = 0
        sup = len(quadrant) - 1
        
        pos = obj.z - obj.size

        while sup >= inf:

            m = (inf + sup) // 2

            if pos == quadrant[m].oldPos.z - quadrant[m].oldSize:
                
                if obj == quadrant[m]: 
                    return m
                
                # si deux balles ont exactement la meme position z, alors la changer un tout petit peu pour eviter un crash
                obj.z += 0.001
                obj.nextPos.z += 0.001
                obj.oldPos.z += 0.001
                return self.sInsert_index(obj, quadrantIndex)
                
            if pos > quadrant[m].oldPos.z - quadrant[m].oldSize:
                inf = m + 1
            else:
                sup = m - 1
                
        return inf
        
    def remove(self, obj) -> None:
        """Supprime un objet dans le AABB_sorted_array, en le trouvant selon sa
        plus petite position.
        Preconditions: 
            - les quadrants sont tries
            - des qu'un objet est insere, on met a jour sa oldPos
        Args:
            obj (ArgBall): L'objet a supprimer
            quadrantIndex (int): l'index du quadrant dans lequel l'objet seras supprime
        """
                
        minY = obj.oldPos.y - obj.oldSize
        maxY = obj.oldPos.y + obj.oldSize
        
        # decision du/des quadrants de destruction
        if obj.oldPos.x - obj.oldSize <= self.xMilieu:
            if minY <= self.yMilieu: self.sRemove(obj, 0)
            if maxY >= self.yMilieu: self.sRemove(obj, 1)
            
        if obj.oldPos.x + obj.oldSize >= self.xMilieu: 
            if minY <= self.yMilieu: self.sRemove(obj, 2)
            if maxY >= self.yMilieu: self.sRemove(obj, 3)

    def sRemove(self, obj, quadrantIndex) -> None:
        """Supprime un objet dans le quadrant, en le trouvant selon sa
        plus petite position.
        La recherche de l'element se fait grace a l'algorithme de Dichotomie
        Preconditions: 
            - les quadrants sont tries
            - des qu'un objet est insere, on met a jour sa oldPos
        Args:
            obj (ArgBall): L'objet a supprimer
        """
        
        quadrant = self[quadrantIndex]
        
        m = 0
        inf = 0
        sup = len(quadrant) - 1

        pos = obj.oldPos.z - obj.oldSize

        while sup >= inf:

            m = (inf + sup) // 2

            if obj == quadrant[m]:
                quadrant.pop(m)
                return
            elif pos > quadrant[m].oldPos.z - quadrant[m].oldSize:
                inf = m + 1
            else:
                sup = m - 1
        
        #suppression
        m = (inf + sup) // 2
        
        if obj == quadrant[m]:
            quadrant.pop(m)
            
    def collisionHandler(self) -> int:
        """Detecte et gere toute les collisions,
        en utilisant l'algorithme AABB sweep and prune
        Precondition: 
            - les quadrants sont tries
            
        Returns:
            (int) : nomre de checks de collision (pour le debug)
        """
        collisionChecks = 0
        
        for quadrant in self:
            index = 0
            
            while index < len(quadrant): #parcourir tout les objets
                e = quadrant[index]
                index += 1

                if not (e.name.startswith(ROBOTS_ENTITY_PREF) or e.name.startswith(PLAYER_ENTITY_NAME)): continue # ne pas faire de checks de collision pour les gems

                maxZ = e.z + e.size

                i = index
                while i < len(quadrant) and maxZ >= quadrant[i].z - quadrant[i].size:
                    coll = quadrant[i]
                    i += 1

                    if e.collide(coll):
                        if e.size > coll.size:
                            e.eat(coll)
                            break
                        elif coll.size > e.size:
                            coll.eat(e)
                            break

                    # debug
                    collisionChecks += 1
        
        return collisionChecks


    def findNearestSmaller(self, obj):
        """trouve l'objet le plus proche de l'objet de départ,
        en prenant parti des caracteristique du AABB sorted array divisé en quadrants
        Args:
            obj (agarBall): l'objet duquel on cherche le voisin le plus proche
        Returns:
            (agarBall) : l'objet le plus proche de l'objet original
        """
        mini = 100000000000000000000
        miniObj = None
        quadrantsNonVisites = [0,1,2,3]

        minY = obj.oldPos.y - obj.oldSize
        maxY = obj.oldPos.y + obj.oldSize
        
        # detection du/des premiers plus proches dans les quadrants ou l'obj est present
        if obj.oldPos.x - obj.oldSize <= self.xMilieu:
            if minY <= self.yMilieu: mini, miniObj = self.nearestSmaller(obj, 0, mini, miniObj); quadrantsNonVisites.remove(0)
            if maxY >= self.yMilieu: mini, miniObj = self.nearestSmaller(obj, 1, mini, miniObj); quadrantsNonVisites.remove(1)
            
        if obj.oldPos.x + obj.oldSize >= self.xMilieu: 
            if minY <= self.yMilieu: mini, miniObj = self.nearestSmaller(obj, 2, mini, miniObj); quadrantsNonVisites.remove(2)
            if maxY >= self.yMilieu: mini, miniObj = self.nearestSmaller(obj, 3, mini, miniObj); quadrantsNonVisites.remove(3)

        #check dans les autres quadrants non visites, si ils peuvent contenir un plus proche
        for quadIndex in quadrantsNonVisites:
            # calcul de la distance entre le centre de la balle, et le quadrant
            if quadIndex < 2: minX, maxX = 0, self.xMilieu
            else: minX, maxX = self.xMilieu, 2*self.xMilieu

            if quadIndex%2 == 0: minY, maxY = 0, self.yMilieu
            else: minY, maxY = self.yMilieu, 2*self.yMilieu

            dx = max(minX - obj.x, 0, obj.x - maxX)
            dy = max(minY - obj.y, 0, obj.y - maxY)

            if (dx**2 + dy**2)**0.5 < mini:
                mini, miniObj = self.nearestSmaller(obj, quadIndex, mini, miniObj)

        return miniObj
        

    def nearestSmaller(self, obj, quadrantIndex, mini, miniObj):
        """Donne l'objet le plus proche dans un quadrant, et sa distance a l'objet initial,
        en prenant parti de mla forme de donnee d'un AABB
        Args:
            obj (agarBall): l'objet duquel on cherche le plus proche voisin
            quadrantIndex (int): l'index du quadrant de recherche
            mini (int): la distance minimale avec l'actuel plus proche voisin
            miniObj (agarBall): le plus proche voisin
        Returns:
            (tuple): le plus proche voisin et sa disance
        """

        quadrant = self[quadrantIndex]

        if len(quadrant) == 0: return mini, miniObj

        index = self.sInsert_index(obj, quadrantIndex)
        
        #sup
        i = index
        while i < len(quadrant) and quadrant[i] and quadrant[i].z - obj.z < mini:
            if quadrant[i] != obj and obj.dist(quadrant[i])**0.5 - quadrant[i].size/2 < mini \
                and obj.size > quadrant[i].size:
                mini = obj.dist(quadrant[i])**0.5 - quadrant[i].size/2
                miniObj = quadrant[i]
            i += 1
            
        #inf
        i = index
        
        while i >= 0 and i < len(quadrant) and quadrant[i] and obj.z - quadrant[i].z < mini:
            if quadrant[i] != obj and obj.dist(quadrant[i])**0.5 - quadrant[i].size/2 < mini \
                and obj.size > quadrant[i].size:
                mini = obj.dist(quadrant[i])**0.5 - quadrant[i].size/2 
                miniObj = quadrant[i]
            i -= 1

        return mini, miniObj

        
    def __str__(self) -> str:
        resultat = ""
        for i in range(4):
            resultat += "quadrant " + str(i) + " : " + str([e.name + " : pos: " + str(e.position) + " s: " + str(e.size)  for e in self[i]]) + "; \n"
        return resultat

def cle(obj):
    return obj.oldPos.z - obj.oldSize