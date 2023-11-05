import numpy as np
import json

matrix = np.load('matrix_46.npy')

# np.set_printoptions(threshold=np.inf)
res_dict = dict()

num_elements = matrix.size
res_dict['sum'] = np.sum(matrix)
res_dict['avr'] = res_dict['sum']/num_elements

# Главная диагональ
md = matrix.diagonal()
res_dict['sumMD'] = np.sum(md)
res_dict['avrMD'] = res_dict['sumMD']/md.size

sd = np.fliplr(matrix).diagonal()
# Побочная диагональ
res_dict['sumSD'] = np.sum(sd)
res_dict['avrSD'] = res_dict['sumSD']/sd.size

res_dict['max'] = matrix.max()
res_dict['min'] = matrix.min()

for key in res_dict.keys():
  res_dict[key] = float(res_dict[key])

with open('matrix_stat.json', 'w') as result:
  result.write(json.dumps(res_dict))

norm_matrix = np.ndarray( matrix.shape, dtype=float)

for i in range(0, matrix[0].size):
  for j in range(0, matrix[0].size):
    norm_matrix[i][j] = matrix[i][j] / res_dict['sum']

np.save('norm_matrix', norm_matrix)