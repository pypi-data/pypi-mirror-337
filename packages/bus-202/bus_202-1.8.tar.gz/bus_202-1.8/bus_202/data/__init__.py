import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent

class DataFrames:
    _midterm = None
    _financials = None
    _exec_comp = None
    _a1_df = None
    _a3_df = None
    _gapfinder = None
    _sweet_things = None
    _sweet_things_simple = None
    _new_ceo = None
    _restate = None
    
    @property
    def gapfinder(self):
        if self._gapfinder is None:
            self._gapfinder = pd.read_excel(DATA_DIR / 'gapfinder.xlsx')
        return self._gapfinder
    
    @property
    def midterm(self):
        if self._midterm is None:
            self._midterm = pd.read_excel(DATA_DIR / 'midterm.xlsx')
        return self._midterm
    
    @property
    def financials(self):
        if self._financials is None:
            self._financials = pd.read_excel(DATA_DIR / 'financials.xlsx')
        return self._financials
    
    @property
    def exec_comp(self):
        if self._exec_comp is None:
            self._exec_comp = pd.read_excel(DATA_DIR / 'exec_comp.xlsx')
        return self._exec_comp
    
    @property
    def a1_df(self):
        if self._a1_df is None:
            self._a1_df = pd.read_excel(DATA_DIR / 'a1_df.xlsx')
        return self._a1_df
    
    @property
    def a3_df(self):
        if self._a3_df is None:
            self._a3_df = pd.read_excel(DATA_DIR / 'a3_df.xlsx')
        return self._a3_df
    
    @property
    def sweet_things(self):
        if self._sweet_things is None:
            self._sweet_things = pd.read_excel(DATA_DIR / 'sweet_things.xlsx')
        return self._sweet_things
    
    @property
    def sweet_things_simple(self):
        if self._sweet_things_simple is None:
            self._sweet_things_simple = pd.read_excel(DATA_DIR / 'sweet_things_simple.xlsx')
        return self._sweet_things_simple
    
    @property
    def new_ceo(self):
        if self._new_ceo is None:
            self._new_ceo = pd.read_excel(DATA_DIR / 'new_ceo.xlsx')
        return self._new_ceo
    
    @property
    def restate(self):
        if self._restate is None:
            self._restate = pd.read_excel(DATA_DIR / 'restate.xlsx')
        return self._restate

# Create a single instance
_data = DataFrames()

# Define module-level functions that return the data
def midterm():
    return _data.midterm

def financials():
    return _data.financials

def exec_comp():
    return _data.exec_comp

def a1_df():
    return _data.a1_df

def a3_df():
    return _data.a3_df

def gapfinder():
    return _data.gapfinder

def sweet_things():
    return _data.sweet_things

def sweet_things_simple():
    return _data.sweet_things_simple

def new_ceo():
    return _data.new_ceo

def restate():
    return _data.restate
