#!/usr/bin/env python

import pandas as pd
import nibabel as nib
import numpy as np

def relabel(data, db):
    aff = data.get_affine()
    hdr = data.get_header()
    img = data.get_data()
    out = np.zeros(img.shape)

    # find all nodes in each network
    for network in np.unique(db['Network']):
        nodes = db.loc[db['Network'] == network, 'Node']

        # find all voxels in each node
        for node in nodes:
            idx = np.where(img == node)
            out[idx] = network

    out = nib.nifti1.Nifti1Image(out, aff, header=hdr)
    return(out)

db = pd.read_csv('shen_268_parcellation_networklabels.csv')

d1 = nib.load('shen_1mm_268_parcellation.nii.gz')
d2 = nib.load('shen_2mm_268_parcellation.nii.gz')

d1 = relabel(d1, db)
d2 = relabel(d2, db)

d1.to_filename('shen_1mm_268_networks.nii.gz')
d2.to_filename('shen_2mm_268_networks.nii.gz')
