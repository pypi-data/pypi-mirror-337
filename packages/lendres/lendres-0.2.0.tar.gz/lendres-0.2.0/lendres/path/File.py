"""
Created on November 16, 2022
@author: Lance A. Endres
"""
import os
from   io                                                       import TextIOWrapper


class File():

    @classmethod
    def SplitFileByNumberOfLines(cls, path:str, numberOfLines:int=40000, hasHeader:bool=True):
        """
        Constructor.

        Parameters
        ----------
        path : string
            Full path and file name of the file to split.
        numberOfLines : integer
            The number of lines to include in each file.
        hasHeader : bool
            Set to True if the file contains a header line (one line only).  The header will then be copied
            into each file.  Set to False if the file does not contain a header.

        Returns
        -------
        outputFiles : list
            A list of the files generated from the split.
        """
        # Removes the file extension and returns everything else, including the directory.
        baseFileName    = os.path.splitext(path)[0]

        outputFiles     = []

        with open(path, "r") as sourceFile:
            lineCount   = 0
            fileNumber  = 0

            header      = ""
            if hasHeader:
                header  = sourceFile.readline()
            lines       = []

            # Read all the lines.
            # Every time we read a "numberOfLines" a file is written from the read lines.  The number of lines
            # is the cleared and line reading continues.  Note that this means there is likely left over lines
            # as the file will not contain a number of lines evenly divisible by "numberOfLines."  Those are
            # written after the loop.
            for line in sourceFile:
                lineCount += 1
                lines.append(line)

                # Write one file every time we reach the number of specified lines.
                if lineCount % numberOfLines == 0:
                    fileNumber += 1
                    outputFileName = cls._WriteFileSection(baseFileName, fileNumber, header, lines)
                    outputFiles.append(outputFileName)
                    lines = []

            # Write any remaining lines.
            if len(lines) > 0:
                fileNumber += 1
                outputFileName = cls._WriteFileSection(baseFileName, fileNumber, header, lines)
                outputFiles.append(outputFileName)

        return outputFiles


    @classmethod
    def _WriteFileSection(cls, baseFileName:str, fileNumber:int, header:str, lines:list[str]):
        """
        Writes the lines to a new file.

        Parameters
        ----------
        baseFileName : string
            Root file name to use for the output file name.  The part number will be appended to
            this name to create a new, unique file name.
        fileNumber : integer
            The number of the file.  This function is used when breaking a file into a sequence of files.
            This number is the current count of written files (including the current one).
        header : string
            The header text to write to the file.
        lines : list of strings
            The lines to write to the file.

        Returns
        -------
        outputFileName : string
            The path and file name of the file written.
        """
        outputFileName = baseFileName+" part "+str(fileNumber)+".csv"
        with open(outputFileName, "w") as outputFile:
            if header != "":
                outputFile.write(header)
            outputFile.writelines(lines)

        return outputFileName


    @classmethod
    def CombineFiles(cls, outputFileName:str, listOfFiles:list[str], removeFilesAfterCombining:bool=False):
        """
        Combines multiple text/csv files into a single document.

        Parameters
        ----------
        outputFileName : string
            Output file path and name.
        listOfFiles : list of strings
            List of input files to read from.
        removeFilesAfterCombining : boolean
            If True, the input files are deleted after they are read.

        Returns
        -------
        None.
        """
        if len(listOfFiles) < 2:
            raise Exception("A list of files must be supplied.")

        directory   = os.path.dirname(listOfFiles[0])
        writeHeader = True

        with open(directory+"\\"+outputFileName, "w") as outputFile:
            for fileName in listOfFiles:
                # Copy the contents of the current file into the output file.
                cls._CopyToOutputFile(fileName, outputFile, writeHeader)

                # Only write the header the from the first file.
                writeHeader = False

                if removeFilesAfterCombining:
                    os.remove(fileName)


    @classmethod
    def _CopyToOutputFile(cls, inputFileName:str, outputFile:TextIOWrapper, writeHeader:bool):
        """
        Copies the contents of a file to the output file.  Opens the file and writes it to an existing file object.

        Parameters
        ----------
        inputFileName : string
            The path and file name of the input file to read from.
        outputFile : file object
        writeHeader : boolean
            If True, the all lines of the input file are written to the output.  If False, the first
            line of the input file is skipped and not written to the output file.

        Returns
        -------
        None.
        """
        with open(inputFileName, "r") as inputFile:
            header = inputFile.readline()

            if writeHeader:
                outputFile.writelines(header)

            lines  = []
            # Read all the lines.
            for line in inputFile:
                lines.append(line)

            outputFile.writelines(lines)