"""
Methods for extracting Implied Vol and producing skew reports

"""
from collections import Counter
import copy
from decimal import Decimal
import datetime as dt
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd
import scipy as sp
import scipy.interpolate as inter
from scipy.optimize import minimize
import scipy.stats as si
# pylint: disable=invalid-name, consider-using-f-string

class ImpliedVol():
    """
    Implied Volatility Extraction methods

    """
    @classmethod
    def implied_vol_newton_raphson(cls, opt_params: dict) -> float | str:
        """
        Finds implied volatility using Newton-Raphson method - needs
        knowledge of partial derivative of option pricing formula
        with respect to volatility (vega)

        Parameters
        ----------
        S : Float
            Stock Price. The default is 100.
        K : Float
            Strike Price. The default is 100.
        T : Float
            Time to Maturity.  The default is 0.25 (3 Months).
        r : Float
            Interest Rate. The default is 0.005 (50bps)
        q : Float
            Dividend Yield.  The default is 0.
        cm : Float
            # Option price used to solve for vol. The default is 5.
        epsilon : Float
            Degree of precision. The default is 0.0001
        option : Str
            Type of option. 'put' or 'call'. The default is 'call'.
        default : Bool
            Whether the function is being called directly (in which
            case values that are not supplied are set to default
            values) or called from another function where they have
            already been updated.

        Returns
        -------
        result : Float
            Implied Volatility.

        """

        # Manaster and Koehler seed value
        opt_params['vi'] = np.sqrt(
            abs(np.log(opt_params['S'] / opt_params['K'])
                + opt_params['r'] * opt_params['T']) * (2 / opt_params['T']))

        opt_params['ci'] = cls.black_scholes_merton(
            opt_params=opt_params, sigma=opt_params['vi'])

        opt_params['vegai'] = cls.black_scholes_merton_vega(
            opt_params=opt_params, sigma=opt_params['vi'])

        opt_params['mindiff'] = abs(opt_params['cm'] - opt_params['ci'])

        while (abs(opt_params['cm'] - opt_params['ci'])
               >= opt_params['epsilon']
               and abs(opt_params['cm'] - opt_params['ci'])
               <= opt_params['mindiff']):

            opt_params['vi'] = (
                opt_params['vi']
                - (opt_params['ci'] - opt_params['cm']) / opt_params['vegai'])

            opt_params['ci'] = cls.black_scholes_merton(
                opt_params=opt_params, sigma=opt_params['vi'])

            opt_params['vegai'] = cls.black_scholes_merton_vega(
                opt_params=opt_params, sigma=opt_params['vi'])

            opt_params['mindiff'] = abs(opt_params['cm'] - opt_params['ci'])

        if abs(opt_params['cm'] - opt_params['ci']) < opt_params['epsilon']:
            result = opt_params['vi']
        else:
            result = 'NA'

        return result


    @classmethod
    def implied_vol_bisection(cls, opt_params: dict) -> float | str:
        """
        Finds implied volatility using bisection method.

        Parameters
        ----------
        S : Float
            Stock Price. The default is 100.
        K : Float
            Strike Price. The default is 100.
        T : Float
            Time to Maturity.  The default is 0.25 (3 Months).
        r : Float
            Interest Rate. The default is 0.005 (50bps)
        q : Float
            Dividend Yield.  The default is 0.
        cm : Float
            # Option price used to solve for vol. The default is 5.
        epsilon : Float
            Degree of precision. The default is 0.0001
        option : Str
            Type of option. 'put' or 'call'. The default is 'call'.
        default : Bool
            Whether the function is being called directly (in which
            case values that are not supplied are set to default
            values) or called from another function where they have
            already been updated.

        Returns
        -------
        result : Float
            Implied Volatility.

        """

        opt_params['vLow'] = 0.005
        opt_params['vHigh'] = 4
        opt_params['cLow'] = cls.black_scholes_merton(
            opt_params=opt_params, sigma=opt_params['vLow'])

        opt_params['cHigh'] = cls.black_scholes_merton(
            opt_params=opt_params, sigma=opt_params['vHigh'])

        counter = 0

        opt_params['vi'] = (
            opt_params['vLow']
            + (opt_params['cm'] - opt_params['cLow'])
            * (opt_params['vHigh'] - opt_params['vLow'])
            / (opt_params['cHigh'] - opt_params['cLow']))

        while abs(opt_params['cm'] - cls.black_scholes_merton(
                opt_params=opt_params,
                sigma=opt_params['vi'])) > opt_params['epsilon']:

            counter = counter + 1
            if counter == 100:
                result = 'NA'

            if cls.black_scholes_merton(
                    opt_params=opt_params,
                    sigma=opt_params['vi']) < opt_params['cm']:
                opt_params['vLow'] = opt_params['vi']

            else:
                opt_params['vHigh'] = opt_params['vi']

            opt_params['cLow'] = cls.black_scholes_merton(
                opt_params=opt_params, sigma=opt_params['vLow'])

            opt_params['cHigh'] = cls.black_scholes_merton(
                opt_params=opt_params, sigma=opt_params['vHigh'])

            opt_params['vi'] = (
                opt_params['vLow']
                + (opt_params['cm'] - opt_params['cLow'])
                * (opt_params['vHigh'] - opt_params['vLow'])
                / (opt_params['cHigh'] - opt_params['cLow']))

        result = opt_params['vi']

        return result


    @classmethod
    def implied_vol_naive(cls, opt_params: dict) -> float:
        """
        Finds implied volatility using simple naive iteration,
        increasing precision each time the difference changes sign.

        Parameters
        ----------
        S : Float
            Stock Price. The default is 100.
        K : Float
            Strike Price. The default is 100.
        T : Float
            Time to Maturity.  The default is 0.25 (3 Months).
        r : Float
            Interest Rate. The default is 0.005 (50bps)
        q : Float
            Dividend Yield.  The default is 0.
        cm : Float
            # Option price used to solve for vol. The default is 5.
        epsilon : Float
            Degree of precision. The default is 0.0001
        option : Str
            Type of option. 'put' or 'call'. The default is 'call'.

        Returns
        -------
        result : Float
            Implied Volatility.

        """

        # Seed vol
        opt_params['vi'] = 0.2

        # Calculate starting option price using this vol
        opt_params['ci'] = cls.black_scholes_merton(
            opt_params=opt_params, sigma=opt_params['vi'])

        # Initial price difference
        opt_params['price_diff'] = opt_params['cm'] - opt_params['ci']

        if opt_params['price_diff'] > 0:
            opt_params['flag'] = 1

        else:
            opt_params['flag'] = -1

        # Starting vol shift size
        opt_params['shift'] = 0.01

        opt_params['price_diff_start'] = opt_params['price_diff']

        while abs(opt_params['price_diff']) > opt_params['epsilon']:

            # If the price difference changes sign after the vol shift,
            # reduce the decimal by one and reverse the sign
            if (np.sign(opt_params['price_diff'])
                != np.sign(opt_params['price_diff_start'])):
                opt_params['shift'] = opt_params['shift'] * -0.1

            # Calculate new vol
            opt_params['vi'] += (opt_params['shift'] * opt_params['flag'])

            # Set initial price difference
            opt_params['price_diff_start'] = opt_params['price_diff']

            # Calculate the option price with new vol
            opt_params['ci'] = cls.black_scholes_merton(
                opt_params=opt_params, sigma=opt_params['vi'])

            # Price difference after shifting vol
            opt_params['price_diff'] = opt_params['cm'] - opt_params['ci']

            # If values are diverging reverse the shift sign
            if (abs(opt_params['price_diff'])
                > abs(opt_params['price_diff_start'])):
                opt_params['shift'] = -opt_params['shift']

        result = opt_params['vi']

        return result


    @classmethod
    def implied_vol_naive_verbose(cls, opt_params: dict) -> float:
        """
        Finds implied volatility using simple naive iteration,
        increasing precision each time the difference changes sign.

        Parameters
        ----------
        S : Float
            Stock Price. The default is 100.
        K : Float
            Strike Price. The default is 100.
        T : Float
            Time to Maturity.  The default is 0.25 (3 Months).
        r : Float
            Interest Rate. The default is 0.005 (50bps)
        q : Float
            Dividend Yield.  The default is 0.
        cm : Float
            # Option price used to solve for vol. The default is 5.
        epsilon : Float
            Degree of precision. The default is 0.0001
        option : Str
            Type of option. 'put' or 'call'. The default is 'call'.

        Returns
        -------
        result : Float
            Implied Volatility.

        """

        opt_params['vi'] = 0.2
        opt_params['ci'] = cls.black_scholes_merton(
            opt_params=opt_params, sigma=opt_params['vi'])

        opt_params['price_diff'] = opt_params['cm'] - opt_params['ci']
        if opt_params['price_diff'] > 0:
            opt_params['flag'] = 1
        else:
            opt_params['flag'] = -1
        while abs(opt_params['price_diff']) > opt_params['epsilon']:
            while opt_params['price_diff'] * opt_params['flag'] > 0:
                opt_params['ci'] = cls.black_scholes_merton(
                    opt_params=opt_params, sigma=opt_params['vi'])

                opt_params['price_diff'] = opt_params['cm'] - opt_params['ci']
                opt_params['vi'] += (0.01 * opt_params['flag'])

            while opt_params['price_diff'] * opt_params['flag'] < 0:
                opt_params['ci'] = cls.black_scholes_merton(
                    opt_params=opt_params, sigma=opt_params['vi'])

                opt_params['price_diff'] = opt_params['cm'] - opt_params['ci']
                opt_params['vi'] -= (0.001 * opt_params['flag'])

            while opt_params['price_diff'] * opt_params['flag'] > 0:
                opt_params['ci'] = cls.black_scholes_merton(
                    opt_params=opt_params, sigma=opt_params['vi'])

                opt_params['price_diff'] = opt_params['cm'] - opt_params['ci']
                opt_params['vi'] += (0.0001 * opt_params['flag'])

            while opt_params['price_diff'] * opt_params['flag'] < 0:
                opt_params['ci'] = cls.black_scholes_merton(
                    opt_params=opt_params, sigma=opt_params['vi'])

                opt_params['price_diff'] = opt_params['cm'] - opt_params['ci']
                opt_params['vi'] -= (0.00001 * opt_params['flag'])

            while opt_params['price_diff'] * opt_params['flag'] > 0:
                opt_params['ci'] = cls.black_scholes_merton(
                    opt_params=opt_params, sigma=opt_params['vi'])

                opt_params['price_diff'] = opt_params['cm'] - opt_params['ci']
                opt_params['vi'] += (0.000001 * opt_params['flag'])

            while opt_params['price_diff'] * opt_params['flag'] < 0:
                opt_params['ci'] = cls.black_scholes_merton(
                    opt_params=opt_params, sigma=opt_params['vi'])

                opt_params['price_diff'] = opt_params['cm'] - opt_params['ci']
                opt_params['vi'] -= (0.0000001 * opt_params['flag'])

        result = opt_params['vi']

        return result


    @staticmethod
    def black_scholes_merton(
        opt_params: dict,
        sigma: float) -> float:
        """
        Black-Scholes-Merton Option price

        Parameters
        ----------
        S : Float
            Stock Price. The default is 100.
        K : Float
            Strike Price. The default is 100.
        T : Float
            Time to Maturity.  The default is 0.25 (3 Months).
        r : Float
            Interest Rate. The default is 0.005 (50bps)
        q : Float
            Dividend Yield.  The default is 0.
        sigma : Float
            Implied Volatility.  The default is 0.2 (20%).
        option : Str
            Type of option. 'put' or 'call'. The default is 'call'.

        Returns
        -------
        opt_price : Float
            Option Price.

        """

        opt_params['b'] = opt_params['r'] - opt_params['q']
        opt_params['carry'] = np.exp(
            (opt_params['b'] - opt_params['r']) * opt_params['T'])
        opt_params['d1'] = (
            (np.log(opt_params['S'] / opt_params['K'])
             + (opt_params['b'] + (0.5 * sigma ** 2)) * opt_params['T'])
              / (sigma * np.sqrt(opt_params['T'])))
        opt_params['d2'] = (
            (np.log(opt_params['S'] / opt_params['K'])
             + (opt_params['b'] - (0.5 * sigma ** 2)) * opt_params['T'])
              / (sigma * np.sqrt(opt_params['T'])))

        # Cumulative normal distribution function
        opt_params['Nd1'] = si.norm.cdf(opt_params['d1'], 0.0, 1.0)
        opt_params['minusNd1'] = si.norm.cdf(-opt_params['d1'], 0.0, 1.0)
        opt_params['Nd2'] = si.norm.cdf(opt_params['d2'], 0.0, 1.0)
        opt_params['minusNd2'] = si.norm.cdf(-opt_params['d2'], 0.0, 1.0)

        if opt_params['option'] == "call":
            opt_price = (
                (opt_params['S'] * opt_params['carry'] * opt_params['Nd1'])
                - (opt_params['K']
                   * np.exp(-opt_params['r'] * opt_params['T'])
                   * opt_params['Nd2']))

        elif opt_params['option'] == 'put':
            opt_price = (
                (opt_params['K']
                 * np.exp(-opt_params['r'] * opt_params['T'])
                 * opt_params['minusNd2'])
                - (opt_params['S']
                   * opt_params['carry']
                   * opt_params['minusNd1']))

        else:
            print("Please supply a value for option - 'put' or 'call'")

        return opt_price


    @staticmethod
    def black_scholes_merton_vega(
        opt_params: dict,
        sigma: float) -> float:
        """
        Black-Scholes-Merton Option Vega

        Parameters
        ----------
        S : Float
            Stock Price. The default is 100.
        K : Float
            Strike Price. The default is 100.
        T : Float
            Time to Maturity.  The default is 0.25 (3 Months).
        r : Float
            Interest Rate. The default is 0.005 (50bps)
        q : Float
            Dividend Yield.  The default is 0.
        sigma : Float
            Implied Volatility.  The default is 0.2 (20%).

        Returns
        -------
        opt_vega : Float
            Option Vega.

        """

        opt_params['b'] = opt_params['r'] - opt_params['q']
        opt_params['carry'] = np.exp(
            (opt_params['b'] - opt_params['r']) * opt_params['T'])
        opt_params['d1'] = (
            (np.log(opt_params['S'] / opt_params['K'])
             + (opt_params['b'] + (0.5 * sigma ** 2)) * opt_params['T'])
              / (sigma * np.sqrt(opt_params['T'])))
        opt_params['nd1'] = (
            1 / np.sqrt(2 * np.pi)) * (np.exp(-opt_params['d1'] ** 2 * 0.5))

        opt_vega = (opt_params['S']
                    * opt_params['carry']
                    * opt_params['nd1']
                    * np.sqrt(opt_params['T']))

        return opt_vega


