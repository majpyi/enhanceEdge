import M
import numpy as np
from change import *




while solve(raw2) == 0:
    solve(raw2)

# solve(raw2)
# change(raw2,149,56,tagp,1)
cv2.imwrite("C.jpg", raw2)

np.savetxt('re.csv', raw2, fmt="%d", delimiter=',')
np.savetxt('raw.csv', raw, fmt="%d", delimiter=',')
np.savetxt('tagp.csv', tagp, fmt="%d", delimiter=',')
