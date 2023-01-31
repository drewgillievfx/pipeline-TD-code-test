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
import sys
import numpy as np
import sys 

##############################################################################

# def matte(image):
#     # Create a black image buffer with the desired frame size
#     black_img = oiio.ImageBuf(oiio.ImageSpec(2048, 1080, 3, oiio.FLOAT))
#     black_img.fill((0, 0, 0))

#     # Paste the resized image onto the black image buffer
#     img_start = (0, 111)
#     black_img.insert(img, img_start[0], img_start[1])





##############################################################################
##############################################################################


if __name__ == '__main__':
    """
    Script Outline.
    1. 
    """
    
    
    
    
    print(F'\nSTARTING SCRIPT------------\n')  # Only for testing purposes---.
    ##########################################################################
    """ File Handling. """
    input_image = sys.argv[1]  
    filename = "bars.jpg"
    xres = 2048
    yres = 1080
    channels = 3  # RGB
    pixels = np.zeros((yres, xres, channels), dtype=np.uint8)


    out = oiio.ImageOutput.create(filename)
    spec = ImageSpec(xres, yres, channels, 'unit8')
    out.open(filename, spec)
    out.write_image(pixels)
    out.close()


    # input_filename = input_image  # Input Image.
    # cropped_out = ('CROPPED_' + input_image)  # For Testing Purposes.
    # matte_out = ('MATTE_' + input_image)  # For Testing Purposes.
    # output_filename = ('FINAL_' + input_image)  # Final Result.

    # """ Crop Resolution. """
    # crop_res_x = 2048
    # crop_res_y = 858

    # # Open the input exr image.
    # im = oiio.ImageBuf(input_filename)

    # # Get the image dimmensions.
    # width = im.spec().width
    # height = im.spec().height
    # print(F'Original width: {width}')
    # print(F'Original height: {height}')

    # # Set image new dimmensions
    # # Find difference between resolution in and cropped resolution.
    # delta_x = int((width - crop_res_x) / 2)
    # delta_y = int((height - crop_res_y) / 2)

    # # Set width to final width
    # width = width - (delta_x*2)
    # height = height - (delta_y*2)
    # print(F'New width: {width}')
    # print(F'New height: {height}')

    # # Matte the image with bars
    # # final = matte(input_filename)

    # # Get the ImageSpec of the image
    # spec = im.spec()

    # # Get the width, height, and number of channels of the image
    # width = spec.width
    # height = spec.height
    # channels = spec.nchannels

    # # Get the channel names and data types of the image
    # channel_names = spec.channelnames
    # channel_types = spec.channelformats
    # # Print the information
    # print("Image dimensions:", width, "x", height)
    # print("Number of channels:", channels)
    # print("Channel names:", channel_names)
    # print("Channel types:", channel_types)

    # # Close the image file
    # # im.close()
    # # Save the cropped image as an output
    # im.write(output_filename)

    # Output the final image as an sRGB JPEG
    # im.write(output_filename, oiio.JpgFormat(), {"color_space": "sRGB"})


    ##########################################################################
    print(F'\nFINISHED SCRIPT------------\n')  # Only for testing purposes---.