class SVIModel:
    """
    Stochastic Volatility Inspired model implementation for volatility surfaces
    
    The SVI parameterization is given by:
    w(k) = a + b * (ρ * (k - m) + sqrt((k - m)² + σ²))
    
    where:
    - w(k) is the total implied variance (σ² * T)
    - k is the log-moneyness (log(K/F))
    - a, b, ρ, m, and σ are the SVI parameters
    """
    
    @staticmethod
    def svi_function(k, a, b, rho, m, sigma):
        """
        SVI parametrization function
        
        Parameters
        ----------
        k : ndarray
            Log-moneyness (log(K/F))
        a : float
            Overall level parameter
        b : float
            Controls the angle between the left and right asymptotes
        rho : float
            Controls the skew/rotation (-1 <= rho <= 1)
        m : float
            Controls the horizontal translation
        sigma : float
            Controls the smoothness of the curve at the minimum
            
        Returns
        -------
        ndarray
            Total implied variance w(k)
        """
        return a + b * (rho * (k - m) + np.sqrt((k - m)**2 + sigma**2))
    
    @staticmethod
    def svi_calibrate(strikes, vols, ttm, forward_price, params):
        """
        Calibrate SVI parameters for a single maturity
        
        Parameters
        ----------
        strikes : ndarray
            Option strike prices
        vols : ndarray
            Implied volatilities corresponding to strikes
        ttm : float
            Time to maturity in years
        forward_price : float
            Forward price of the underlying
        params : dict
            Dictionary of parameters including SVI configuration parameters
            
        Returns
        -------
        tuple
            Calibrated SVI parameters (a, b, rho, m, sigma)
        """
        # Convert to log-moneyness
        k = np.log(strikes / forward_price)
        
        # Convert volatilities to total variance
        w = vols**2 * ttm
        
        # Set initial parameters from params dict
        if params['svi_compute_initial']:
            # Compute reasonable initial values based on data
            a_init = np.min(w)
            b_init = (np.max(w) - np.min(w)) / 2
            # Use defaults from params for other values
            rho_init = params['svi_rho_init']
            m_init = params['svi_m_init']
            sigma_init = params['svi_sigma_init']
        else:
            # Use values directly from params
            a_init = params['svi_a_init']
            b_init = params['svi_b_init']
            rho_init = params['svi_rho_init']
            m_init = params['svi_m_init']
            sigma_init = params['svi_sigma_init']
            
        initial_params = (a_init, b_init, rho_init, m_init, sigma_init)
        
        # Define the objective function to minimize (sum of squared errors)
        def objective(params):
            a, b, rho, m, sigma = params
            
            # Apply constraints
            if b < 0 or abs(rho) > 1 or sigma <= 0:
                return 1e10  # Large penalty for invalid parameters
                
            w_model = SVIModel.svi_function(k, a, b, rho, m, sigma)
            return np.sum((w - w_model)**2)
        
        # Set bounds for parameters
        bounds = [
            (None, None),      # a: no bounds
            (0.0001, None),    # b: positive
            (-0.9999, 0.9999), # rho: between -1 and 1
            (None, None),      # m: no bounds
            (0.0001, None)     # sigma: positive
        ]
        
        # Perform the optimization using params
        result = minimize(
            objective, 
            initial_params, 
            bounds=bounds, 
            method='L-BFGS-B',
            options={'maxiter': params['svi_max_iter'], 'ftol': params['svi_tol']}
        )
        
        return result.x
    
    @staticmethod
    def fit_svi_surface(data, params):
        """
        Fit SVI model to the entire volatility surface
        
        Parameters
        ----------
        data : DataFrame
            Option data with columns 'Strike', 'TTM', and implied vol columns
        params : dict
            Dictionary of parameters including spot price and rates
            
        Returns
        -------
        dict
            Dictionary of SVI parameters for each maturity and interpolation function
        """
        # Extract unique maturities
        ttms = sorted(list(set(data['TTM'])))
        
        # Dictionary to store SVI parameters for each maturity
        svi_params = {}
        
        # Fit SVI model for each maturity
        for ttm in ttms:
            # Filter data for this maturity
            ttm_data = data[data['TTM'] == ttm]
            
            # Get strikes and vols
            strikes = np.array(ttm_data['Strike'])
            vol_col = params['vols_dict'][params['voltype']]
            vols = np.array(ttm_data[vol_col])
            
            # Calculate forward price using parameters from params dictionary
            spot = params['spot'] if params['spot'] is not None else params['extracted_spot']
            forward_price = spot * np.exp((params['r'] - params['q']) * ttm)
            
            # Calibrate SVI parameters using params dictionary
            a, b, rho, m, sigma = SVIModel.svi_calibrate(strikes, vols, ttm, forward_price, params)
            
            # Store parameters
            svi_params[ttm] = {
                'a': a,
                'b': b,
                'rho': rho,
                'm': m,
                'sigma': sigma,
                'forward': forward_price
            }
        
        return svi_params
    
    @staticmethod
    def compute_svi_surface(strikes_grid, ttms_grid, svi_params, params):
        """
        Compute volatility surface using SVI parameters
        
        Parameters
        ----------
        strikes_grid : ndarray
            2D grid of strike prices
        ttms_grid : ndarray
            2D grid of time to maturities (in years)
        svi_params : dict
            Dictionary of SVI parameters for each maturity
        params : dict
            Dictionary of additional parameters
            
        Returns
        -------
        ndarray
            2D grid of implied volatilities
        """
        # Get list of ttms for which we have SVI parameters
        svi_ttms = sorted(list(svi_params.keys()))
        
        # Initialize volatility surface grid
        vol_surface = np.zeros_like(strikes_grid)
        
        # Compute SVI implied volatilities
        for i in range(strikes_grid.shape[0]):
            for j in range(strikes_grid.shape[1]):
                strike = strikes_grid[i, j]
                ttm = ttms_grid[i, j]
                
                # Find the closest ttms with SVI parameters
                idx = np.searchsorted(svi_ttms, ttm)
                
                # Handle boundary cases
                if idx == 0:
                    ttm_params = svi_params[svi_ttms[0]]
                elif idx == len(svi_ttms):
                    ttm_params = svi_params[svi_ttms[-1]]
                else:
                    # Interpolate between the two closest ttms
                    ttm_lower = svi_ttms[idx-1]
                    ttm_upper = svi_ttms[idx]
                    
                    params_lower = svi_params[ttm_lower]
                    params_upper = svi_params[ttm_upper]
                    
                    # Linear interpolation weight
                    w = (ttm - ttm_lower) / (ttm_upper - ttm_lower)
                    
                    # Interpolate SVI parameters
                    a = params_lower['a'] * (1-w) + params_upper['a'] * w
                    b = params_lower['b'] * (1-w) + params_upper['b'] * w
                    rho = params_lower['rho'] * (1-w) + params_upper['rho'] * w
                    m = params_lower['m'] * (1-w) + params_upper['m'] * w
                    sigma = params_lower['sigma'] * (1-w) + params_upper['sigma'] * w
                    forward = params_lower['forward'] * (1-w) + params_upper['forward'] * w
                    
                    ttm_params = {'a': a, 'b': b, 'rho': rho, 'm': m, 'sigma': sigma, 'forward': forward}
                
                # Calculate log-moneyness
                k = np.log(strike / ttm_params['forward'])
                
                # Calculate total implied variance using SVI function
                w = SVIModel.svi_function(k, ttm_params['a'], ttm_params['b'], 
                                         ttm_params['rho'], ttm_params['m'], 
                                         ttm_params['sigma'])
                
                # Convert total variance to implied volatility
                if w > 0:
                    vol_surface[i, j] = np.sqrt(w / ttm)
                else:
                    vol_surface[i, j] = 0
        
        return vol_surface
        
    @staticmethod
    def compute_svi_surface_vectorized(strikes_grid, ttms_grid, svi_params, params):
        """
        Compute volatility surface using SVI parameters (vectorized implementation)
        
        Parameters
        ----------
        strikes_grid : ndarray
            2D grid of strike prices
        ttms_grid : ndarray
            2D grid of time to maturities (in years)
        svi_params : dict
            Dictionary of SVI parameters for each maturity
        params : dict
            Dictionary of additional parameters
            
        Returns
        -------
        ndarray
            2D grid of implied volatilities (in decimal form)
        """
        # Get list of ttms for which we have SVI parameters
        svi_ttms = np.array(sorted(list(svi_params.keys())))
        
        # Flatten grids for vectorized computation
        strikes_flat = strikes_grid.flatten()
        ttms_flat = ttms_grid.flatten()
        vol_flat = np.zeros_like(strikes_flat)
        
        # Process each point in the grid
        for i in range(len(strikes_flat)):
            strike = strikes_flat[i]
            ttm = ttms_flat[i]
            
            # Find the closest ttms with SVI parameters
            idx = np.searchsorted(svi_ttms, ttm)
            
            # Interpolate SVI parameters based on maturity
            if idx == 0:
                ttm_params = svi_params[svi_ttms[0]]
            elif idx == len(svi_ttms):
                ttm_params = svi_params[svi_ttms[-1]]
            else:
                # Interpolate between adjacent maturities
                ttm_lower = svi_ttms[idx-1]
                ttm_upper = svi_ttms[idx]
                
                params_lower = svi_params[ttm_lower]
                params_upper = svi_params[ttm_upper]
                
                # Linear interpolation weight
                w = (ttm - ttm_lower) / (ttm_upper - ttm_lower)
                
                # Interpolate each SVI parameter
                ttm_params = {
                    'a': params_lower['a'] * (1-w) + params_upper['a'] * w,
                    'b': params_lower['b'] * (1-w) + params_upper['b'] * w,
                    'rho': params_lower['rho'] * (1-w) + params_upper['rho'] * w,
                    'm': params_lower['m'] * (1-w) + params_upper['m'] * w,
                    'sigma': params_lower['sigma'] * (1-w) + params_upper['sigma'] * w,
                    'forward': params_lower['forward'] * (1-w) + params_upper['forward'] * w
                }
            
            # Calculate log-moneyness
            k = np.log(strike / ttm_params['forward'])
            
            # Apply SVI formula to get total implied variance
            w = SVIModel.svi_function(k, ttm_params['a'], ttm_params['b'], 
                                     ttm_params['rho'], ttm_params['m'], 
                                     ttm_params['sigma'])
            
            # Convert total variance to annualized volatility
            vol_flat[i] = np.sqrt(max(0, w) / ttm)
        
        # Reshape back to original grid dimensions
        vol_surface = vol_flat.reshape(strikes_grid.shape)
        
        return vol_surface
    

