# -*- coding: utf-8 -*-
"""
This module provides a thin wrapper around pillow allowing us to easily create and manipulate images.

@author: C. Andrews, A. Vaccari

2022-04-20  Modified __repr__ to fit an entire line if 8-bit mono
2025-01-06  Removed the dependency on `numpy` and added a `Row` class to allow for 2D array notation.
"""


from PIL import Image
    

class MiddImage:
    """
    This class provides a thin wrapper around the PIL Image class. It boils access down to some basic functionality and also allows for direct access to the pixels.

    Access to the pixels can be done using 2D array notation (e.g., img[x][y]) or using a tuple (e.g., img[x,y]). The former will feel more natural to new Python programmers, but is 50% slower. 
    """
    class Row:
        """
        Hidden helper class that allows us to access a row of pixels using 2D array notation.
        """
        def __init__(self, image, row):
            self.image = image
            self.row = row

        def __getitem__(self, index):
            return self.image[self.row, index]
        
        def __setitem__(self, index, value):
            self.image[self.row, index] = value
    
    def __init__(self, data=None, width=None, height=None, mode='RGB' ):
        if data is None:
            self._data = Image.new(mode, (width, height))
        else:
            self._data = data
        self._pixels = self._data.load()
    
    def __getitem__(self, index):
        """
        Get the pixel at the specified 'index'.
        The 'index' should be a tuple.
        """
        if type(index) == int:
            return MiddImage.Row(self, index)
        else:
            return self._pixels[index]
    
    
    def __setitem__(self, index, value):
        """
        Set the pixel at location 'index'.
        The 'value' should be a three channel tuple.
        """
        self._pixels[index] = value
        

    def __getattr__(self, attr):
        """
        Passes through attributes to the underlying image object.

        Most important attributes are `width`,`height`, and `mode`.
        """
        return getattr(self._data, attr)
    

    def __repr__(self):
        """
        Show the pixels of the image.
        """
        return repr(list(self._data.getdata()))
        
    def save(self, filename):
        """
        Save the image as 'filename' into the current working directory.
        """
        self._data.save(filename)
    
    def show(self):
        """
        Show the image.
        """
        self._data.show()
    
    def copy(self):
        """
        Returns a new MiddImage with identical contents.
        """
        new_image = MiddImage(self._data.copy())
        return new_image
    
    
def new(width, height, mode='RGB'):
    """
    Create a new image with the specified width and height.
    """
    return MiddImage(width=width, height=height, mode=mode)


def open(filename):
    """
    Open an image file located in 'filename' (which is assumed to be in the working directory
    or an absolute path.
    """
    image_data = Image.open(filename)
    new_image = MiddImage(data=image_data)
    return new_image