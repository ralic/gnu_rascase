# -*- coding: utf-8 -*-
"""
En este modulo se encuentran las clases base de la capa modelo del paradigma MVC++

"""
##
## main.py
## Login : <freyes@yoda>
## Started on  Sat Jan 19 16:24:12 2008 Felipe Reyes
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

import gconf
import xml.dom.minidom
import xml.dom.ext
import logging
import os

#por alguna razón al importar se va de hocico,
#se produce algo como import circular
from rascase.core import logical
from rascase.core import physical

log = logging.getLogger("core.base")

XML_URI = "http://freyes.linuxdiinf.org/rascase"

class ModelBase:
    """clase base para la implementación de las clases modelo"""
    def __init__(self, path):
        self._name = None
        self._path = path

    def save(self, path=None):
        raise NotImplemented

    def get_path(self):
        return self._path

    def print_model(self):
        return False

    def export_to_png(self):
        return False

    def check(self):
        raise NotImplemented

    #metodos para enriquecer la clase
    def __eq__(self, y):
        """Retorna True si los dos objetos usan el mismo path para el archivo, en caso contrario retorna False"""
        if not(y.__class__ is ModelBase):
            return False
        elif (self._path == y.get_path()):
            return True
        else:
            return False

    def __ne__(self, y):
        """Retorna False si los objetos utilizan rutas distintas para almacenar el proyecto, en caso contrario retorna True"""
        if not(y.__class__ is ModelBase):
            return False
        elif (self._path != y.get_path()):
            return True
        else:
            return False

class LogicalBase:
    def __init__(self):
        self._name = None
        self._codename = None
        self._description = None

    def get_name(self):
        return self._name

    def set_name(self, value):
        self._name = value

    def get_codename(self):
        return self._codename

    def set_codename(self, value):
        self._codename = value

    def get_description(self):
        return self._description

    def set_description(self, value):
        self._description = value

    def to_xml(self, doc, uri):
        raise NotImplemented

    def check(self):
        raise NotImplemented

class RectBase:
    def __init__(self):
        self._linecolor = None
        self._linewidth = None
        self._fillcolor = None
        self._width = None
        self._height = None
        self._pos_x = None
        self._pos_y = None
        self._dragbox = None

    def set_linecolor(self, value):
        self._linecolor = value

    def get_linecolor(self):
        return self._linecolor

    def set_linewidth(self, value):
        self._linewidth = value

    def get_linewidth(self):
        return self._linewidth

    def set_fillcolor(self, value):
        self._fillcolor = value

    def get_fillcolor(self):
        return self._fillcolor

    def set_width(self, value):
        self._width = value

    def get_width(self):
        return self._width

    def set_height(self, value):
        self._height = value

    def get_height(self):
        return self._height

    def set_x(self, value):
        self._pos_x = value

    def get_x(self):
        return self._pos_x

    def set_y(self, value):
        self._pos_y = value

    def get_y(self):
        return self._pos_y

class ConfigurationManager:
    def __init__(self):
        self._client = gconf.client_get_default()
        self._client.add_dir('/apps/rascase', gconf.CLIENT_PRELOAD_NONE)

    def get_entity_color(self):
        res = self._client.get_string('/apps/rascase/entity_color')
        print 'entity_color: ', res
        return res

    def set_entity_color(self, value):
        self._client.set_string('/apps/rascase/entity_color', value)

    def add_recently_opened(self,path):
        pass

    def set_label_color(self, value):
        self._client.set_string('/apps/rascase/label_color', value)

    def get_label_color(self):
        return self._client.get_label_color('/apps/rascase/label_color')

    def set_relationship_color(self, value):
        self._client.set_string('/apps/rascase/relationship_color', value)

    def get_relationship_color(self):
        return self._client.get_string('/apps/rascase/relationship_color')

    def set_table_color(self, value):
        self._client.set_string('/apps/rascase/table_color', value)

    def get_table_color(self):
        return self._client.get_string('/apps/rascase/table_color')

    def set_reference_color(self, value):
        self._client.set_string('/apps/rascase/reference_color', value)

    def get_reference_color(self):
        return self._client.get_string('/apps/rascase/reference_color')

    def set_inheritance_color(self, value):
        self._client.set_string('/apps/rascase/inheritance_color', value)

    def get_inheritance_color(self):
        return self._client.get_string('/apps/rascase/inheritance_color')

    def set_last_project_opened(self, path):
        self._client.set_string('/apps/rascase/last_project', value)

    def get_last_project_opened(self):
        return self._client.get_string('/apps/rascase/last_project')

