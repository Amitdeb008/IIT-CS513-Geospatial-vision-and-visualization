#The source code is in the file 'smear_detection.py'
#Output images: 
	Average Image - 'Average_Image.jpg'
	Gaussian Filter Image - 'Gaussian_Filter_Image.jpg'
	Adaptive Threshold Image - 'Adaptive_Threshold_Image.jpg'
	Edge Detection Image - 'Edge_Detection_Image.jpg'
	Final output Image - 'Final_Output_Image.jpg'
	
#Program Execution:
1. Install python
2. Install following packages
	- opencv3 : conda -c install conda-forge opencv3
	- numpy : conda -c install conda-forge numpy
	- scipy : conda -c install conda-forge scipy 
	- glob : conda -c install conda-forge glob
	- scikit-image : conda install scikit-image
3. To detect smear of lens used in cam_0 : Run command 'python smear_detection.py <path to cam_0 folder>'
4. To detect smear of lens used in cam_1 : Run command 'python smear_detection.py <path to cam_1 folder>'
5. To detect smear of lens used in cam_2 : Run command 'python smear_detection.py <path to cam_2 folder>'
6. To detect smear of lens used in cam_3 : Run command 'python smear_detection.py <path to cam_3 folder>'
7. To detect smear of lens used in cam_5 : Run command 'python smear_detection.py <path to cam_5 folder>'  
