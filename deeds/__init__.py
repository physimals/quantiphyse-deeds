from PySide import QtGui

from quantiphyse.gui.widgets import Citation
from quantiphyse.utils import debug
from quantiphyse.utils.exceptions import QpException

from .deeds_wrapper import deedsReg

CITE_TITLE = "MIND: Modality Independent Neighbourhood Descriptor for Multi-modal Deformable Registration"
CITE_AUTHOR = "MP Heinrich, M Jenkinson, M Bhushan, T Matin, F Gleeson, M Brady, JA Schnabel"
CITE_JOURNAL = "Medical Image Analysis. vol. 16(7) 2012, pp. 1423-1435"

class DeedsRegMethod:
    def __init__(self):
        self.name = "deeds"
        self.options_layout = None

    def reg(self, regdata, refdata, warp_rois, options):
        return deedsReg(regdata, refdata, warp_rois, **options)

    def interface(self):
        if self.options_layout is None:
            vbox = QtGui.QVBoxLayout()

            cite = Citation(CITE_TITLE, CITE_AUTHOR, CITE_JOURNAL)
            vbox.addWidget(cite)

            grid = QtGui.QGridLayout()

            grid.addWidget(QtGui.QLabel("Regularisation parameter (alpha)"), 0, 0)
            self.alpha = QtGui.QDoubleSpinBox()
            self.alpha.setValue(2.0)
            self.alpha.setMinimum(0)
            self.alpha.setMaximum(10.0)
            self.alpha.setSingleStep(0.1)
            grid.addWidget(self.alpha, 0, 1)

            grid.addWidget(QtGui.QLabel("Num random samples per node"), 1, 0)
            self.randsamp = QtGui.QSpinBox()
            self.randsamp.setValue(50)
            self.randsamp.setMinimum(1)
            self.randsamp.setMaximum(100)
            grid.addWidget(self.randsamp, 1, 1)

            grid.addWidget(QtGui.QLabel("Number of levels"), 2, 0)
            self.levels = QtGui.QSpinBox()
            self.levels.setValue(5)
            self.levels.setMinimum(1)
            self.levels.setMaximum(10)
            grid.addWidget(self.levels, 2, 1)

            #grid.addWidget(QtGui.QLabel("Grid spacing for each level"), 3, 0)
            #self.spacing = QtGui.QLineEdit()
            #grid.addWidget(self.spacing, 3, 1)

            #grid.addWidget(QtGui.QLabel("Search radius for each level"),4, 0)
            #self.radius = QtGui.QLineEdit()
            #grid.addWidget(self.radius,4, 1)

            #grid.addWidget(QtGui.QLabel("Quantisation of search step size for each level"),5, 0)
            #self.radius = QtGui.QLineEdit()
            #grid.addWidget(self.radius,5, 1)

            #grid.addWidget(QtGui.QLabel("Use symmetric approach"),6, 0)
            #self.symm = QtGui.QCheckBox()
            #self.symm.setChecked(True)
            #grid.addWidget(self.symm,6, 1)

            grid.setColumnStretch(2, 1)
            vbox.addLayout(grid)

            self.options_layout = vbox
        return self.options_layout

    def options(self):
        self.interface()
        return {"alpha" : self.alpha.value(),
                "randsamp" : self.randsamp.value(),
                "levels" : self.levels.value()}


QP_MANIFEST = {"reg-methods" : [DeedsRegMethod,]}