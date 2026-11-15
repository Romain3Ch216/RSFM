import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from skimage.transform import resize
from skimage.filters import gaussian

img = np.load('img.npy')
shape = img.shape
factor = 4
high_res_shape = (factor * shape[0], factor * shape[1])
high_res = resize(img, output_shape=high_res_shape)

row, col = 50, 50
n_rows, n_cols = 30, 30

fig, ax = plt.subplots()
plt.imshow(img)
rect = patches.Rectangle([col, row], n_cols, n_rows, linewidth=3, edgecolor='r', facecolor='none')
ax.add_patch(rect)
plt.savefig('img.pdf', dpi=100, pad_inches=0.05, bbox_inches='tight')

fig, ax = plt.subplots()
plt.imshow(high_res)
rect = patches.Rectangle([factor * col, factor * row], factor * n_cols, factor * n_rows, linewidth=3, edgecolor='r', facecolor='none')
ax.add_patch(rect)
plt.savefig('high_res_img.pdf', dpi=100, pad_inches=0.05, bbox_inches='tight')

fig = plt.figure()
plt.imshow(img[row:row+n_rows, col:col+n_cols])
plt.savefig('patch.pdf', dpi=100, pad_inches=0.05, bbox_inches='tight')

fig = plt.figure()
plt.imshow(high_res[factor * row:factor * (row + n_rows), factor * col:factor * (col+n_cols)])
plt.savefig('high_res_patch.pdf', dpi=100, pad_inches=0.05, bbox_inches='tight')

sigma = 1
blurred = gaussian(img, sigma=(sigma, sigma))
fig, ax = plt.subplots()
plt.imshow(blurred)
rect = patches.Rectangle([col, row], n_cols, n_rows, linewidth=3, edgecolor='r', facecolor='none')
ax.add_patch(rect)
plt.savefig('blurred_img.pdf', dpi=100, pad_inches=0.05, bbox_inches='tight')


fig = plt.figure()
plt.imshow(blurred[row:row+n_rows, col:col+n_cols])
plt.savefig('blurred_patch.pdf', dpi=100, pad_inches=0.05, bbox_inches='tight')
