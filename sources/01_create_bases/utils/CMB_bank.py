import json
import random
from PIL import Image, ImageDraw, ImageFont

import os
import time

from rich.progress import track

# custom
from .load_data import get_fakedataset

class CMB_GENERATOR_CLASS():
    """
    Description:
    """
    def __init__(self, 
                 bank =str(),
                 output_dir=str(),
                 template_path=str(), 
                 template_options=dict(), 
                 font_options=dict()
                 ):
        super(CMB_GENERATOR_CLASS, self).__init__()
        self._bank                  = bank
        self._output_dir            = output_dir
        self._TEMPLATE_PATH         = template_path
        self._TEMPLATE_OPTIONS      = template_options
        self._FONT_OPTIONS          = font_options
        self.__TRANSACTION_TYPES    = [(0, 'VIREMENTS RECUS'), 
                                        (1, 'VIREMENTS EMIS ET PRELEVEMENTS'), 
                                        (2, 'PAIEMENTS PAR CARTES'), 
                                        (3, 'SERVICES ET FRAIS BANCAIRES')]

    def build_annotation(self, args):
        # dates must be added to DATA
        json_annot = dict()
        json_annot['image_id'] = args['image_name'] + '.png'
        json_annot['width'] = 100
        json_annot['height'] = 200
        json_annot['table'] = dict()
        json_annot['table']['donnees'] = dict()
        json_annot['table']['donnees']['dates'] = dict()
        json_annot['table']['donnees']['libelles'] = dict()
        json_annot['table']['donnees']['debits'] = dict()
        json_annot['table']['donnees']['credits'] = dict()

        # json_annot['table']['donnees']['dates']['transactions_y'] = []
        json_annot['table']['donnees']['dates']['textes'] = args['dates']
        json_annot['table']['donnees']['libelles']['textes'] =  [elt[0] for elt in args['lib_cre_deb']]
        json_annot['table']['donnees']['credits']['textes'] = [elt[1] if elt[1] != 0 else None for elt in args['lib_cre_deb']]
        json_annot['table']['donnees']['debits']['textes'] = [elt[2] if elt[2] != 0 else None for elt in args['lib_cre_deb']]

        with open(f"{args['output_dir']}/{args['image_name']}.json", "w") as outfile:
            json.dump(json_annot, outfile)

    
    def get_data(self):
        """ Retourne les données 
        """

        FAKE_DATASET                = get_fakedataset(bank=self._bank)
        CMB_TRANSACTION_TYPES       = random.sample( self.__TRANSACTION_TYPES,  k = random.randint(1, 4))
        CMB_TRANSACTION_TYPES       = sorted(CMB_TRANSACTION_TYPES, key=lambda x: x[0])
        OUTPUT_                     = []

        for _, libelle_groupe in CMB_TRANSACTION_TYPES:
            TMP_                    = FAKE_DATASET[libelle_groupe]
            max_ = abs(self._TEMPLATE_OPTIONS['MAX_LEN_TRANSAC'] - len(OUTPUT_))
            n                       = random.randint(1, max_) if max_ != 0 else None
            if not n : continue
            random.shuffle(TMP_)
            OUTPUT_.append(libelle_groupe)
            OUTPUT_.extend(random.sample(TMP_, min(n, len(TMP_))))

        return OUTPUT_
        
    def generate_one_image(self, img_name):
        BASE_IMAGE              = Image.open(self._TEMPLATE_PATH)
        draw                    = ImageDraw.Draw(BASE_IMAGE)
    
        YEAR_BASE               = random.randint(18,23)
        MONTH_BASE              = random.randint(1,12) 
        DATA                    = self.get_data()

        ANNOT_ARGS              = {
                                    'image_name': None,
                                    'dates': [],
                                    'lib_cre_deb': []
                                }

        # Font
        FF_REGULAR              = ImageFont.truetype(self._FONT_OPTIONS['FF_REGULAR'], 23)
        FF_BOLD                 = ImageFont.truetype(self._FONT_OPTIONS['FF_BOLD'],23) 

        # control variables
        c_color_index           = 0
        c_transaction           = 0
        row_index_precedent     = None
        stop_multi_row          = True
        skip_next_row           = False
        multi_rows_libelle_data = list([])

        ### DELETE TRANSACTIONS
        for row_y in range(self._TEMPLATE_OPTIONS['Y_MIN'] , self._TEMPLATE_OPTIONS['Y_MAX']  + 1, self._TEMPLATE_OPTIONS['Y_GAP']) :
            draw.rectangle(
                        [
                            (127 + self._TEMPLATE_OPTIONS['OFFSET'] ,  row_y - 1), # 127 : X_min_du_template 1545 : X_max_du_template
                            (1545, row_y + self._TEMPLATE_OPTIONS['BOX_HEIGHT'])
        ],fill="white")


        for row_index, row_y in enumerate(range(self._TEMPLATE_OPTIONS['Y_MIN'] , self._TEMPLATE_OPTIONS['Y_MAX']  + 1, self._TEMPLATE_OPTIONS['Y_GAP'])) :
            row_color       = self._TEMPLATE_OPTIONS['ROWS_COLORS'][c_color_index % len(self._TEMPLATE_OPTIONS['ROWS_COLORS'] )] # choisir la couleur de la transaction

            if skip_next_row  and stop_multi_row:
                skip_next_row = False
                continue
            # PREMIER TITRE #TODO : A améliorer
            #### TODO : A Revoir
            if c_transaction >= len(DATA):
                continue
            #### TODO : A Revoir
            if type(DATA[c_transaction]) == type(''):
                if  row_y + self._TEMPLATE_OPTIONS['Y_GAP'] > self._TEMPLATE_OPTIONS['Y_MAX']: # On est a la dernière ligne ne pas ecrit de titre
                    continue
                for c_column in range(1,3 + 1):
                    cols_coords = self._TEMPLATE_OPTIONS['HEADER_COLS_LIMITS'][f'col_{c_column}']
                    box_width = cols_coords[1] - cols_coords[0]
                    if c_column == 1:
                        text_x = cols_coords[0]
                        draw.text((text_x, row_y + self._TEMPLATE_OPTIONS['OFFSET']), str(DATA[c_transaction]) , fill="black", font=FF_BOLD)
                    elif c_column == 3:
                        text_x = cols_coords[0] + box_width - draw.textsize(str(random.randint(750, 1500)), FF_REGULAR)[0] - 21*self._TEMPLATE_OPTIONS['OFFSET']
                        draw.text((text_x, row_y + self._TEMPLATE_OPTIONS['OFFSET']), str(random.randint(750, 1500)) + ' €' , fill="black", font=FF_REGULAR)
                    else :
                        text_x = cols_coords[0]
                        draw.text((text_x, row_y + self._TEMPLATE_OPTIONS['OFFSET']), str('Sous-total : ') , fill="black", font=FF_REGULAR)
                c_transaction  = min(c_transaction + 1, len(DATA) - 1)
                c_color_index = 0
                continue
            # Fin PREMIER TITRE

            # Si la prochaine transaction est un text alors (il s'agit d'une ligne) : ## C'était une solution technique
            next_transaction = min(c_transaction + 1, len(DATA) - 1)
            if type(DATA[next_transaction]) == type(''):
                skip_next_row = True
            # Fin : Si la prochaine t

            for c_column in range(1,6):
                cols_coords = self._TEMPLATE_OPTIONS['TABLE_COLS_LIMITS'][f'col_{c_column}']
                box_width = cols_coords[1] - cols_coords[0] - self._TEMPLATE_OPTIONS['OFFSET']
                            ### Masquer les elements du template
                
                # couleur du rectangle
                draw.rectangle(
                    [
                        (cols_coords[0] + self._TEMPLATE_OPTIONS['OFFSET'] ,  row_y - 1),
                        (cols_coords[0] + box_width, row_y + self._TEMPLATE_OPTIONS['BOX_HEIGHT'])
                    ],
                    fill=row_color
                )

                fetched_data = DATA[c_transaction]
                if c_column == 1:
                    ANNOT_ARGS['lib_cre_deb'].append(fetched_data)
                # print(fetched_data)
                # Recuperer les données de la  colonnes
                if stop_multi_row or row_index == row_index_precedent:   
                            # Données colonnes
                            if c_column == 1:
                                data = f'{c_transaction:02d}/{MONTH_BASE:02d}'
                            elif c_column == 2:
                                data = f'{c_transaction:02d}/{MONTH_BASE:02d}/20{YEAR_BASE}'
                                ANNOT_ARGS['dates'].append(data)
                            elif c_column == 3:
                                if len(fetched_data[0].split('\n')) == 1:
                                    data = f'{fetched_data[0].upper()}'
                                else :
                                    multi_rows_libelle_data = fetched_data[0].split('\n')
                                    stop_multi_row = False
                                    data = str(multi_rows_libelle_data.pop(0))
                                    row_index_precedent = row_index
                            elif c_column == 4:
                                data = '{:,.2f}'.format(fetched_data[1]).replace(',', ' ').replace('.', ',') if fetched_data[1] != 0 else ''
                                # data = 'COl4'
                            else :
                                # data = 'COl5'
                                data =  '{:,.2f}'.format(fetched_data[2]).replace(',', ' ').replace('.', ',') if fetched_data[2] != 0 else ''
                else:
                        if c_column == 3:
                            # print(cols_coords[0])
                            # print(multi_rows_libelle_data)
                            data = multi_rows_libelle_data.pop(0)
                        else : 
                            data = ''
                
                # Coords
                if c_column == 1 or c_column == 2:
                    text_x = cols_coords[0] + self._TEMPLATE_OPTIONS['OFFSET'] + (box_width - draw.textsize(data, FF_REGULAR)[0]) // 2 # centrer
                elif c_column == 3:
                    # Justifer à gauche
                    text_x = cols_coords[0] + self._TEMPLATE_OPTIONS['OFFSET']
                else:
                    # justifier à droite les colonnes de montants
                    text_x = cols_coords[0] + box_width - draw.textsize(data, FF_REGULAR)[0] - 10
                    
                if c_transaction <= self._TEMPLATE_OPTIONS['MAX_LEN_TRANSAC']:
                    draw.text((text_x, row_y + self._TEMPLATE_OPTIONS['OFFSET']), data , fill="black", font=FF_REGULAR)
                    if c_column in [4,5]:
                        # Créer la ligne vertical relie deux points (x_1, y_1) et  (x_2, y_2)
                        draw.line([(cols_coords[0] - 10, row_y), (cols_coords[0] - 10, row_y + self._TEMPLATE_OPTIONS['BOX_HEIGHT'] + 1)], fill='black', width=3)
            
            # Arreter le multirow si il y a plus de données dans multiroxs_libelle_data
            stop_multi_row = True if len(multi_rows_libelle_data) == 0 else False

            if stop_multi_row:
                c_transaction = c_transaction + 1
            c_color_index = c_color_index + 1
            
        BASE_IMAGE.save('{}/images/{}.png'.format(self._output_dir, img_name))
        ### generate annotation TODO
        ANNOT_ARGS['image_name'] = img_name
        ANNOT_ARGS['output_dir'] = self._output_dir + '/annotations'
        self.build_annotation(ANNOT_ARGS)

            ### generate annotation TODO
            #for (i)
       
    def generate_many(self, n=10):
        for i in track(range(1, n+1), description='Processing...'):
            self.generate_one_image(img_name='cmb_image_{}'.format(i))