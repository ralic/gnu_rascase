# -*- coding: utf-8 -*-
"""
Este modulo contiene las clases relacionadas con la implementación de las funcionalidades a nivel de modelo para la gestión de 'modelos lógicos'

"""
##
## logical.py
## Login : <freyes@yoda>
## Started on  Sat Jan 19 17:02:59 2008 Felipe Reyes
## $Id$
## 
## Copyright (C) 2008 Felipe Reyes
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
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##

import logging
import os
from datetime import datetime
from time import time
from pkg_resources import resource_filename

#from rascase.core.base import *
from rascase.core import base

#set the logging
log = logging.getLogger('core.logical')

class LogicalModel(base.ModelBase):
    def __init__(self, path=None):
        log.debug("LogicalModel.__init__(path=%s)", path)
        base.ModelBase.__init__(self, path)
        self._entities_list = list()
        self._relationships_list = list()
        self._inheritance_list = list()

        # if the path given is None, then we use an empty model provided by the software
        if (self._path == None):
            now = datetime.fromtimestamp(time())
            newmodelname = str(now.year) + str(now.month) + str(now.day) + \
                           str(now.hour) + str(now.minute) + str(now.second) + '.rxl'
            srcname = resource_filename('rascase.resources', 'sample_logical_model.rxl')
            dstname = os.path.join('/tmp/', newmodelname)
            try:
                copy(srcname, dstname)
            except (IOError, os.error), why:
                log.debug("Can't copy %s to %s: %s" % (`srcname`, `dstname`, str(why)))

            self._path = dstname

        #now we must construct the logical model
        doc = xml.dom.minidom.parse(self._path)
        modelo = doc.childNodes[0]

        for i in modelo.childNodes:
            if i.nodeType == i.TEXT_NODE:
                print "datos: '", i.data, "'"


    def generate_physical_model(self, path=None):
        return False

    def add_entity(self, entity):
        self._entities_list.append(entity)

    def get_entity(self, codename):
        return None

    def del_entity(self, codename):
        return False

    def get_all_entites(self):
        return self._entities_list

    def save(self, path=None):
        """Almacena el modelo en el archivo pasado como parámetro o el utilizado la última vez que se guardó el modelo"""
        log.debug("Saving the Logical model %s", self._path)

        doc = xml.dom.minidom.Document()

        # crete the logicalmodel node and add it to the document
        logicalmodel = doc.createElementNS(XML_URI, "ras:logicalmodel")
        doc.appendChild(logicalmodel)

        # generate the xml for the entities
        for i in range(len(self._entities_list)):
            log.debug("saving entity: %s", self._entities_list[i].get_codename())
            entity_node = self._entities_list[i].to_xml(doc, XML_URI)
            logicalmodel.appendChild(entity_node)

        #generate the xml for the relationships
        for i in range(len(self._relationships_list)):
            log.debug("saving relationship: %s", self._relationships_list[i].get_codename())
            relationship_node = self._relationships_list[i].to_xml(doc, XML_URI)
            logicalmodel.appendChild(relationship_node)

        # generate the xml for the inheritances
        for i in range(len(self._inheritance_list)):
            log.debug("saving inheritance: %s", self._inheritance_list[i].get_codename())
            inheritance_node = self._inheritance_list[i].to_xml(doc, XML_URI)
            logicalmodel.appendChild(inheritance_node)

        # if there is some path given by parameter will be used
        if path!=None:
            self._path = path

        # write the xml into a file
        xml.dom.ext.PrettyPrint(doc, open(self._path, "w"))



