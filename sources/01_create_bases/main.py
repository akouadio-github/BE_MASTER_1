import os
import json
import argparse

from rich.pretty import pprint # progress bar

from utils.CMB_bank import CMB_GENERATOR_CLASS
from utils.HSBC_bank import HSBC_GENERATOR_CLASS
from utils.LCL_bank import LCL_GENERATOR_CLASS
from utils.SG_bank import SG_GENERATOR_CLASS

def get_configs(bank='cmb'):
    with open('./configs/config_{}.json'.format(bank)) as config_data:
        config = json.load(config_data)
    return config

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Générateur de relevés de comptes')
    parser.add_argument('-n', '--nombre', help='Nombre d\'images. Default n=1' )
    args = parser.parse_args()


    for index, bank in enumerate(['LCL', 'HSBC', 'CMB', 'SG'], start=1):
        pprint(">>>>>> Step {} over {} : {} BANK".format(index, 3, bank))

        config = get_configs(bank=bank)
        if not os.path.exists('{}/{}'.format(config['OUTPUT_DIR'], bank)):
            os.makedirs('{}/{}/images/'.format(config['OUTPUT_DIR'], bank))
            os.makedirs('{}/{}/annotations/'.format(config['OUTPUT_DIR'], bank))
        
        settings = [
            config['BANK'], # bank
            '{}/{}'.format(config['OUTPUT_DIR'], bank), # output_dir=
            config['IMAGE_PATH'],  # template_path = 
            config['TEMPLATE_OPTIONS'],  # template_options = 
            config['FONT_OPTIONS'] # font_options = 
        ]
        if bank == 'LCL':
            GENERATOR = LCL_GENERATOR_CLASS(*settings)
        elif bank == 'HSBC':
            GENERATOR = HSBC_GENERATOR_CLASS(*settings)
        elif bank == 'SG':
            GENERATOR = SG_GENERATOR_CLASS(*settings)
        else : # CMB
            GENERATOR = CMB_GENERATOR_CLASS(*settings)

        if args.nombre:
            nb = int(args.nombre)
        else:
            nb = 1
        if bank != 'HSBC':
            continue
        GENERATOR.generate_many(n=nb)
    pprint(">>>>>> Completed ...")
