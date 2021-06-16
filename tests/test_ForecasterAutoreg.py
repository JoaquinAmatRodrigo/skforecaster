# test_ForecasterAutoreg.py 
import pytest
from pytest import approx
import numpy as np
import pandas as pd
from skforecast import __version__
from skforecast.ForecasterAutoreg import ForecasterAutoreg
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor


# Test initializations
#-------------------------------------------------------------------------------
def test_init_lags_attribute_when_integer_is_passed():
   
    forecaster = ForecasterAutoreg(LinearRegression(), lags=10)
    assert (forecaster.lags == np.arange(10) + 1).all()
    
def test_init_lags_attribute_when_list_is_passed():
   
    forecaster = ForecasterAutoreg(LinearRegression(), lags=[1, 2, 3])
    assert (forecaster.lags == np.array([1, 2, 3])).all()
    
def test_init_lags_attribute_when_range_is_passed():
   
    forecaster = ForecasterAutoreg(LinearRegression(), lags=range(1, 4))
    assert (forecaster.lags == np.array(range(1, 4))).all()
    
def test_init_lags_attribute_when_numpy_arange_is_passed():
   
    forecaster = ForecasterAutoreg(LinearRegression(), lags=np.arange(1, 10))
    assert (forecaster.lags == np.arange(1, 10)).all()
    

def test_init_exception_when_lags_argument_is_int_less_than_1():
    
    with pytest.raises(Exception):
        ForecasterAutoreg(LinearRegression(), lags=-10)
        
def test_init_exception_when_lags_argument_is_range_starting_at_zero():
    
    with pytest.raises(Exception):
        ForecasterAutoreg(LinearRegression(), lags=range(0, 4))
            
        
        
def test_init_exception_when_lags_argument_is_numpy_arange_starting_at_zero():
    
    with pytest.raises(Exception):
        ForecasterAutoreg(LinearRegression(), lags=np.arange(0, 4))
        
        
def test_init_exception_when_lags_argument_is_list_starting_at_zero():
    
    with pytest.raises(Exception):
        ForecasterAutoreg(LinearRegression(), lags=[0, 1, 2])
        
        
# Test method create_lags()
#-------------------------------------------------------------------------------
def test_create_lags_when_lags_is_3_and_y_is_numpy_arange_10():
    '''
    Check matrix of lags is created properly
    '''
    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    results = forecaster.create_lags(y=np.arange(10))
    expected = (np.array([[2., 1., 0.],
                         [3., 2., 1.],
                         [4., 3., 2.],
                         [5., 4., 3.],
                         [6., 5., 4.],
                         [7., 6., 5.],
                         [8., 7., 6.]]),
               np.array([3., 4., 5., 6., 7., 8., 9.]))

    assert (results[0] == expected[0]).all()
    assert (results[1] == expected[1]).all()
    


def test_create_lags_exception_when_len_of_y_is_less_than_maximum_lag():
   
    forecaster = ForecasterAutoreg(LinearRegression(), lags=10)
    with pytest.raises(Exception):
        forecaster.create_lags(y=np.arange(5))
        
        
# Test method fit()
#-------------------------------------------------------------------------------
def test_fit_exception_when_y_and_exog_have_different_lenght():

    forecaster = ForecasterAutoreg(LinearRegression(), lags=5)
    with pytest.raises(Exception):
        forecaster.fit(y=np.arange(50), exog=np.arange(10))
    with pytest.raises(Exception):
        forecaster.fit(y=np.arange(50), exog=pd.Series(np.arange(10)))


def test_last_window_stored_when_fit_forecaster():
    
    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    forecaster.fit(y=np.arange(50))
    assert (forecaster.last_window == np.array([47, 48, 49])).all()
    
    
def test_in_sample_residuals_stored_when_fit_forecaster():
    
    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    forecaster.fit(y=np.arange(5))
    assert (forecaster.in_sample_residuals == np.array([0., 0.])).all()


# Test method predict()
#-------------------------------------------------------------------------------
def test_predict_exception_when_steps_lower_than_1():

    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    forecaster.fit(y=np.arange(50))
    with pytest.raises(Exception):
        forecaster.predict(steps=0)

def test_predict_exception_when_forecaster_fited_without_exog_and_exog_passed_when_predict():

    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    forecaster.fit(y=np.arange(50))
    with pytest.raises(Exception):
        forecaster.predict(steps=10, exog=np.arange(10))


def test_predict_exception_when_forecaster_fited_with_exog_but_not_exog_passed_when_predict():

    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    forecaster.fit(y=np.arange(50), exog=np.arange(50))
    with pytest.raises(Exception):
        forecaster.predict(steps=10)
        
        
def test_predict_exception_when_exog_lenght_is_less_than_steps():

    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    forecaster.fit(y=np.arange(50), exog=np.arange(50))
    with pytest.raises(Exception):
        forecaster.predict(steps=10, exog=np.arange(5))
        
        
def test_predict_exception_when_last_window_argument_is_not_numpy_array_or_pandas_series():

    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    forecaster.fit(y=np.arange(50))
    with pytest.raises(Exception):
        forecaster.predict(steps=10, last_window=[1,2,3])


