import PyOpenColorIO as ocio
import OpenImageIO as oiio
from OpenImageIO import ImageSpec
from OpenImageIO import ImageInput
from OpenImageIO import ImageOutput
from OpenImageIO import ImageBuf
from OpenImageIO import ImageBufAlgo
from OpenImageIO import ROI
import sys
import subprocess


"""
2. Write a script that uses dcraw or other command line raw developing
software to process the provided raw file.
    - To the best of my knowledge there isn't a python solution here
    - you will need to use subprocess to execute a command.
    - Convert from .cr2 to ACEScg .exr file using dcraw
    - commit a sample file for verification
    - Convert that ACEScg exr file to an sRGB .jpeg
    - commit a sample file for verification


"""
def check_file_type(file_to_check):
    if file_to_check.endswith('.cr2'):
        return True
    else:
        return False


def convert(image_to_convert, cs_origin, cs_destination, save_as ):
    """ This function should take a linear .exr and convert to a sRGB .jpg """

    input_image = image_to_convert  # 'test.exr'
    color_space_origin = cs_origin  # 'linear'
    destination_color_space = cs_destination  # 'sRGB'

    Src = ImageBuf(input_image)  
    Dst = ImageBufAlgo.colorconvert(Src, color_space_origin, destination_color_space)  

    # Error checking.
    if Dst.has_error :
        print("Error was:", Dst.geterror())
        print(F'\nTried Colorspace Conversion: {cs_origin} --> {cs_destination}')
    else:
        print(F'\nColorspace CONVERTED from {cs_origin} --> {cs_destination}')
        print(F'Converted: {export_1}')

    ok = Dst.write(save_as)
    if not ok:
        print("Error was:", Dst.geterror())
    else:
        print(F'SUCCSESS!')
    

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
    ##########################################################################
    """ 1. File Handling. """
    # Bring in the image through the terminal when this script is called.
    if len(sys.argv) > 1:
        if check_file_type(sys.argv[1]):
            print('Checking File....')  # Only for testing purposes--------.
        else:
            print(F'This file type cannot be used with this script.')
    else:
        print('\n======================================================')
        print('There was no file passed.\nPlease run the command like:')
        print('python3 {file_path_name} {file_to_process_path}')
        print('======================================================\n')

    input_image = sys.argv[1]

    export_1 = ('ACEScg_' + input_image)
    export_1 = export_1.replace('.cr2', '.exr')


    export_2 = ('sRGB_' + input_image)
    export_2 = export_2.replace('.cr2', '.jpg')


    ##########################################################################
    """ 2. DCRAW to tiff. """

    print('\n---------- DCRAW ----------')

    # Call dcraw to convert the CR2 file to a TIFF file
    subprocess.call(["dcraw", "-v", "-4" "-o[6]", "-w", input_image])
    
    print('---------------------------\n')

    print(F'Photo to be processed: {input_image}')
    tiff = input_image.replace('.cr2', '.exr')
    # jpg = tiff.replace('.tiff', '.jpg')
    print(F'dcraw -->: {tiff}')

    ##########################################################################
    """ 3. Convert from raw into ACEScg. """
    cs_1 = 'sRGB'
    cs_2 = 'acescg'

    convert(tiff, cs_1, cs_2, export_1 )
    print(F'Commit 1: {export_1}')

    ##########################################################################
    """ 4. Convert from ACEScg to sRGB. """
    cs_3 = 'acescg'
    cs_4 = 'sRGB'

    # convert(tiff, cs_3, cs_4, export_2 )
    # print(F'Commit 2: {export_2}')
   

    ##########################################################################
    print(F'\nFINISHED SCRIPT------------\n')  # Only for testing purposes---.

   