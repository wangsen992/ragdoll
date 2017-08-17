"""
Ragdoll initialisation.
"""

from .db import *
from .nutrient import *
from .component import *
from .loader import *
from .dictionary import *
from .human import *
from .req import *
# from .plots import *


__version__=0.1

mongo = MongoDB(host='47.93.246.201', 
				port=27017, 
				database='eatech', 
				user='harry', 
				password='password',
				collections=['FM'])