import pandas as pd
import os
ALL = [[], [], [], [], [], [], [], [], [], [], [], []]
ALL[0].append(1)
ALL[1].append(2)
ALL[2].append(3)
ALL[3].append(4)
ALL[4].append(5)
ALL[5].append(6)
ALL[6].append(7)
ALL[7].append(8)
ALL[8].append(1)
ALL[9].append(2)
ALL[10].append(3)
ALL[11].append(4)
# ALL[0].extend(SCLUP_)
# ALL[1].extend(TRFUP_)
# ALL[2].extend(CORUP_)
# ALL[3].extend(CORDOWN_)
print("转置中")
dataframe = pd.DataFrame(ALL).T
list_name = [' ','x1', 'y1', 'z1', 'x2', 'y2', 'z2', 'x3', 'y3', 'z3', 'x4', 'y4', 'z4']
save = os.path.join(r'D:\Deep-Learing\NetModel\3D\csv' , 'test' + ".csv")
dataframe.to_csv(save, header=True, index_label=list_name)