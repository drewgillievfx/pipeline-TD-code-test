"""
oiio_challenge_1.py
Start Date: 20230131
Version: 1.0
Written by: Drew Gillie

1. Write a script that uses OIIO/OCIO to do the following operations on
laika_framing_chart.exr
    - Crop from 2348x1566 to 2048x858
    - Matte the 2048x858 image into a 2048x1080 frame with black bars top and
    bottom
    - Output this resulting 2048x1080 image as an sRGB jpeg - commit the output
    jpeg for verification
""" 


import OpenImageIO as oiio
from OpenImageIO import ImageSpec
from OpenImageIO import ImageBuf
from OpenImageIO import ImageBufAlgo
from OpenImageIO import ROI
import PyOpenColorIO as ocio
# import numpy as np
import sys

##############################################################################


def convert(image_to_convert, color_space_origin, destination_color_space,
            save_as):
    """ This function should take a linear .exr and convert to a sRGB .jpg """

    converted_image = ImageBufAlgo.colorconvert(image_to_convert,
                                                color_space_origin,
                                                destination_color_space)

    if converted_image.has_error:
        print("Error was", converted_image.geterror())
    ok = converted_image.write(save_as)
    if not ok:
        print("Error was", converted_image.geterror())

    return converted_image


def test_prints(buf):
    print(F'\n===================================================')
    print(F'Resolution is {buf.spec().width} x {buf.spec().height}')
    print(F'File Format is {buf.file_format_name} ')
    print(F'File Name is {buf.name} \n')
    print(F'Colorspace is {buf.spec()} \n')

    print(F'xbegin is {buf.xbegin} --> {buf.xend}')
    print(F'ybegin is {buf.ybegin} --> {buf.yend}\n')

    print(F'Xmin is {buf.xmin} --> {buf.xmax}')
    print(F'Ymin is {buf.ymin} --> {buf.ymax}\n')

    print(F'roi is {buf.roi}\n')


def set_pixels_black(my_buffer):
    # Set pixels to black in the area needed. Lazy way, but it works better.
    for y in range((my_buffer.ybegin), (my_buffer.yend)):
        for x in range((my_buffer.xbegin), (my_buffer.xend)):
            my_buffer.setpixel(x, y, (0.0, 0.0, 0.0))
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
        if sys.argv[1].endswith('.exr'):
            print('Checking File....')  # Only for testing purposes--------.
        else:
            print(F'This file type cannot be used with this script.')
    else:
        print('\n======================================================')
        print('There was no file passed.\nPlease run the command like:')
        print('python3 {file_path_name} {file_to_process_path}')
        print('======================================================\n')

    input_image = sys.argv[1]

    # Set names for the output files.
    cropped_out = ('CROPPED_' + input_image)
    cropped_out = cropped_out.replace('.exr', '.jpg')

    matte_out = ('MATTE_' + input_image)
    matte_out = matte_out.replace('.exr', '.jpg')

    output_filename = ('FINAL_' + input_image)
    output_filename = output_filename.replace('.exr', '.jpg')

    ##########################################################################
    """ 2. Loading Image into Buffer. """
    buf = ImageBuf(input_image)  # Create an image buffer from file.

    # test_prints(buf)
    print(F'-- Finished Loading Photo.')

    ##########################################################################
    """ 3. CONVERTING LINEAR TO sRGB. """
    converted_buf = convert(buf, 'linear', 'sRGB', output_filename)

    print(F'-- Finished Color Conversion.')

    buf = converted_buf

    ##########################################################################
    """ 4. CROPPING. """

    # Crop Resolution.
    crop_res_x = 2048
    crop_res_y = 858

    # Find difference of input image and what the cropped image should be.
    delta_x = int((buf.spec().width - crop_res_x) / 2)
    delta_y = int((buf.spec().height - crop_res_y) / 2)

    # Crop size = difference + crop resolution.
    crop_width = delta_x + crop_res_x
    crop_height = delta_y + crop_res_y

    # Crop new buffer to the specified region (should be 2048 x 858)
    empty_buffer = buf
    cropped_buf = ImageBufAlgo.crop(empty_buffer, ROI(delta_x, crop_width,
                                    delta_y, crop_height))

    # Write the cropped image to file and check dimmensions.
    cropped_buf.write(output_filename)

    print(F'-- Finished Cropping.')

    ##########################################################################
    """ 5. MATTE. """

    # Declare the matte resolution - should be the same as final resolution.
    final_res_x = 2048
    final_res_y = 1080

    # Create an image in the buffer set at the final resolution
    black_pixels = ImageSpec(final_res_x, final_res_y, 4, "uint8")
    black_buf = ImageBuf(black_pixels)

    duplicate_black_buffer = black_buf.copy()  # Needed for proper sizing.

    # Set pixels to black in the area needed. Lazy way, but it works better.
    set_pixels_black(duplicate_black_buffer)

    print(F'-- Finished Matte.')

    ##########################################################################
    """ 6. Composite foreground and background. """
    foreground = ImageBuf(output_filename)  # Cropped image.
    background = duplicate_black_buffer  # ImageBuf('test_5.jpg')  # Matte image.

    # Set point to composite cropped image over matte.
    final_delta_x = final_res_x - crop_res_x
    final_delta_y = final_res_y - crop_res_y

    final_offset_y = int((final_res_y - crop_res_y) / 2)

    oiio.ImageBufAlgo.paste(background, 0, final_offset_y, 0, 0, foreground)

    background.write(output_filename)
    print(F'-- Finished Composite.')

    ##########################################################################
    print(F'\nFINISHED SCRIPT------------\n')  # Only for testing purposes---.
