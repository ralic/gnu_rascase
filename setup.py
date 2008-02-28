#!/usr/bin/python2.4
##
## setup.py
## Login : <freyes@yoda.>
## Started on  Fri Dec 14 22:14:38 2007 Felipe Reyes
## $Id$
## 
## Copyright (C) 2007 Felipe Reyes <felipereyes@gmail.com>
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
## 
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
##

from setuptools import setup

setup(name="Rascase",
      version='0.1',
      description="A simple tool to develop Entity-Relationship models",
      author="Felipe Reyes",
      author_email="felipereyes@gmail.com",
      url="http://rascase.linuxdiinf.org",
      packages=['rascase'],
      package_data={
        'rascase':
            ['resources/glade/*',
             'resources/pixmaps/*',
             'resources/uidefs/*']
        },
      entry_points = {'console_scripts':
                      ['rascase = rascase.controllers:start',]
                      }
      )
