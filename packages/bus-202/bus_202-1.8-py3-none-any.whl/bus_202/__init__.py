import pandas as pd
from pathlib import Path
from .data_visualization.trim import trim
from .data_visualization.boxplot import boxplot
from .data_visualization.histogram import histogram
from .data_visualization.scatter import scatter
from .data import midterm, financials, exec_comp, a1_df, a3_df, gapfinder, sweet_things, sweet_things_simple, new_ceo, restate
from .stats.ci import ci
from .stats.reg import reg

# Add this line to expose the functions at package level
__all__ = ['trim', 'boxplot', 'histogram', 'ci', 
           'midterm', 'financials', 'exec_comp', 
           'a1_df', 'a3_df', 'gapfinder', 'sweet_things',
           'sweet_things_simple', 'reg', 'scatter']
