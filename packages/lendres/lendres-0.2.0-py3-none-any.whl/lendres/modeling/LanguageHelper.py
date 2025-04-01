"""
Created on July 16, 2022
@author: Lance A. Endres

The NLTK stop words must be downloaded before using this module.  See below to find
a function for doing this.
"""
import os
import pandas                                                        as pd
import unicodedata
from   bs4                                                           import BeautifulSoup

# Natural language processing tool-kit.
import nltk
from   nltk.tokenize.toktok                                          import ToktokTokenizer
import contractions

# For plotting images & adjusting colors.
import matplotlib.pyplot                                             as plt
import matplotlib.figure                                             as fig

from   wordcloud                                                     import WordCloud
from   wordcloud                                                     import STOPWORDS

import itertools

import re
import spacy


class LanguageHelper():
    stopWords = nltk.corpus.stopwords.words("english")


    @classmethod
    def DownloadStopWords(cls):
        """
        Downloads or upgrades the NLTK stop words.

        Returns
        -------
        None.
        """
        nltk.download("stopwords")
        # Alternate method.
        os.system("python -m spacy download en_core_web_sm")


    @classmethod
    def RemoveFromStopWordsList(cls, words):
        """
        Remove words from the list of stop words.

        Parameters
        ----------
        words : string or list of strings
            Words to remove from the stop words.

        Returns
        -------
        None.
        """
        if type(words) != list:
            words = [words]

        for word in words:
            # Prevent an error or trying to remove a word not in the list.
            if word in cls.stopWords:
                cls.stopWords.remove(word)


    @classmethod
    def AppendToStopWordsList(cls, words):
        """
        Add words to the list of stop words.

        Parameters
        ----------
        words : string or list of strings
            Words to remove from the stop words.

        Returns
        -------
        None.
        """
        if type(words) != list:
            words = [words]

        for word in words:
            # Prevent an error or trying to remove a word not in the list.
            if word not in cls.stopWords:
                cls.stopWords.append(word)


    @classmethod
    def ResetStopWordsList(cls):
        """
        Resets the stop words list.

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """
        cls.stopWords = nltk.corpus.stopwords.words("english")


    @classmethod
    def RemoveStopWords(cls, text):
        """
        Removes stop words.  This function automatically operates
        on the text in the correct way for different types of data structions.

        Parameters
        ----------
        text : Pandas DataFrame, list, or string
            The text to operate on.

        Returns
        -------
        result : Pandas DataFrame, list, or string
            The processed text.
        """
        result  = None

        if type(text) == pd.core.series.Series:
            result = text.apply(lambda entry : cls.RemoveStopWords(entry))
        elif type(text) == list:
            result = [token for token in text if token not in cls.stopWords]
        elif type(text) == str:
            result = cls.RemoveStopWordsFromString(text)

        return result


    @classmethod
    def RemoveStopWordsFromString(cls, text):
        """
        Removes stop words from a single string of text.

        Parameters
        ----------
        text : string
            The text to operate on.

        Returns
        -------
        text : string
            The processed text.
        """
        result = text

        for word in cls.stopWords:
            pattern = r"(^|[^\w])" + word + r"\b"
            #pattern = r"(?:^|\W)rocket(?:$|\W)"
            result = re.sub(pattern, "", result)

        return result


    @classmethod
    def GetStopWords(cls, tokens):
        return [token for token in tokens if token in cls.stopWords]


    @classmethod
    def StripHtmlTags(cls, text):
        """
        Removes HTML tags.  This function automatically operates
        on the text in the correct way for different types of data structions.

        Parameters
        ----------
        text : Pandas DataFrame, list, or string
            The text to operate on.

        Returns
        -------
        result : Pandas DataFrame, list, or string
            The processed text.
        """
        result = None

        if type(text) == pd.core.series.Series:
            result = text.apply(lambda entry : cls.StripHtmlTags(entry))
        elif type(text) == list:
            result = []
            for i in range(len(text)):
                result.append(BeautifulSoup(text[i], "html.parser").get_text())
        elif type(text) == str:
            result = BeautifulSoup(text, "html.parser").get_text()

        return result


    @classmethod
    def RemoveAccentedCharacters(cls, text):
        """
        Return the normal form form for the Unicode string.  Removes any accent characters.

        Parameters
        ----------
        text : Pandas DataFrame, list, or string
            The text to operate on.

        Returns
        -------
        result : Pandas DataFrame, list, or string
            The processed text.
        """
        result = None

        if type(text) == pd.core.series.Series:
            result = text.apply(lambda entry : cls.RemoveAccentedCharacters(entry))
        elif type(text) == list:
            result = []
            for i in range(len(text)):
                result.append(cls.RemoveAccentedCharactersFromString(text[i]))
        elif type(text) == str:
            result = cls.RemoveAccentedCharactersFromString(text)

        return result


    @classmethod
    def RemoveAccentedCharactersFromString(cls, text):
        """
        Return the normal form form for the Unicode string.  Removes any accent characters.

        Parameters
        ----------
        text : string
            The text to operate on.

        Returns
        -------
        : string
            The processed text.
        """
        return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8", "ignore")


    @classmethod
    def Tokenize(cls, text):
        tokenizer = ToktokTokenizer()
        result    = None

        if type(text) == pd.core.series.Series:
            result = text.apply(lambda entry : cls.Tokenize(entry))
        elif type(text) == list:
            result = []
            for i in range(len(text)):
                tokens = tokenizer.tokenize(text[i])
                result.append([token.strip() for token in tokens])
        elif type(text) == str:
            tokens = tokenizer.tokenize(text)
            result = [token.strip() for token in tokens]

        return result


    @classmethod
    def RemoveMultipleSpaces(cls, text):
        """
        Removes special characters.  This function automatically operates
        on the text in the correct way for different types of data structions.

        Parameters
        ----------
        text : Pandas DataFrame, list, or string
            The text to operate on.
        pattern : string
            regular expression to operate on.

        Returns
        -------
        : Pandas DataFrame, list, or string
            The processed text.
        """
        pattern = r"  +"
        return LanguageHelper.ApplyRegularExpression(text, pattern, " ")


    @classmethod
    def RemoveSpecialCases(cls, text):
        """
        Removes special characters.  This function automatically operates
        on the text in the correct way for different types of data structions.

        Parameters
        ----------
        text : Pandas DataFrame, list, or string
            The text to operate on.
        pattern : string
            regular expression to operate on.

        Returns
        -------
        : Pandas DataFrame, list, or string
            The processed text.
        """
        # Remove text style "emojis" character groups that contain letters.
        # The punctuation would be caught be remove special characters or remove punctuation,
        # however, those would leave random individual characters.

        # Captures:
        # :-p  :-P  ;-p  ;-P  :-D  ;-D
        pattern = r"((:|;)-?([pP]|D))"
        return LanguageHelper.ApplyRegularExpression(text, pattern, " ")


    @classmethod
    def RemoveSpecialCharacters(cls, text, removeDigits=False):
        """
        Removes special characters.  This function automatically operates
        on the text in the correct way for different types of data structions.

        Parameters
        ----------
        text : Pandas DataFrame, list, or string
            The text to operate on.
        pattern : string
            regular expression to operate on.

        Returns
        -------
        : Pandas DataFrame, list, or string
            The processed text.
        """
        pattern = r"[^a-zA-z\s]" if removeDigits else  r"[^a-zA-z0-9\s]"
        return LanguageHelper.ApplyRegularExpression(text, pattern, " ")


    @classmethod
    def RemoveNumbers(cls, text):
        """
        Removes special characters.  This function automatically operates
        on the text in the correct way for different types of data structions.

        Parameters
        ----------
        text : Pandas DataFrame, list, or string
            The text to operate on.

        Returns
        -------
        : Pandas DataFrame, list, or string
            The processed text.
        """
        pattern = r"\d+"
        return LanguageHelper.ApplyRegularExpression(text, pattern)


    @classmethod
    def RemovePunctuation(cls, text):
        """
        Removes punctuation.  This function automatically operates
        on the text in the correct way for different types of data structions.

        Parameters
        ----------
        text : Pandas DataFrame, list, or string
            The text to operate on.

        Returns
        -------
        : Pandas DataFrame, list, or string
            The processed text.
        """
        pattern = r"[^\w\s]"
        return LanguageHelper.ApplyRegularExpression(text, pattern, " ")


    @classmethod
    def RemoveInternetHandles(cls, text):
        """
        Removes Twitter handles.  This function automatically operates
        on the text in the correct way for different types of data structions.

        Parameters
        ----------
        text : Pandas DataFrame, list, or string
            The text to operate on.

        Returns
        -------
        : Pandas DataFrame, list, or string
            The processed text.
        """
        # @(\w{1,15})
        # Matches the @ followed by characters.
        # \b matches if the handle is followed by puncuation instead of space.
        # (^|[^@\w])
        # Removes extraneous spaces from around the match.
        pattern = r"(^|[^@\w])@(\w{1,15})\b"
        return LanguageHelper.ApplyRegularExpression(text, pattern)


    @classmethod
    def RemoveWebAddresses(cls, text):
        """
        Removes web addresses.  This function automatically operates
        on the text in the correct way for different types of data structions.

        Parameters
        ----------
        text : Pandas DataFrame, list, or string
            The text to operate on.

        Returns
        -------
        text : Pandas DataFrame, list, or string
            The processed text.
        """
        pattern = r"(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{0,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"
        return LanguageHelper.ApplyRegularExpression(text, pattern)

    @classmethod
    def RunAllPreprocessing(cls, text, removeStopWords=False):
        """
        Run all the text preprocessing steps.

        Parameters
        ----------
        text : TYPE
            DESCRIPTION.
        removeStopWords : boolean, optional
            If true, the stop words are removed before using the text in the word cloud. The default is False.

        Returns
        -------
        text : string
            The processed text.
        """
        text = LanguageHelper.RemoveInternetHandles(text)
        text = LanguageHelper.RemoveWebAddresses(text)
        text = LanguageHelper.ToLowercase(text)

        if removeStopWords:
            text = LanguageHelper.RemoveStopWords(text)

        text = LanguageHelper.RemovePunctuation(text)
        text = LanguageHelper.RemoveSpecialCharacters(text)
        text = LanguageHelper.StripHtmlTags(text)
        return text


    @classmethod
    def CreateWordCloud(cls, text:pd.core.series.Series|list|str, width:int=800, height:int=600, returnMostCommon:bool=False, numberOfMostCommon:int=10) -> fig.Figure:
        """
        Creates a plot of a word cloud.

        Parameters
        ----------
        text : pd.core.series.Series, list, or string
            The text to operate on.
        width : integer
            Plot width.
        height : integer
            Plot height.
        returnMostCommon : bool
            If True, the most common words are returned.
        numberOfMostCommon : int
            The number of most common words to return.  Only returned is returnMostCommon is True.

        Returns
        -------
        figure : matplotlib.figure.Figure
            The newly created figure.
        : list
            The most common words in the word cloud.
        """
        if type(text) == pd.core.series.Series:
            text = text.tolist()
            text = " ".join(text)
        elif type(text) == list:
            text = " ".join(text)

        wordcloud = WordCloud(
            stopwords=STOPWORDS,
            background_color="white",
            colormap="viridis",
            width=width,
            height=height,
            collocations=True
        ).generate(text)

        # Plot the wordcloud object.
        pixelsPerInch = 50
        figure        = plt.figure(figsize=(width/pixelsPerInch,height/pixelsPerInch))
        plt.imshow(wordcloud, interpolation="bilInear")
        plt.axis("off")
        plt.show()

        if returnMostCommon:
            return figure, list(itertools.islice(wordcloud.words_.keys(), numberOfMostCommon))
        else:
            return figure


    @classmethod
    def ApplyRegularExpression(cls, text, pattern, replaceString=""):
        """
        Applies a regular expression patttern to text.  This function automatically operates
        on the text in the correct way for different types of data structions.

        Parameters
        ----------
        text : Pandas DataFrame, list, or string
            The text to operate on.
        pattern : string
            regular expression to operate on.

        Returns
        -------
        text : Pandas DataFrame, list, or string
            The processed text.
        """
        result  = None

        if type(text) == pd.core.series.Series:
            result = text.apply(lambda entry : cls.ApplyRegularExpression(entry, pattern, replaceString))
        elif type(text) == list:
            result = []
            for i in range(len(text)):
                newString = re.sub(pattern, replaceString, text[i]).strip()
                if newString != "":
                    result.append(newString)
        elif type(text) == str:
            result = re.sub(pattern, replaceString, text).strip()

        return result


    @classmethod
    def ToLowercase(cls, text):
        """
        Convert all characters to lowercase.  This function automatically operates
        on the text in the correct way for different types of data structions.

        Parameters
        ----------
        text : Pandas DataFrame, list, or string
            The text to operate on.

        Returns
        -------
        result : Pandas DataFrame, list, or string
            The processed text.
        """
        result = None

        if type(text) == pd.core.series.Series:
            result = text.apply(lambda entry : cls.ToLowercase(entry))
        elif type(text) == list:
            result = []
            for i in range(len(text)):
                result.append(text[i].lower())
        elif type(text) == str:
            result = text.lower()

        return result


    @classmethod
    def ReplaceContractions(cls, text):
        """
        Replace contractions in string of text.  This function automatically operates
        on the text in the correct way for different types of data structions.

        Parameters
        ----------
        text : Pandas DataFrame, list, or string
            The text to operate on.

        Returns
        -------
        result : Pandas DataFrame, list, or string
            The processed text.
        """
        result = None

        if type(text) == pd.core.series.Series:
            result = text.apply(lambda entry : cls.ReplaceContractions(entry))
        elif type(text) == list:
            result = []
            for i in range(len(text)):
                result.append(contractions.fix(text[i]))
        elif type(text) == str:
            result = contractions.fix(text)

        return result


    @classmethod
    def SimpleStemmer(cls, text):
        """
        Stemming using Porter Stemmer.
        """
        porterStemmer = nltk.porter.PorterStemmer()
        text          = " ".join([porterStemmer.stem(word) for word in text.split()])
        return text


    @classmethod
    def Lemmatize(cls, text):
        """
        Lemmatize the text.  This function automatically operates
        on the text in the correct way for different types of data structions.

        Parameters
        ----------
        text : Pandas DataFrame, list, or string
            The text to operate on.

        Returns
        -------
        result : Pandas DataFrame, list, or string
            The processed text.
        """
        # !pip install spacy
        # !python -m spacy download en_core_web_sm
        # Install language packages using Anaconda environments.
        nlp    = spacy.load("en_core_web_sm")

        result = None

        if type(text) == pd.core.series.Series:
            result = text.apply(lambda entry : cls.Lemmatize(entry))
        elif type(text) == list:
            result = []
            for i in range(len(text)):
                newText = nlp(text[i])
                newText = " ".join([word.text if word.lemma_ == "-PRON-" else word.lemma_ for word in newText])
                result.append(newText)
        elif type(text) == str:
            result = nlp(text)
            result = " ".join([word.text if word.lemma_ == "-PRON-" else word.lemma_ for word in result])

        return result


    @classmethod
    def JoinTokens(cls, text):
        """
        Joins the text.  This function automatically operates
        on the text in the correct way for different types of data structions.

        Parameters
        ----------
        text : Pandas DataFrame, list, or string
            The text to operate on.

        Returns
        -------
        result : Pandas DataFrame, list, or string
            The processed text.
        """
        result = None

        if type(text) == pd.core.series.Series:
            result = text.apply(lambda entry : cls.JoinTokens(entry))
        elif type(text) == list:
            result = " ".join(text)

        return result