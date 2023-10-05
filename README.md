# ColorSeasonMatch

## Dependencies
- CV2 (pip install opencv-python)
- Tk
- Colormath (pip install colormath)
- numpy

## Common problems
### 'numpy._DTypeMeta' object is not subscriptable
pip install --upgrade numpy

### module 'numpy' has no attribute 'asscalar'
Open the line where the error is coming from in color_diff.py
Change numpy.asscalar(delta_e) to numpy.asarray(delta_e).item()