class Entity(LogicalBase, RectBase):
    def __init__(self, x=0, y=0, xmlnode=None):
        LogicalBase.__init__(self)
        RectBase.__init__(self)
        self._attributes_list = list()

        if (xmlnode != None):
            self.set_name(xmlnode.getAttributeNS(XML_URI, "ras:name"))
            self.set_codename(xmlnode.getAttributeNS(XML_URI, "ras:codename"))
            self.set_description(xmlnode.getAttributeNS(XML_URI, "ras:description"))

            #get the position of the entity
            self.set_x(xmlnode.getAttributeNS(XML_URI, "ras:x"))
            self.set_y(xmlnode.getAttributeNS(XML_URI, "ras:y"))

            #get the dimentions of the entity
            self.set_height(xmlnode.getAttributeNS(XML_URI, "ras:height"))
            self.set_width(xmlnode.getAttributeNS(XML_URI, "ras:width"))

            #get the visual properties of the entity
            self.set_linecolor(xmlnode.getAttributeNS(XML_URI, "ras:linecolor"))
            self.set_linewidth(xmlnode.getAttributeNS(XML_URI, "ras:linewidth"))
            self.set_fillcolor(xmlnode.getAttributeNS(XML_URI, "ras:fillcolor"))

            


    def add_attribute(self, attribute):
        return False

    def del_attribute(self, attribute):
        return False

    def to_xml(self, doc, uri):
        """Transforma la información que almacena el objeto en un nodo xml y lo retorna"""
        entity = doc.createElementNS(uri, "ras:entity")

        entity.setAttributeNS(uri, "ras:name", self.get_name())
        entity.setAttributeNS(uri, "ras:codename", self.get_codename())
        entity.setAttributeNS(uri, "ras:description", self.get_description())

        entity.setAttributeNS(uri, "ras:x", self.get_x())
        entity.setAttributeNS(uri, "ras:y", self.get_y())

        entity.setAttributeNS(uri, "ras:height", self.get_height())
        entity.setAttributeNS(uri, "ras:width", self.get_width())

        entity.setAttributeNS(uri, "ras:linecolor", self.get_linecolor())
        entity.setAttributeNS(uri, "ras:linewidth", self.get_linewidth())
        entity.setAttributeNS(uri, "ras:fillcolor", self.get_fillcolor())

        for i in range(len(self._attributes_list)):
            log.debug("to xml %s.%s", self.get_codename(),
                      self._attributes_list[i].get_codename())
            attrnode = self._attributes_list[i].to_xml(doc, uri)
            entity.appendChild(attrnode)

        return entity

class Attribute(LogicalBase):
    def __init__(self):
        self._primary_key = False
        self._data_type = None
        self._default_value = None
        self._mandatory = False

    def set_primary_key(self, value):
        pass

    def is_primary_key(self):
        return False

    def set_default_value(self, value):
        pass

    def get_default_value(self):
        pass

    def set_data_type(self, value):
        pass

    def get_data_type(self):
        pass

    def set_mandatory(self, value):
        pass

    def is_mandatory(self):
        pass


class Relationship(LogicalBase):

    CARDINALITY_1_1 = 0
    CARDINALITY_1_N = 1
    CARDINALITY_N_1 = 2
    CARDINALITY_N_N = 3
    
    def __init__(self, entity1, entity2):
        self._cardinality = None
        self._entity1 = entity1
        self._entity2 = entity2

    def set_cardinality(self, value):
        pass

    def get_cardinality(self):
        pass

    def set_entity1(self, entity):
        pass

    def get_entity1(self):
        pass

    def set_entity2(self, entity):
        pass

    def get_entity2(self):
        pass

class Inheritance(LogicalBase):
    def __init__(self, father, son):
        self._father = father
        self._son = son

class LogicalDataType:
    CHARACTER = 0
    VARCHAR = 1
    BIT = 2
    VARBIT = 3
    NUMERIC = 4
    DECIMAL = 5
    INTEGER = 6
    SMALLINT = 7
    FLOAT = 8
    REAL = 9
    DOUBLE = 10
    DATE = 11
    TIME = 12
    TIMESTAMP = 13
    INTERVAL = 14

    def to_string(cls, type):
        pass
    to_string = classmethod(to_string) #transforma el metodo to_string en estatico

    def get_description(cls, type):
        pass

    get_description = classmethod(get_description)

class Label(RectBase):
    def __init__(self, text):
        self._text = ""

    def set_text(self, text):
        pass

    def get_text(self):
        pass


class Rectangle(RectBase):
    def __init__(self, x, y):
        self.set_x = x
        self.set_y = y

