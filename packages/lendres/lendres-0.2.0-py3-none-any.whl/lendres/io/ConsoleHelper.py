"""
Created on December 4, 2021
@author: Lance A. Endres
"""
import pandas                                                   as pd
import IPython
import sys

class ConsoleHelper():

    # Class variables.
    VERBOSENONE         =  0
    VERBOSEELEVATED     = 10
    VERBOSETESTING      = 20
    VERBOSEREQUESTED    = 30
    VERBOSEERROR        = 40
    VERBOSEWARNING      = 50
    VERBOSEIMPORTANT    = 60
    VERBOSEALL          = 70
    VERBOSEDEBUG        = 80

    MarkdownTitleLevel  =  3


    def __init__(self, verboseLevel=50, useMarkDown=False):
        """
        Constructor.

        Parameters
        ----------
        verboseLevel : int, optional
            Specified how much output should be written. The default is 2.
            A class that uses verbose levels can choose how it operates.
        useMarkDown : bool, optional
            Specifies if mark down formatting should be used.  The default is False.

        Returns
        -------
        None.
        """
        # The amount of messages to display.
        self.verboseLevel           = verboseLevel
        self.questionNumber         = 0
        self.useMarkDown            = useMarkDown


    @classmethod
    def ClearIPythonConsole(cls):
        """
        Clears the console when IPython is used.

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """
        try:
            iPython = IPython.get_ipython()
            if iPython is not None:
                iPython.run_line_magic("clear", "")
        except:
            pass


    @classmethod
    def ClearIPythonVariables(cls):
        """
        Clears the varialbes when IPython is used.

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """
        try:
            iPython = IPython.get_ipython()
            if iPython is not None:
                iPython.get_ipython().run_line_magic("reset", "-sf")
        except:
            pass


    def ConvertPrintLevel(cls, verboseLevel):
        """
        Converts a level of None into a default value.

        Parameters
        ----------
        verboseLevel : int
            Level that the message is printed at.

        Returns
        -------
        verboseLevel : int
            A valid print level.
        """
        if verboseLevel == None:
            return cls.verboseLevel
        else:
            return verboseLevel


    def PrintQuestionTitle(self, number=None, verboseLevel=None):
        """
        Prints a divider with the question number to the console.

        Parameters
        ----------
        number : int, optional
            The question number.  If none is provided, the previously printed number
            is incremented by one and that value is used.
        verboseLevel : int, optional
            Level that the message is printed at.  Default is None, which is treated as VERBOSEALL.

        Returns
        -------
        None.
        """
        if self.verboseLevel >= self.ConvertPrintLevel(verboseLevel):

            if number == None:
                self.questionNumber += 1
            else:
                self.questionNumber = number

            self.PrintSectionTitle("Question " + str(self.questionNumber))


    def PrintSectionTitle(self, title, verboseLevel=None):
        """
        Prints a divider and title to the console.

        Parameters
        ----------
        title : string
            Title to dislay.
        verboseLevel : int, optional
            Level that the message is printed at.  Default is None, which is treated as VERBOSEALL.

        Returns
        -------
        None.
        """
        if self.verboseLevel >= self.ConvertPrintLevel(verboseLevel):

            if self.useMarkDown:
                # Don't use spaces between the asterisks and message so it prints bold in markdown.
                prefix = "#"
                for i in range(ConsoleHelper.MarkdownTitleLevel):
                    prefix += "#"

                IPython.display.display(IPython.display.Markdown(prefix + " " + title))

            else:
                quotingHashes = "######"

                # The last number is accounting for spaces.
                hashesRequired = len(title) + 2*len(quotingHashes) + 4
                hashes = ""
                for i in range(hashesRequired):
                    hashes += "#"

                print("\n\n\n" + hashes)
                print(quotingHashes + "  " + title + "  " + quotingHashes)
                print(hashes)


    def Print(self, message, verboseLevel=None):
        """
        Displays a message if the specified level is at or above the verbose Level.

        Parameters
        ----------
        message : string
            Message to display.
        verboseLevel : int, optional
            Level that the message is printed at.  Default is None, which is treated as VERBOSEALL.

        Returns
        -------
        None.
        """
        if self.verboseLevel >= self.ConvertPrintLevel(verboseLevel):
            #print(message)
            sys.stdout.write(message+"\n")
            sys.stdout.flush()


    def PrintBold(self, message, verboseLevel=None):
        """
        Prints a message.  If markdown is enable it will use markdown to make the message bold.  If markdown is not used,
        it will use asterisks to help the text stand out.

        Parameters
        ----------
        message : string
            Warning to dislay.
        verboseLevel : int, optional
            Level that the message is printed at.  Default is None, which is treated as VERBOSEALL.

        Returns
        -------
        None.
        """
        if self.verboseLevel >= self.ConvertPrintLevel(verboseLevel):
            quotingNotation = "***"

            if self.useMarkDown:
                # Don't use spaces between the asterisks and message so it prints bold in markdown.
                IPython.display.display(IPython.display.Markdown(quotingNotation + message + quotingNotation))
            else:
                # Use the ","s in the print function to add spaces between the asterisks and message.  For plain text
                # output, this makes it more readable.
                print(quotingNotation, message, quotingNotation)


    @classmethod
    def FormatAsColorString(self, message:str, forgroundColor:tuple, backgroundColor:tuple=None) -> str:
        """
        Adds color information to a string.  The colors are specified as RGB tuples.

        Parameters
        ----------
        message : str
            The message to format.
        forgroundColor : tuple
            A color in RGB format.  The components are specified in as integars in the range of 0-255.
        backgroundColor : tuple, optional
            A color in RGB format.  The components are specified in as integars in the range of 0-255.. The default is None.

        Returns
        -------
        str
            The formated message.
        """
        colorSpecification = "\33[38;2;" + str(forgroundColor[0])  + ";" + str(forgroundColor[1])  + ";" + str(forgroundColor[2])

        if backgroundColor is not None:
            colorSpecification += ";48;2;"    + str(backgroundColor[0]) + ";" + str(backgroundColor[1]) + ";" + str(backgroundColor[2])

        colorSpecification += "m"

        # End tag returns to the default print color.
        message = colorSpecification + message + "\33[m"

        return message


    def PrintInColor(self, message:str, forgroundColor:tuple, backgroundColor:tuple=None, verboseLevel=None):
        """
        Prints a message formated with a foreground and/or background color.

        Parameters
        ----------
        message : str
            The message to format.
        forgroundColor : tuple
            A color in RGB format.  The components are specified in as integars in the range of 0-255.
        backgroundColor : tuple, optional
            A color in RGB format.  The components are specified in as integars in the range of 0-255.. The default is None.
        verboseLevel : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.
        """
        message = self.FormatAsColorString(message, forgroundColor, backgroundColor)
        self.Print(message, verboseLevel)


    def PrintWarning(self, message):
        """
        Prints a warning message.

        Parameters
        ----------
        message : string
            Warning to dislay.

        Returns
        -------
        None.
        """
        if self.verboseLevel >= self.ConvertPrintLevel(ConsoleHelper.VERBOSEWARNING):
            self.PrintInColor("WARNING: " + message, (255, 0, 0), (255, 255, 255))


    def PrintError(self, message):
        """
        Prints an error message.

        Parameters
        ----------
        message : string
            Error to dislay.

        Returns
        -------
        None.
        """
        if self.verboseLevel >= self.ConvertPrintLevel(ConsoleHelper.VERBOSEERROR):
            self.PrintInColor("ERROR: " + message, (255, 0, 0), (255, 255, 255))


    def PrintNewLine(self, count=1, verboseLevel=None):
        """
        Displays a line return.

        Parameters
        ----------
        count : int, optional
            The number of new lines to print.  Default is one.
        verboseLevel : int, optional
            Level that the message is printed at.  Default is None, which is treated as VERBOSEALL.

        Returns
        -------
        None.
        """
        for i in range(count):
            self.Print("", verboseLevel)


    def PrintTitle(self, title, verboseLevel=None):
        """
        Prints a title.  With mark down, this is printed bold.  Without markdown, a new line
        is printed, then the title is printed.

        Parameters
        ----------
        title : string
            Title to rpint.
        verboseLevel : int, optional
            Level that the message is printed at.  Default is None, which is treated as VERBOSEALL.

        Returns
        -------
        None.
        """
        if not self.useMarkDown:
            self.PrintNewLine(2, verboseLevel)

        self.PrintBold(title, verboseLevel)


    def Display(self, message, verboseLevel=None):
        """
        Displays a message if the specified level is at or above the verbose level.

        Parameters
        ----------
        message : string
            Message to display.
        verboseLevel : int, optional
            Level that the message is printed at.  Default is None, which is treated as VERBOSEALL.

        Returns
        -------
        None.
        """
        if self.verboseLevel >= self.ConvertPrintLevel(verboseLevel):
            IPython.display.display(message)


    def DisplayDataFrame(self, dataFrame, verboseLevel=None, numberOfRows="all", numberOfColumns="all", cleanUp="reset"):
        """
        Displays a DataFrame with the specified number of rows and columns.

        Parameters
        ----------
        dataFrame : pandas.DataFrame
            DataFrame to display.
        verboseLevel : int, optional
            Level that the message is printed at.  Default is None, which is treated as VERBOSEALL.
        numberOfRows : int, optional
            The number of rows to display. The default is "all".
        numberOfColumns : int, optional
            The number of columns to display. The default is "all".
        cleanUp : string, optional
            Method used to restore normal display output.  The options are:
            reset : Resets DataFrame displaying to the default.
            restore : Restores it to the settings present before calling this function.
            none : Leaves the specified settings in place.

        Returns
        -------
        None.
        """
        if self.verboseLevel >= self.ConvertPrintLevel(verboseLevel):
            # Handle the input arguments.
            if numberOfRows == "all":
                numberOfRows = None

            if numberOfColumns == "all":
                numberOfColumns = None

            # Save current values.
            storedRowsToDisplay    = pd.get_option("display.max_rows")
            storedColumnsToDisplay = pd.get_option("display.max_columns")

            # Set the options.
            pd.set_option("display.max_rows", numberOfRows)
            pd.set_option("display.max_columns", numberOfColumns)

            # Display the DataFrame.
            IPython.display.display(dataFrame)

            # Handle clean up.
            if cleanUp == "reset":
                pd.reset_option("display.max_rows")
                pd.reset_option("display.max_columns")

            elif cleanUp == "restore":
                pd.set_option("display.max_rows", storedRowsToDisplay)
                pd.set_option("display.max_columns", storedColumnsToDisplay)

            elif cleanUp == "none":
                pass

            else:
                raise Exception("The argument specified for clean up is invalid.")


    def FormatBinaryAsString(x, n=5):
        """
        Get the binary representation of x.

        Parameters
        ----------
        x : int
        n : int
            Minimum number of digits. If x needs less digits in binary, the rest
            is filled with zeros.

        Returns
        -------
        str
        """
        return "{0:b}".format(x).zfill(n)


    def FormatProbabilityForOutput(self, probability, decimalPlaces=3):
        """
        Formats and prints a probability.  Displays it as both a fraction and a percentage.

        Parameters
        ----------
        probability : decimal
            The probability to display.
        decimalPlacess : int
            Optional, the number of digits to display (default=3).

        Returns
        -------
        None.
        """
        output = str(round(probability, decimalPlaces))
        output += " (" + str(round(probability*100, decimalPlaces-2)) + " percent)"
        return  output


    def PrintTwoItemPercentages(self, data, category, item1Name, item2Name):
        """
        Calculates and displays precentages of each item type in a category.

        Parameters
        ----------
        data : Pandas DataFrame
            The data.
        category : string
            Name of category to use.
        item1Name : string
            Name of first type of entry in the data[category] series.
        item2Name : string
            Name of second type of entry in the data[category] series.

        Returns
        -------
        None.
        """
        counts     = data[category].value_counts()
        totalCount = data[category].count()

        item1Percent  = counts[item1Name] / totalCount
        item2Percent  = counts[item2Name] / totalCount

        print("Total entries in the \"" + category + "\" category:", totalCount)
        print("Percent of \"" + item1Name + "\":", self.FormatProbabilityForOutput(item1Percent))
        print("Percent of \"" + item2Name + "\":", self.FormatProbabilityForOutput(item2Percent))


    def PrintHypothesisTestResult(self, nullHypothesis, alternativeHypothesis, pValue, levelOfSignificance=0.05, precision=4):
        """
        Prints the result of a hypothesis test.

        Parameters
        ----------
        nullHypothesis
        data : Pandas DataFrame
            The data.
        alternativeHypothesis : string
            A string that specifies what the alternative hypothesis is.
         pValue : double
            The p-value output from the statistical test.
        levelOfSignificance : double
            Name of second type of entry in the data[category] series.
        precision : int
            The number of significant digits to display for the p-value.
        useMarkDown : bool
            If true, markdown output is enabled.

        Returns
        -------
        None.
        """
        # Display the input values that will be compared.  This ensures the values can be checked so that
        # no mistake was made when entering the information.  The raw p-value is output so it can be examined without
        # any formatting that may obscure the value.  The the values are output in an easier to read format.
        print("Raw p-value:", pValue)
        print("\nP-value:            ", round(pValue, precision))
        print("Level of significance:", round(levelOfSignificance, precision))

        # Check the test results and print the message.
        if pValue < levelOfSignificance:
            self.PrintBoldMessage("The null hypothesis CAN be rejected.")
            print(alternativeHypothesis)
        else:
            self.PrintBoldMessage("The null hypothesis CAN NOT be rejected.")
            print(nullHypothesis)