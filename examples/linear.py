import numpy as np
import cInterpol

def test_PieceWisePolyInterpol_call():
    pwpi=cInterpol.PieceWisePolyInterpol.mk_from_array(np.array([0.0,1.0,2.0]),np.array([[0.0],[1.0],[2.0]]))
    assert pwpi(0.5) == 0.5
    assert pwpi(1.5) == 1.5
