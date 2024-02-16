import json
import random
from PIL import Image, ImageDraw, ImageFont

import os
import time

from rich.progress import track

# custom
from .load_data import get_fakedataset

class SG_GENERATOR_CLASS():
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
        super(SG_GENERATOR_CLASS, self).__init__()
        self._bank                  = bank
        self._output_dir            = output_dir
        self._TEMPLATE_PATH         = template_path
        self._TEMPLATE_OPTIONS      = template_options
        self._FONT_OPTIONS          = font_options
    
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

    ## TODO : continuer
    def get_data(self):
        """ Retourne les données 
        """
        SG_COMBINED_DATA = get_fakedataset(bank='SG')
        random.shuffle(SG_COMBINED_DATA)
        return SG_COMBINED_DATA
        
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
        FF_REGULAR              = ImageFont.truetype(self._FONT_OPTIONS['FF_REGULAR'], self._FONT_OPTIONS['F_SIZE'])

        # control variables
        c_transaction           = 0
        row_index_precedent     = None
        stop_multi_row          = True
        multi_rows_libelle_data = list([])

        for row_index, row_y in enumerate(range(self._TEMPLATE_OPTIONS['Y_MIN'] , self._TEMPLATE_OPTIONS['Y_MAX']  + 1, self._TEMPLATE_OPTIONS['Y_GAP']), start=1):
            for c_column in range(1,6):
                    box_height = 70
                    cols_coords = self._TEMPLATE_OPTIONS['TABLE_COLS_LIMITS'][f'col_{c_column}']
                    box_width = cols_coords[1] - cols_coords[0] - self._TEMPLATE_OPTIONS['OFFSET']

                    ### Masquer les elements du template
                    draw.rectangle(
                    [
                        (cols_coords[0] + self._TEMPLATE_OPTIONS['OFFSET'] ,  row_y - 1),
                        (cols_coords[0] + box_width, row_y + box_height)
                    ],
                    fill="white"
                )
                    if stop_multi_row or row_index == row_index_precedent:   
                        # Données colonnes
                        fetched_data = DATA[c_transaction]
                        if c_column == 1:
                            ANNOT_ARGS['lib_cre_deb'].append(fetched_data)
                        if c_column == 1:
                            data = f'{row_index:02d}/{MONTH_BASE:02d}'
                        elif c_column == 2:
                            data = f'{row_index:02d}/{MONTH_BASE:02d}/{YEAR_BASE}'
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
                        else :
                            data =  '{:,.2f}'.format(fetched_data[2]).replace(',', ' ').replace('.', ',') if fetched_data[2] != 0 else ''
                    else:
                        if c_column == 3:
                            data = multi_rows_libelle_data.pop(0)
                        else : 
                            data = ''

                    # Coords
                    if c_column == 1 or c_column == 2:
                        text_x = cols_coords[0] + self._TEMPLATE_OPTIONS['OFFSET'] + (box_width - draw.textsize(data, FF_REGULAR)[0]) // 2 # centrer
                    elif c_column == 3:
                        # Start the text from the left in the 2nd column
                        text_x = cols_coords[0] + self._TEMPLATE_OPTIONS['OFFSET'] + 10
                    else:
                        # justifier à droite les colonnes de montants
                        text_x = cols_coords[0] + box_width - draw.textsize(data, FF_REGULAR)[0] - 17
                    
                    if row_index <= self._TEMPLATE_OPTIONS['MAX_LEN_TRANSAC']:
                        draw.text((text_x, row_y + 1), data , fill="black", font=FF_REGULAR)

            stop_multi_row = True if len(multi_rows_libelle_data) == 0 else False
            
            if stop_multi_row:
                c_transaction = c_transaction + 1
 
        BASE_IMAGE.save('{}/images/{}.png'.format(self._output_dir, img_name))

        ### generate annotation TODO
        ANNOT_ARGS['image_name'] = img_name
        ANNOT_ARGS['output_dir'] = self._output_dir + '/annotations'
        self.build_annotation(ANNOT_ARGS)

       
    def generate_many(self, n=10):
        for i in track(range(1, n+1), description='Processing...'):
            self.generate_one_image(img_name='sg_image_{}'.format(i))
        
