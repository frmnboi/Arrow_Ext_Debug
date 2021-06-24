import pyarrow.csv as csvreader
import pyarrow.compute as compute
from pyarrow import concat_tables
import pyarrow as pa

import os


# import helperfuncs
from helperfuncs import vol_adj_close


class dataReader:
    def __init__(self):
        ticker = None

    def __str__(self):
        return self.data.__str__()

    def __repr__(self):
        return self.__str__()

    def readCSV(
        self,
        ticker,
    ):
        
        self.ticker = ticker
        self.data = csvreader.read_csv( os.getcwd()+'/'+ticker.upper() + "_google.csv" )


    # creates an arrow sequence
    def compareSpeed(self):
        #intrinsic
        #takes 2.8, 3.2, 3.7ms to complete
        #self.data=self.data.append_column("Volume_Adjusted_Close",pa.compute.divide(self.data['close'],self.data['volume']))

        #numpy conversions
        #takes 3.1 or 3.9 ms to complete
        # close=self.data['close'].to_numpy()
        # vol=self.data['volume'].to_numpy()
        # self.data=self.data.append_column("Volume_Adjusted_Close",pa.array(close/vol))
        
        #pandas conversion.  I could do partial conversions, but I know it does numpy as a backend, so it can't be faster than native numpy
        #11.2 to 15.5 ms
        # panda=self.data.to_pandas()
        # panda["Volume_Adjusted_Close"]=panda['close']/panda['volume']
        # self.data=pa.Table.from_pandas(panda)

        #custom function.  I don't know if this actually will work, as imoprt_pyarrow seems needed
        # print("import pyarrow status:")
        # print(helperfuncs.import_pyarrow())
        voladjclose=vol_adj_close(self.data['close'].combine_chunks(),self.data['volume'].combine_chunks())
        # voladjclose=helperfuncs.vol_adj_close(self.data['close'].combine_chunks(),self.data['volume'].combine_chunks())
        self.data=self.data.append_column("Volume_Adjusted_Close",voladjclose)



        



a = dataReader()
a.readCSV(
    "SPY"
)
print(a)

import pandas
print(a.data.to_pandas())

import sys

print("Array has size of: ")
print(sys.getsizeof(a.data) / 1e6)
print("Megabytes")

from datetime import datetime as dt
start=dt.now()
a.compareSpeed()
print(dt.now()-start)
print(a)
