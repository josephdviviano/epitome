import os
import copy
import csv
import numpy as np

# init some useful variables
dir_ana = '/srv/MRI/ANALYSIS/REST/'

# define the things
labels = [('Dorsal attention A', (-22, -2, 54)), 
          ('Dorsal attention B', (-34, -38, 44)), 
          ('Dorsal attention C', (-18, -69, 51)),
          ('Dorsal attention D', (-51, -64, -2)),
          ('Dorsal attention E', (-8, -63, 57)),
          ('Dorsal attention F', (-49, 3, 34)), 
          ('Default A', (-27, 23, 48)),
          ('Default B', (-41, -60, 29)),
          ('Default C', (-64, -20, -9)),
          ('Default D', (-7, 49, 18)),
          ('Default E', (-25, -32, -18)),
          ('Default F', (-7, -52, 26))]

# labels = [('Dorsal attention A', (-22, -2, 54)), 
#           ('Dorsal attention B', (-34, -38, 44)), 
#           ('Dorsal attention C', (-18, -69, 51)),
#           ('Dorsal attention D', (-51, -64, -2)),
#           ('Dorsal attention E', (-8, -63, 57)),
#           ('Dorsal attention F', (-49, 3, 34)), 
#           ('Default A', (-27, 23, 48)),
#           ('Default B', (-41, -60, 29)),
#           ('Default C', (-64, -20, -9)),
#           ('ATOL mPFC', (-4, 62, 14)),
#           ('Default E', (-25, -32, -18)),
#           ('ATOL PCC', (-10, -48, 36))]

# do the things

column_names = []
# come up with column names
for x in range(len(labels)):
    for y in range(len(labels)):
        if x < y:
            column_names.append(str(labels[x][0] + '*' + labels[y][0]))

# open a CSV file
with open('ROI_distances.txt', 'wb') as csvfile:
    out = csv.writer(csvfile, delimiter='\t')
    
    # write header
    out.writerow(column_names)

    # write each row (1 per subject)
    rowdata = []
    for x in range(len(labels)):
        for y in range(len(labels)):
            if x < y:
                d = np.sqrt(((labels[x][1][0] - labels[y][1][0])**2 +
                             (labels[x][1][1] - labels[y][1][1])**2 +
                             (labels[x][1][2] - labels[y][1][2])**2))
                rowdata.append(str(d))
    out.writerow(rowdata)

csvfile.close()
