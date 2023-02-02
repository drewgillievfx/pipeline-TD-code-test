import PyOpenColorIO as OCIO
# from PyOpenColorIO import CONSTANTS
import OpenImageIO as oiio
from OpenImageIO import ImageSpec
from OpenImageIO import ImageInput
from OpenImageIO import ImageOutput
from OpenImageIO import ImageBuf
from OpenImageIO import ImageBufAlgo
from OpenImageIO import ROI
import sys 


"""
2. Write a script that uses dcraw or other command line raw developing software to process the provided raw file.
    - To the best of my knowledge there isn't a python solution here - you will need to use subprocess to execute a command.
    - Convert from .cr2 to ACEScg .exr file using dcraw - commit a sample file for verification
    - Convert that ACEScg exr file to an sRGB .jpeg - commit a sample file for verification


"""

def convert(image_to_convert, cs_origin, cs_destination, save_as ):
    """ This function should take a linear .exr and convert to a sRGB .jpg """

    input_image = image_to_convert  # 'test.exr'
    color_space_origin = cs_origin  # 'linear'
    destination_color_space = cs_destination  # 'sRGB'

    Src = ImageBuf(input_image)  
    Dst = ImageBufAlgo.colorconvert(Src, color_space_origin, destination_color_space)  

    if Dst.has_error :
        print("Error was", Dst.geterror())
    ok = Dst.write(save_as)
    if not ok:
        print("Error was", Dst.geterror())

##############################################################################
##############################################################################
if __name__ == '__main__':
    """
    Script Outline.
    1. .cr2 to ACEScg .exr file using dcraw
    2. Commit sample
    3. ACEScg exr file to an sRGB .jpeg
    4. commit sample
    """
    
    print(F'\nSTARTING SCRIPT------------\n')  # Only for testing purposes---.
    get_image = sys.argv[1]
    
    convert(get_image, 'linear', 'sRGB', 'CONVERT.jpg' )
    
    

##########################################################################
print(F'\nFINISHED SCRIPT------------\n')  # Only for testing purposes---.

   