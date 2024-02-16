from utils.db import (
    LIBELLES_PAIEMENT_PAR_CARTES, 
    MONTANTS_PAIEMENT_PAR_CARTES,
    LIBELLES_VIREMENTS_EMIS_PRELEVEMENTS,
    MONTANTS_VIREMENTS_EMIS_PRELEVEMENTS,
    LIBELLES_VIREMENTS_RECUS,
    MONTANTS_VIREMENTS_RECUS,
    LIBELLES_SERVICES_FRAIS_BANCAIRES,
    MONTANTS_SERVICES_FRAIS_BANCAIRES
)

def get_fakedataset(bank='LCL'):
    if bank in ['LCL', 'SG']:
        COMBINED_DATA = list(zip(LIBELLES_PAIEMENT_PAR_CARTES, MONTANTS_PAIEMENT_PAR_CARTES))
        COMBINED_DATA += list(zip(LIBELLES_VIREMENTS_EMIS_PRELEVEMENTS, MONTANTS_VIREMENTS_EMIS_PRELEVEMENTS))
        COMBINED_DATA += list(zip(LIBELLES_VIREMENTS_RECUS, MONTANTS_VIREMENTS_RECUS))
        COMBINED_DATA += list(zip(LIBELLES_SERVICES_FRAIS_BANCAIRES, MONTANTS_SERVICES_FRAIS_BANCAIRES))
        
        COMBINED_DATA = [(x,) + y for x, y in COMBINED_DATA]
        return COMBINED_DATA
    elif bank == 'HSBC':
        COMBINED_DATA = [
            ('CB SHHAO PU SHENG DA SHA 01/09\nCBN 4971 60XX XXXX 3631\n64,00 CNY COMMISSION 0,23\n1 EUR=7,872 CNY',8.36,0),
            ('VIREMENT SEPA RECU - 2200-01135 05.09\nSEPTEMBRE 2023\nMALABOUS CELINE\nMALABOUS CELINE ',0, 200.00),
            ('COTISHSBC HEXAGONE ZPMA 75728 05.09 =X 418\n01/08/2023 AU 31/08/2023\nCOM. TAX. EUR 4,18', 4.18, 0),
            ('PRLV SEPARECURCUR YDI2 09874 05.09\nPAGPO1104N3LOK\nFR35ZZZ418323\nBOUYGUES TELECOM BOUYGUES TELECOM\nBT1150650WE94\nBox',32.64,0),
            ('PRLV SEPARECURCUR YDI6 42009 05.09 \n65825872325\nFR47ZZZ568651\nLBP IARD\nOOIARDNM22173637\nXXX00065825872325 NM22173637', 12.04, 0),
            ('CBCARREFOURMARKET — 06/09 07.09\nBREST 29\nCBN 4971 60XX XXXX 3631',2.55,0),
            ('PRLV SEPARECURCUR YDIO 01251 07.09 \n1029236192545\nLU96ZZZ0000000000000000058\nPayPal Europe S.a.r. et Cie S.C.A\n5D2J224Z44U6S', 19.99, 0)
        ]
        return COMBINED_DATA
    else :
        COMBINED_DATA = {
                'VIREMENTS RECUS' : list((x,) + y for x, y in zip(LIBELLES_VIREMENTS_RECUS, MONTANTS_VIREMENTS_RECUS)),
                'VIREMENTS EMIS ET PRELEVEMENTS' : list((x,) + y for x, y in zip(LIBELLES_VIREMENTS_EMIS_PRELEVEMENTS, MONTANTS_VIREMENTS_EMIS_PRELEVEMENTS)),
                'PAIEMENTS PAR CARTES' :  list((x,) + y for x, y in zip(LIBELLES_PAIEMENT_PAR_CARTES, MONTANTS_PAIEMENT_PAR_CARTES)),
                'SERVICES ET FRAIS BANCAIRES' : list((x,) + y for x, y in zip(LIBELLES_SERVICES_FRAIS_BANCAIRES, MONTANTS_SERVICES_FRAIS_BANCAIRES)),
        }
        return COMBINED_DATA