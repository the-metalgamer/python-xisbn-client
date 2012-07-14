"""
Client for the xisbn api
"""

import re
import urllib2 as urllib

BASE_URL = "http://xisbn.worldcat.org/webservices/xid/isbn/"

METHOD_REGEX = "to10|to13|fixChecksum|getMetadata|getEditions"
METHOD_REGEX_OBJECT = re.compile(METHOD_REGEX)

FORMAT_REGEX = "xml|html|json|python|ruby|php|txt|csv"
FORMAT_REGEX_OBJECT = re.compile(FORMAT_REGEX)

LIBRARY_REGEX = "ebook|freeebook|bookmooch|paperbackswap|wikipedia|oca|hathi"
LIBRARY_REGEX_OBJECT = re.compile(LIBRARY_REGEX)

FL_REGEX = "author|city|ed|form|lang|lccn|oclcnum|originalLang|publisher|title|url|year|\*"
FL_REGEX_OBJECT = re.compile(FL_REGEX)


class xisbnclient(object):

    """
    Class for the xisbnapi
    """

    def __init__(self):

        """
        Constructor method for the xisbnclient
        """

        self.method = None
        self._format = None
        self.library = None
        self.fl = None
        self.startIndex = None
        self.count = None
        self.ai = None
        self.token = None
        self._hash = None
        self.isbn = None
        self.url = None

    def request(self, isbn, method=None, _format=None, library=None, fl=None,
                startIndex=None, count=None, ai=None, token=None, _hash=None):

        """
        Request the webservice

        @param isbn: the isbn to search for. Must be a string of
                     a length 10 or 13
        @param method: the method to use. Must be None or a string and match
                       to10|to13|fixChecksum|getMetadata|getEditions
        @param _format: the _format for the response. Must be None or a string
                        and match xml|html|json|python|ruby|php|txt|csv
        @param library: the library to limit the search. Must be None or
                        a string and match ebook|freeebook|bookmooch|paperbackswap|wikipedia|oca|hathi
        @param fl: What stored fields should be returned. Must be None or
                   a string, if you want only one field or every field, or
                   a list of multiple fields.
        @param startIndex: the index of the first search result. Must be
                           a string or None.
        @param count: the number of search results. Must be a string or None.
        @param ai: the affiliate id. Must be a string or None.
        @param token: Must be None or a string.
        @param _hash: Must be None or a string.
        """

        if isinstance(isbn, str):
            if len(isbn) in (10, 13):
                self.isbn = isbn
            else:
                raise ValueError("isbn must have an length of 10 or 13")
        else:
            raise TypeError("isbn must be a string")

        if method is not None:
            if isinstance(method, str):
                if METHOD_REGEX_OBJECT.match(method):
                    self.method = method
                else:
                    raise ValueError("method must match to10|to13|fixChecksum|getMetadata|getEditions")
            else:
                raise TypeError("method must be a string or None")
        else:
            self.method = False

        if _format is not None:
            if isinstance(_format, str):
                if FORMAT_REGEX_OBJECT.match(_format):
                    self._format = _format
                else:
                    raise ValueError("_format must match xml|html|json|python|ruby|text|csv")
            else:
                raise TypeError("_format must be a string or None")
        else:
            self._format = False

        if library is not None:
            if isinstance(library, str):
                if LIBRARY_REGEX_OBJECT.match(library):
                    self.library = library
                else:
                    raise ValueError("library must match ebook|freeebook|bookmooch|paperbackswap|wikipedia|oca|hathi")
            else:
                raise TypeError("library must be a string or None")
        else:
            self.library = False

        if fl is not None:
            if isinstance(fl, str):
                self.fl = fl
            elif isinstance(fl, list):
                fields = []
                for field in fl:
                    if isinstance(field, str):
                        if FL_REGEX_OBJECT.match(field):
                            fields.append(field)
                        else:
                            raise ValueError("field must match author|city|ed|form|lang|lccn|oclcnum|originalLang|publisher|title|url|year|*")
                    else:
                        raise TypeError("field must be a str")
                self.fl = ",".join(fields)
            else:
                raise TypeError("fl must be a string, None or a list")
        else:
            self.fl = False

        if startIndex is not None:
            if isinstance(startIndex, str):
                self.startIndex = startIndex
            else:
                raise TypeError("startIndex must be a string or None")
        else:
            self.startIndex = False

        if count is not None:
            if isinstance(count, str):
                self.count = count
            else:
                raise TypeError("count must be a string or None")
        else:
            self.count = False

        if ai is not None:
            if isinstance(ai, str):
                self.ai = ai
            else:
                raise TypeError("ai must be a string or None")
        else:
            self.ai = False

        if token is not None:
            if isinstance(token, str):
                self.token = token
            else:
                raise TypeError("token must be a string or None")
        else:
            self.token = False

        if _hash is not None:
            if isinstance(_hash, str):
                self._hash = _hash
            else:
                raise TypeError("_hash must be a string or None")
        else:
            self._hash = False

        self.url = "".join([BASE_URL, self.isbn])

        variables = []

        if self.method is not False:
            method_variable = "=".join(["method", self.method])
            variables.append(method_variable)

        if self._format is not False:
            format_variable = "=".join(["format", self._format])
            variables.append(format_variable)

        if self.library is not False:
            library_variable = "=".join(["library", self.library])
            variables.append(library_variable)

        if self.fl is not False:
            fl_variable = "=".join(["fl", self.fl])
            variables.append(fl_variable)

        if self.startIndex is not False:
            startIndex_variable = "=".join(["startIndex", self.startIndex])
            variables.append(startIndex_variable)

        if self.count is not False:
            count_variable = "=".join(["count", self.count])
            variables.append(count_variable)

        if self.ai is not False:
            ai_variable = "=".join(["ai", self.ai])
            variables.append(ai_variable)

        if self.token is not False:
            token_variable = "=".join(["token", self.token])
            variables.append(token_variable)

        if self._hash is not False:
            hash_variable = "=".join(["hash", self._hash])
            variables.append(hash_variable)

        if len(variables) is not 0:
            variables_string = "&".join(variables)
        else:
            variables_string = False

        if variables_string:
            self.url = "?".join([self.url, variables_string])

        return "".join(urllib.urlopen(self.url).readlines())