def test_predict_exception_when_last_window_lenght_is_less_than_maximum_lag():

    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    forecaster.fit(y=np.arange(50))
    with pytest.raises(Exception):
        forecaster.predict(steps=10, last_window=pd.Series([1, 2]))
        

def test_predict_output_when_regresor_is_LinearRegression_lags_is_3_ytrain_is_numpy_arange_50_and_steps_is_5():

    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    forecaster.fit(y=np.arange(50))
    predictions = forecaster.predict(steps=5)
    expected = np.array([50., 51., 52., 53., 54.])
    assert predictions == approx(expected)
    
    
# Test method _check_y()
#-------------------------------------------------------------------------------
def test_check_y_exception_when_y_is_int():
    
    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    with pytest.raises(Exception):
        forecaster._check_y(y=10)
        
def test_check_y_exception_when_y_is_list():
    
    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    with pytest.raises(Exception):
        forecaster._check_y(y=[1, 2, 3])
        
        
def test_check_y_exception_when_y_is_numpy_array_with_more_than_one_dimension():
    
    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    with pytest.raises(Exception):
        forecaster._check_y(y=np.arange(10).reshape(-1, 1))
        
        
        
# Test method _check_last_window()
#-------------------------------------------------------------------------------
def test_check_last_window_exception_when_last_window_is_int():
    
    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    with pytest.raises(Exception):
        forecaster._check_y(y=10)
        
def test_check_last_window_exception_when_last_window_is_list():
    
    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    with pytest.raises(Exception):
        forecaster._check_y(y=[1, 2, 3])
        
        
def test_check_last_window_exception_when_last_window_is_numpy_array_with_more_than_one_dimension():
    
    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    with pytest.raises(Exception):
        forecaster._check_y(y=np.arange(10).reshape(-1, 1))
    
    
# Test method _check_exog()
#-------------------------------------------------------------------------------
def test_check_exog_exception_when_exog_is_int():

    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    with pytest.raises(Exception):
        forecaster._check_exog(exog=10)
        
        
def test_check_exog_exception_when_exog_is_list():

    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    with pytest.raises(Exception):
        forecaster._check_exog(exog=[1, 2, 3])
        
        
def test_check_exog_exception_when_exog_is_numpy_array_with_more_than_2_dimensions():

    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    with pytest.raises(Exception):
        forecaster._check_exog(exog=np.arange(30).reshape(-1, 10, 3))
        
        
def test_check_exog_exception_when_ref_type_is_pandas_series_and_exog_is_numpy_array_with_more_than_1_column():

    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    with pytest.raises(Exception):
        forecaster._check_exog(
            exog     = np.arange(30).reshape(-1, 2),
            ref_type = pd.Series
        )
        
        
def test_check_exog_exception_when_ref_type_is_pandas_series_and_exog_is_numpy_array_with_more_than_2_dimensions():

    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    with pytest.raises(Exception):
        forecaster._check_exog(exog=np.arange(30).reshape(-1, 10, 3))
        
        
def test_check_exog_exception_when_exog_has_diferent_number_of_columns_than_ref_shape():

    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    with pytest.raises(Exception):
        forecaster._check_exog(
            exog      = np.arange(30).reshape(-1, 3),
            ref_type  = np.ndarray,
            ref_shape = (1, 2)
        )

def test_check_exog_exception_when_exog_is_1d_numpy_array_and_ref_shape_has_more_than_1_column():

    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    with pytest.raises(Exception):
        forecaster._check_exog(
            exog      = np.arange(30),
            ref_type  = np.ndarray,
            ref_shape = (1, 5)
        )
        
        
def test_check_exog_exception_when_exog_is_pandas_series_and_ref_shape_has_more_than_1_column():

    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    with pytest.raises(Exception):
        forecaster._check_exog(
            exog      = pd.Series(np.arange(30)),
            ref_type  = np.ndarray,
            ref_shape = (1, 5)
        )

        
# Test method _preproces_y()
#-------------------------------------------------------------------------------
def test_preproces_y_when_y_is_pandas_series():

    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    assert (forecaster._preproces_y(y=pd.Series([0, 1, 2])) == np.arange(3)).all()
    

def test_preproces_y_when_y_is_1d_numpy_array():

    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    assert (forecaster._preproces_y(y=np.arange(3)) == np.arange(3)).all()
    


# Test method _preproces_last_window()
#-------------------------------------------------------------------------------
def test_preproces_last_window_when_last_window_is_pandas_series():

    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    assert (forecaster._preproces_last_window(last_window=pd.Series([0, 1, 2])) == np.arange(3)).all()
    

def test_preproces_last_window_when_last_window_is_1d_numpy_array():

    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    assert (forecaster._preproces_last_window(last_window=np.arange(3)) == np.arange(3)).all()


# Test method _preproces_exog()
#-------------------------------------------------------------------------------
def test_preproces_exog_when_exog_is_pandas_series():

    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    assert (forecaster._preproces_exog(exog=pd.Series([0, 1, 2])) == np.arange(3).reshape(-1, 1)).all()
    

