"""
oiio_challenge_1.py
Start Date: 20230131
Version: 1.0
Written by: Drew Gillie

1. Write a script that uses OIIO/OCIO to do the following operations on laika_framing_chart.exr
    - Crop from 2348x1566 to 2048x858
    - Matte the 2048x858 image into a 2048x1080 frame with black bars top and bottom
    - Output this resulting 2048x1080 image as an sRGB jpeg - commit the output jpeg for verification
"""


import OpenImageIO as oiio
from OpenImageIO import ImageSpec
from OpenImageIO import ImageInput
from OpenImageIO import ImageOutput
from OpenImageIO import ImageBuf
from OpenImageIO import ImageBufAlgo
from OpenImageIO import ROI
import numpy as np
import sys 

##############################################################################
"""
Currently, a lot of this code does not work when run through a function and is
done in the main.  This might be doable if writing an image in the processing
of this script is acceptable, however this is not the best case scenario.
"""


def check_file_type(file_to_check):
    if file_to_check.endswith('.exr'):
        return True
    else:
        return False


def set_pixels_black(my_buffer):
    # Set pixels to black in the area needed. Lazy way, but it works better.
    for y in range((my_buffer.ybegin), (my_buffer.yend)) :
        for x in range((my_buffer.xbegin), (my_buffer.xend)) :
            my_buffer.setpixel (x, y, (0.0, 0.0, 0.0))
##############################################################################
##############################################################################
if __name__ == '__main__':
    """
    Script Outline.
    1. File check and handling.
    2. Load image into buffer.
    3. Convert from linear to sRGB
    4. Crop image.
    5. Create an image of all black pixels (matte)
    6. Composite the cropped and matte images together
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

    # Set some names for the output files.
    cropped_out = ('CROPPED_' + input_image)  # For Testing Purposes.
    cropped_out = cropped_out.replace('.exr', '.jpg')
    
    matte_out = ('MATTE_' + input_image)  # For Testing Purposes.
    matte_out = matte_out.replace('.exr', '.jpg')
    
    output_filename = ('FINAL_' + input_image)  # Final Result.
    output_filename = output_filename.replace('.exr', '.jpg')

    print (F'-- Test 1: File Check.')


    ##########################################################################
    """ 2. Loading Image into Buffer. """
    ## in
    buf = ImageBuf(input_image)  # Create an image buffer from file 

    print (F'\n===================================================')
    print (F'Resolution is {buf.spec().width} x {buf.spec().height}')
    print (F'File Format is {buf.file_format_name} ')
    print (F'File Name is {buf.name} \n')
    # print (F'Colorspace is {buf.spec()} \n')

    # print (F'xbegin is {buf.xbegin} --> {buf.xend}')
    # print (F'ybegin is {buf.ybegin} --> {buf.yend}\n')

    # print (F'Xmin is {buf.xmin} --> {buf.xmax}')
    # print (F'Ymin is {buf.ymin} --> {buf.ymax}\n')

    # print (F'roi is {buf.roi}\n')

    buf.write('test_2.jpg')
    print (F'-- Finished opening photo.')
    print (F'-- Test 2: Image Check.')


    ##########################################################################
    """ 3. CONVERTING LINEAR TO sRGB. """
    color_space_origin = 'linear'
    destination_color_space = 'sRGB'

    Src = buf  # Set source to input file 
    Dst = ImageBufAlgo.colorconvert(Src, color_space_origin, destination_color_space)  

    if Dst.has_error :
        print("Error was", Dst.geterror())
    ok = Dst.write('converted.jpg')
    if not ok:
        print("Error was", Dst.geterror())
    
    print (F'-- Finished converting photo.')

    # convert = ImageBuf(Dst)    
    buf = Dst
    buf.write('test_3.jpg')
    print (F'-- Test 3: Conversion Check.')
    
    ##########################################################################
    """ 4. CROPPING. """

    # Crop Resolution. 
    crop_res_x = 2048
    crop_res_y = 858

    # Set difference of input image and what the cropped image should be.
    delta_x = int((buf.spec().width - crop_res_x) / 2)
    delta_y = int((buf.spec().height - crop_res_y) / 2)
    print (F'deltaX is {delta_x} deltaY is {delta_y} \n')

    crop_width = delta_x + crop_res_x
    crop_height = delta_y + crop_res_y

    # # Set pixels to blue in the area needed. TESTING PURPOSES
    # for y in range((buf.ybegin+delta_y), (buf.yend-delta_y)) :
    #     for x in range((buf.xbegin+delta_x), (buf.xend-delta_x)) :
    #         buf.setpixel (x, y, (0.0, 0.0, 1.0))

    # Crop B to the specified region (should be 2048 x 858)
    A = buf
    cropped_buf = ImageBufAlgo.crop(A, ROI(delta_x, crop_width, delta_y, crop_height))
    print (F'\n===================================================')

    # Write the cropped image to file and check dimmensions
    cropped_buf.write(cropped_out)
    print (F'-- Finished Cropping.')

    cropped_buf.write('test_4.jpg')
    print (F'-- Test 4: Crop Check.')

    ##########################################################################
    """ 5. MATTE. """
    # Declare the matte resolution - should be the same as final resolution.
    final_res_x = 2048
    final_res_y = 1080

    # Create an image in the buffer set at the final resolution
    black = ImageSpec(final_res_x, final_res_y, 4, "uint8")
    black_buf = ImageBuf(black)

    # Make a separate, duplicate copy of A
    # M = B.copy()

    # Set pixels to black in the area needed. Lazy way, but it works better.
    matte = set_pixels_black(black_buf)  # Returns a black image in RGB
    # set_pixels_black(M)  # Returns a black image in RGB
    black_buf = ImageBuf(matte)

    # black_buf.write(matte_out)
    # matte.write(matte_out)
    # M.write(matte_out)

    print (F'{matte_out} has been created \n')
    print (F'Matte Width {final_res_x} Matte Height {final_res_y} \n')

    
    final_delta_x = final_res_x - crop_res_x
    final_delta_y = final_res_y - crop_res_y
    print (F'-- Finished Matte.')

    black_buf.write('test_5.jpg')
    print (F'-- Test 5: Matte Check.')

    ##########################################################################
    """ 6. Composite foreground and background. """
    foreground = cropped_buf
    background = black_buf

    # Set where to composit at
    roi = ROI(delta_x, crop_width, delta_y, crop_height)
    composite = ImageBufAlgo.over(foreground,background)
    composite.write(output_filename)
    print (F'-- Finished Composite.')

       
    composite.write('test_6.jpg')
    print (F'-- Test 6: Composite Check.')

    ##########################################################################
    print(F'\nFINISHED SCRIPT------------\n')  # Only for testing purposes---.
