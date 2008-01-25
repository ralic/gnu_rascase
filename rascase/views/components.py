# coding: utf-8
##
## components.py
## Login : <freyes@yoda.>
## Started on  Sun Dec 16 00:46:33 2007 Felipe Reyes
## $Id$
## 
## Copyright (C) 2007 Felipe Reyes
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

import goocanvas
import gobject
import gtk

import rascase.views.base

class LineBaseComponent:
    def __init__(self):
        self._line_width = None
        self._line_color = None

    def set_line_width(self, value):
        pass

    def get_line_width(self):
        pass

    def set_line_color(self, value):
        pass

    def get_line_color(self):
        pass

class RectBaseComponent(goocanvas.Group):

    _ANCHO = 100
    _ALTO = 200
    _ANCHO_LINEA = 1.0
    _COLOR_RELLENO = rascase.views.base.TANGO_COLOR_SKYBLUE_LIGHT

    def __init__(self, x, y, bodytype='rect'):
        goocanvas.Group.__init__(self,can_focus = True)
        
        if (bodytype == 'table'):
            self._body = goocanvas.Table(width=EntityComponent._ANCHO,
                                         height=EntityComponent._ALTO,
                                         line_width=EntityComponent._ANCHO_LINEA)
        
        elif (bodytype == 'rect'):
            self._body = goocanvas.Rect(width=EntityComponent._ANCHO,
                                        height=EntityComponent._ALTO,
                                        line_width=EntityComponent._ANCHO_LINEA,
                                        fill_color_rgba=EntityComponent._COLOR_RELLENO,
                                        stroke_color="black")
        else:
            raise RuntimeError
            
        self.translate(x, y)
        print EntityComponent._COLOR_RELLENO
        self.add_child(self._body)
        self._dragging= False
        
        self.dragbox = {
            'NW': rascase.views.base.DragBox('NW',-5,-5),
            'N' : rascase.views.base.DragBox('N', self._ANCHO/2-2.5,-5),
            'NE': rascase.views.base.DragBox('NE',self._ANCHO-5,-5),
            'E' : rascase.views.base.DragBox('E', self._ANCHO-5,self._ALTO/2),
            'SE': rascase.views.base.DragBox('SE',self._ANCHO-5,self._ALTO-5),
            'S' : rascase.views.base.DragBox('S', self._ANCHO/2-2.5,self._ALTO-5),
            'SW': rascase.views.base.DragBox('SW',-5, self._ALTO-5),
            'W' : rascase.views.base.DragBox('W', -5,self._ALTO/2)
            }

        for item in self.dragbox.keys():
            self.add_child(self.dragbox[item])
        

    def set_x(self, x):
        pass

    def get_x(self):
        pass

    def set_y(self, y):
        pass

    def get_y(self):
        pass
    
    def set_width(self, width):
        pass

    def get_width(self):
        pass

    def set_height(self, height):
        pass

    def get_height(self):
        pass

    def set_linecolor(self, color):
        pass

    def get_linecolor(self):
        pass

    def set_linewidth(self, width):
        pass

    def get_linewidth(self):
        pass

    def set_fillcolor(self, color):
        pass

    def get_fillcolor(self, color):
        pass

    def on_focus_in(self, item, target, event):
        pass

    def on_focus_out(self, item, target, event):
        pass

    def on_button_press(self, item, target, event):
        pass

    def on_button_release(self, item, target, event):
        pass

    def on_enter_notify(self, item, target, event):
        pass

    def on_leave_notifiy(self, item, target, event):
        pass

    def on_motion(self, item, target, event):
        pass


