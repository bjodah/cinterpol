import numpy as np
import cinterpol

def test_PieceWisePolyInterpol_call():
    pwpi=cinterpol.PieceWisePolyInterpol.mk_from_array(np.array([0.0,1.0]),np.array([[0.0],[1.0]]))
    assert pwpi(0.5) == 0.5