class Project:
    def __init__(self, filepath=None):
        """Construye un proyecto y los modelos asociados a este

        Si no es pasada la ruta de un proyecto como parámetro (opicon por defecto) se construye un proyecto vacio, es decir, con las opciones por defecto y sin modelos asociados"""
        ## self._name = None
        self._path = filepath
        self._models_list = list()

        doc = xml.dom.minidom.parse(self._path)
        projectnode = doc.childNodes[0]

        for node in projectnode.childNodes:
            if node.nodeType == node.TEXT_NODE:
                continue

            modelname = node.getAttributeNS(XML_URI, 'modelpath')

            log.info("found the model %s inside project %s", modelname, self._path)

            # we get the extension of the filename
            extension = os.path.basename(modelname).split('.', 2)[1]
            log.debug("extension of %s is %s", modelname, extension)

            #rxl == rascase xml logical
            #rxf == rascase xml fisico (physical in spanish)
            if (extension == "rxl"):
                self._models_list.append(logical.LogicalModel(path=modelname))
            elif (extension == "rxf"):
                self._models_list.append(PhysicalModel(path=modelname))
            else:
                print "problemas con la extension: ", extension
                print os.path.basename(modelname), modelname

    ## #averiguar para que mierda puse la propiedad 'name'
    ## def set_name(self, name):
    ##     pass

    def get_name(self):
        "Retorna el nombre del archivo, puede ser usado para ponerlo en el titulo de la ventana"
        return os.path.basename(self._path)

    def add_model(self, model):
        if not(type(model) is ModelBase):
            log.error("The argument passed to %s.add_model is not a ModelBase instance (%s)", self, model)
            raise RuntimeError
        elif (model in self._models_list): #this only checks the references, _not_ the path
            log.debug("Trying to add to the project an already existing model")
            return False

        self._models_list.append(model)
        return True

    def get_models(self):
        """Retorna la lista de modelos asociados al proyecto"""
        return self._models_list

    def del_model(self, model, del_from_disk=False):
        """Elimina el objeto modelo pasado como y opcionalmente borra el archivo asociado al modelo (por defecto no lo hace)

        Si la operación se lleva a cabo con éxito returna True, en caso contrario retorna False y escribe en el log el problema"""
        if not(model in self._models_list):
            log.debug("Trying to delete a model that does not exist in the project")
            return False
        else:
            if (self._models_list.count(model) != 1):
                log.error("The model %s is %s in the project", model, self._models_list.count(model))
                return False
            if (del_from_disk):
                filepath = model.get_path()
                self._models_list.remove(model)
                os.remove(filepath)
            else:
                self._models_list.remove(model)
            return True

    def save(self, path=None):
        """Almacena el proyecto en el archivo pasado como parámetro o el utilizado la última vez que se guardó el proyecto"""
        doc = xml.dom.minidom.Document()

        # crete the project node and add it to the document
        prj = doc.createElementNS(URI_XML, "ras:project")
        doc.appendChild(prj)

        for i in range(len(self._models_list)):
            model = doc.createElementNS(XML_URI, "ras:model")
            model.setAttributeNS(XML_URI, "ras:modelpath", self._models_list[i].get_path())
            prj.appendChild(model)

        if path!=None:
            self._path = path

        file_out = open(self._path, "w")
        xml.dom.ext.PrettyPrint(doc, file_out)

class Print:
    """Esta clase se encarga de imprimir"""
    pass
