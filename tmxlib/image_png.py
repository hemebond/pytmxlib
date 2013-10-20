
from __future__ import division

from array import array
from StringIO import StringIO

import png

import tmxlib
import tmxlib.image_base


class PngImage(tmxlib.image_base.Image):
    def load_image(self):
        """Load the image from self.data, and set self.size
        """
        try:
            self._image_data
            return self.size
        except AttributeError:
            reader = png.Reader(bytes=self.data).asRGBA8()
            w, h, data, meta = reader
            self._image_data = tuple(data)
            if self._size:
                assert (w, h) == self._size
            else:
                self._size = w, h
            return w, h

    @property
    def image_data(self):
        try:
            return self._image_data
        except AttributeError:
            self.load_image()
            return self._image_data

    def get_pixel(self, x, y):
        x, y = self._wrap_coords(x, y)
        return tuple(v / 255 for v in self.image_data[y][x * 4:(x + 1) * 4])

    def _repr_png_(self, _crop_box=None):
        """Hook for IPython Notebook

        See: http://ipython.org/ipython-doc/stable/config/integrating.html
        """
        if _crop_box:
            left, up, right, low = _crop_box
            data = [l[left * 4:right * 4] for l in self.image_data[up:low]]
            out = StringIO()
            png.from_array(data, 'RGBA').save(out)
            return out.getvalue()
        return self.data
