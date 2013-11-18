#!/usr/bin/python
# -*- coding: utf-8 -*-
#     LICENSE: The GNU Public License v3 or Greater
#
#     Search The Sky (SearchTheSky) v0.0.1
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

from distutils.core import setup
import publish
import cloudtb

ctb_packages = ['SearchTheSky.' + n for n in cloudtb.publish.ctb_packages]
setup(name= publish.SUBTITLE,
      version=publish.VERSION,
      description='A Powerful code re-factoring tool for multiple programming '
          'languages. Includes Regular Expression tools.',
      author='Garrett Berg',
      author_email='garrett@cloudformdesign.com',
      url='http://cloudformdesign.com/products/searchthesky',
      packages = ['SearchTheSky',]+
                  ctb_packages,
      package_dir = {'': 'publish'}
     )
    