class VolMethods():
    """
    Methods for extracting Implied Vol and producing skew reports

    """
    @classmethod
    def smooth(
        cls,
        params: dict,
        tables: dict) -> tuple[dict, dict]:
        """
        Create a column of smoothed implied vols

        Parameters
        ----------
        order : Int
            Polynomial order used in numpy polyfit function. The
            default is 3.
        voltype : Str
            Whether to use 'bid', 'mid', 'ask' or 'last' price. The
            default is 'last'.
        smoothopt : Int
            Minimum number of options to fit curve to. The default
            is 6.

        Returns
        -------
        DataFrame
            DataFrame of Option prices.

        """

        # Create a dictionary of the number of options for each
        # maturity
        mat_dict = dict(Counter(tables['imp_vol_data']['Days']))

        # Create a sorted list of the different number of days to
        # maturity
        maturities = sorted(list(set(tables['imp_vol_data']['Days'])))

        # Create a sorted list of the different number of strikes
        strikes_full = sorted(list(set((tables['imp_vol_data'][
            'Strike'].astype(float)))))

        # create copy of implied vol data
        tables['imp_vol_data_smoothed'] = copy.deepcopy(tables['imp_vol_data'])

        for ttm, count in mat_dict.items():

            # if there are less than smoothopt (default is 6) options
            # for a given maturity
            if count < params['smoothopt']:

                # remove that maturity from the maturities list
                maturities.remove(ttm)

                # and remove that maturity from the implied vol
                # DataFrame
                tables['imp_vol_data_smoothed'] = tables[
                    'imp_vol_data_smoothed'][
                        tables['imp_vol_data_smoothed']['Days'] != ttm]

        # Create empty DataFrame with the full range of strikes as
        # index
        tables['smooth_surf'] = pd.DataFrame(index=strikes_full)

        # going through the maturity list (in reverse so the columns
        # created are in increasing order)
        for maturity in reversed(maturities):

            # Extract the strikes for this maturity
            strikes = tables['imp_vol_data'][tables['imp_vol_data'][
                'Days']==maturity]['Strike']

            # And the vols (specifying the voltype)
            vols = tables['imp_vol_data'][tables['imp_vol_data'][
                'Days']==maturity][str(
                    params['vols_dict'][str(params['voltype'])])]

            # Fit a polynomial to this data
            curve_fit = np.polyfit(strikes, vols, params['order'])
            p = np.poly1d(curve_fit)

            # Create empty list to store smoothed implied vols
            iv_new = []

            # For each strike
            for strike in strikes_full:

                # Add the smoothed value to the iv_new list
                iv_new.append(p(strike))

            # Append this list as a new column in the smooth_surf
            # DataFrame
            tables['smooth_surf'].insert(0, str(maturity), iv_new)

        # Apply the _vol_map function to add smoothed vol column to
        # DataFrame
        tables['imp_vol_data_smoothed'] = (
            tables['imp_vol_data_smoothed'].apply(
                lambda x: cls._vol_map(x, tables), axis=1))

        return params, tables


    @staticmethod
    def _vol_map(
        row: pd.Series,
        tables: dict) -> pd.Series:
        """
        Map value calculated in smooth surface DataFrame to
        'Smoothed Vol' column.

        Parameters
        ----------
        row : Array
            Each row in the DataFrame.

        Returns
        -------
        row : Array
            Each row in the DataFrame.

        """
        row['Smoothed Vol'] = (
            tables['smooth_surf'].loc[row['Strike'], str(row['Days'])])

        return row


    @classmethod
    def map_vols(
        cls,
        params: dict,
        tables: dict) -> tuple[inter._rbf.Rbf, inter._rbf.Rbf]:
        """
        Create vol surface mapping function

        Parameters
        ----------
        tables : Dict
            Dictionary containing the market data tables.

        Returns
        -------
        vol_surface : scipy.interpolate.rbf.Rbf
            Vol surface interpolation function.

        """
        params, tables = cls.smooth(params=params, tables=tables)
        data = tables['imp_vol_data_smoothed']
        try:
            t_vols_smooth = data['Smoothed Vol'] * 100
        except KeyError:
            t_vols_smooth = data['Imp Vol - Last'] * 100
        t_vols = data['Imp Vol - Last'] * 100
        t_strikes = data['Strike']
        t_ttm = data['TTM'] * 365
        vol_surface = sp.interpolate.Rbf(
            t_strikes,
            t_ttm,
            t_vols,
            function=params['rbffunc'],
            smooth=5,
            epsilon=5)

        vol_surface_smoothed = sp.interpolate.Rbf(
            t_strikes,
            t_ttm,
            t_vols_smooth,
            function=params['rbffunc'],
            smooth=5,
            epsilon=5)

        return vol_surface, vol_surface_smoothed


    @staticmethod
    def get_vol(
        maturity: str,
        strike: int,
        params: dict,
        surface_models: dict) -> float:
        """
        Return implied vol for a given maturity and strike

        Parameters
        ----------
        maturity : Str
            The date for the option maturity, expressed as 'YYYY-MM-DD'.
        strike : Int
            The strike expressed as a percent, where ATM = 100.

        Returns
        -------
        imp_vol : Float
            The implied volatility.

        """
        strike_level = params['spot'] * strike / 100
        maturity_date = dt.datetime.strptime(maturity, '%Y-%m-%d')
        start_date = dt.datetime.strptime(params['start_date'], '%Y-%m-%d')
        ttm = (maturity_date - start_date).days
        if params['smoothing']:
            imp_vol = surface_models[
                'vol_surface_smoothed'](strike_level, ttm)
        else:
            imp_vol = surface_models['vol_surface'](strike_level, ttm)

        return np.round(imp_vol, 2)


    @classmethod
    def create_vol_dict(
        cls,
        params: dict,
        surface_models: dict) -> dict:
        """
        Create dictionary of implied vols by tenor and strike to use in skew
        report

        Parameters
        ----------
        params : Dict
            Dictionary of key parameters.
        surface_models : Dict
            Dictionary of vol surfaces.

        Returns
        -------
        vol_dict : Dict
            Dictionary of implied vols.

        """
        vol_dict = {}
        start_date = dt.datetime.strptime(params['start_date'], '%Y-%m-%d')
        for month in range(1, params['skew_months']+1):
            for strike in [80, 90, 100, 110, 120]:
                maturity = dt.datetime.strftime(
                    start_date + relativedelta(months=month), '%Y-%m-%d')
                vol_dict[(month, strike)] = cls.get_vol(
                    maturity=maturity, strike=strike, params=params,
                    surface_models=surface_models)

        return vol_dict


    @classmethod
    def print_skew_report(
        cls,
        vol_dict: dict,
        params: dict) -> None:
        """
        Print a report showing implied vols for 80%, 90% and ATM strikes and
        selected tenor length

        Parameters
        ----------
        vol_dict : Dict
            Dictionary of implied vols.
        params : Dict
            Dictionary of key parameters.

        Returns
        -------
        Prints the report to the console.

        """
        # Set decimal format
        dp2 = Decimal(10) ** -2  # (equivalent to Decimal '0.01')

        if params['skew_direction'] == 'full':
            cls._full_skew(vol_dict=vol_dict, params=params, dp2=dp2)
        else:
            cls._header(params=params)

            if params['skew_direction'] == 'up':
                cls._upside_skew(vol_dict=vol_dict, params=params, dp2=dp2)

            else:
                cls._downside_skew(vol_dict=vol_dict, params=params, dp2=dp2)


    @staticmethod
    def _header(params: dict) -> None:

        print('='*78)
        print(': {:^74} :'.format('Skew Summary'))
        print('-'*78)

        # Contract traded on left and period covered on right
        print(': Underlying Ticker : {:<19}{} : {} :'.format(
            params['ticker_label'],
            'Close of Business Date',
            params['start_date']))
        print('-'*78)

        # Strike and skew headers
        print(': {:^12} :{:^34} : {:^23} :'.format(
            'Maturity',
            'Strike',
            'Skew'))
        print('-'*78)

        if params['skew_direction'] == 'up':

            print(': {:>15}{:>7}   : {:>7}   : {:>7}   : {:>10}'\
                  ' : {:>10} :'.format(
                ': ',
                'ATM',
                '110%',
                '120%',
                '+10% Skew',
                '+20% Skew'))

        if params['skew_direction'] == 'down':
            print(': {:>15}{:>7}   : {:>7}   : {:>7}   : {:>10}'\
                  ' : {:>10} :'.format(
                ': ',
                '80%',
                '90%',
                'ATM',
                '-10% Skew',
                '-20% Skew'))


    @staticmethod
    def _downside_skew(
        vol_dict: dict,
        params: dict,
        dp2: Decimal) -> None:

        # Monthly skew summary for selected number of months
        for month in range(1, params['skew_months'] + 1):
            if month < 10:
                month_label = ' '+str(month)
            else:
                month_label = str(month)
            print(': {} Month Vol : {:>7}   : {:>7}   : {:>7}   : {:>7}'\
                  '    : {:>7}    :'.format(
                month_label,
                Decimal(vol_dict[(month, 80)]).quantize(dp2),
                Decimal(vol_dict[(month, 90)]).quantize(dp2),
                Decimal(vol_dict[(month, 100)]).quantize(dp2),
                Decimal((vol_dict[(month, 90)]
                         - vol_dict[(month, 100)]) / 10).quantize(dp2),
                Decimal((vol_dict[(month, 80)]
                         - vol_dict[(month, 100)]) / 20).quantize(dp2)))

        print('-'*78)
        print('='*78)


    @staticmethod
    def _upside_skew(
        vol_dict: dict,
        params: dict,
        dp2: Decimal) -> None:

        # Monthly skew summary for selected number of months
        for month in range(1, params['skew_months'] + 1):
            if month < 10:
                month_label = ' '+str(month)
            else:
                month_label = str(month)
            print(': {} Month Vol : {:>7}   : {:>7}   : {:>7}   : {:>7}'\
                  '    : {:>7}    :'.format(
                month_label,
                Decimal(vol_dict[(month, 100)]).quantize(dp2),
                Decimal(vol_dict[(month, 110)]).quantize(dp2),
                Decimal(vol_dict[(month, 120)]).quantize(dp2),
                Decimal((vol_dict[(month, 110)]
                         - vol_dict[(month, 100)]) / 10).quantize(dp2),
                Decimal((vol_dict[(month, 120)]
                         - vol_dict[(month, 100)]) / 20).quantize(dp2)))

        print('-'*78)
        print('='*78)


    @staticmethod
    def _full_skew(
        vol_dict: dict,
        params: dict,
        dp2: Decimal) -> None:

        print('='*115)
        print(': {:^111} :'.format('Skew Summary'))
        print('-'*115)

        # Contract traded on left and period covered on right
        print(': Underlying Ticker : {:<56}{} : {} :'.format(
            params['ticker_label'],
            'Close of Business Date',
            params['start_date']))
        print('-'*115)

        # Strike and skew headers
        print(': {:^13} : {:^47} : {:^45} :'.format(
            'Maturity',
            'Strike',
            'Skew'))
        print('-'*115)

        # Header rows
        print(': {:>16}{:>6}  : {:>6}  : {:>6}  : {:>6}  : {:>6}  : {:>9}'\
              ' : {:>9} : {:>9} : {:>9} :'.format(
            ': ',
            '80%',
            '90%',
            'ATM',
            '110%',
            '120%',
            '-20% Skew',
            '-10% Skew',
            '+10% Skew',
            '+20% Skew'))

        # Set decimal format
        dp2 = Decimal(10) ** -2  # (equivalent to Decimal '0.01')

        # Monthly skew summary for selected number of months
        for month in range(1, params['skew_months'] + 1):
            if month < 10:
                month_label = ' '+str(month)
            else:
                month_label = str(month)
            print(': {} Month Vol  : {:>6}  : {:>6}  : {:>6}  : {:>6}  : '\
                  '{:>6}  : {:>7}   : {:>7}   : {:>7}   : {:>7}   :'.format(
                month_label,
                Decimal(vol_dict[(month, 80)]).quantize(dp2),
                Decimal(vol_dict[(month, 90)]).quantize(dp2),
                Decimal(vol_dict[(month, 100)]).quantize(dp2),
                Decimal(vol_dict[(month, 110)]).quantize(dp2),
                Decimal(vol_dict[(month, 120)]).quantize(dp2),
                Decimal((vol_dict[(month, 80)]
                         - vol_dict[(month, 100)]) / 20).quantize(dp2),
                Decimal((vol_dict[(month, 90)]
                         - vol_dict[(month, 100)]) / 10).quantize(dp2),
                Decimal((vol_dict[(month, 110)]
                         - vol_dict[(month, 100)]) / 10).quantize(dp2),
                Decimal((vol_dict[(month, 120)]
                         - vol_dict[(month, 100)]) / 20).quantize(dp2)))

        print('-'*115)
        print('='*115)
