import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from rusta_scraper.external_data_loader.pim_api import load_pim_data
from rusta_scraper.external_data_loader.opti_api import load_opti_missing_prices, load_prices

load_pim_data()
load_opti_missing_prices()
load_prices()