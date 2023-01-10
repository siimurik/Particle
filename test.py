# Import all the necessary packages
#import uproot  # check out the documentation about the basics at https://uproot.readthedocs.io/en/latest/basic.html
import os
import glob
import matplotlib.pyplot as plt
import awkward as ak
import datetime as dt
import numpy as np
import vector
import itertools
vector.register_awkward()

#path to parquet files
DATA_DIR = "."
PATHS = list(set(glob.glob(os.path.join(DATA_DIR, '*.parquet'))))

#filtering function
def createFilter(data,minMu,minEl):
    mu_isolation_cut = ak.sum(abs(data.Muon_pfRelIso04_all) < 0.4, axis=1) == minMu
    muon_pt_cut = ak.sum(data.Muon_pt > 5, axis=1) ==minMu
    muon_eta_cut = ak.sum(abs(data.Muon_eta) < 2.4, axis=1) == minMu
    muon_sip_cut = ak.sum(abs(data.Muon_sip3d) < 4, axis=1) == minMu
    muon_dxy_cut = ak.sum(abs(data.Muon_dxy) < 0.5, axis=1) == minMu
    muon_dz_cut = ak.sum(abs(data.Muon_dz) < 1.0, axis=1) == minMu
    mu_cuts = mu_isolation_cut * muon_pt_cut * muon_eta_cut * muon_sip_cut * muon_dxy_cut * muon_dz_cut

    el_isolation_cut = ak.sum(abs(data.Electron_pfRelIso03_all) < 0.4, axis=1) == minEl
    el_pt_cut = ak.sum(data.Electron_pt > 7, axis=1) ==minEl
    el_eta_cut = ak.sum(abs(data.Electron_eta) < 2.5, axis=1) == minEl
    el_sip_cut = ak.sum(abs(data.Electron_sip3d) < 4, axis=1) == minEl
    el_dxy_cut = ak.sum(abs(data.Electron_dxy) < 0.5, axis=1) == minEl
    el_dz_cut = ak.sum(abs(data.Electron_dz) < 1.0, axis=1) == minEl
    el_cuts = el_isolation_cut * el_pt_cut * el_eta_cut * el_sip_cut * el_dxy_cut * el_dz_cut

    return mu_cuts * el_cuts

#this whole thing should be in a loop
start=dt.datetime.now()
for inf in PATHS:

    #reading the files
    data=ak.from_parquet(inf)

    # E and mu impact parameters and their significance
    data['Muon_ip3d']=np.sqrt(data.Muon_dxy*data.Muon_dxy + data.Muon_dz*data.Muon_dz)
    data['Muon_sip3d']=data.Muon_ip3d/np.sqrt(data.Muon_dxyErr*data.Muon_dxyErr + data.Muon_dzErr*data.Muon_dzErr)
    data['Electron_ip3d']=np.sqrt(data.Electron_dxy*data.Electron_dxy + data.Electron_dz*data.Electron_dz)
    data['Electron_sip3d']=data.Electron_ip3d/np.sqrt(data.Electron_dxyErr*data.Electron_dxyErr + data.Electron_dzErr*data.Electron_dzErr)

    #using the filtering function
    fourMu    = createFilter(data,4,0)
    twoMuTwoE = createFilter(data,2,2)
    fourEl    = createFilter(data,0,4)

    hzz4mu   = data[fourMu].to_list()
    hzz2e2mu = data[twoMuTwoE].to_list()
    hzz4e    = data[fourEl].to_list()

    # Sample sizes:
    print("Higgs to ZZ to 4 muons sample size: %i" % len(hzz4mu))
    print("Higgs to ZZ to 2 electrons and 2 muons sample size: %i" % len(hzz2e2mu))
    print("Higgs to ZZ to 4 electrons sample size: %i" % len(hzz4e))
    print(inf)
stop=dt.datetime.now()
print(stop-start)

print(hzz4mu[0])