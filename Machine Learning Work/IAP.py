# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 21:19:42 2019

@author: Michael Carolan, Steven Yang
"""
import numpy as np
import pynance as pn

def get_stock_prices(ticker, value, date_range):
    """
    Return a dictionary of the value information for a stock with ticker over
    date_range
    
    Inputs:
        ticker (string): Ticker of desired stock
        value (string): High, Low, Open, Close, Adj Close or Volume, data to return
        date_range (tuple): (start_year, end_year) as ints
    
    Outputs:
        values (dict): All values in date_range keyed on Timestamp
    """
    #lookup ticker on range
    stock = pn.data.get(ticker, str(date_range[0]), str(date_range[1]))
    raw = stock.to_dict()               #dicts keyed on values with timestamps
    
    #return dict on desired value
    values = raw[value]
    
    return values
    
    
def prices_to_bools(values):
    """
    Return a dictionary of bools indicating whether the value increased (True)
    or decreased(False)
    
    Inputs:
        values (dict): from get_stock_prices()
        
    Outputs:
        bools (dict): bools indicating up or down keyed on Timestamp, based on the next day
    """
    bools = {}
    nums = list(values.values())
    new_nums = []
    
    for i in range(len(nums)-1):  # create bools
        val = nums[i+1] > nums[i]
        new_nums.append(val)
        
    keys = list(values.keys())
    keys.pop(0)  # remove first index because we can't compare it
    
    for i in range(len(keys)):
        bools[keys[i]] = new_nums[i]
        
    return bools
    
    
    
def get_data(ticker, value, date_range):
    """
    Return a formatted array
    
    Inputs:
        ticker (string): Ticker of desired stock
        value (string): High, Low, Open, Close, Adj Close or Volume, data to return
        date_range (tuple): (start_year, end_year) as ints
        
    Outputs:
        array (numpy.array): array for training
    """
    values = get_stock_prices(ticker, value, date_range)
    bools = prices_to_bools(values)
    
    return np.array(list(bools.values()))