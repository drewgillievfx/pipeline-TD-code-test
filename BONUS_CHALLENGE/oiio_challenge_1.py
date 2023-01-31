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

def crop(image):
    # Create a black image buffer with the desired frame size
    black_img = oiio.ImageBuf(oiio.ImageSpec(2048, 1080, 3, oiio.FLOAT))
    black_img.fill((0, 0, 0))

    # Paste the resized image onto the black image buffer
    img_start = (0, 111)
    black_img.insert(img, img_start[0], img_start[1])

    

    # buf.xbegin = 150
    # buf.xend = 2198
    # buf.ybegin = 354
    # buf.yend = 1212


def matte(matte_name, width, height):
    # Create a black image buffer with the desired frame size
    channels = 3  # RGB
    pixels = np.zeros((height, width, channels), dtype=np.uint8)


    out = oiio.ImageOutput.create(matte_name)
    spec = ImageSpec(width, height, channels, 'unit8')
    out.open(matte_name, spec)
    out.write_image(pixels)
    out.close()

    

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
    input_image = sys.argv[1]  # Input Image.
    cropped_out = ('CROPPED_' + input_image)  # For Testing Purposes.
    matte_out = ('MATTE_' + input_image)  # For Testing Purposes.
    output_filename = ('FINAL_' + input_image)  # Final Result.


    """ Crop Resolution. """
    crop_res_x = 2048
    crop_res_y = 858

    ##########################################################################
    # Returns a black image in RGB
    matte(matte_out, 2048, 1080)
    black_buf = ImageBuf(matte_out)

    ## in
    buf = ImageBuf(input_image)  # Create an image buffer from file 

    print (F'\n===================================================')
    print (F'Resolution is {buf.spec().width} x {buf.spec().height}')
    print (F'File Format is {buf.file_format_name} ')
    print (F'File Name is {buf.name} \n')

    print (F'xbegin is {buf.xbegin} --> {buf.xend}')
    print (F'ybegin is {buf.ybegin} --> {buf.yend}\n')

    print (F'Xmin is {buf.xmin} --> {buf.xmax}')
    print (F'Ymin is {buf.ymin} --> {buf.ymax}\n')

    print (F'roi is {buf.roi}\n')
    ##########################################################################
    """ CROPPING. """
    # Set difference of input image and what the cropped image should be.
    delta_x = int((buf.spec().width - crop_res_x) / 2)
    delta_y = int((buf.spec().height - crop_res_y) / 2)
    print (F'deltaX is {delta_x} deltaY is {delta_y} \n')

    crop_width = delta_x + crop_res_x
    crop_height = delta_y + crop_res_y

    # set pixels to blue in the area needed.
    for y in range((buf.ybegin+delta_y), (buf.yend-delta_y)) :
        for x in range((buf.xbegin+delta_x), (buf.xend-delta_x)) :
            buf.setpixel (x, y, (0.0, 0.0, 1.0))

    # Set B to be the upper left 200x100 region of A
    A = buf
    B = ImageBufAlgo.crop(A, ROI(delta_x,crop_width,delta_y,crop_height))
    ##########################################################################


    # Crop Size.
    # buf.spec().width = 2048
    # buf.spec().height = 858

    # Final Crop Size.
    # buf.spec().width = 2048
    # buf.spec().height = 1080
    print (F'\n===================================================')

    print (F'Final Resolution is {buf.spec().width} x {buf.spec().height}')
    ##########################################################################

    """ Composite foreground and background. """
    fg = ImageBuf('test1.exr') 
    bg = buf 
    dest = ImageBufAlgo.over(fg,bg)
    ##########################################################################
    """ Final writing of image and saving file. """
    # buf.write(output_filename)
    B.write(output_filename)
    # dest.write(output_filename)
    
    ##########################################################################


    # xorigin = fullwidth - cropwidth
    # yorigin = fulllength - croplength    # Crop window position

    # # pixels = np.zeros((croplength, cropwidth, 3), dtype="uint8")
    

    # # spec = ImageSpec(cropwidth, croplength, 3, "uint8")
    # # buf = ImageBuf(spec)  # Constructs a buffer for the image

    # buf.set_full (0, 1024, 0, 768, 0, 1)
    # pixels = buf.get_pixels(oiio.FLOAT)
    
    # ImageBuf.xmin = xorigin
    # ImageBuf.xmax = cropwidth + xorigin + 1  # must go 1 past max
    # ImageBuf.ymin = yorigin
    # ImageBuf.ymax = yorigin + yorigin + 1  # must go 1 past max

    # # Set the whole image to red (the dumb slow way, but it works):
    # for y in range(buf.ybegin, buf.yend) :
    #     for x in range(buf.xbegin, buf.xend) :
    #         buf.setpixel (x, y, (1.0, 0.0, 0.0))

    # buf.set_pixels(roi(), buf)


    # spec.full_x = 0
    # spec.full_y = 0

    # spec.width = fullwidth
    # spec.width = fulllength

    # spec.x = xorigin
    # spec.y = yorigin

    # out = ImageOutput.open(cropped_out, spec)

    # z = 0   # Always zero for 2D images
    # for y in range(yorigin, yorigin+croplength):
    #     out.write_scanline(y, z, 'UINT8', pixels[y-origin:y-yorigin+1])
    # out.close()


# A = ImageBuf("A.tif")

# # Make a separate, duplicate copy of A
# B = A.copy()

# # Make another copy of A, but converting to float pixels
# C = A.copy ("float")

# # Make another copy of A, but converting to float pixels
# C = ImageBuf()
# C.copy (A, oiio.FLOAT)



    ##########################################################################


    # fg =ImageBuf(im)
    # bg =ImageBuf('foo.jpg')
    # dst = ImageBufAlgo.over(bg, fg)

    # Open the output image
    # output_image = oiio.ImageOutput.create("cropped.exr")
    # output_image.open(output_filename, spec)
    # output_image.write(output_filename)

    # Write the cropped image to the output file
    # output_image.open(spec)
    # output_image.write_image(oiio.FLOAT, im.channel(0, ybegin, xbegin))

    # Close the input and output images
    # im.close()
    # output_image.close()

    # Output the final image as an sRGB JPEG
    # im.write(output_filename, oiio.JpgFormat(), {"color_space": "sRGB"})
# spec = ImageSpec(width, length, channels, format)
# spec.attribute ("oiio:ColorSpace", "scene_linear")

    ##########################################################################
    print(F'\nFINISHED SCRIPT------------\n')  # Only for testing purposes---.
