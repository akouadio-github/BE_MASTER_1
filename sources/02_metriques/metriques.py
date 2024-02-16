import json
import numpy as np

class METRIQUE:
    def __init__(self, path_t, path_ocr) -> None:
        self._path_t    = path_t
        self._path_m    = path_ocr

    # Utils
    def json_matx(self, path) -> np.matrix():
        with open (path,"r") as f :
            data        = json.load(f)
            data        = data["table"]["donnees"]
            mat      = [data[key]['textes'] for key in data.keys()]
            mat      = np.array(mat).T
            mat      = np.matrix(mat)
        return mat

    def matx_adj(self, matrix):
        return np.where(matrix, 1, 0)
    
    def mult_adj(self, path_t, path_m):
        m_t = self.json_matx(path_t)
        m_t = self.matx_adj(m_t)

        m_m = self.json_matx(path_m)
        m_m = self.matx_adj(m_m)
        return np.multiply(m_t,m_m)
    
    def lib_score(self, str_a, str_b):
        return 90
    
    def amount_in(self, x, L):
        return x in L[:,2] or x in L[:,3] 

    #### Metriques
    def metrique_1(self, path_t,path_m):
        """Taux de données extraites"""
        m_t         = self.json_matx(path_t)
        m_t         = self.json_matx(m_t)


        produit     = self.mult_adj(path_t, path_m)

        return np.sum(produit)/np.sum(m_t)
    
    def metrique_6(self, path_t, path_m):
        # TODO : Tester
        """Taux de transactions correctements extraites"""
        m_t         = self.json_matx(path_t)
        m_t         = self.json_matx(m_t)

        m_m = self.json_matx(path_m)
        m_m = self.matx_adj(m_m)
        correct_trans = 0

        for i in range(m_m.shape[0]):
            if (m_m[i,0] == m_t[i,0] and
                self.lib_score(m_m[i,1], m_t[i,1]) >= 90 and
                (self.amount_in(m_m[i,2], m_t) or self.amount_in(m_m[i,3], m_t))
                ):
                correct_trans += 1
        return correct_trans / m_m.shape[0]
    
    def metrique_2_4(self, path_t, path_m):
        """Taux de données extraites par champs"""
        m_t         = self.json_matx(path_t)
        m_t         = self.json_matx(m_t)

        produit     = self.mult_adj(path_t, path_m)

        return np.sum(produit, axis=0)/np.sum(m_t, axis=0)
    

    def metrique_9(self, path_t,path_OCR) :
        """ Ecart des montants débits crédits"""
        errs        = []
        m_t         = self.json_matx(path_t)
        m_m         = self.json_matx(path_OCR)
        ecart       = 0
    
        for i in range(0, len(m_m) - 1):
            try :
                ecart = abs(float(m_m[i,2]) - float(m_t[i,2]))
            except :
                x = "err"
                errs.append(x)
        return (np.mean(ecart), errs)
    
    def metrique_10(self, path_t, path_m):
        """Taux de crédit/débit permutés"""
        m_t = self.json_matx(path_t)
        m_m = self.json_matx(path_m)

        m_t = self.matx_adj(m_t)
        m_m = self.matx_adj(m_m)


        taux = np.sum(
            np.all(
                m_t[:, -2:] == 1 - m_m[:, -2:], axis=1)
        ) / m_t.shape[0]

        return taux
    




    