import re
from copy import copy
from dataclasses import dataclass
from datetime import datetime
from queue import Queue
from typing import List, Iterable

from pyttman.core.mixins import PrettyReprMixin


class MessageMixin(PrettyReprMixin):
    """
    Pyttman MessageMixin, to extend the functionality
    of existing Message classes provided by 3rd party
    libraries and APIs, to also accommodate for the
    internal requirements of the Message object
    which is expected to fulfill a certain contract
    of attributes and methods for parsing messages.

    The MessageMixin class can be included in multiple
    inheritance when a Message-like class is developed
    for supporting a 3rd party library / API.
    """
    __repr_fields__ = ("author", "user", "created", "entities")

    @dataclass
    class Author:
        id: int = None

    def __init__(self, content=None, **kwargs):
        self.author = self.Author()
        self.user = None
        self.created = datetime.now()
        self.client = None
        self.content = content
        self.entities = {}

        try:
            self.content_with_format = str(content).splitlines(keepends=True)
        except ValueError:
            self.content_with_format = None

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.content == other.content
        return False

    def __getitem__(self, index: int) -> str:
        return self.content[index]

    def segmented(self, batch_size: int) :
        if batch_size < len(self.content_with_format):
            return self.content_with_format

        segment = []
        original_content = copy(self.content)
        formatted_content = copy(self.content_with_format)

        while formatted_content:
            segment.append(formatted_content.pop(0))
            if len(" ".join(segment)) >= batch_size:
                self.content = segment
                yield self
                segment.clear()

        self.content = segment
        yield self
        self.content = original_content


    def segmented2(self, batch_size: int):
        """
        Returns a generator that yields the content
        of the message in segments of 'batch_size'.
        The generator will yield the content closest to
        a complete word, and not split words in half,
        which is why the generator may yield less than
        'batch_size' elements.
        """
        buf = []
        content = copy(self.content_with_format)
        while content:
            if len(" ".join(buf)) + len(content[0]) < batch_size:
                buf.append(content.pop(0))
            else:
                if buf:
                    yield " ".join(buf).lstrip(" ").rstrip(" ")
                else:
                    first_element = content.pop(0)
                    cutoff = first_element[:batch_size]
                    yield cutoff
                    content.insert(0, first_element[len(cutoff):])
                buf = []
        yield " ".join(buf).lstrip(" ").rstrip(" ")

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, val):
        if val is None:
            self._content = ["None"]
        elif isinstance(val, str):
            self._content = val.split()
        elif isinstance(val, list) or isinstance(val, tuple):
            self._content = [str(i) for i in val]
        elif isinstance(val, dict):
            self._content = str(val).split()
        else:
            try:
                self._content = repr(val).split()
            except Exception:
                raise TypeError(f"content cannot be type {type(val)} "
                                f"as it is could not be typecast to "
                                f"str.")

    def sanitized_content(self, preserve_case=False) -> List[str]:
        """
        Return a sanitized version of the .content property.
        This means that the contents in the message
        are stripped of all symbols while digits are still kept.
        Case is preserved if preserve_case is True.
        :return: list
        """
        out = []
        for i in self.content:
            sanitized = re.sub(r"[^\w\s]", "", i)
            if preserve_case:
                out.append(sanitized)
            else:
                out.append(sanitized.lower())
        return out

    def lowered_content(self) -> List[str]:
        """
        Returns the content of the message case lowered.
        :return: list, str
        """
        return [i.lower() for i in self.content]

    def as_str(self, sanitized: bool = False) -> str:
        """
        Return the 'content' field as joined string
        :param sanitized: Return the content as sanitized_content or not
        :return: str
        """
        if sanitized:
            return " ".join(self.sanitized_content())
        elif self.content_with_format is not None:
            return str().join(self.content_with_format)
        return " ".join(self.content)

    def as_list(self, sanitized: bool = False) -> List:
        """
        Return the 'content' field as list
        :return: list
        """
        if sanitized:
            content = self.sanitized_content()
        else:
            content = self.content

        if isinstance(content, list):
            return content
        elif isinstance(content, str):
            return content.split()

    def remove(self, item):
        """
        Removes element from self.content.
        :return: None
        """
        self.content.remove(item)


class Message(MessageMixin):
    """
    Standard implementation of the MessageMixin
    class without extending any functionality.
    """
    pass


class Reply(MessageMixin):
    """
    The Reply object is expected to be  returned
    from all Intent subclasses.
    """
    pass


class ReplyStream(Queue):
    """
    The ReplyStream class can be used instead of
    the Reply class, whenever a collection of
    Reply objects are to be returned to the
    user. 
    """

    def __init__(self, collection: Iterable = None):
        super().__init__()
        if collection is not None:
            if isinstance(collection, str):
                self.put(collection)
            else:
                try:
                    iter(collection)
                except Exception:
                    raise AttributeError("'collection' must be iterable")
                else:
                    [self.put(i) for i in collection]

    def get(self, block=True, timeout=None):
        """
        Remove and return an item from the ReplyStream.
        """
        element = self._get()
        return Reply(element) if not isinstance(element, Reply) else element
