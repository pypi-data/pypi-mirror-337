"""
Created on December 4, 2021
@author: Lance A. Endres
"""
import numpy                                                         as np
import matplotlib
import matplotlib.pyplot                                             as plt
import matplotlib.figure                                             as fig
import matplotlib.axes                                               as ax
from   matplotlib.collections                                        import LineCollection
import math

#import seaborn                                                       as sns

import os
import shutil
from   io                                                            import BytesIO
import base64
from   PIL                                                           import Image
from   PIL                                                           import ImageChops
from   PIL                                                           import ImageColor

# It seems you cannot initialize a class variable (FormatSettings) with a class of the same name so we need to import this as another name.
from   lendres.plotting.FormatSettings                               import FormatSettings as FormatSettingsClass
from   lendres.plotting.AxesHelper                                   import AxesHelper
from   lendres.path.Path                                             import Path


class PlotHelper():
    """
    This is a helper class for creating plots.
        It does do formatting and provided formatting options.
        It does handle creating new plots for some none trivial plotting cases (e.g. multi-axes plots).
        It does have some plotting utility functions such as saving figures to files.
        It does not plot lines.

    See also FormatSettings.
    """
    # Class level variables.

    # Default location of saved files is a subfolder of the current working directory.
    DefaultOutputDirectory      = "./Output/"

    #If true, the image is saved to a subfolder or the current folder called "Output."  If false, the path is assumed to be part
    # of "saveFileName."  If false and no path is part of "saveFileName" the current directory is used.
    UseDefaultOutputDirectory   = True

    # Format settings.
    FormatSettings              = FormatSettingsClass()
    defaultFormatSettings       = FormatSettingsClass()
    storedFormatSettings        = None

    currentColor                = 0


    @classmethod
    def ResetSettings(cls):
        """
        Restores the original built-in format settings.

        Returns
        -------
        None.
        """
        cls.SetSettings(FormatSettingsClass())


    @classmethod
    def SetSettings(cls, formatSettings:FormatSettings=None, **kwargs):
        """
        Sets the format settings.  It is necessary to supply either an instance  of FormatSettings or at least one
        keyword argument that is passed to FormatSettings.

        If keyword arguments are supplied, the original built-in setttings are used as the basis of the settings and the
        settings supplied as keyword arguments are overwritten.

        The default settings are established and any stored settings (from pushed settings) will be cleared.

        Parameters
        ----------
        formatSettings : FormatSettings, optional
            The format settings. The default is None.
        **kwargs : keyword arguments
            Keyword arguments recognized by FormatSettings.

        Returns
        -------
        None.
        """
        # If formatSettings is None, create a new instance.
        if formatSettings is None:
            formatSettings = FormatSettingsClass(**kwargs)

        cls.FormatSettings        = formatSettings
        cls.defaultFormatSettings = formatSettings
        cls.storedFormatSettings  = None


    @classmethod
    def PushSettings(cls, formatSettings:FormatSettingsClass|str="current", **kwargs):
        """
        Sets the format settings (temporarily).  It is necessary to supply either an instance of FormatSettings or
        at least one keyword argument that is passed to FormatSettings.  The original settings are restored by
        calling "PopSettings".

        If keyword arguments are supplied, they are used to override the settings.  The value of "base" specifies if
        the "current" or "default" settings are used as the base settings to override.

        Pushing the settings does not erase or reset any parameters when keyword arguments are specified alone.  They
        key word arguments are used to overwrite/update existing values.  To reset the format settings, supply your
        own new instance of FormatSettings.

        Parameters
        ----------
        formatSettings : FormatSettings|str, optional
            Specified the basis of the settings to apply the keyword arguments to.
                "current"                 - The current format settings are used.
                "default"                 - The default format settings are used.
                FormatSettings instalnce  - The supplied instance of the format settings are used.
            The default is "current".
        **kwargs : keyword arguments
            Keyword arguments recognized by FormatSettings.

        Returns
        -------
        None.
        """
        match formatSettings:
            case "current":
                # Create a new instance by copying the existing settings.
                formatSettings = cls.FormatSettings.Copy().Update(**kwargs)
            case "default":
                formatSettings = cls.defaultFormatSettings.Copy().Update(**kwargs)
            case FormatSettingsClass():
                formatSettings = formatSettings.Copy().Update(**kwargs)
            case _:
                raise Exception("Invalid 'formatSettings' parameter provided to 'PushSettings'.")

        # Gaurd against a forgotten call to "Pop".
        if cls.storedFormatSettings is not None:
            cls.PopSettings()

        cls.storedFormatSettings = cls.FormatSettings
        cls.FormatSettings        = formatSettings


    @classmethod
    def PopSettings(cls):
        """
        Restores the previous settings.

        Returns
        -------
        None.
        """
        if cls.storedFormatSettings is None:
            raise Exception("Invalid call to PopSettings.  Settings must first be pushed before popping.")

        cls.FormatSettings        = cls.storedFormatSettings
        cls.storedFormatSettings  = None


    @classmethod
    def GetListOfPlotStyles(self) -> list:
        """
        Get a list of the plot styles.

        Returns
        -------
        styles : list
            A list of plot styles.
        """
        directory  = Path.GetDirectory(__file__)
        styleFiles = Path.GetAllFilesByExtension(directory, "mplstyle")
        styles     = [os.path.splitext(styleFile)[0] for styleFile in styleFiles]
        return styles


    @classmethod
    def GetScaledStandardSize(cls):
        """
        Gets the standard font size adjusted with the scaling factor.

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """
        return plt.rcParams["font.size"]


    @classmethod
    def GetScaledAnnotationSize(cls) -> float:
        """
        Gets the annotation font size adjusted with the scaling factor.

        Parameters
        ----------
        None.

        Returns
        -------
        : float
            Scaled annotation size.
        """
        return cls.FormatSettings.Scale*cls.FormatSettings.AnnotationSize


    @classmethod
    def __FindParameterFile(cls):
        parameterFile = cls.FormatSettings.ParameterFile

        # If the parameter file is one of the built in ones, we don't have to do anything.
        if parameterFile in plt.style.available:
            return parameterFile

        # Add the file extension if it was not included.
        if not parameterFile.endswith(".mplstyle"):
            parameterFile += ".mplstyle"

        # If we can locate the file, then we are done.
        if os.path.exists(parameterFile):
            return parameterFile

        # Try the library's installation location.
        location = os.path.join(Path.GetDirectory(__file__), parameterFile)
        if os.path.exists(location):
            return location

        # Could not locate the file, so raise an exception.
        raise Exception("Could not locate the parameter file \"{}\".".format(cls.FormatSettings.ParameterFile))


    @classmethod
    def Format(cls):
        """
        Sets the font sizes, weights, and other properties of a plot.

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """
        # If the file does not contain a directory, assume the same directory as this file.
        # If the file does not contain a file extension, assume a default.
        parameterFile = cls.__FindParameterFile()

        # Reset so we start from a clean slate.  This prevent values that were changed previously from unexpectedly leaking
        # through to another plot.  This resets everything then applies new base formatting (matplotlib, seaborn, et cetera).
        cls.ResetMatPlotLib()
        cls.currentColor = -1

        # Establish the parameters specified in the input file.
        plt.style.use(parameterFile)

        # Apply override, if they exist.
        if cls.FormatSettings.Overrides is not None:
            plt.rcParams.update(cls.FormatSettings.Overrides)

        # Apply scaling.
        parameters = {
            "font.size"              : cls._ScaleFontSize(plt.rcParams["font.size"]),
            "figure.titlesize"       : cls._ScaleFontSize(plt.rcParams["figure.titlesize"]),
            "legend.fontsize"        : cls._ScaleFontSize(plt.rcParams["legend.fontsize"]),
            "legend.title_fontsize"  : cls._ScaleFontSize(plt.rcParams["legend.title_fontsize"]),
            "axes.titlesize"         : cls._ScaleFontSize(plt.rcParams["axes.titlesize"]),
            "axes.labelsize"         : cls._ScaleFontSize(plt.rcParams["axes.labelsize"]),
            "xtick.labelsize"        : cls._ScaleFontSize(plt.rcParams["xtick.labelsize"]),
            "ytick.labelsize"        : cls._ScaleFontSize(plt.rcParams["ytick.labelsize"]),
            "axes.linewidth"         : plt.rcParams["axes.linewidth"]*cls.FormatSettings.Scale,                   # Axis border.
            "patch.linewidth"        : plt.rcParams["patch.linewidth"]*cls.FormatSettings.Scale,                  # Legend border.
            "lines.linewidth"        : plt.rcParams["lines.linewidth"]*cls.FormatSettings.Scale,
            "lines.markersize"       : plt.rcParams["lines.markersize"]*cls.FormatSettings.Scale,
            "axes.labelpad"          : plt.rcParams["axes.labelpad"]*cls.FormatSettings.Scale,
        }
        plt.rcParams.update(parameters)


    @classmethod
    def ResetMatPlotLib(cls):
        """
        Resets Matplotlib to the default settings.

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """
        plt.rcdefaults()


    @classmethod
    def _ScaleFontSize(cls, size) -> float:
        """
        Scale a font by the scale.  Checks for missing values and converts values that are strings to their numerical values.

        Parameters
        ----------
        size : None, string, or float
            The size of the font.  If None is supplied, the default value is used.

        Returns
        -------
        : float
            The font size converted to a numerical value and scaled.
        """
        if size is None:
            size = matplotlib.font_manager.fontManager.get_default_size();

        if type(size) is str:
            size = cls.ConvertFontRelativeSizeToPoints(size)

        return size*cls.FormatSettings.Scale


    @classmethod
    def ConvertFontRelativeSizeToPoints(cls, relativeSize) -> float:
        """
        Converts a relative size (large, small, medium, et cetera) to a numerical value.

        Parameters
        ----------
        relativeSize : string
            A Matplotlib relative font size string.

        Returns
        -------
        : float
            The font size as a flaot.
        """
        if type(relativeSize) is not str:
            raise Exception("The relative font size must be a string.")

        defaultSize = matplotlib.font_manager.fontManager.get_default_size();
        scalings    = matplotlib.font_manager.font_scalings

        if not relativeSize in scalings:
            raise Exception("Not a valid relative font size.")

        return scalings[relativeSize] * defaultSize


    @classmethod
    def NewTopAndBottomAxisFigure(cls, title:str, topFraction:float=0.25) -> tuple[fig.Figure, tuple[ax.Axes, ax.Axes]]:
        """
        Creates a new figure that has two axes, one above another.

        Parameters
        ----------
        title : str
            Figure title.
        topFraction : float
            The fraction of the total space the top figure should use.

        Returns
        -------
        figure : matplotlib.figure.Figure
            The newly created figure.
        (boxAxis, historgramAxis) : matplotlib.axes.Axes tuple
            The top axis and bottom axis, respectively, for the box plot and histogram.
        """
        # Check input.
        if topFraction <= 0 or topFraction >= 1.0:
            raise Exception("Top percentage out of range.")

        figure, (boxAxis, histogramAxis) = plt.subplots(2, sharex=True, gridspec_kw={"height_ratios" : (topFraction, 1-topFraction)})

        figure.suptitle(title)

        return figure, (boxAxis, histogramAxis)


    @classmethod
    def NewSideBySideAxisFigure(cls, title:str, width:float=15, height:float=5) -> tuple[fig.Figure, tuple[ax.Axes, ax.Axes]]:
        """
        Creates a new figure that has two axes, one above another.

        Parameters
        ----------
        title : str
            Title to use for the plot.
        width : float, optional
            The width of the figure. The default is 15.
        height : float, optional
            The height of the figure. The default is 5.

        Returns
        -------
        figure : matplotlib.figure.Figure
            The newly created figure.
        (leftAxis, rightAxis) : tuple[matplotlib.axes.Axes]
            The left axis and right axis, respectively.
        """
        figure, (leftAxis, rightAxis) = plt.subplots(1, 2)

        figure.set_figwidth(width)
        figure.set_figheight(height)


        figure.suptitle(title)

        return figure, (leftAxis, rightAxis)


    @classmethod
    def NewMultiXAxesFigure(cls, numberOfAxes:int) -> tuple[fig.Figure, list]:
        """
        Creates a new figure that has multiple axes that are on top of each other.  The axes have an aligned (shared) y-axis.

        Parameters
        ----------
        numberOfAxes : int
            The number of axes to create.

        Returns
        -------
        figure : matplotlib.figure.Figure
            The newly created figure.
        [axis1, axis2, ..., axisN] : list[matplotlib.axes.Axes]
            The axeses from top to bottom.
        """
        figure = plt.figure()
        axes   = figure.gca()

        axeses = cls.MultiXAxes(axes, numberOfAxes)

        return figure, axeses


    @classmethod
    def MultiXAxes(cls, baseAxes:matplotlib.axes.Axes, numberOfAxes:int) -> tuple[fig.Figure, list]:
        """
        Creates a multiple axes that are on top of each other.  The axes have an aligned (shared) y-axis.

        Parameters
        ----------
        baseAxes : matplotlib.axes.Axes
            The base axes to add the other axeses to.
        numberOfAxes : int
            The total number of axes to create.

        Returns
        -------
        figure : matplotlib.figure.Figure
            The figure the axeses are on.  If no figure existed, a new figure is created.
        [axis1, axis2, ..., axisN] : list[matplotlib.axes.Axes]
            The axeses from top to bottom..
        """
        axeses = [baseAxes]

        for i in range(1, numberOfAxes):
            axeses.insert(0, baseAxes.twiny())

        AxesHelper.SetMultipleXAxisPostions(axeses, cls.FormatSettings.Scale)

        return axeses


    @classmethod
    def NewMultiYAxesFigure(cls, numberOfAxes:int) -> tuple[fig.Figure, list]:
        """
        Creates a new figure that has multiple axes that are on top of each other.  The
        axes have an aligned (shared) x-axis.

        The first axis will be the left axis.  The remaining axes are stacked on the right side.

        Parameters
        ----------
        numberOfAxes : int
            The number of axes to create.

        Returns
        -------
        figure : matplotlib.figure.Figure
            The newly created figure.
        [leftAxes, rightAxes1, rightAxes2, ..., rightAxesN] : list[matplotlib.axes.Axes]
            The left axes and all the right axeses.
        """
        figure = plt.figure()
        axes   = figure.gca()

        axeses = cls.MultiYAxes(axes, numberOfAxes)

        return figure, axeses


    @classmethod
    def MultiYAxes(cls, baseAxes:matplotlib.axes.Axes, numberOfAxes:int) -> tuple[fig.Figure, list]:
        """
        Creates a new figure that has multiple axes that are on top of each other.  The
        axes have an aligned (shared) x-axis.

        The first axis will be the left axis.  The remaining axes are stacked on the right side.

        Parameters
        ----------
        baseAxes : matplotlib.axes.Axes
            The base axes to add the other axeses to.
        numberOfAxes : int
            The number of axes to create.

        Returns
        -------
        figure : matplotlib.figure.Figure
            The newly created figure.
        [leftAxes, rightAxes1, rightAxes2, ..., rightAxesN] : list[matplotlib.axes.Axes]
            The left axes and all the right axeses.
        """
        axeses = [baseAxes]

        for i in range(1, numberOfAxes):
            # Create the remaining axis and specify that the same x-axis should be used.
            axeses.insert(0, baseAxes.twinx())

        # Change the positions of the y-axis labels and ticks.
        AxesHelper.SetForMultipleYAxesPostions(axeses)

        return axeses


    @classmethod
    def ConvertKeyWordArgumentsToSeriesSets(cls, numberOfSets:int, **kwargs) -> list:
        """
        Converts key word arguments into a set of key word arguments.

        Example:
            ConvertKeyWordArgumentsToSeriesSets(2, color="r")
            Output:
                [{color:"r"}, {color:"r"}]

                ConvertKeyWordArgumentsToSeriesSets(2, color=["r", "g"], linewidth=3)
                Output:
                    [{color:"r", linewidth=3}, {color:"g", linewidth=3}]

        Parameters
        ----------
        numberOfSets : int
            The number of output key word argument sets.
        **kwargs : keyword arguments
            The key word arguments to convert.

        Returns
        -------
        keyWordArgumentSets : list
            A list of length numberOfSets that contains individual key word argument dictionaries.
        """
        keyWordArgumentSets = []

        for i in range(numberOfSets):
            seriesKwargs = {}

            for key, value in kwargs.items():
                match value:
                    case int() | float() | str() | None:
                        seriesKwargs[key] = value

                    case list():
                        seriesKwargs[key] = value[i]

                    case _:
                        raise Exception("Unknown type found.\nType:  "+str(type(value))+"\nKey:   "+str(key)+"\nValue: "+str(value)+"\nSupplied kwargs:\n"+str(kwargs))

            keyWordArgumentSets.append(seriesKwargs)
        return keyWordArgumentSets


    @classmethod
    def FormatNewArtisticFigure(cls, parameterFile:str=None) -> tuple[fig.Figure, ax.Axes]:
        """
        Create a new artistic plot.

        Parameters
        ----------
        parameterFile : str, optional
            A Matplotlib parameter style file. The default is None.

        Returns
        -------
        figure : matplotlib.figure.Figure
            The newly created figure.
        axes : matplotlib.axes.Axes
            The axes of the plot.
        """
        if parameterFile is None:
            parameterFile = "artistic"

        cls.PushSettings(parameterFile=parameterFile)
        cls.Format()

        figure  = plt.figure()
        axes    = plt.gca()

        # Zero lines.
        axes.axhline(y=0, color="black", linewidth=3.6*cls.FormatSettings.Scale)
        axes.axvline(x=0, color="black", linewidth=3.6*cls.FormatSettings.Scale)
        AxesHelper.AddArrows(axes, color="black")

        # Erase axis numbers (labels).
        axes.set(xticks=[], yticks=[])

        cls.PopSettings()

        return figure, axes


    @classmethod
    def _MakeLineCollectionSegments(cls, x, y):
        """
        Create list of line segments from x and y coordinates, in the correct format for LineCollection:
        an array of the form numlines x (points per line) x 2 (x and y) array
        """
        # Originally from https://nbviewer.org/github/dpsanders/matplotlib-examples/blob/master/colorline.ipynb
        points   = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        return segments


    @classmethod
    def PlotGradientColorLine(
            cls,
            x,
            y,
            z=None,
            axes:       matplotlib.axes.Axes        = None,
            colorMap:   matplotlib.colors.Colormap  = plt.get_cmap("copper"),
            norm:       matplotlib.colors.Normalize = plt.Normalize(0.0, 1.0),
            linewidth:  int                         = 3,
            alpha:      float                       = 1.0
        ):
        """
        Plot a colored line with coordinates x and y
        Optionally specify colors in the array z
        Optionally specify a colormap, a norm function and a line width
        """
        # Originally from https://nbviewer.org/github/dpsanders/matplotlib-examples/blob/master/colorline.ipynb

        # Default colors equally spaced on [0,1].
        if z is None:
            z = np.linspace(0.0, 1.0, len(x))

        # Special case if a single number.
        if not hasattr(z, "__iter__"):  # to check for numerical input -- this is a hack
            z = np.array([z])

        z = np.asarray(z)

        segments       = cls._MakeLineCollectionSegments(x, y)
        lineCollection = LineCollection(segments, array=z, cmap=colorMap, norm=None, linewidth=linewidth, alpha=alpha)

        if axes is None:
            axes = plt.gca()
        axes.add_collection(lineCollection)

        return lineCollection


    @classmethod
    def GetColorCycle(cls, lineColorCycle:str=None, numberFormat:str="RGB") -> list:
        """
        Gets the default Matplotlib colors in the color cycle.

        Parameters
        ----------
        lineColorCycle : str, optional
            The color cycle to use for line colors.
                None      : The color cycle is taken from the format settings.
                "pyplot"  : The Matplotlib default color cycle is returned.
                "seaborn" : The default Seaborn color cycle is returned.
            The default is None.
        numberFormat : str, optional
            The number format to return the colors as.  The options are "RGB" or "hex".  The
            default is "RGB".

        Returns
        -------
        : list
            Colors in the color cycle.
        """
        numberFormat = numberFormat.lower()
        if numberFormat != "rgb" and numberFormat != "hex":
            raise Exception("The number format specified is not valid.\nRequested format: "+numberFormat)

        if lineColorCycle is None:
            lineColorCycle = cls.FormatSettings.LineColorCycle

        if lineColorCycle == "pyplot":
            prop_cycle = plt.rcParams['axes.prop_cycle']
            colors     = prop_cycle.by_key()['color']

            if numberFormat == "rgb":
                colors = cls.ListOfHexToRgb(colors)

        elif lineColorCycle == "seaborn":
            colors = [(0.2980392156862745,  0.4470588235294118,  0.6901960784313725),
                      (0.8666666666666667,  0.5176470588235295,  0.3215686274509804),
                      (0.3333333333333333,  0.6588235294117647,  0.40784313725490196),
                      (0.7686274509803922,  0.3058823529411765,  0.3215686274509804),
                      (0.5058823529411764,  0.4470588235294118,  0.7019607843137254),
                      (0.5764705882352941,  0.47058823529411764, 0.3764705882352941),
                      (0.8549019607843137,  0.5450980392156862,  0.7647058823529411),
                      (0.5490196078431373,  0.5490196078431373,  0.5490196078431373),
                      (0.8,                 0.7254901960784313,  0.4549019607843137),
                      (0.39215686274509803, 0.7098039215686275,  0.803921568627451)]
            #colors = sns.color_palette()

            if numberFormat == "hex":
                colors = cls.ListOfRgbToHex(colors)

        else:
            raise Exception("Unkown color style requested.\nRequested style: "+lineColorCycle)

        return colors


    @classmethod
    def ListOfHexToRgb(cls, colors:list|tuple) -> list:
        """
        Convert a list of colors represented as hexadecimal strings into RGB colors.

        Parameters
        ----------
        colors : array like of strings
            An array like series of strings that are hexadecimal values representing colors.

        Returns
        -------
        : List of tuples.
            RGB colors in a List of colors in a tuple.
        """
        return [ImageColor.getrgb(color) for color in colors]


    @classmethod
    def RgbToHex(cls, color:list|tuple) -> str:
        """
        Converts an RGB color to a hexadecimal string color.

        Parameters
        ----------
        color : array like
            A RGB color.

        Returns
        -------
        : str
            A hexadecimal color.
        """
        if isinstance(color[0], float):
            color = [math.floor(255*x) for x in color]

        return "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])


    @classmethod
    def ListOfRgbToHex(cls, colors:list) -> list:
        """
        Converts an list of RGB colors to a list of hexadecimal string colors.

        Parameters
        ----------
        colors : array like of array like
            A list of RGB colors.

        Returns
        -------
        : list of string
            List of hexadecimal colors.
        """
        if isinstance(colors[0][0], float):
            colors = [[math.floor(255*x) for x in color] for color in colors]

        return ["#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2]) for color in colors]


    @classmethod
    def NextColor(cls):
        if cls.currentColor == len(cls.GetColorCycle())-1:
            cls.currentColor = 0
        else:
            cls.currentColor += 1
        return cls.GetColorCycle()[cls.currentColor]


    @classmethod
    def NextColorAsHex(cls):
        return cls.RgbToHex(cls.NextColor())


    @classmethod
    def CurrentColor(cls):
        return cls.GetColorCycle()[cls.currentColor]


    @classmethod
    def CurrentColorAsHex(cls):
        return cls.RgbToHex(cls.CurrentColor())


    @classmethod
    def GetColor(cls, color:int) -> tuple:
        return cls.GetColorCycle()[color]


    @classmethod
    def GetDefaultOutputDirectory(cls) -> str:
        """
        Gets the default output location for saving figures.

        Returns
        -------
        : string
            The default saving location for figures.
        """
        return os.path.join(os.getcwd(), cls.DefaultOutputDirectory)


    @classmethod
    def DeleteOutputDirectory(cls):
        """
        Removes all the files and subdirectories in the default output directory and then deletes the directory.

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """
        if os.path.isdir(cls.DefaultOutputDirectory):
            shutil.rmtree(cls.DefaultOutputDirectory)


    @classmethod
    def SavePlot(cls, saveFileName:str, figure:matplotlib.figure.Figure=None, transparent=False):
        """
        Saves a plot with a set of default parameters.

        Parameters
        ----------
        saveFileName : str
            The (optionally) path and file name to save the image to.
        figure : matplotlib.figure.Figure, optional
            The figure to save.  If None is specified, the current figure will be used.  The default is None.
        transparent : bool, optional
            Specificies if the background of the plot should be transparent.  If True, the background will be set to transparent, if False, nothing no
            action is taken.  The default is False.

        Returns
        -------
        None.
        """
        if figure == None:
            figure = plt.gcf()

        # Default is to use the save path and file name exactly as it was passed.
        path = saveFileName

        # If the default ouptput folder is specified, we need to make sure it exists and update
        # the save path to account for it.
        if cls.UseDefaultOutputDirectory:

            # Directory needs to exist.
            if not os.path.isdir(cls.DefaultOutputDirectory):
                os.mkdir(cls.DefaultOutputDirectory)

            # Update path.
            path = os.path.join(cls.DefaultOutputDirectory, saveFileName)

        # And, finally, get down to the work.
        figure.savefig(path, dpi=500, transparent=transparent, bbox_inches="tight")


    @classmethod
    def SavePlotToBuffer(cls, figure=None, format="png", autoCrop=False, borderSize=0) -> BytesIO:
        """
        Saves a plot to a buffer.

        Parameters
        ----------
        figure : Figure, optional
            The figure to save.  If "None" is specified, the current figure will be used.
        format : string, optional
            The image output format.  Default is "png".

        Returns
        -------
        plot : BytesIO
            Buffer with the figure written to it.
        """
        if figure == None:
            figure = plt.gcf()

        buffer = cls.SaveToBuffer(figure, "PNG" if autoCrop else format)

        if autoCrop:
            figure = Image.open(buffer).convert("RGB")
            buffer.close()
            figure = cls.CropWhiteSpace(figure, borderSize)
            buffer = cls.SaveToBuffer(figure, format)

        image     = buffer.getvalue()
        plot      = base64.b64encode(image)
        plot      = plot.decode("utf-8")

        buffer.close()

        return plot


    @classmethod
    def SaveToBuffer(cls, figure, format="PNG") -> BytesIO:
        """
        Saves a figure or image to an IO byte buffer.

        Parameters
        ----------
        figure : matplotlib.figure.Figure or PIL.Image.Image, optional
            The figure/image to save.
        format : string, optional
            The image output format.  Default is "png".

        Returns
        -------
        buffer : BytesIO
            Buffer with the figure written to it.
        """
        buffer = BytesIO()

        figureType = type(figure)

        if figureType == matplotlib.figure.Figure:
            figure.savefig(buffer, format=format, bbox_inches="tight")
        elif figureType == Image.Image:
            figure.save(buffer, format=format, bbox_inches="tight")
        else:
            raise Exception("Unknown figure type.")

        buffer.seek(0)
        return buffer


    @classmethod
    def CropWhiteSpace(cls, image, borderSize):
        """
        Crops white space from the border of an image.

        Parameters
        ----------
        image : ByteIO
            An image saved in a buffer.
        borderSize : int
            The size of the border, in pixels, to leave remaing around the edge.

        Returns
        -------
        image : BytesIO
            Buffer with the cropped image.
        """
        backGround = Image.new(image.mode, image.size, image.getpixel((0, 0)))
        difference = ImageChops.difference(backGround, image)

        #difference = ImageChops.add(difference, difference, 2.0, -100)

        boundingBox = difference.getbbox()

        if boundingBox:
            boundingBox = [
                boundingBox[0]-borderSize,
                boundingBox[1]-borderSize,
                boundingBox[2]+borderSize,
                boundingBox[3]+borderSize
            ]
            return image.crop(boundingBox)
        else:
            return image