import numpy as np

class DataMunger:
    def __init__(self, summary_types):
        self.summary_types = summary_types

    def getYearVars(self, df, yearRange, varChoice1, varChoice2=None):
        '''Filter to years and in range and select variables.'''
        dff = df[(df.year >= yearRange[0]) & (df.year <= yearRange[1])]
        if varChoice2 == None:
            dff = dff[[varChoice1, 'grant_damt']] 
        else: 
            dff = dff[[varChoice1, varChoice2, 'grant_damt']]

        return dff

    def create_summaries(self, df, myVar, aggVars):
        '''Summarize data into multi-level pandas df.'''
        g = df.groupby(aggVars)
        
        rez = g.agg([np.sum, lambda x: np.shape(x)[0], np.mean]).rename(columns={
                    'sum': self.summary_types[0],
                    '<lambda>': self.summary_types[1],
                    'mean': self.summary_types[2],
                })[myVar]
        
        return rez

