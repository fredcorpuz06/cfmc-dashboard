import numpy as np

class DataMunger:
    def __init__(self, summary_types):
        self.summary_types = summary_types

    def get_year_vars(self, df, yearRange, myVar, aggVars):
        '''Filter to years and in range and select variables.'''
        dff = df[(df.year >= yearRange[0]) & (df.year <= yearRange[1])]
        dff = dff[[myVar] + aggVars]

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

    def sankey_manipulations(self, rez, aggVars):
        '''Restructure data for Plotly Sankey Diagram'''
        # Restructure to source & target columns
        if len(aggVars) == 2:
            rez_all = rez[aggVars + self.summary_types].rename(columns={
                aggVars[0]: 'source',
                aggVars[1]: 'target'
            })  
        else:
            rez01 = rez[aggVars + self.summary_types].rename(columns={
                aggVars[0]: 'source',
                aggVars[1]: 'target'
            })
            rez01['target'] = rez01.target + '0'

            rez12 = rez[aggVars + self.summary_types].rename(columns={
                aggVars[1]: 'source',
                aggVars[2]: 'target'
            })
            rez12['source'] = rez12.source + '0'
            
            rez_all = rez01.append(rez12, ignore_index=True, sort=True)

        # Replace source and target nodes w/ index
        source_nodes = rez_all.source.tolist()
        target_nodes = rez_all.target.tolist()
        all_nodes = set(source_nodes + target_nodes)

        myMap = {}
        for i, n in enumerate(sorted(all_nodes)):
            myMap[n] = i

        rez_all = rez_all.replace(myMap)

        return (rez_all, myMap)



