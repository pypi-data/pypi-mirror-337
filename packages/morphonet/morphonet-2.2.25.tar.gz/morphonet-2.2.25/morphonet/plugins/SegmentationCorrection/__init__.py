from .Delete import *
from .Deli import *


# -*- coding: latin-1 -*-
defaultPlugins=[]

from .Fuse import Fuse
defaultPlugins.append(Fuse())

from .Gaumi import Gaumi
defaultPlugins.append(Gaumi())

from .Splax import Splax
defaultPlugins.append(Splax())

from .Disco import Disco
defaultPlugins.append(Disco())

from .Delete import Delete
defaultPlugins.append(Delete())

from .Deli import Deli
defaultPlugins.append(Deli())

from .CopyPaste import CopyPaste
defaultPlugins.append(CopyPaste())

from .Match import Match
defaultPlugins.append(Match())

from .Fusoc import Fusoc
defaultPlugins.append(Fusoc())







