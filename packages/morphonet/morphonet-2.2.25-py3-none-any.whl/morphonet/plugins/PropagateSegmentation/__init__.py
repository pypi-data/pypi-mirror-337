# -*- coding: latin-1 -*-
defaultPlugins=[]

from .Propa import Propa
defaultPlugins.append(Propa())

#from .Propro import Propro
#defaultPlugins.append(Propro())

#from .Propi import Propi
#defaultPlugins.append(Propi())

from .Prope import Prope
defaultPlugins.append(Prope())

from .TrackAndFuse import TrackAndFuse
defaultPlugins.append(TrackAndFuse())