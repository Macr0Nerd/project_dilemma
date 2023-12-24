"""
Copyright 2023 Gabriele Ron

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from abc import ABCMeta, abstractmethod
from collections.abc import MutableMapping, MutableSequence, Sequence
from typing import Self


class Base(metaclass=ABCMeta):
    """base class for other interfaces

    :var _required_attributes: required attributes to match as subclass
    :vartype _required_attributes: Sequence[str]
    """
    _required_attributes: Sequence[str]

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @classmethod
    def __subclasshook__(cls, __subclass):
        """determine if an object is a subclass of the current class

        :param __subclass: object to check
        :return: if a subclass is a subclass of the current class
        """
        if cls is Self:
            for required_attribute in cls._required_attributes:
                if not any(required_attribute in superclass.__dict__ for superclass in __subclass.__mro__):
                    break
            else:
                return True

        return NotImplemented


Round = MutableMapping[str, bool]
"""maps the node to whether or not it cooperated"""
RoundList = MutableSequence[Round | Sequence[Round]]
"""list of moves"""
