Hi Drew,

This test has been added specifically for the Media Systems Pipeline TD position to get some samples of OCIO and OIIO usage as well as colorspace transforms. In this directory you will find 2 files:

- laika_framing_chart.exr
- canon_5d_mkII_sample_raw.cr2

I have 3 additional challenges for you - one of which is an opportunity to revise a previous challenge.

1. Write a script that uses OIIO/OCIO to do the following operations on laika_framing_chart.exr
    - Crop from 2348x1566 to 2048x858
    - Matte the 2048x858 image into a 2048x1080 frame with black bars top and bottom
    - Output this resulting 2048x1080 image as an sRGB jpeg - commit the output jpeg for verification

2. Write a script that uses dcraw or other command line raw developing software to process the provided raw file.
    - To the best of my knowledge there isn't a python solution here - you will need to use subprocess to execute a command.
    - Convert from .cr2 to ACEScg .exr file using dcraw - commit a sample file for verification
    - Convert that ACEScg exr file to an sRGB .jpeg - commit a sample file for verification

Github has a 100mb file size limit. Some of these files may range larger than that if uncompressed - if so apply compression using dcraw or OIIO and note it in the script.

3. I provided the following feedback on the initial review of Challenge 1:

Excercise 2 and 3 look good - they're smaller exercises and they meet the requirements and are very legible. In exercise 1 there's a lot of code execution happening at the module level, some of it before all of the function definitions and some of it after. The functions themselves reference global variables a lot with little to no argument passing. How variables are named, scoped, and passed between functions is a big part of what I look for in these tests and he sort of side steps that with the use of globals. Having a lot of code at the module level also means that you can't import the file and execute individual functions for debugging without executing all of the module level code.

I would like to see a revision of that first challenge with that feedback in mind. I'm looking for better flow, lack of global variables and the ability to import this module for debugging functions with minimal code execution. Hint - `if __name__ == "__main__"` that you see in many command line python scripts isn't just for show.

I've created this file in a branch called BONUS-CHALLENGE. Please complete your work in this branch and send a link to a pull request to merge it into your existing final-code branch when complete.

Good Luck! Thank you for your time!

Rachel Lowe
Lead Stage and Camera TD
Laika Entertainment
