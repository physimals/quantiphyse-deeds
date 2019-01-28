"""
Quantiphyse - Plugin for DEEDS registration method

Copyright (c) 2013-2018 University of Oxford
"""
from .method import DeedsRegMethod
from .tests import DeedsProcessTest

QP_MANIFEST = {
    "reg-methods" : [DeedsRegMethod,],
    "process-tests" : [DeedsProcessTest,],
}
