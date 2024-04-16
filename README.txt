######################################################################################
How to run the entire Project
 - Open Terminal
 - Go to project folder
 - Create python virtual env using: virtualenv venv
 - Activate virtual env using: source venv/bin/activate
 - Run `pip install -r requirements.txt`
 - Run `python main.py`

######################################################################################
Project flow is as follows:
This script illustrates the procedure for generating synthetic microscope and dye images of parasitic microorganisms, compressing these images, and assessing whether the parasite exhibits signs of cancer using both a slower and a faster approach.

Import the requisite libraries, including custom modules for image generation, compression, and cancer detection.
Generate a base image and simulate microscope and dye images based on this reference image.
Store the generated images on the disk.
Compress the microscope and dye images using a quadtree representation.
Save the compressed images onto the disk.
Determine if the parasite has cancer utilizing the slower method:
a. Load the microscope and dye images.
b. Compute the overlap between the images, indicating the presence of dye within the parasite.
c. Output the findings and ascertain whether the parasite has cancer based on a predetermined threshold.
d. Record and display the execution time.
Determine if the parasite has cancer utilizing the faster method:
a. Load the compressed microscope and dye images.
b. Extract the images from the compressed format.
c. Calculate the overlap between the images using the optimized method.
d. Output the findings and assess whether the parasite has cancer based on a predefined threshold.
e. Record and display the execution time.

######################################################################################