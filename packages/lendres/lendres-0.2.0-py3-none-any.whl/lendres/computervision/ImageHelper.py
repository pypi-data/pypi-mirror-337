"""
Created on June 24, 2022
@author: Lance A. Endres
"""
import numpy                                                         as np
from   matplotlib                                                    import pyplot                     as plt
import math
import cv2

from   lendres.plotting.PlotHelper                                   import PlotHelper


class ImageHelper():
    _arrayImageSize = 2.5


    @classmethod
    def DefaultSettings(cls):
        """
        Gets the default image plotting settings parameter file.

        Recommended usage:
            PlotHelper.PushSettings(parameterFile=ImageHelper.DefaultSettings())
            # Display images.
            ...
            PlotHelper.PopSettings()

        Returns
        -------
        : str
            The name of the parameters file..
        """
        return "imagedefault"


    @classmethod
    def PlotImage(cls, image, title=None, size=6, colorConversion=None):
        """
        Plot example image.

        Parameters
        ----------
        image : image
            Image to plot.
        title : string
            Title of the figure.
        size : float
            Size (width and height) of figure.
        colorConversion : OpenCV color conversion enumeration.
            Color conversion to perform before plotting.  Images are plotted in RGB.  For example, if the
            image is in BGR (as is used in OpenCV) then cv2.COLOR_BGR2RGB should be passed.

        Returns
        -------
        figure : matplotlib.figure.Figure
            The newly created figure.
        """
        # Defining the figure size.  Automatically adjust for the number of images to be displayed.
        PlotHelper.Format()

        # Adding subplots with 3 rows and 4 columns.
        figure = plt.gcf()
        figure.set_figwidth(size)
        figure.set_figheight(size)

        axis   = plt.gca()

        # Plotting the image.
        if colorConversion != None:
            image = cv2.cvtColor(image, colorConversion)
        axis.imshow(image)

        if title != None:
            axis.set_title(title)

        # Turn off the grid lines.
        axis.grid(False)

        plt.show()
        return figure


    @classmethod
    def CreateImageArrayPlot(cls, images, labels, columns=4, colorConversion=None):
        """
        Plots the images in an array.

        Parameters
        ----------
        images : array like
            Set of images to plot.
        labels : array like
            Set of labels to use for the individual images.
        columns : integer
            The number of columns to plot.
        colorConversion : OpenCV color conversion enumeration.
            Color conversion to perform before plotting.  Images are plotted in RGB.  For example, if the
            image is in BGR cv2.COLOR_BGR2RGB should be passed.

        Returns
        -------
        None.
        """
        # Calculate required values.
        numberOfImages = len(images)
        rows           = math.ceil(numberOfImages/columns)

        # Defining the figure size.  Automatically adjust for the number of images to be displayed.
        PlotHelper.Format()
        figure = plt.figure()
        figure.set_figwidth(columns*cls._arrayImageSize+2)
        figure.set_figheight(rows*cls._arrayImageSize+2)

        # Position in the index array/range.
        k = -1

        for i in range(columns):
            for j in range(rows):
                # Adding subplots with 3 rows and 4 columns.
                axis = figure.add_subplot(rows, columns, i*rows+j+1)

                # Plot the image.  Convert colors if required.
                k +=1
                image = images[k]
                if colorConversion != None:
                    image = cv2.cvtColor(image, colorConversion)
                axis.imshow(image)

                # Turn off white grid lines.
                axis.grid(False)

                axis.set_title(labels[k], y=0.9)

        # Adjust spacing so titles don't run together.
        plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)

        plt.show()


    @classmethod
    def DisplayColorChannels(cls, image, colorConversion=None):
        """
        Displays an image along with the individual color channels.

        Parameters
        ----------
        image : image
            Image in an array.
        colorConversion : OpenCV color conversion enumeration.
            Color conversion to perform before plotting.  Images are plotted in RGB.  For example, if the
            image is in BGR cv2.COLOR_BGR2RGB should be passed.

        Returns
        -------
        None.
        """
        imageArray = cv2.split(image)
        imageArray.insert(0, image)
        titles = ["Original", "Blue", "Green", "Red"]
        ImageHelper.CreateImageArrayPlot(imageArray, titles, columns=4, colorConversion=colorConversion)


    @classmethod
    def DisplayChromaKey(cls, image, lowerBounds, upperBounds, maskBlurSize=3, colorConversion=None, inputBoundsFormat="hsv"):
        """
        Displays an image along with the image separated into two components based on chroma keying.

        Parameters
        ----------
        image : image
            Image in an array.
        lowerBounds : numpy array of 3 values.
            Lower bounds of mask.
        maskBlurSize : int
            Size of the blur to apply to the mask.  Must be an odd number.
        upperBounds : numpy array of 3 values.
            Upper bounds of mask.
        colorConversion : OpenCV color conversion enumeration.
            Color conversion to perform before plotting.  Images are plotted in RGB.  For example, if the
            image is in BGR cv2.COLOR_BGR2RGB should be passed.
        inputBoundsFormat : string
            Format of lowerBounds and upperBounds.

        Returns
        -------
        None.
        """
        imageArray = ImageHelper.ChromaKey(image, lowerBounds, upperBounds, maskBlurSize, inputBoundsFormat)

        imageArray.insert(0, image)
        titles = ["Original", "Masked Image", "Image Remainder", "Mask"]
        ImageHelper.CreateImageArrayPlot(imageArray, titles, columns=4, colorConversion=colorConversion)


    @classmethod
    def ApplyColorConversion(cls, images, colorConversion):
        """
        Applies a color conversion to the images.

        Parameters
        ----------
        images : array like set of images
            Images in an array.
        colorConversion : OpenCV color conversion enumeration.
            Color conversion to perform before plotting.  Images are plotted in RGB.  For example, if the
            image is in BGR cv2.COLOR_BGR2RGB should be passed.

        Returns
        -------
        newImages : array like set of images
            The new images with the conversion applied.
        """
        newImages = np.empty(images.shape, dtype=images.dtype)

        if len(images.shape) < 4:
            # Only one image provided.  Shape of input is similar to (width, height, color_depth).
            newImages = cv2.cvtColor(images, colorConversion)
        else:
            # More than one image provided.
            for i in range(len(images)):
                newImages[i] = cv2.cvtColor(images[i], colorConversion)

        return newImages


    @classmethod
    def ApplyGaussianBlur(cls, images, **kwargs):
        """
        Applies a gaussian blur to the images.

        Parameters
        ----------
        images : array like set of images
            Images in an array.
        **kwargs : keyword arguments
            Arguments passed to the Gaussian filter.  For example, "ksize=(5,5), sigmaX=0"

        Returns
        -------
        newImages : array like set of images
            The new images with the blur applied.
        """
        newImages = np.empty(images.shape, dtype=images.dtype)

        if len(images.shape) < 4:
            # Only one image provided.  Shape of input is similar to (width, height, color_depth).
            newImages = cv2.GaussianBlur(images, **kwargs)
        else:
            # More than one image provided.
            for i in range(len(images)):
                newImages[i] = cv2.GaussianBlur(images[i], **kwargs)

        return newImages


    @classmethod
    def ApplyHighPassFilter(cls, images, convertToGrey=True, **kwargs):
        """
        Applies a high pass filter to images(s).

        Parameters
        ----------
        images : array like set of images
            Images in an array.
        convertToGrey : TYPE, optional
            DESCRIPTION. The default is True.
        **kwargs : keyword arguments
            Arguments passed to the Gaussian filter.  For example, "ksize=(21, 21), sigmaX=3"

        Returns
        -------
        highPass : array like set of images
            The high passed images.
        """
        # The high pass filter is created by subtracting a low pass filter from the original image(s).
        lowPass  = cls.ApplyGaussianBlur(images, **kwargs)
        highPass = images - lowPass

        # If specified, the images are converted to a greyish color.  This is the expected result of a high pass.
        if convertToGrey:
            highPass -= 127

        return highPass


    @classmethod
    def ChromaKey(cls, image, lowerBounds, upperBounds, maskBlurSize=3, inputBoundsFormat="hsv"):
        """
        Splits the image into two components based on chroma keying.

        Parameters
        ----------
        image : image
            Image in an array.
        lowerBounds : numpy array of 3 values.
            Lower bounds of mask.
        upperBounds : numpy array of 3 values.
            Upper bounds of mask.
        maskBlurSize : int
            Size of the blur to apply to the mask.  Must be an odd number.
        inputBoundsFormat : string
            Format of lowerBounds and upperBounds.

        Returns
        -------
        maskedImage : image
            Part of the image that passes the mask.
        imageRemainder : image
            Part of the image that did not pass the mask.
        mask : image
            Mask used on the image.
        """
        imageArray = []
        if inputBoundsFormat == "bgr":
            imageArray = ImageHelper.ChromaKeyWithBGR(image, lowerBounds, upperBounds, maskBlurSize)
        elif inputBoundsFormat == "hsv":
            imageArray = ImageHelper.ChromaKeyWithHSV(image, lowerBounds, upperBounds, maskBlurSize)
        else:
            raise Exception("Input bounds format argument not valid.")

        return imageArray


    @classmethod
    def GetChromaKeyPart(cls, images, lowerBounds, upperBounds, maskBlurSize=3, inputBoundsFormat="hsv", keep="bounded"):
        """
        Applies a chroma key filter to the images and returns the portion of interest.

        The ChromaKey functions splits an image into 3 parts, the bounded part, the remained, and the mask.  This function
        goes through an array of images and returns just one of those parts for all images.

        Parameters
        ----------
        images : array like set of images
            Images in an array.
        lowerBounds : numpy array of 3 values.
            Lower bounds of mask.
        upperBounds : numpy array of 3 values.
            Upper bounds of mask.
        maskBlurSize : int
            Size of the blur to apply to the mask.  Must be an odd number.
        inputBoundsFormat : string
            Format of lowerBounds and upperBounds.
        keep : string
            Part of the split image to keep.
            bounded : The original image that is bounded by the input.
            remainder : The original image that is outside of the input bounds.
            mask : The mask used to separate the image.

        Returns
        -------
        newImages : array like set of images
            An array of images that contains the specified part of the split image.
        """

        """
        Should be updated to use np arrays like ApplyGaussianBlur.
        """

        keepIndex = 0
        if keep == "bounded":
            keepIndex = 0
        elif keep == "remainder":
            keepIndex = 1
        elif keep == "mask":
            keepIndex = 2
        else:
            raise Exception("The input argument \"keep\" contains an invalid value.")

        newImages = []

        for i in range(len(images)):
            imageArray = ImageHelper.ChromaKey(images[i], lowerBounds, upperBounds, maskBlurSize, inputBoundsFormat)
            newImages.append(imageArray[keepIndex])

        return newImages


    @classmethod
    def ChromaKeyWithBGR(cls, image, lowerBounds, upperBounds, maskBlurSize=3):
        """
        Splits the image into two components based on chroma keying.

        Parameters
        ----------
        image : image
            Image in an array.
        lowerBounds : numpy array of 3 values.
            Lower bounds of mask.
        upperBounds : numpy array of 3 values.
            Upper bounds of mask.
        maskBlurSize : int
            Size of the blur to apply to the mask.  Must be an odd number.

        Returns
        -------
        maskedImage : image
            Part of the image that passes the mask.
        imageRemainder : image
            Part of the image that did not pass the mask.
        mask : image
            Mask used on the image.
        """
        mask           = cv2.inRange(image, lowerBounds, upperBounds)
        mask           = cv2.medianBlur(mask, maskBlurSize)
        maskedImage    = cv2.bitwise_and(image, image, mask=mask)
        imageRemainder = image - maskedImage

        return [maskedImage, imageRemainder, mask]


    @classmethod
    def ChromaKeyWithHSV(cls, image, lowerBounds, upperBounds, maskBlurSize=3):
        """
        Splits the image into two components based on chroma keying.

        Parameters
        ----------
        image : image
            Image in an array.
        lowerBounds : numpy array of 3 values.
            Lower bounds of mask.
        upperBounds : numpy array of 3 values.
            Upper bounds of mask.
        maskBlurSize : int
            Size of the blur to apply to the mask.  Must be an odd number.

        Returns
        -------
        maskedImage : image
            Part of the image that passes the mask.
        imageRemainder : image
            Part of the image that did not pass the mask.
        mask : image
            Mask used on the image.
        """
        hsvImage       = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask           = cv2.inRange(hsvImage, lowerBounds, upperBounds)
        mask           = cv2.medianBlur(mask, maskBlurSize)
        maskedImage    = cv2.bitwise_and(image, image, mask=mask)
        imageRemainder = image - maskedImage

        return [maskedImage, imageRemainder, mask]