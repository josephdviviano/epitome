##   Print a 2D histogram % scatter plot discribing the correlation between  ##
##      stat maps in the same space (must have the same voxel dimensions)    ##
import numpy as np
from scipy.stats import spearmanr
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import nibabel as nib
import os

## options ####################################################################
oDir  = '/Users/jdv/Downloads'
oDat1 = 'PCC_ADNIlong_scDN_marguiles_p1000b500_STRSTRUCTblv_lv1.img'
oDat2 = 'PCCmarguiles_p1000b500_OASIS_sm0wrp_maskFIT_STRSTRUCTblv_lv1.img'
oCMap = plt.cm.bone
oPrintSVG = 0  # 1 = print, 0 = skip, may generate very large files

## Load data ##################################################################
dat1 = nib.load(os.path.join(oDir, oDat1)).get_data()
dat2 = nib.load(os.path.join(oDir, oDat2)).get_data()

# transform into vector
dims = np.shape(dat1)
nVox = dims[0]*dims[1]*dims[2]*dims[3]
dat1 = np.reshape(dat1, nVox, -1)
dat2 = np.reshape(dat2, nVox, -1)

# remove zero-values (assume outside brain mask, use smaller mask)
mask = np.intersect1d(np.union1d(np.where(dat1 > 0)[0], np.where(dat1 < 0)[0]),
	                  np.union1d(np.where(dat2 > 0)[0], np.where(dat2 < 0)[0]))
dat1 = dat1[mask]
dat2 = dat2[mask]

# compute correlations
r   = pearsonr(dat1, dat2)
rho = spearmanr(dat1, dat2)

## Plotting: 2D Histogram #####################################################
figHist  = plt.figure(1, figsize=(8,8), facecolor='white')
axHist2D = plt.subplot2grid((9,9), (1,0), colspan=8, rowspan=8)
axHistX  = plt.subplot2grid((9,9), (0,0), colspan=8)
axHistY  = plt.subplot2grid((9,9), (1,8), rowspan=8)

# plot 2DHist, and histogram for each axis
H, xEdges, yEdges = np.histogram2d(dat1, dat2, bins=(100, 100))
axHist2D.imshow(H.T, interpolation='nearest', aspect='auto', cmap=oCMap)
axHistX.hist(dat1, bins=xEdges, facecolor='black', 
	               alpha=0.5, edgecolor='white' )
axHistY.hist(dat2, bins=yEdges, facecolor='black', 
	               alpha=0.5, edgecolor='white',
	               orientation='horizontal')

# set axis limits
axHistX.set_xlim( [xEdges.min(), xEdges.max()] )
axHistY.set_ylim( [yEdges.min(), yEdges.max()] )
axHist2D.set_ylim([axHist2D.get_ylim()[1], axHist2D.get_ylim()[0]])

# remove ugly boxes & ticks
axHistX.spines['top'].set_visible(False)
axHistX.spines['right'].set_visible(False)
axHistX.spines['left'].set_visible(False)
axHistX.set_xticks([])
axHistX.set_yticks([])

axHistY.spines['top'].set_visible(False)
axHistY.spines['bottom'].set_visible(False)
axHistY.spines['right'].set_visible(False)
axHistY.set_xticks([])
axHistY.set_yticks([])

# place bin labels on 2DHist
ticks2D = np.arange(0,101,10)
axHist2D.set_xticks(ticks2D)
axHist2D.set_yticks(ticks2D)
axHist2D.set_xticklabels(np.round(xEdges[ticks2D],2), fontsize=8)
axHist2D.set_yticklabels(np.round(yEdges[ticks2D],2), fontsize=8)

# label axes & title
axHist2D.set_xlabel(oDat1, fontsize=10)
axHist2D.set_ylabel(oDat2, fontsize=10)
figHist.suptitle('Correlation of statmaps, '
	             'rho = '  + str(rho[0]) + ', r = ' + str(r[0]))

# print figure
plt.savefig(os.path.join(oDir,'2DHist.png'))
if oPrintSVG == 1:
	plt.savefig(os.path.join(oDir,'2DHist.svg'))

## Scatterplot
figScat = plt.figure()
plt.scatter(dat1, dat2, s=20, c='black', marker='.')
plt.tick_params(axis='both', labelsize=8)
plt.xlabel(oDat1, fontsize=10)
plt.ylabel(oDat2, fontsize=10)
plt.title('Correlation of statmaps, '
	      'rho = '  + str(rho[0]) + ', r = ' + str(r[0]), fontsize=12)

# print figure
plt.savefig(os.path.join(oDir,'scatter.png'))
if oPrintSVG == 1:
	plt.savefig(os.path.join(oDir,'scatter.svg'))

## JDV Jun 23 2013 ############################################################