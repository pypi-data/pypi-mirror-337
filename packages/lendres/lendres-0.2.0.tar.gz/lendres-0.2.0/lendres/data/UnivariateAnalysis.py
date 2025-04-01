"""
Created on December 27, 2021
@author: Lance A. Endres
"""
import seaborn                                                       as sns
import matplotlib.pyplot                                             as plt
import numpy                                                         as np

from   lendres.plotting.PlotHelper                                   import PlotHelper
from   lendres.plotting.AxesHelper                                   import AxesHelper
from   lendres.io.ConsoleHelper                                      import ConsoleHelper


class UnivariateAnalysis():
    supFigureYAdjustment = 1.0


    @classmethod
    def CreateCountFigure(cls, data, columnName, titleSuffix=None, xLabelRotation=None):
        """
        Creates a bar chart that plots a primary category and subcategory as the hue.

        Parameters
        ----------
        data : Pandas DataFrame
            The data.
        primaryColumnName : string
            Column name in the DataFrame.
        subColumnName : string
            If present, the column used as the hue.
        titleSuffix : string or None, optional
            If supplied, the string is prepended to the title.
        xLabelRotation : float
            Rotation of x labels.

        Returns
        -------
        figure : Figure
            The newly created figure.
        """
        # Must be run before creating figure or plotting data.
        PlotHelper.Format()

        # This creates the bar chart.  At the same time, save the figure so we can return it.
        axes = sns.countplot(x=columnName, data=data)
        figure = plt.gcf()

        # Label the perentages of each column.
        cls.LabelPercentagesOnColumnsOfBarGraph(axes)

        # Titles.
        title = "\"" + columnName + "\"" + " Category"
        AxesHelper.Label(axes, title=title, xLabels=columnName, yLabels="Count", titleSuffix=titleSuffix)

        # Option to rotate the x-axis labels.
        AxesHelper.RotateXLabels(xLabelRotation)

        # Turn off the x-axis grid.
        axes.grid(False, axis="x")

        # Make sure the plot is shown.
        plt.show()

        return figure


    @classmethod
    def LabelPercentagesOnColumnsOfBarGraph(cls, axes):
        """
        Labels each column with a percentage of the total sum of all columns.

        Parameters
        ----------
        axes : matplotlib.axes.Axes
            Matplotlib axes to plot on.

        Returns
        -------
        None.
        """
        # Number of entries.
        total = 0

        # Find the total count first.
        for patch in axes.patches:
            total += patch.get_height()

        for patch in axes.patches:
            # Percentage of the column.
            percentage = "{:.1f}%".format(100*patch.get_height()/total)

            # Find the center of the column/patch on the x-axis.
            x = patch.get_x() + patch.get_width()/2

            # Height of the column/patch.  Add a little so it does not touch the top of the column.
            y = patch.get_y() + patch.get_height() + 0.5

            # Plot a label slightly above the column and use the horizontal alignment to center it in the column.
            axes.annotate(percentage, (x, y), size=PlotHelper.GetScaledAnnotationSize(), fontweight="bold", horizontalalignment="center")


    @classmethod
    def CreateBoxPlot(cls, data, column):
        """
        Creates a bar chart that shows the percentages of each type of entry of a column.

        Parameters
        ----------
        data : pandas.DataFrame
            The data.
        column : string
            Category name in the DataFrame.

        Returns
        -------
        figure : matplotlib.figure.Figure
            The newly created figure.
        """
        # Must be run before creating figure or plotting data.
        PlotHelper.Format()

        # Save it so we can return it.  Once "show" is called, the figure is no longer accessible.
        figure = plt.gcf()
        figure.set_figwidth(10)
        figure.set_figheight(1.25)

        # This creates the bar chart.  At the same time, save the figure so we can return it.
        axis = plt.gca()
        cls.PlotBoxPlot(axis, data, column)

        title = "Column " + "\"" + column + "\""
        axis.set(title=title, xlabel=column, ylabel="Count")

        # Make sure the plot is shown.
        plt.show()

        return figure


    @classmethod
    def PlotBoxPlot(cls, axis, data, column, autoLabelX=True, color=None):
        """
        Univariate box plot creation.

        Parameters
        ----------
        axis : axis
            Matplotlib axis to plot on.
        data : pandas.DataFrame
            The data.
        column : string
            Category name in the DataFrame.
        autoLabelX : bool
            If true, x axis will be labeled with a name generated from the column.

        Returns
        -------
        None.
        """
        if color is None:
            color = "cyan"

        # Boxplot will be created and a star will indicate the mean value of the column.
        sns.boxplot(x=data[column], ax=axis, showmeans=True, color=color)

        if autoLabelX:
            axis.set(xlabel=column)
        else:
            axis.set(xlabel=None)


    @classmethod
    def PlotHistogram(cls, axis, data, column, autoLabelX=True, bins=None, color=None, annotateMean=False):
        """
        Univariate histogram creation.

        Parameters
        ----------
        axis : axis
            Matplotlib axis to plot on.
        data : pandas.DataFrame
            The data.
        column : string
            Category name in the DataFrame.
        bins : int
            Size of data bins to use.

        Returns
        -------
        None.
        """
        if color is None:
            color = "gray"

        if bins:
            sns.histplot(data[column], kde=True, ax=axis, bins=bins, palette="winter")
        else:
            sns.histplot(data[column], kde=True, ax=axis, color=color)

        # Show the mean as vertical line.
        mean = np.mean(data[column])
        axis.axvline(mean, color="g", linestyle="--")

        if annotateMean:
            yPosition = cls.GetTopOfTallestPatch(axis)
            cls.AnnotateMean(mean, axis, yPosition)

        # Label the axis.
        if autoLabelX:
            axis.set(xlabel=column)
        else:
            axis.set(xlabel=None)


    @classmethod
    def GetTopOfTallestPatch(cls, axis):
        yPosition = 0
        for patch in axis.patches:
            # Height of the column/patch.
            y = patch.get_y() + patch.get_height()
            if y > yPosition:
                yPosition = y
        return yPosition


    @classmethod
    def AnnotateMean(cls, mean, axis, yPosition):
        axis.annotate(
            "Mean {0:0.2f}".format(mean),
            xy=(mean, yPosition),                                          # Point to annotate (top of the highest patch at the mean).
            xytext=(3, 0),                                                 # Move text to the right and down a few points.
            textcoords="offset points",                                    # Specifies that xytext is in points.
            size=PlotHelper.GetScaledAnnotationSize(),                     # Font size.
            fontweight="bold",                                             # Bold font.
        )


    @classmethod
    def CreateBoxAndHistogramPlot(cls, data, column, title=None, limits=None, numberOfTicks=None):
        """
        Creates a new figure that has a box plot and histogram for a single variable analysis.

        Parameters
        ----------
        data : pandas.DataFrame
            The data.
        column : string
            Category name in the DataFrame.
        scale : double
            Scaling parameter used to adjust the plot fonts, lineweights, et cetera for the output scale of the plot.

        Returns
        -------
        figure : matplotlib.figure.Figure
            The newly created figure.
        """
        if title is None:
            title = "Column " + "\"" + column + "\""

        figure, (boxAxis, histogramAxis) = PlotHelper.NewTopAndBottomAxisFigure(title)

        cls.PlotBoxPlot(boxAxis, data, column, autoLabelX=False)
        cls.PlotHistogram(histogramAxis, data, column)

        if limits is not None:
            PlotHelper.SetXAxisLimits(boxAxis, limits, numberOfTicks)
            PlotHelper.SetXAxisLimits(histogramAxis, limits, numberOfTicks)

        plt.show()

        return figure


    @classmethod
    def BoxPlotAndLimitsDisplay(cls, dataHelper, columns, count=5):
        """
        Creates a box plot and displays the min and max values.

        Parameters
        ----------
        dataHelper : DataHelper
            DataHelper that contains the data.
        columns : list of strings
            Columns to generate the display for.
        count : int
            Number of minimum and maximum values to display.

        Returns
        -------
        None.
        """
        for column in columns:
            cls.CreateBoxPlot(dataHelper.data, column)
            minMaxValues = dataHelper.GetMinAndMaxValues(column, count, method="quantity")
            dataHelper.consoleHelper.Display(minMaxValues, ConsoleHelper.VERBOSEREQUESTED)


    @classmethod
    def CreateSideBySideHistogramPlot(cls, leftData, rightData, title, leftTitle, rightTitle, bins=None):
        """
        Creates side-by-side histogram plots.

        Parameters
        ----------


        Returns
        -------
        None.
        """
        # Create the figure and axes.
        figure, (leftAxis, rightAxis) = PlotHelper.NewSideBySideAxisFigure(title)

        if bins != None:
            sns.histplot(leftData, kde=True, ax=leftAxis, bins=bins, palette="winter")
            sns.histplot(rightData, kde=True, ax=rightAxis, bins=bins, palette="winter")
        else:
            sns.histplot(leftData, kde=True, ax=leftAxis, palette="winter")
            sns.histplot(rightData, kde=True, ax=rightAxis, palette="winter")

        leftAxis.set(xlabel=leftTitle)
        rightAxis.set(xlabel=rightTitle)

        plt.show()

        return figure


    @classmethod
    def CreateDistributionComparisonFigure(cls, samples, column, sampleTitles, title=None, bins=None, limits=None, numberOfTicks=None, annotateMean=False):
        """
        Creates a box plot and histogram for two sets of data.  Useful for comparing two data sets to see how the distributions, outliers, mean, and median compare.

        Parameters
        ----------
        samples : list of pandas.DataFrame
            The data sets.
        column : string
            The column of the data to compare..
        sampleTitles : list of strings
            The titles to use for each box plot and histogram pair.
        title : string, optional
            Plot title. The default is None.  If none is supplied, one will be automatically generated.
        bins : int, optional
            The number of bins pasted to the histogram. The default is None.
        limits : Two dimensional list, optional
            The x-axis limits.  If specified, the x-axis limits are set to these values. The default is None.
        numberOfTicks : int, optional
            Number of x-axis ticks. The default is None.
        annotateMean : bool, optional
            If True, the mean is annoated on the histogram. The default is False.

        Returns
        -------
        figure : matplotlib.figure.Figure
            The newly created figure.
        """
        # Must be run before creating figure or plotting data.
        PlotHelper.Format()

        # Create figure and a row of axes.
        topPercent      = 0.20
        numberOfSamples = len(samples)
        heightRatios    = [topPercent, 1-topPercent] * numberOfSamples
        gridspec        = {"height_ratios" : heightRatios}
        figure, axes    = plt.subplots(2*numberOfSamples, 1, sharex=True, gridspec_kw=gridspec, layout="constrained")
        figure.set_figwidth(10)
        figure.set_figheight(numberOfSamples*6)

        for i in range(numberOfSamples):
            color = sns.color_palette()[i]

            cls.PlotBoxPlot(axes[2*i], samples[i], column, autoLabelX=False, color=color)
            cls.PlotHistogram(axes[2*i+1], samples[i], column, autoLabelX=True, color=color, annotateMean=annotateMean)

            # Add the sample title to the top of the box plot axis.
            axes[2*i].set_title(sampleTitles[i], y=0.8)

            # Add the ticks and tick labels all the histogram axes.  The x-axis label is also supposed to
            # be added, but it doesn't seem to work with "sharex=True" used in "plt.subplots" for some reason.
            axes[2*i+1].tick_params(axis="x", bottom=True, labelbottom=True)

            if limits is not None:
                AxesHelper.SetXAxisLimits(axes[2*i], limits, numberOfTicks)
                AxesHelper.SetXAxisLimits(axes[2*i+1], limits, numberOfTicks)

        if title is None:
            title = "Distribution of "+column+" by Sample Set"
        figure.suptitle(title, y=1.03*UnivariateAnalysis.supFigureYAdjustment)

        plt.show()

        return figure