# Import all the necessary packages
import sys
import uproot  # check out the documentation about the basics at https://uproot.readthedocs.io/en/latest/basic.html
import os
import glob
import matplotlib.pyplot as plt
import awkward as ak
import datetime as dt
import vector

DATA_DIR = "/home/siimep_x11/Documents/Magister/Particle"
PATHS = list(set(glob.glob(os.path.join(DATA_DIR, '*.root'))))

start=dt.datetime.now()
# For the purposes of this lesson, let us open only the first of the MC files.
#for infile in PATHS:
infile = sys.argv[1]
events = uproot.open(infile + ":Events") # Take the events directory of the .root file
filtered = events.arrays(None,"(nMuon+nElectron>3)")
outfile = infile.split("/")[-1].replace('root', 'parquet')
ak.to_parquet(filtered,outfile)

stop=dt.datetime.now()
print(stop-start)

# HOWTO: >python3 reducesd_dataset.py  Run2012C_DoubleMuParked.root 

# In order to just browse the contents of the events like datatypes and branch names:
#events.show()