class EntityComponent(RectBaseComponent):
    __gsignals__ = {
        'on-movement': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ())
        }
    
    def __init__(self,x,y):
        #goocanvas.Group.__init__(self, can_focus = True)
        RectBaseComponent.__init__(self, x, y)


        #signals del foco
        self.connect("focus_in_event", self.on_focus_in)
        self.connect("focus_out_event", self.on_focus_out)
        self.connect("button_press_event", self.on_double_click_press)
        self.connect("button_press_event",self.on_button_press)
        self.connect("button_release_event",self.on_button_release)
        self.connect("motion_notify_event",self.on_motion)
        self.connect("enter_notify_event",self.on_enter_notify)
        self.connect("leave_notify_event",self.on_leave_notify)
        
        

    def add_attribute(self,attribute):
        """Agrega un nuevo atributo a la entidad"""

        self._cuerpo.add_child(attribute)
        self._cuerpo.set_child_properties(attribute,
                                          row=self._num_columns,
                                          column=0,
					  x_align=0.0)
        print "numero de columnas", self._num_columns
        self._num_columns += 1
        self.request_update()

    #reescritura de metodos
    
    #senales
    def on_double_click_press(self,item,target,event):
        if event.type == gtk.gdk._2BUTTON_PRESS:
            print "*** se hizo doble click", type(target)
            
            
    def on_focus_in (self, item, target_item, event):
        for aux in self.dragbox.keys():
            self.dragbox[aux].props.visibility = goocanvas.ITEM_VISIBLE
        

    def on_focus_out (self, item, target_item, event):
        for aux in self.dragbox.keys():
            self.dragbox[aux].props.visibility = goocanvas.ITEM_HIDDEN

    def on_button_press(self,item,target,event):
        canvas = item.get_canvas()
        canvas.grab_focus(item)
        
        for aux in self.dragbox.keys():
            if self.dragbox[aux].is_dragging():
                return True
            
        self._dragging = True
        fleur = gtk.gdk.Cursor(gtk.gdk.FLEUR)
        canvas = item.get_canvas ()
        canvas.pointer_grab(item, 
                        gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.BUTTON_RELEASE_MASK,
                        fleur, event.time)
        self.drag_x = event.x
        self.drag_y = event.y
        return True
    
    def on_button_release(self,item,target,event):
        for aux in self.dragbox.keys():
            if self.dragbox[aux].is_dragging():
                return True

        self._dragging = False
        canvas = item.get_canvas ()
        canvas.pointer_ungrab(item, event.time)
        return True
        
    def on_enter_notify(self,item,target,event):
        pass
        
    def on_leave_notify(self,item,target,event):
        pass
        
    def on_motion(self,item,target,event):
        for aux in self.dragbox.keys():
            if self.dragbox[aux].is_dragging():
                return True
         
        canvas = item.get_canvas ()

        if not (event.state == gtk.gdk.BUTTON1_MASK) and not self._dragging:
            return False
        
        new_x = event.x
        new_y = event.y
        item.translate (new_x - self.drag_x, new_y - self.drag_y)
        self.emit('on-movement')
        

    #get-set de propiedad
    def get_body(self):
        """Retorna el cuerpo del objeto

        """
        return self._body

class AttributeComponent(goocanvas.Text):
    """Componente gráfico que se pone dentro de una entidad"""
    def __init__(self, name):
        self.default_value = None # 
        self.mandatory = False # 
        self.primary_key = False # 
        self.data_type = None # 
        text = name + "\t"
        if self.mandatory:
            text = text + "True"
        else:
            text = text + "False"
        goocanvas.Text.__init__(self, text=text, 
				anchor=gtk.ANCHOR_SE,
				can_focus = False)

    def refresh(self):
        pass

    def set_primary_key (self, valor) :
        pass

    def get_primary_key (self) :
        pass

    def set_default_value (self, value) :
        pass

    def get_default_value (self) :
        pass
    def set_data_type (self, datatype) :
        pass

    def get_data_type (self) :
        pass
    
    def set_mandatory (self, mandatory) :
        pass
    
    def get_mandatory (self) :
        pass

class RelationshipComponent(LineBaseComponent):
    def __init__(self, entity1, entity2):
        pass

    def set_cardinality(self, type_):
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

    def on_entity_movement(self, item):
        pass
    
class InheritanceComponent(LineBaseComponent):
    def __init__(self, father, son):
        self._father = father
        self._son = son

    def set_father(self, father):
        pass

    def get_father(self):
        pass

    def set_son(self, son):
        pass

    def get_son(self):
        pass

    def on_entity_movement(self, item):
        pass

class TableComponent(RectBaseComponent):
    def __init__(self):
        RectBaseComponent.__init__(self)


class ReferenceComponent(LineBaseComponent):
    def __init__(self):
        LineBaseComponent.__init__(self)



class Canvas:
    """Esta clase configura el canvas que provee goocanvas

    """
    def __init__(self):
        self.scrolled_win = gtk.ScrolledWindow()
        self.scrolled_win.set_shadow_type(gtk.SHADOW_IN)
        self.scrolled_win.show()
            
        self._mycanvas = goocanvas.Canvas()
        self._mycanvas.set_flags(gtk.CAN_FOCUS)
        self._mycanvas.set_size_request(300, 300)
        self._mycanvas.set_bounds(0, 0, 600, 600)
        root = self._mycanvas.get_root_item()
        self._mycanvas.set_root_item(root)
        self._mycanvas.show()
    
        self.scrolled_win.add(self._mycanvas)
    
    
    def add_child(self, child):
        self._mycanvas.get_root_item().add_child(child)


class RectangleComponent(RectBaseComponent):
    def __init__(self):
        RectBaseComponent.__init__(self)
        self._transparency = 0.0

    def set_transparency(self, opacity):
        pass

class LabelComponent(RectBaseComponent):
    def __init__(self, x, y, text):
        RectBaseComponent.__init__(self)
        self.set_x(x)
        self.set_y(y)
        self._text = text

    def set_text(self, text):
        pass

    def get_text(self):
        pass



