#from allantools.dataset import Dataset
#from allantools import noise
import allantools as at
import pytest
import numpy as np

"""
    unit-tests for allantools.Noise() Kasdin & Walter
    noise-generator
"""

@pytest.fixture
def noisegen():
    return at.Noise()

@pytest.mark.parametrize("n", range(2,20))
def test_timeseries_length(noisegen, n):
    """
        check that the time-series is of correct length
    """
    nr = pow(2,n)
    noisegen.set_input(nr=nr)
    noisegen.generateNoise()
    print( nr )
    print( len( noisegen.time_series ) )
    assert( len( noisegen.time_series ) == nr )



@pytest.mark.parametrize("b",[0, -1, -2, -3, -4])
@pytest.mark.parametrize("tau",[1,2,3,4,5, 20, 30])
@pytest.mark.parametrize("qd",[3e-15, 5e-10, 6e-9, ]) # 7e-6 2e-20
def test_adev(noisegen, b, tau, qd):
    """
        check that time-series has the ADEV that we expect
    """
    noisegen.set_input(nr=pow(2,16), qd=qd , b=b)
    noisegen.generateNoise()
    (taus,devs,errs,ns)=at.adev( noisegen.time_series, taus=[tau], rate=1.0 )
    
    adev_calculated = devs[0]
    adev_predicted = noisegen.adev(tau0=1.0, tau=tau)
    #print( taus,devs )
    print( b, tau, qd, adev_calculated, adev_predicted, adev_calculated/adev_predicted )
    assert np.isclose( adev_calculated, adev_predicted, rtol=3e-1, atol=0)
    # NOTE high relative tolarence here !!

@pytest.mark.xfail
@pytest.mark.parametrize("b",[-2, -3, -4] )
@pytest.mark.parametrize("tau",[1, 3])
@pytest.mark.parametrize("qd",[6e-9, 7e-6])
def test_mdev_failing(noisegen, b, tau, qd):
    test_mdev(noisegen, b, tau, qd)
    
@pytest.mark.parametrize("b",[0, -1,  ])
@pytest.mark.parametrize("tau",[2,4,5, 20, 30])
@pytest.mark.parametrize("qd",[2e-20])
def test_mdev(noisegen, b, tau, qd):
    """
        check that time-series has the MDEV that we expect
    """
    noisegen.set_input(nr=pow(2,16), qd=qd , b=b)
    noisegen.generateNoise()
    (taus,devs,errs,ns)=at.mdev( noisegen.time_series, taus=[tau], rate=1.0 )
    
    mdev_calculated = devs[0]
    mdev_predicted = noisegen.mdev(tau0=1.0, tau=tau)
    #print( taus,devs )
    print( b, tau, qd, mdev_calculated, mdev_predicted, mdev_calculated/mdev_predicted )
    assert np.isclose( mdev_calculated, mdev_predicted, rtol=2e-1, atol=0)
    # NOTE high relative tolarence here !!
            
if __name__ == "__main__":
    #test_timeseries_length( at.Noise() )
    #test_adev( at.Noise() )
    #test_mdev( at.Noise() )
    pytest.main()