def test_preproces_exog_when_exog_is_1d_numpy_array():

    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    assert (forecaster._preproces_exog(exog=np.arange(3)) == np.arange(3).reshape(-1, 1)).all()
    
    
# Test method test_set_paramns()
#-------------------------------------------------------------------------------
def test_set_paramns():
    
    forecaster = ForecasterAutoreg(LinearRegression(fit_intercept=True), lags=3)
    new_paramns = {'fit_intercept': False}
    forecaster.set_params(**new_paramns)
    expected = {'copy_X': True,
                 'fit_intercept': False,
                 'n_jobs': None,
                 'normalize': False,
                 'positive': False
                }
    assert forecaster.regressor.get_params() == expected


# Test method test_set_lags()
#-------------------------------------------------------------------------------
def test_set_lags_excepion_when_lags_argument_is_int_less_than_1():
    
    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    with pytest.raises(Exception):
        ForecasterAutoreg(LinearRegression(), lags=-10)

def test_set_lags_excepion_when_lags_argument_has_any_value_less_than_1():
    
    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    with pytest.raises(Exception):
        ForecasterAutoreg(LinearRegression(), lags=range(0, 4))
        
        
def test_set_lags_when_lags_argument_is_int():
    
    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    forecaster.set_lags(lags=5)
    assert (forecaster.lags == np.array([1, 2, 3, 4, 5])).all()
    assert forecaster.max_lag == 5
    
def test_set_lags_when_lags_argument_is_list():
    
    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    forecaster.set_lags(lags=[1,2,3])
    assert (forecaster.lags == np.array([1, 2, 3])).all()
    assert forecaster.max_lag == 3
    
def test_set_lags_when_lags_argument_is_1d_numpy_array():
    
    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    forecaster.set_lags(lags=np.array([1,2,3]))
    assert (forecaster.lags == np.array([1, 2, 3])).all()
    assert forecaster.max_lag == 3
    
    
# Test method set_out_sample_residuals()
#-------------------------------------------------------------------------------
def test_set_out_sample_residuals_exception_when_residuals_argument_is_list():
    
    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    with pytest.raises(Exception):
        forecaster.set_out_sample_residuals(residuals=[1,2,3])
        
        
def test_set_out_sample_residuals_when_residuals_lenght_is_less_or_equal_to_1000():
    
    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    forecaster.set_out_sample_residuals(residuals=np.arange(10))
    assert (forecaster.out_sample_residuals == np.arange(10)).all()
    

def test_set_out_sample_residuals_when_residuals_lenght_is_greater_than_1000():
    
    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    forecaster.set_out_sample_residuals(residuals=np.arange(2000))
    assert len(forecaster.out_sample_residuals) == 1000
    
    
# Test method get_coef()
#-------------------------------------------------------------------------------
def test_get_coef_when_regressor_is_LinearRegression():
    forecaster = ForecasterAutoreg(LinearRegression(), lags=3)
    forecaster.fit(y=np.arange(5))
    expected = np.array([0.33333333, 0.33333333, 0.33333333])
    assert forecaster.get_coef() == approx(expected)
    
def test_get_coef_when_regressor_is_Ridge():
    forecaster = ForecasterAutoreg(Ridge(), lags=3)
    forecaster.fit(y=np.arange(5))
    expected = np.array([0.2, 0.2, 0.2])
    assert forecaster.get_coef() == approx(expected)
    
def test_get_coef_when_regressor_is_Lasso():
    forecaster = ForecasterAutoreg(Lasso(), lags=3)
    forecaster.fit(y=np.arange(50))
    expected = np.array([9.94565217e-01, 6.16219995e-17, 0.00000000e+00])
    assert forecaster.get_coef() == approx(expected)


def test_get_coef_when_regressor_is_RandomForest():
    forecaster = ForecasterAutoreg(RandomForestRegressor(n_estimators=1, max_depth=2), lags=3)
    forecaster.fit(y=np.arange(5))
    expected = None
    assert forecaster.get_coef() is None
    

# Test method get_feature_importances
#-------------------------------------------------------------------------------
def test_get_feature_importances_when_regressor_is_RandomForest():
    forecaster = ForecasterAutoreg(RandomForestRegressor(n_estimators=1, max_depth=2, random_state=123), lags=3)
    forecaster.fit(y=np.arange(10))
    expected = np.array([0.94766355, 0., 0.05233645])
    assert forecaster.get_feature_importances() == approx(expected)
    
def test_get_feature_importances_when_regressor_is_GradientBoostingRegressor():
    forecaster = ForecasterAutoreg(GradientBoostingRegressor(n_estimators=1, max_depth=2, random_state=123), lags=3)
    forecaster.fit(y=np.arange(10))
    expected = np.array([0.1509434 , 0.05660377, 0.79245283])
    assert forecaster.get_feature_importances() == approx(expected)
    
def test_get_feature_importances_when_regressor_is_linear_model():
    forecaster = ForecasterAutoreg(Lasso(), lags=3)
    forecaster.fit(y=np.arange(50))
    expected = None
    assert forecaster.get_feature_importances() is None
    
    
    
# Test method _estimate_boot_interval
#-------------------------------------------------------------------------------
