# FAKE DATASETS (LIBELLE, CREDIT AND DEBITS)
# (DEBIT, CREDIT)
LIBELLES_PAIEMENT_PAR_CARTES = [
    "Paiement de la facture d'électricité",
    "Achat de fournitures de bureau",
    "Paiement de la facture de téléphone",
    "Virement reçu de Mme Martin",
    "Achat de matériel informatique",
    "Paiement de la facture d'eau",
    "Virement à M. Leblanc",
    "Achat de mobilier de bureau",
    "Paiement de la facture d'internet",
    "Virement reçu de Mme Petit",
    "Achat de logiciels",
    "Paiement de la facture de gaz",
    "Virement à M. Lefevre",
    "Achat de matériel de communication",
    "Paiement de la facture de chauffage",
    "Virement reçu de Mme Leroy",
    "Paiement de la facture d'électricité",
    "Virement à M. Dupont",
    "Achat de fournitures de bureau",
    "Paiement de la facture de téléphone",
    "Virement reçu de Mme Martin",
    "Achat de matériel informatique",
    "Paiement de la facture d'eau",
    "Virement à M. Leblanc",
    "Achat de mobilier de bureau",
    "Paiement de la facture d'internet",
    "Virement reçu de Mme Petit",
    "Achat de logiciels",
    "VIR de la ENEDIS",
    "VIR EXPR 010123",
    "LETT ADJ PRO",
    "VIR ESP",
    "COM PRLV SEPA IMP GROUPAMA",
    "CHQ. 8108224",
    "VIR ESP",
    "COM PRLV SEPA IMP EDF SEI",
    "FRAIS PT CHQ 8108224 SUR CTE IC",
    "VIR ESP",
    "REM CHQ 00001 CH 8821504",
    
]

MONTANTS_PAIEMENT_PAR_CARTES = [
    (100, 0),(200, 0),(300.99, 0),(400.0, 0),(0, 500.99),(600, 0),(700, 0),(8.99, 0),(900, 0),(10.0, 0),(0, 1100.9),(1200, 0),(1300, 0),(140.9, 0),(1500, 0),(16.0, 0),(0, 1700),(1800, 0),(1900, 0),(2000, 0),(2100, 0),(0, 2200),(2300, 0),(2400, 0),(2500, 0),(2600, 0),(2700, 0),(0, 2800),(2900, 0),(3000, 0),(0, 250),(12, 0),(0, 170),(20, 0),(0, 500),(0, 320),(20, 0), (27, 0), (0, 210), (0, 250)
]



##### VIREMENTS EMIS ET PRELEVEMENTS
LIBELLES_VIREMENTS_EMIS_PRELEVEMENTS = [
    'EMIS/PRLV SEPA LMDE MUTUELLE INTERIALE\nLIBELLE:Cotisations MULTI 8749\nREF.CLIENT:OPE-6537891-98-P-UR-84673\nID.CREANCIER:FR90.DJJEB\nREF.MANDAT: 67537392',
    'EMIS/PRLV - BOUTIQUE XYZ\nLIBELLE:Article de mode tendance\nREF.COMMANDE:CMD-20231101-001',
    'EMIS/PRLV SEPA FACTURE ELECTRICITE\nLIBELLE:Consommation d\'électricité\nREF.FACTURE:ELEC-20231101-001',
    'EMIS/VIR AMI\nLIBELLE:Remboursement prêt\nREF.AMI:JOHNDOE123',
    'EMIS/PLRV ABC\nLIBELLE:Courses alimentaires\nREF.TICKET:TM-20231101-001'
]
MONTANTS_VIREMENTS_EMIS_PRELEVEMENTS = [
    (17,0), (100,0), (156.8,0), (320,0), (17,0)
]


##### VIREMENTS RECU
LIBELLES_VIREMENTS_RECUS = [
    'VIR RECU INST MR LE VEN PAUL \n LIBELLE:Paylib CEnNRV7uFM DU 20 \n 23-10-29 A 19:05:15 C EST HDHYE \nREF.CLIENT:VIREMENT POUR LE REPAS DE FAMILLE',
    'VIREMENT RECU EMPLOYEUR\nLIBELLE:Salaire du mois de novembre\nREF.SALARIE:EMP12345',
    'VIREMENT RECU SARL UNIVEA \n LIBELLE:REMBT DG BEL AIR KOUAKOU \n REF.CLIENT:RBTDGBAPODU1023',
 ]
MONTANTS_VIREMENTS_RECUS = [
    (0,85.99),  (0, 550), (0, 150)
]

##### SERVICES ET FRAIS BANCAIRES
LIBELLES_SERVICES_FRAIS_BANCAIRES = [
    'FRAIS ASSURANCE MOYEN DE PAIEMENT',
    'FRAIS COTISATION OFFRE JEUNE'
]
MONTANTS_SERVICES_FRAIS_BANCAIRES = [
    (2.5, 0), (8, 0)
]