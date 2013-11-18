#!/usr/bin/python
# -*- coding: utf-8 -*-
#     LICENSE: The GNU Public License v3 or Greater
#
#     Search The Sky (SearchTheSky) v0.0.2
#     Copyright 2013 Garrett Berg
#     
#     This file is part of Search The Sky, a tool that provides powerful code 
#     refactoring in a single tool. This includes:
#       - Interactive regular expression building with file search and replace
#       - (future) integration with python ropetools for python refactoring
#`      - (future) integration with the Java and C tool "cscope" for
#           refactoring in those langages.
#       - (future) other changes -- proposed by you! Suggest them at 
#    
#     You are free to redistribute and/or modify Search The Sky 
#     under the terms of the GNU General Public License (GPL), version 3
#     or (at your option) any later version.
#    
#     You should have received a copy of the GNU General Public
#     License along with Search The Sky.  If you can't find it,
#     see <http://www.gnu.org/licenses/>

import pdb
from cloudtb import publish

VERSION = '0.0.2'
TITLE = 'Search The Sky'
SUBTITLE = 'SearchTheSky'
LICENSE = 'The GNU Public License v3 or Greater'
publish.YOUR_LICENSE = """  
#     LICENSE: The GNU Public License v3 or Greater
#
#     {title} ({subtitle}) v{version}
#     Copyright 2013 Garrett Berg
#     
#     This file is part of {title}, a tool that provides powerful code 
#     refactoring in a single tool. This includes:
#       - Interactive regular expression building with file search and replace
#       - (future) integration with python ropetools for python refactoring
#`      - (future) integration with the Java and C tool "cscope" for
#           refactoring in those langages.
#       - (future) other changes -- proposed by you! Suggest them at 
#    
#     You are free to redistribute and/or modify {title} 
#     under the terms of the GNU General Public License (GPL), version 3
#     or (at your option) any later version.
#    
#     You should have received a copy of the GNU General Public
#     License along with {title}.  If you can't find it,
""".format(version = VERSION, title = TITLE, subtitle = SUBTITLE)

publish.LAST_LINE = '''#     see <http://www.gnu.org/licenses/>'''

#publish.CLOUDTB_VERSION_URL = (
#        'https://github.com/cloudformdesign/cloudtb/archive/v0.1.1.zip')
publish.CLOUDTB_VERSION_URL = (
        '/home/user/Projects/CloudformDesign/PythonCloudform/cloudtb')

if __name__ == '__main__':
    from cloudtb import dbe
    import pdb
    publish.main()
