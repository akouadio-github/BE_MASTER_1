import json
import numpy as np

class METRIQUE:
    def __init__(self, path_t, path_ocr) -> None:
        self._path_t    = path_t
        self._path_m    = path_ocr
    
    # extraction du fichier JSON en matrice
    def json_matx(self, path) -> np.matrix():
        with open (path,"r") as f :
            data        = json.load(f)
            data        = data["table"]["donnees"]
            mat      = [data[key]['textes'] for key in data.keys()]
            mat      = np.array(mat).T
            mat      = np.matrix(mat)
        return mat
    
    # matrice vers matrice d'adjacence
    def matx_adj(self, matrix):
        return np.where(matrix, 1, 0)
    
    # produit booléen entre deux matrice d'adjacence
    def mult_adj(self, path_t, path_m):
        m_t = self.json_matx(path_t)
        m_t = self.matx_adj(m_t)

        m_m = self.json_matx(path_m)
        m_m = self.matx_adj(m_m)
        return np.multiply(m_t,m_m)
    
    # fonction d'appartenance (formalisme pour rendre lisible nos fonctions)
    def appartient(self, x, L):
        return(x in L) 

    # fonction d'appartenance aux montants (débits ou crédits)
    def amount_in(self, x, L):
        return x in L[:,2] or x in L[:,3] 

    # metrique 1 (vérification des dimensions du tableau)
    def metrique_1(self, path_t, path_OCR):
        m_t = self.json_matx(path_t)
        m_OCR = self.json_matx(path_OCR)

        n_t = np.shape(m_t)
        n_OCR = np.shape(m_OCR)

        if n_OCR[1]*n_t[0]==0:
            return(False)
        if n_OCR[0]<2:
            return(False)
        if n_OCR[1]!=4:
            return(False)
        
        return(True)

    # metrique 2 (taux de données extraites)
    def metrique_2(self, path_t,path_m):
        m_t         = self.json_matx(path_t)
        m_t         = self.matx_adj(m_t)

        produit     = self.mult_adj(path_t, path_m)

        return np.sum(produit)/np.sum(m_t)
    
    # metrique 3 à 6 (taux de données extraites par champs)
    def metrique_3_6(self, path_t, path_m):
        m_t         = self.json_matx(path_t)
        m_t         = self.matx_adj(m_t)

        produit     = self.mult_adj(path_t, path_m)

        return np.sum(produit, axis=0)/np.sum(m_t, axis=0)

    # metrique 7 (taux de transactions extraites)
    def metrique_7(self, path_t, path_m):
        m_m = self.json_matx(path_m)

        with open (path_t,"r") as f :
            data = json.load(f)
        donnees = data["table"]["donnees"]

        Nb_transactions = 0
        
        for i in range(0,len(m_m)):
            bouton = False
            if self.appartient(m_m[i,0],donnees["dates"]["textes"])==True:
                if self.appartient(m_m [i,1],donnees["libelles"]["textes"])==True:
                    if ( (m_m[i,2]!=None and m_m[i,3]==None) or (m_m[i,2]==None and m_m[i,3]!=None) ) and self.appartient(m_m[i,2],donnees["debits"]["textes"])==True and self.appartient(m_m[i,3],donnees["credits"]["textes"])==True:
                        Nb_transactions = Nb_transactions + 1
                        bouton = True
                    if ( (m_m[i,2]!=None and m_m[i,3]==None) or (m_m[i,2]==None and m_m[i,3]!=None) ) and self.appartient(m_m[i,3],donnees["debits"]["textes"])==True and self.appartient(m_m[i,2],donnees["credits"]["textes"])==True and bouton==False:
                        Nb_transactions = Nb_transactions + 1
        return Nb_transactions/len(m_m)

    # metrique 8 (lib_score ou taux d'erreur basé sur la distance de Levenstein entre chaines de caractères)
    def lib_score(self, str_a, str_b, maxi):
        a = str_a
        l_a = len(a)
        b = str_b
        l_b = len(b)

        if (min((l_a,l_b))==0):
            return(max(l_a,l_b)/maxi)
        if (a[0]==b[0]):
            return(self.lib_score(a[1:],b[1:],maxi))
        return(1/maxi+min(self.lib_score(a[1:],b[1:],maxi),self.lib_score(a,b[1:],maxi),self.lib_score(a[1:],b,maxi)))

    # metrique 9 (taux de transactions correctement extraites)
    def metrique_9(self, path_t, path_m):
        m_t = self.json_matx(path_t)
        m_m = self.json_matx(path_m)

        correct_trans = 0

        for i in range(m_m.shape[0]):
            if (m_m[i,0] == m_t[i,0] and self.lib_score(m_m[i,1], m_t[i,1],max(len(m_m[i,1]),len(m_t[i,1]))) <= 0.10 and (self.amount_in(m_m[i,2], m_t) or self.amount_in(m_m[i,3], m_t))):
                correct_trans += 1
        return correct_trans / m_m.shape[0]
    
    # metrique 10 (moyenne des écarts de débits)
    def metrique_10(self, path_t,path_OCR) :
        errs        = []
        m_t         = self.json_matx(path_t)
        m_m         = self.json_matx(path_OCR)
        ecart       = 0
        ligne_bonne = 0

        for i in range(0, len(m_m)):
            try :
                ecart = ecart + abs(float(m_m[i,2]) - float(m_t[i,2]))
                ligne_bonne = ligne_bonne + 1
            except :
                x = "err"
                errs.append(x)
        if (ligne_bonne==0):
            return("on ne peut pas calculer la metrique ecart debit")
        return (ecart/ligne_bonne, errs)
    
    # metrique 11 (moyenne des écarts de crédits)
    def metrique_11(self, path_t,path_OCR) :
        errs        = []
        m_t         = self.json_matx(path_t)
        m_m         = self.json_matx(path_OCR)
        ecart       = 0
        ligne_bonne = 0

        for i in range(0, len(m_m)):
            try :
                ecart = ecart + abs(float(m_m[i,3]) - float(m_t[i,3]))
                ligne_bonne = ligne_bonne + 1
            except :
                x = "err"
                errs.append(x)
        if (ligne_bonne==0):
            return("on ne peut pas calculer la metrique ecart credit")
        return (ecart/ligne_bonne, errs)
    
    # metrique 12 (taux de débits/crédits permutés)
    def metrique_12(self, path_t, path_m):
        m_t = self.json_matx(path_t)
        m_m = self.json_matx(path_m)

        m_t = self.matx_adj(m_t)
        m_m = self.matx_adj(m_m)

        taux = sum(np.all(m_t[:, -2:] == 1 - m_m[:, -2:], axis=1)) / m_t.shape[0]

        return taux

