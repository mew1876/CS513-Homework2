import os.path

import Loader

if not os.path.isfile('LinksShelf.dat'):
	Loader.loadLinks()
if not os.path.isfile('ProbePointsShelf.dat'):
	Loader.loadProbePoints()

