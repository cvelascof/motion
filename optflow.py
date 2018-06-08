"""Interface and utility methods for different optical flow algorithms."""

# TODO: Implement this method.
def get_method(name):
  """Return a callable function for the optical flow method corresponding to
  the given name. The available options are:\n\

  +----------------------------------------------------------------------------+
  | Python-based implementations                                               |
  +-------------------+--------------------------------------------------------+
  |     Name          |              Description                               |
  +===================+========================================================+
  |  lucaskanade      | OpenCV implementation of the Lucas-Kanade method       |
  |                   | with interpolated motion vectors for areas with no     |
  |                   | precipitation.                                         |
  +-------------------+--------------------------------------------------------+

  +----------------------------------------------------------------------------+
  | Methods implemented in C (these require separate compilation and linkage)  |
  +-------------------+--------------------------------------------------------+
  |     Name          |              Description                               |
  +===================+========================================================+
  |  brox             | implementation of the variational method of Brox et al.|
  |                   | (2004) from IPOL (http://www.ipol.im/pub/art/2013/21)  |
  +-------------------+--------------------------------------------------------+
  |  clg              | implementation of the Combined Local-Global (CLG)      |
  |                   | method of Bruhn et al., 2005 from IPOL                 |
  |                   | (http://www.ipol.im/pub/art/2015/44)                   |
  +-------------------+--------------------------------------------------------+
  """
  pass