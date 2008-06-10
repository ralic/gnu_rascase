# coding=utf-8
##
## base.py
## Login : <freyes@yoda>
## Started on  Tue Jan 22 11:29:49 2008 Felipe Reyes
## $Id$
##
## Copyright (C) 2008 Felipe Reyes <felipereyes@gmail.com>
##
## This file is part of Rascase.
##
## Rascase is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## Rascase is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
##

import gobject
import gtk
import gtk.glade
import goocanvas
import cairo
import pangocairo
import pango
import os
import math
import color
##logging system
import logging
log = logging.getLogger('views')
##

from pkg_resources import resource_filename

#Tango colors taken from
#http://tango.freedesktop.org/Tango_Icon_Theme_Guidelines
TANGO_COLOR_BUTTER_LIGHT = int("fce94fff",16)
TANGO_COLOR_BUTTER_MID = int("edd400ff",16)
TANGO_COLOR_BUTTER_DARK = int("c4a000ff",16)
TANGO_COLOR_ORANGE_LIGHT = int("fcaf3eff",16)
TANGO_COLOR_ORANGE_MID = int("f57900ff",16)
TANGO_COLOR_ORANGE_DARK = int("ce5c00ff",16)
TANGO_COLOR_CHOCOLATE_LIGHT = int("e9b96eff",16)
TANGO_COLOR_CHOCOLATE_MID = int("c17d11ff",16)
TANGO_COLOR_CHOCOLATE_DARK = int("8f5902ff",16)
TANGO_COLOR_CHAMELEON_LIGHT = int("8ae234ff",16)
TANGO_COLOR_CHAMELEON_MID = int("73d216ff",16)
TANGO_COLOR_CHAMELEON_DARK = int("4e9a06ff",16)
TANGO_COLOR_SKYBLUE_LIGHT = int("729fcfff",16)
TANGO_COLOR_SKYBLUE_MID = int("3465a4ff",16)
TANGO_COLOR_SKYBLUE_DARK = int("204a87ff",16)
TANGO_COLOR_PLUM_LIGHT = int("ad7fa8ff",16)
TANGO_COLOR_PLUM_MID = int("75507bff",16)
TANGO_COLOR_PLUM_DARK = int("5c3566ff",16)
TANGO_COLOR_SCARLETRED_LIGHT = int("ef2929ff",16)
TANGO_COLOR_SCARLETRED_MID = int("cc0000ff",16)
TANGO_COLOR_SCARLETRED_DARK = int("a40000ff",16)
TANGO_COLOR_ALUMINIUM1_LIGHT = int("eeeeecff",16)
TANGO_COLOR_ALUMINIUM1_MID = int("d3d7cfff",16)
TANGO_COLOR_ALUMINIUM1_DARK = int("babdb6ff",16)
TANGO_COLOR_ALUMINIUM2_LIGHT = int("888a85ff",16)
TANGO_COLOR_ALUMINIUM2_MID = int("555753ff",16)
TANGO_COLOR_ALUMINIUM2_DARK = int("2e3436ff",16)
TRANSPARENT_COLOR = int("000000",16)

class RectBaseComponent(goocanvas.ItemSimple, goocanvas.Item):
    __gsignals__ = {
        'on-movement': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),
        'on-double-click': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),
        'changed-dimensions': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ())
        }

    def __init__(self, **kwargs):


        ### properties
        if 'width' in kwargs:
            self.width = kwargs['width']
            del kwargs['width']
        else:
            self.width = 100

        if 'height' in kwargs:
            self.height = kwargs['height']
            del kwargs['height']
        else:
            self.height = 200

        if 'x' in kwargs:
            self._x = kwargs['x']
            del kwargs['x']
        else:
            self._x = 0

        if 'y' in kwargs:
            self._y = kwargs['y']
            del kwargs['y']
        else:
            self._y = 0

        goocanvas.ItemSimple.__init__(self, **kwargs)

        self.translate(self.x, self.y)
        self.line_width = self.get_property("line-width")
        self._dragging= False

        #signals del foco
        self.connect("focus_in_event", self._on_focus_in)
        self.connect("focus_out_event", self._on_focus_out)
        self.connect("button_press_event", self._on_double_click_press)
        self.connect("button_press_event",self._on_button_press)
        self.connect("button_release_event",self._on_button_release)
        self.connect("motion_notify_event",self._on_motion)

    def set_x(self, x):
        self.translate(float(x)-self._x,0)
        self._x = x

    def get_x(self):
        return self._x

    def set_y(self, y):
        self.translate(0, y-self._y)
        self._y = y

    def get_y(self):
        return self._y

    def translate(self, diff_x, diff_y):
        goocanvas.ItemSimple.translate(self, diff_x, diff_y)
        self._x += diff_x
        self._y += diff_y

    def set_width(self, width):
        assert width is not None

        self._width = float(width)

    def get_width(self):
        return self._width

    def set_height(self, height):
        assert height is not None

        self._height = float(height)

    def get_height(self):
        return self._height

    def set_linecolor(self, color):

        if isinstance(color, str) or isinstance(color, unicode):
            self.set_property("stroke-color", color)
        elif isinstance(color, int) or isinstance(color, long):
            self.set_property("stroke-color-rgba", color)
        else:
            log.error("passing %s to set_linecolor (%s)", color, type(color))

        self._linecolor = self.get_property("stroke-color-rgba")

    def get_linecolor(self):
        return self.get_property("stroke-color-rgba")

    def set_linewidth(self, width):
        self.set_property("line-width", width)

    def get_linewidth(self):
        return self.get_property("line-width")

    def set_fillcolor(self, color):

        self._fillcolor = color

        if isinstance(color, str):
            self.set_property("fill-color", color)
        elif isinstance(color, int) or isinstance(color, long):
            self.set_property("fill-color-rgba", color)
        else:
            log.debug("passing %s to set_linecolor", color)

    def get_fillcolor(self):
        return self._fillcolor

    def get_body(self):
        return self._body

    def get_bg(self):
        if hasattr(self, "_bg"):
            return self._bg
        else:
            return None

    #senales
    def _on_double_click_press(self,item,target,event):
        if event.type == gtk.gdk._2BUTTON_PRESS:
            self.emit("on-double-click")

    def _on_focus_in (self, item, target_item, event):
        if hasattr(self, "_old_linecolor"):
            return

        self._old_linecolor = self.get_linecolor()
        self.set_linecolor(0x000000FF)

    def _on_focus_out (self, item, target_item, event):
        self.set_linecolor(self._old_linecolor)
        del self._old_linecolor

    def _on_button_press(self,item,target,event):
        canvas = item.get_canvas()
        canvas.grab_focus(item)

        self._dragging = True
        fleur = gtk.gdk.Cursor(gtk.gdk.FLEUR)
        canvas = item.get_canvas ()
        canvas.pointer_grab(item,
                            gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.BUTTON_RELEASE_MASK,
                            fleur, event.time)
        self.drag_x = event.x
        self.drag_y = event.y
        return True

    def _on_button_release(self,item,target,event):

        self._dragging = False
        canvas = item.get_canvas ()
        canvas.pointer_ungrab(item, event.time)
        return True

    def _on_motion(self,item,target,event):

        if not (event.state == gtk.gdk.BUTTON1_MASK) and not self._dragging:
            return False

        new_x = event.x
        new_y = event.y
        item.translate (new_x - self.drag_x, new_y - self.drag_y)
        self.emit("on-movement")

    ### item implementation

    def do_simple_create_path(self, cr):
        cr.rectangle(0, 0, self.width, self.height)

    x = property(get_x, set_x, None, "The x coordinate of the item")
    y = property(get_y, set_y, None, "The y coordinate of the item")
    width = property(get_width, set_width, None, "The width of the item")
    height = property(get_height, set_height, None, "The height of the item")

class DragBox(goocanvas.Rect):

    def __init__(self,name,x,y):
        goocanvas.Rect.__init__(self,
                                x = x,
                                y = y,
                                width = 10,
                                height = 10,
                                line_width = 0.5,
                                fill_color = "black",
                                visibility = goocanvas.ITEM_HIDDEN)

        self.name = name
        self._dragging = False

        #conexion de senales
        self.connect("button_press_event",self._on_button_press)
        self.connect("button_release_event",self._on_button_release)
        self.connect("motion_notify_event",self._on_motion)
        self.connect("enter_notify_event",self._on_enter_notify)
        self.connect("leave_notify_event",self._on_leave_notify)


    def is_dragging(self):
        return self._dragging

    #senales
    def _on_button_press(self,item,target,event):

        self._dragging = True
        fleur = gtk.gdk.Cursor(gtk.gdk.FLEUR)
        canvas = item.get_canvas ()
        canvas.pointer_grab(item,
                            gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.BUTTON_RELEASE_MASK,
                            fleur, event.time)
        self.drag_x = event.x
        self.drag_y = event.y
        return True

    def _on_button_release(self,item,target,event):
        self._dragging = False
        canvas = item.get_canvas ()
        canvas.pointer_ungrab(item, event.time)

        return True

    def _on_enter_notify(self,item,target,event):
        item.set_property("fill-color-rgba", TANGO_COLOR_BUTTER_LIGHT)

    def _on_leave_notify(self,item,target,event):
        item.set_property("fill-color-rgba", int("000000ff",16))

    def _on_motion(self,item,target,event):
        canvas = item.get_canvas ()

        if not (event.state == gtk.gdk.BUTTON1_MASK) and not self._dragging:
            return False

        new_x = event.x
        new_y = event.y

        body = item.get_parent().get_body()
        bg = item.get_parent().get_bg()

        if item.name == 'N':
            dif = new_y - self.drag_y
            item.translate(0,dif)

            body.props.height = body.props.height - dif
            body.translate(0,dif)

            # this is trick to get a color behind a goocanvas.Table
            if bg != None:
                if isinstance(bg, goocanvas.Text):
                    pass
                else:
                    bg.props.height = bg.props.height - dif

                bg.translate(0,dif)

            #make the dragbox follow the corners of the square
            item.get_parent().dragbox['NW'].translate (0,dif)
            item.get_parent().dragbox['NE'].translate (0,dif)
            item.get_parent().dragbox['W'].translate (0,dif/2)
            item.get_parent().dragbox['E'].translate (0,dif/2)

        elif item.name == 'NE':
            dif_x = new_x - self.drag_x
            dif_y = new_y - self.drag_y
            item.translate(dif_x, dif_y)

            body.props.width = body.props.width + dif_x
            body.props.height = body.props.height - dif_y
            body.translate(0, dif_y)

            if bg != None:
                if isinstance(bg, goocanvas.Text):
                    pass
                else:
                    bg.props.width = bg.props.width + dif_x
                    bg.props.height = bg.props.height - dif_y

                bg.translate(0, dif_y)

            #make the dragbox follow the corner
            item.get_parent().dragbox['NW'].translate(0, dif_y)
            item.get_parent().dragbox['N'].translate(dif_x/2, dif_y)
            item.get_parent().dragbox['E'].translate(dif_x, dif_y/2)
            item.get_parent().dragbox['SE'].translate(dif_x, 0)

        elif item.name == 'E':
            dif = new_x - self.drag_x
            item.translate(dif,0)

            body.props.width = body.props.width + dif

            if bg != None:
                bg.props.width = body.props.width + dif

            #make the dragbox
            item.get_parent().dragbox['NE'].translate (dif, 0)
            item.get_parent().dragbox['SE'].translate (dif, 0)
            item.get_parent().dragbox['N'].translate (dif/2, 0)
            item.get_parent().dragbox['S'].translate (dif/2, 0)

        elif item.name == 'SE':
            dif_x = new_x - self.drag_x
            dif_y = new_y - self.drag_y
            item.translate(dif_x, dif_y)

            body.props.width = body.props.width + dif_x
            body.props.height = body.props.height + dif_y

            if bg != None:
                bg.props.width = bg.props.width + dif_x
                if isinstance(bg, goocanvas.Text):
                    pass
                else:
                    bg.props.height = bg.props.height + dif_y

            #move the dragbox
            item.get_parent().dragbox['N'].translate (dif_x/2, 0)
            item.get_parent().dragbox['NE'].translate (dif_x, 0)
            item.get_parent().dragbox['E'].translate (dif_x, dif_y/2)
            item.get_parent().dragbox['S'].translate (dif_x/2, dif_y)
            item.get_parent().dragbox['SW'].translate (0, dif_y)
            item.get_parent().dragbox['W'].translate (0, dif_y/2)

        elif item.name == 'S':
            dif = new_y - self.drag_y
            item.translate(0,dif)

            body.props.height = body.props.height + dif

            if bg != None:
                if isinstance(bg, goocanvas.Text):
                    pass
                else:
                    bg.props.height = bg.props.height + dif

            #move the dragbox
            item.get_parent().dragbox['W'].translate (0, dif/2)
            item.get_parent().dragbox['SW'].translate (0, dif)
            item.get_parent().dragbox['SE'].translate (0, dif)
            item.get_parent().dragbox['E'].translate (0, dif/2)

        elif item.name == 'SW':
            dif_x = new_x - self.drag_x
            dif_y = new_y - self.drag_y
            item.translate(dif_x,dif_y)

            body.props.height = body.props.height + dif_y
            body.props.width = body.props.width - dif_x
            body.translate(dif_x,0)

            if bg != None:
                if isinstance(bg, goocanvas.Text):
                    pass
                else:
                    bg.props.height = bg.props.height + dif_y
                    bg.props.width = bg.props.width - dif_x

                bg.translate(dif_x, 0)

            #move the dragbox
            item.get_parent().dragbox['N'].translate(dif_x/2, 0)
            item.get_parent().dragbox['NW'].translate (dif_x, 0)
            item.get_parent().dragbox['W'].translate (dif_x, dif_y/2)
            item.get_parent().dragbox['S'].translate (dif_x/2, dif_y)
            item.get_parent().dragbox['SE'].translate (0, dif_y)
            item.get_parent().dragbox['E'].translate (0, dif_y/2)

        elif item.name == 'W':
            dif = new_x - self.drag_x
            item.translate(dif, 0)

            body.props.width = body.props.width - dif
            body.translate(dif,0)

            if bg != None:
                bg.props.width = bg.props.width - dif
                bg.translate(dif, 0)

            #move the dragbox
            item.get_parent().dragbox['N'].translate (dif/2, 0)
            item.get_parent().dragbox['NW'].translate (dif, 0)
            item.get_parent().dragbox['SW'].translate (dif, 0)
            item.get_parent().dragbox['S'].translate (dif/2, 0)

        elif item.name == 'NW':
            dif_x = new_x - self.drag_x
            dif_y = new_y - self.drag_y
            item.translate(dif_x,dif_y)

            body.props.height = body.props.height - dif_y
            body.props.width = body.props.width - dif_x
            body.translate(dif_x,dif_y)

            if bg != None:
                if isinstance(bg, goocanvas.Text):
                    pass
                else:
                    bg.props.height = bg.props.height - dif_y
                    bg.props.width = bg.props.width - dif_x
                bg.translate(dif_x,dif_y)


            #move the dragbox
            item.get_parent().dragbox['E'].translate (0, dif_y/2)
            item.get_parent().dragbox['NE'].translate (0, dif_y)
            item.get_parent().dragbox['N'].translate (dif_x/2, dif_y)
            item.get_parent().dragbox['W'].translate (dif_x, dif_y/2)
            item.get_parent().dragbox['SW'].translate (dif_x, 0)
            item.get_parent().dragbox['S'].translate (dif_x/2, 0)

        item.get_parent().emit("changed-dimensions")


class RectangleComponent(RectBaseComponent):
    def __init__(self, **kwargs):
        RectBaseComponent.__init__(self, **kwargs)
        self._transparency = 0.0
        self.set_fillcolor(TRANSPARENT_COLOR)

    def set_transparency(self, opacity):
        pass

class LabelComponent(RectBaseComponent):

    def __init__(self, control, **kwargs):

        ### setup properties

        #text
        if 'text' in kwargs:
            self.text = unicode(kwargs['text'])
            del kwargs['text']
        else:
            self.text = "Label"

        #use_markup
        if 'use_markup' in kwargs:
            self.use_markup = unicode(kwargs['use_markup'])
            del kwargs['use_markup']
        else:
            self.use_markup = False

        #font
        if 'font' in kwargs:
            self.font = unicode(kwargs['font'])
            del kwargs['font']
        else:
            self.font = 'Sans'

        #font_size
        if 'font_size' in kwargs:
            self.font_size = float(kwargs['font_size'])
            del kwargs['font_size']
        else:
            self.font_size = 10.0

        #text_color
        if 'text_color' in kwargs:
            self.text_color = gtk.gdk.color_parse(kwargs['text_color'])
            del kwargs['text_color']
        else:
            self.text_color = gtk.gdk.Color(0, 0, 1)


        RectBaseComponent.__init__(self, **kwargs)
        self._control = control

        self.connect("on-double-click", self._on_edit_label_selected)

    def set_text(self, text):
        self._bg.set_property("text", text)
        self.translate(0,0)

    def get_text(self):
        return self._bg.get_property("text")

    def set_font(self, font):
        """Define la fuente que debe usar la instancia de LabelComponent

        El parametro font es un string con el mismo formato que el constructor de pango.FontDescription"""
        self._bg.set_property("font", font)
        self.translate(0,0)

    def get_font(self):
        "Retorna la fuente que esta usando la instancia de LabelComponent"
        return self._bg.get_property("font")

    #signals
    def _on_edit_label_selected(self, item):
        #self._control.
        pass

    ### item implementation
    def do_simple_paint(self, cr, bounds):
        cr.move_to(10,20)
        pangocr = pangocairo.CairoContext(cr)
        layout = pangocr.create_layout()

        if self.use_markup:
            layout.set_markup(self.text)
        else:
            layout.set_text(self.text)

        layout.set_wrap(pango.WRAP_WORD)
        layout.set_width(int(self.width*pango.SCALE))
        needed_height = layout.get_size()[1]/pango.SCALE
        if self.height < needed_height:
            self.height = needed_height

        self.bounds.x1 = float(self.x)
        self.bounds.y1 = float(self.y)
        self.bounds.x2 = float(self.width) +200
        self.bounds.y2 = float(self.height)+200

        RectBaseComponent.do_simple_paint(self, cr, bounds)

        desc = pango.FontDescription("%s %s" % (self.font, str(self.font_size)))
        layout.set_font_description(desc)
        cr.set_source_rgb (color.gdk2rgb(self.text_color)[0],
                           color.gdk2rgb(self.text_color)[1],
                           color.gdk2rgb(self.text_color)[2])
        #pangocairo.CairoContext.update_layout(layout)
        pangocr.update_layout(layout)
        #pangocairo.CairoContext.show_layout(layout)
        pangocr.show_layout(layout)
        pangocr.layout_path(layout)
        ## cr.move_to(self.line_width + 5, self.line_width + 10)

        ## cr.set_source_rgb (color.gdk2rgb(self.text_color)[0],
        ##                    color.gdk2rgb(self.text_color)[1],
        ##                    color.gdk2rgb(self.text_color)[2])

        ## cr.select_font_face(self.font,
        ##                     cairo.FONT_SLANT_NORMAL,
        ##                     cairo.FONT_WEIGHT_BOLD)

        ## cr.set_font_size(self.font_size)
        ## cr.show_text (self.text)


    def do_simple_update (self, cr):

        RectBaseComponent.do_simple_update(self, cr)
        half_lw = self.line_width/2
        self.bounds.x1 = float(self.x - half_lw)
        self.bounds.y1 = float(self.y - half_lw)
        self.bounds.x2 = float(self.x + self.width + half_lw)
        self.bounds.y2 = float(self.y + self.height + half_lw)
        return None

gobject.type_register(LabelComponent)


class EntityComponent(RectBaseComponent):

    def __init__(self, name, x=0, y=0, width=100, height=100):
        RectBaseComponent.__init__(self, width=width, height=height)
        self.attr_list = list()
        self._num_rows = 0
        self._bg = self._body

        self.set_x(float(x))
        self.set_y(float(y))

        # this table is the top level table of the EntityComponent
        # only contains the entity name, line separator, attributes table
        self._toptable = goocanvas.Table(parent=self,
                                         width=self.get_width(),
                                         height=self.get_height(),
                                         column_spacing=5,
                                         row_spacing=2,
                                         fill_color="black")

        # the title of the entity
        self._name = name
        self._entity_title = goocanvas.Text(text="<b>" + str(self._name) + "</b>",
                                            use_markup=True,
                                            font="sans 8")

        self._toptable.add_child(self._entity_title)
        self._toptable.set_child_properties(self._entity_title,
                                            row=0,
                                            column=0,
                                            x_align=0.5,
                                            top_padding=5,
                                            left_padding=5)

        #line to use like separator between the entity name and the attributes
        pts = goocanvas.Points([(1,1),(100,1)])
        self._line = goocanvas.Polyline(parent=self._toptable,
                                        points=pts,
                                        stroke_color="black",
                                        line_width=1)

        self._toptable.set_child_properties(self._line,
                                            row=1,
                                            column=0)

        # this table must contain the attributes
        self._body = goocanvas.Table(width=self.get_width(),
                                     height=self.get_height(),
                                     column_spacing=5,
                                     row_spacing=2,
                                     fill_color="black")

        self._toptable.add_child(self._body)
        self._toptable.set_child_properties(self._body,
                                            row=2,
                                            column=0,
                                            x_align=0.0,
                                            top_padding=5)

    def add_attribute(self,attribute):
        "Agrega un nuevo atributo a la entidad"

        self.attr_list.append(attribute)

        self._body.add_child(attribute.items['name'])
        self._body.set_child_properties(attribute.items['name'],
                                        row=self._num_rows,
                                        column=0,
                                        x_align=0.0,
                                        left_padding=5)

        self._body.add_child(attribute.items['mandatory'])
        self._body.set_child_properties(attribute.items['mandatory'],
                                        row=self._num_rows,
                                        column=1,
                                        x_align=0.5)

        self._body.add_child(attribute.items['datatype'])
        self._body.set_child_properties(attribute.items['datatype'],
                                        row=self._num_rows,
                                        column=2,
                                        x_align=0.0)

        self._num_rows += 1
        self.request_update()


    def set_fillcolor(self, color):

        self._fillcolor = color

        if isinstance(color, str):
            self._bg.set_property("fill-color", color)
        elif isinstance(color, int) or isinstance(color, long):
            self._bg.set_property("fill-color-rgba", color)
        else:
            log.debug("passing %s to set_linecolor", color)


    def get_icon_path(cls):

        filename = resource_filename('rascase.resources.pixmaps', 'entity-icon.png')
        return filename

    get_icon_path = staticmethod(get_icon_path) #makes the method static

    #get-set de propiedad
    def get_body(self):
        """Retorna el cuerpo del objeto

        """
        return self._body

    def set_title(self, name):
        self._name = "<b>" + name + "</b>"

    def refresh(self):
        print "nombre entidad:", self._name
        self._entity_title.set_property("text", self._name)
        self.translate(0,0) #trick to update the view

class AttributeComponent(gobject.GObject):
    "Componente gráfico que se pone dentro de una entidad"
    def __init__(self, name, datatype, default_value=None, pk=False, mandatory=False):
        gobject.GObject.__init__(self)
        self._name = name
        self._default_value = default_value
        self._mandatory = mandatory
        self._primary_key = pk
        self._data_type = datatype[0]

        if len(datatype) > 1:
            self._data_type_length = datatype[1]
        else:
            self._data_type_length = None

        self.items = {'mandatory':goocanvas.Text(text="", use_markup=True, font="sans 8"),
                      'name':goocanvas.Text(text="", use_markup=True, font="sans 8"),
                      'datatype':goocanvas.Text(text="", use_markup=True, font="sans 8")
                      }

        if self._mandatory:
            text_m = "[M]"
        else:
            text_m = ""

        if self._primary_key:
            text_name = "<u>" + self._name + "</u>"
        else:
            text_name = self._name

        #FIXME: this should not happen, the controller must do this
        from rascase.core import LogicalDataType
        text_dt = LogicalDataType.to_string(self._data_type)
        if isinstance(self._data_type_length, int):
            text_dt = text_dt + "(" + str(self._data_type_length) + ")"

        self.items['mandatory'].set_property("text", text_m)
        self.items['name'].set_property("text", text_name)
        self.items['datatype'].set_property("text", text_dt)

    def refresh(self):
        mod = self.get_data("model")

        if mod.is_mandatory() != self._mandatory:
            self._mandatory = mod.is_mandatory()
            if self._mandatory:
                text_m = "[M]"
            else:
                text_m = ""
            self.items['mandatory'].set_property("text", text_m)

        self._name = mod.get_name()
        self._primary_key = mod.is_primary_key()
        if self._primary_key:
            text_name = "<u>" + self._name + "</u>"
        else:
            text_name = self._name

        self.items['name'].set_property("text", text_name)

        #FIXME: this should not happen, the controller must do this
        dt_changed = False
        if mod.get_data_type()[0] != self._data_type:
            self._data_type = mod.get_data_type()[0]
            dt_changed = True

        if (len(mod.get_data_type())>1):
            if mod.get_data_type()[1] != self._data_type_length:
                self._data_type_length = mod.get_data_type()[1]
                dt_changed = True
        else:
            self._data_type_length = None
            dt_changed = True
        if dt_changed:
            from rascase.core import LogicalDataType
            text_dt = LogicalDataType.to_string(self._data_type)
            if self._data_type_length != None:
                text_dt = text_dt + "(" + str(self._data_type_length) + ")"

            self.items['datatype'].set_property("text", text_dt)

        #trick to update the view
        for key in self.items.keys():
            self.items[key].translate(0,0)

    def set_primary_key (self, valor) :
        self._primary_key = valor

    def get_primary_key (self) :
        return self._primary_key

    def set_default_value (self, value) :
        self._default_value = value

    def get_default_value (self) :
        return self._default_value

    def set_data_type (self, datatype):
        """Define el tipo de dato del atributo, datatype es una tuple() de uno o dos elementos,
        el primer elemento es el tipo de dato y el segundo elemento (opcional) es un entero
        que representa el largo del tipo de dato.

        Por ejemplo datatype=(LogicalDataType.VARCHAR, 10) representa un varchar de largo 10
        """
        self._data_type = datatype[0]

        if len(datatype) > 1:
            self._data_type_length = datatype[1]
        else:
            self._data_type_length = None

    def get_data_type (self) :
        if self._data_type_length != None:
            return (self._data_type, self._data_type_length)
        else:
            return (self._data_type,)

    def set_mandatory (self, mandatory) :
        self._mandatory = mandatory

    def get_mandatory (self) :
        return self._mandatory


class LineBaseComponent(goocanvas.Polyline):
    __gsignals__ = {
        'on-double-click': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ())
        }

    def __init__(self, **kargs):
        goocanvas.Polyline.__init__(self, **kargs)

        if "line_width" in kargs.keys():
            self._line_width = kargs["line_width"]
        else:
            self._line_width = None

        if "line_color" in kargs.keys():
            self._line_color = kargs["line_color"]
        else:
            self._line_color = int("000000",16)

    def set_linewidth(self, value):
        self.set_property("line-width", value)
        self._line_width = value

    def get_linewidth(self):
        return self._line_width

    def set_line_color(self, value):

        if isinstance(value,str):
            self.set_property("stroke-color", value)
        else:
            self.set_property("stroke-color-rgba", value)

        self._line_color = value

    def get_line_color(self):
        return self._line_color

class RelationshipComponent(LineBaseComponent):
    def __init__(self, entity1, dependent1, mandatory1,
                 entity2, dependent2, mandatory2, cardinality, color):

        #entity 1
        self._entity1 = entity1
        self._dependent1 = dependent1
        self._mandatory1 = mandatory1

        #entity 2
        self._entity2 = entity2
        self._dependent2 = dependent2
        self._mandatory2 = mandatory2

        #cardinality
        self._cardinality = cardinality

        LineBaseComponent.__init__(self,
                                   can_focus=True,
                                   points=self._build_points(),
                                   stroke_color_rgba=color)

        # signals connections
        self._entity1.connect("on-movement",self._on_entity_movement)
        self._entity2.connect("on-movement",self._on_entity_movement)
        self.connect("button-press-event", self._on_button_press)
        self.connect("focus-in-event", self._on_focus_in)
        self.connect("focus-out-event", self._on_focus_out)


    def _build_points(self):

        points_list = list()

        if self._entity1.get_x() < self._entity2.get_x():
            x1 = self._entity1.get_x() + self._entity1.get_width()
            x2 = self._entity2.get_x()
        else:
            x1 = self._entity1.get_x()# - self._entity1.get_width()
            x2 = self._entity2.get_x() + self._entity2.get_width()

        y1 = self._entity1.get_y() + self._entity1.get_height()/2
        y2 = self._entity2.get_y() + self._entity2.get_height()/2

        points_list.append((x1,y1))

        #starts variations

        from rascase.core import Relationship

        if self._entity1.get_x() < self._entity2.get_x():
            if self._cardinality == Relationship.CARDINALITY_1_N or \
                   self._cardinality == Relationship.CARDINALITY_1_1:
                if self._dependent1:
                    p1 = (x1+5, y1)
                    points_list.append(p1)
                    points_list.append((p1[0]+10,p1[1]))
                    points_list += self._do_triangle((p1[0]+10,p1[1]), p1, False)
                    pf = p1
                else:
                    pf = (x1+15,y1)
                    points_list.append(pf)

            elif self._cardinality == Relationship.CARDINALITY_N_1 or \
                     self._cardinality == Relationship.CARDINALITY_N_N:
                if self._dependent1:
                    points_list += self._do_pata_triangle((x1,y1),
                                                          (x1+18,y1),
                                                          right=False)
                    pf = (x1+15, y1)

                else:
                    points_list += self._do_pata_gallo((x1+15, y1), (x1,y1))
                    pf = (x1+15, y1)

            if self._mandatory2:
                p1 = (pf[0]+10, pf[1])
                points_list.append(p1)
                points_list += self._do_line(p1)

            else:
                h = pf[0]+15
                k = pf[1]
                r = 5
                points_list += self._do_circle(h, k, r)

        else:
            pass

        #finish variations

        points_list.append((x2,y2))

        pts = goocanvas.Points(points_list)
        return pts

    def _one(self, pt_begin, pt_end):
        pts = list()
        if pt_begin[0] < pt_end[0]:
            #entity 1 is on the left
            dif = pt_end[0] - pt_begin[0]
            p1 = (pt_begin[0]+dif/4, pt_begin[1])
            pts.append(p1)

            if self._mandatory2:
                # draw a vertical line
                pts += self._do_line(p1)
            else:
                # draw a little circle
                # (x-h)^2 + (y-k)^2 = r^2
                r = 5
                h = p1[0]+5
                k = p1[1]
                pts += self._do_circle(h, k, r)
        else:
            #entity 1 is on the right
            dif = pt_begin[0] - pt_end[0]
            p1 = (pt_begin[0]-dif/4, pt_begin[1])
            pts.append(p1)

            if self._mandatory2:
                # draw vertical line
                pts += self._do_line(p1)

            else:
                # draw a little circle
                # (x-h)^2 + (y-k)^2 = r^2
                r = 5
                h = p1[0]-5
                k = p1[1]
                pts += self._do_circle(h, k, r)

        pts.append(pt_end)
        return pts

    def _do_line(self, p1):
        pts = list()

        p2 = (p1[0], p1[1] - 10)
        pts.append(p2)

        p3 = (p1[0], p1[1] + 10)
        pts.append(p3)
        pts.append(p1)
        return pts

    def _do_circle(self, h, k, r):
        pts = list()
        x = h-r
        while x < h+r:
            y = math.sqrt(25-math.pow(x-h,2))+k
            pts.append((x,y))
            x+=0.2 # the step

        x = h-r
        while x < h+r:
            y = -math.sqrt(25-math.pow(x-h,2))+k
            pts.append((x,y))
            x+=0.2 # the step

        return pts

    def _do_triangle(self, pt_begin, pt_end, left_at_end=True):
        pts = list()
        if pt_begin[0] < pt_end[0]:
            #  /|
            #  \|
            p1 = (pt_begin[0]+10, pt_begin[1]-10)
            pts.append(p1)

            p2 = (p1[0], p1[1]+20)
            pts.append(p2)
            pts.append(pt_begin)
            if left_at_end:
                pts.append(p2)

                p3 = (p2[0], p2[1]-10)
                pts.append(p3)
        else:
            # |\
            # |/
            p1 = (pt_begin[0]-10, pt_begin[1]-10)
            pts.append(p1)

            p2 = (p1[0], p1[1]+20)
            pts.append(p2)
            pts.append(pt_begin)

            if left_at_end:
                pts.append(p2)

                p3 = (p2[0], p2[1]-10)
                pts.append(p3)

        return pts

    def _do_pata_triangle(self, pt_begin, pt_end, right=True):
        pts = list()

        if right:
            #    /|-
            # -<  |-
            #    \|-
            p0 = (pt_end[0]-5, pt_end[1])
            pts += self._do_triangle(pt_begin, p0)
            p1 = (p0[0], p0[1]-3)
            pts.append(p1)

            p2 = (p1[0]+5, p1[1])
            pts.append(p2)
            pts.append(p1)

            p3 = (p1[0], p1[1]+6)
            pts.append(p3)

            p4 = (p3[0]+5, p3[1])
            pts.append(p4)
            pts.append(p3)
            pts.append(p0)
            pts.append(pt_end)

        else:
            # -|\
            # -| >-
            # -|/
            p0 = (pt_begin[0]+8, pt_begin[1])
            pts.append(p0)

            p1 = (p0[0], p0[1]-5)
            pts.append(p1)

            p2 = (p1[0]-8, p1[1])
            pts.append(p2)
            pts.append(p1)

            p3 = (p1[0], p1[1]+10)
            pts.append(p3)

            p4 = (p3[0]-8, p3[1])
            pts.append(p4)
            pts.append(p3)
            pts.append(p0)
            pts.append(pt_end)
            pts += self._do_triangle(pt_end, p0, False)

        return pts

    def _do_pata_gallo(self, pt_begin, pt_end, left_at_end=True):

        pts = list()

        pts.append(pt_end)
        pts.append(pt_begin)

        p1 = (pt_end[0], pt_end[1]-5)
        pts.append(p1)
        pts.append(pt_begin)

        p2 = (pt_end[0], pt_end[1]+5)
        pts.append(p2)
        pts.append(pt_begin)

        if left_at_end:
            pts.append(pt_end)

        ## else:
        ##     #  \
        ##     # ---
        ##     #  /
        ##     pts.append(pt_end)

        return pts

    def set_cardinality(self, type_):
        self._cardinality = type_

    def get_cardinality(self):
        return self._cardinality

    def set_entity1(self, entity):
        self._entity1 = entity

    def get_entity1(self):
        return self._entity1

    def set_entity2(self, entity):
        self._entity2 = entity

    def get_entity2(self):
        return self._entity2

    #signal callbacks
    def _on_entity_movement(self, item):
        "Este metodo es ejecutado cada vez que alguna de las entidades de la relacion emite la señal 'on-movement'"
        self.set_property("points", self._build_points())

    def _on_button_press(self, item, target_item, event):
        if event.type == gtk.gdk._2BUTTON_PRESS:
            self.emit("on-double-click")
            print "double click"

        canvas = item.get_canvas()
        canvas.grab_focus(item)

    def _on_focus_in(self, item, target_item, event):
        self.set_line_color(TANGO_COLOR_ORANGE_DARK)

    def _on_focus_out(self, item, target_item, event):
        self.set_line_color(int('000000ff',16))

class InheritanceComponent(LineBaseComponent):
    def __init__(self, father, son, **kargs):

        self._father = father
        self._son = son
        LineBaseComponent.__init__(self,
                                   points=self._build_points(),
                                   stroke_color="green")

        self._father.connect("on-movement", self._on_entity_movement)
        self._son.connect("on-movement", self._on_entity_movement)

    def _build_points(self):
        points_list = list()

        if self._father.get_x() < self._son.get_x():
            x1 = self._father.get_x() + self._father.get_width()
            x2 = self._son.get_x()
        else:
            x1 = self._father.get_x()# - self._father.get_width()
            x2 = self._son.get_x() + self._son.get_width()

        y1 = self._father.get_y() + self._father.get_height()/2
        y2 = self._son.get_y() + self._son.get_height()/2

        points_list.append((x1,y1))

        if self._father.get_x() < self._son.get_x():
            p1 = (x2-15, y2)
            points_list.append(p1)

            p2 = (p1[0] + 5, p1[1])
            points_list.append(p2)

            p3 = (p2[0], p2[1] - 10)
            points_list.append(p3)

            p4 = (p3[0] + 10, p3[1] + 10)
            points_list.append(p4)

            p5 = (p4[0] - 10, p4[1] + 10)
            points_list.append(p5)

            points_list.append(p2)
        else:
            p1 = (x2 + 15, y2)
            points_list.append(p1)

            p2 = (p1[0] - 5, p1[1])
            points_list.append(p2)

            p3 = (p2[0], p2[1] - 10)
            points_list.append(p3)

            p4 = (p3[0] - 10, p3[1] + 10)
            points_list.append(p4)

            p5 = (p4[0] + 10, p4[1] + 10)
            points_list.append(p5)

            points_list.append(p2)

        #points_list.append((x2,y2))

        pts = goocanvas.Points(points_list)

        return pts

    def set_father(self, father):
        self._father = father

    def get_father(self):
        return self._father

    def set_son(self, son):
        self._son = son

    def get_son(self):
        return self._son

    def _on_entity_movement(self, item):
        self.set_property("points", self._build_points())

#physical model components

class TableComponent(RectBaseComponent):
    def __init__(self):
        RectBaseComponent.__init__(self)

class ReferenceComponent(LineBaseComponent):
    def __init__(self):
        LineBaseComponent.__init__(self)



class Canvas(goocanvas.Canvas):
    "Esta clase configura el canvas que provee goocanvas.Canvas"

    def __init__(self, **kargs):
        goocanvas.Canvas.__init__(self, **kargs)
        self.scrolled_win = gtk.ScrolledWindow()
        self.scrolled_win.set_shadow_type(gtk.SHADOW_IN)
        self.scrolled_win.set_data("canvas", self)
        self.scrolled_win.show()

        self.set_flags(gtk.CAN_FOCUS)
        self.set_size_request(640, 480)
        self.set_bounds(0, 0, 800, 700)
        root = self.get_root_item()
        self.set_root_item(root)
        self.show()

        self.scrolled_win.add(self)

    def add_child(self, item):
        self.get_root_item().add_child(item)

class ViewEditEntity:
    def __init__(self, entity, control, parent):

        self._control = control
        self._entity = entity

        glade_file = resource_filename("rascase.resources.glade", "wndeditentity.glade")
        self._wTree = gtk.glade.XML(glade_file)

        signals_dic = {"on_btn_ok_clicked":self._on_btn_ok_clicked,
                       "on_btn_cancel_clicked":self._on_btn_cancel_clicked,
                       "on_new_attr_clicked":self._on_new_attr_clicked}

        self._wTree.signal_autoconnect(signals_dic)
        self._window = self._wTree.get_widget("wndeditentity")
        self._window.set_transient_for(parent)

        ## main information
        widget = self._wTree.get_widget("entry_name")
        widget.set_text(entity.get_name())

        widget = self._wTree.get_widget("entry_codename")
        widget.set_text(entity.get_codename())

        widget = self._wTree.get_widget("txt_description")
        buff = widget.get_buffer()
        buff.set_text(entity.get_description())

        ## attributes
        tree_attributes = self._wTree.get_widget("tree_attributes")

        self._attr_list = gtk.ListStore(gobject.TYPE_STRING, #0 name
                                        gobject.TYPE_STRING, #1 codename
                                        gobject.TYPE_INT,    #2 datatype constant
                                        gobject.TYPE_STRING, #3 datatype string
                                        gobject.TYPE_OBJECT, #4 all data_types
                                        gobject.TYPE_INT,    #5 data_type_length
                                        gobject.TYPE_BOOLEAN,#6 pk
                                        gobject.TYPE_BOOLEAN,#7 mandatory
                                        gobject.TYPE_STRING, #8 description
                                        object)              #9 el objeto atributo

        self._datatypes_store = gtk.ListStore(gobject.TYPE_STRING,# 0 datatype NAME
                                              gobject.TYPE_INT)   # 1 datatype CODE

        from rascase.core import LogicalDataType
        for dt in LogicalDataType.get_data_types():
            self._datatypes_store.append([LogicalDataType.to_string(dt), dt])

        for attr in self._entity.get_attributes():

            if len(attr.get_data_type()) > 1:
                dt_length = int(attr.get_data_type()[1])
            else:
                dt_length = int(0)

            self._attr_list.append([str(attr.get_name()),
                                    str(attr.get_codename()),
                                    int(attr.get_data_type()[0]),
                                    str(LogicalDataType.to_string(attr.get_data_type()[0])),
                                    self._datatypes_store,
                                    dt_length,
                                    attr.is_primary_key(),
                                    attr.is_mandatory(),
                                    attr.get_description(),
                                    attr])

        tree_attributes.set_model(self._attr_list)

        # column name
        col_name = gtk.TreeViewColumn("Nombre")
        tree_attributes.append_column(col_name)
        cell = gtk.CellRendererText()
        cell.set_property("editable", True)
        cell.connect("edited", self._on_name_edited)
        col_name.pack_start(cell)
        col_name.add_attribute(cell, "text", 0)

        #column codename
        col_codename = gtk.TreeViewColumn("Código")
        tree_attributes.append_column(col_codename)
        cell = gtk.CellRendererText()
        cell.set_property("editable", True)
        cell.connect("edited", self._on_codename_edited)
        col_codename.pack_start(cell)
        col_codename.add_attribute(cell, "text", 1)

        # data type ?? por el momento no lo ponemos
        cell = gtk.CellRendererCombo()
        cell.set_property("model",self._datatypes_store)
        cell.set_property("has-entry", False)
        cell.set_property("text-column", 0)#de donde sacar el texto para el combo
        cell.set_property("editable", True)
        cell.connect("edited", self._on_data_type_edited)
        col_datatype = gtk.TreeViewColumn("Tipo de dato", cell)
        col_datatype.set_attributes(cell, text=3)
        tree_attributes.append_column(col_datatype)
        #datatype length
        cell = gtk.CellRendererText()
        cell.set_property("editable", True)
        cell.connect("edited", self._on_data_type_length)
        col_datatype.pack_start(cell)
        col_datatype.add_attribute(cell, "text", 5)


        #pk
        cell = gtk.CellRendererToggle()
        cell.set_property("activatable", True)
        cell.connect("toggled", self._on_pk_togled)
        col = gtk.TreeViewColumn("Identificador", cell)
        col.set_attributes(cell, active=6)
        tree_attributes.append_column(col)

        #mandatory
        cell = gtk.CellRendererToggle()
        cell.set_property("activatable", True)
        cell.connect("toggled", self._on_mandatory_togled)
        col = gtk.TreeViewColumn("Obligatorio", cell)
        col.set_attributes(cell, active=7)
        tree_attributes.append_column(col)

        # column name
        col_name = gtk.TreeViewColumn("Descripción")
        tree_attributes.append_column(col_name)
        cell = gtk.CellRendererText()
        cell.set_property("editable", True)
        cell.connect("edited", self._on_description_edited)
        col_name.pack_start(cell)
        col_name.add_attribute(cell, "text", 8)

        self._window.show_all()

    #signals
    def _on_name_edited(self, cellrenderertext, path, new_text):
        iter_ = self._attr_list.get_iter(path)

        attr = self._attr_list.get_value(iter_, 9)

        attr.set_name(new_text)
        self._attr_list.set_value(iter_, 0, attr.get_name())

        attr.set_codename(new_text)
        self._attr_list.set_value(iter_, 1, attr.get_codename())

    def _on_codename_edited(self, cellrenderertext, path, new_text):
        iter_ = self._attr_list.get_iter(path)

        attr = self._attr_list.get_value(iter_, 9)
        attr.set_codename(new_text)

        self._attr_list.set_value(iter_, 1, attr.get_codename())

    def _on_data_type_edited(self, cellrenderertext, path, new_text):

        iter_ = self._datatypes_store.get_iter_first()
        while iter_ != None:

            value = self._datatypes_store.get_value(iter_, 0)

            if value == new_text:
                iter_2 = self._attr_list.get_iter(path)

                # TODO: debe actualizarse el object
                attr = self._attr_list.get_value(iter_2, 9)
                attr.set_data_type(self._datatypes_store.get_value(iter_, 1),
                                   self._attr_list.get_value(iter_2, 5))

                self._attr_list.set(iter_2, 2, self._datatypes_store.get_value(iter_, 1))
                self._attr_list.set(iter_2, 3, value)
                break

            iter_ = self._datatypes_store.iter_next(iter_)

    def _on_data_type_length(self, cellrenderertext, path, new_text):

        #if try to put a nondigit string in the entry
        if not new_text.isdigit():
            dialog = gtk.Dialog("Largo no valido",
                     self._window,
                     gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                     (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
            hbox = gtk.HBox()

            image = gtk.Image()
            image.set_from_stock(gtk.STOCK_DIALOG_INFO, gtk.ICON_SIZE_DIALOG)
            hbox.pack_start(image)

            label = gtk.Label("El largo de un tipo de dato debe ser numérico")
            hbox.pack_start(label)

            hbox.show_all()
            dialog.vbox.pack_start(hbox)
            dialog.run()
            dialog.destroy()
            return

        iter_ = self._attr_list.get_iter(path)

        attr = self._attr_list.get_value(iter_, 9)
        attr.set_data_type(None, int(new_text))

        if len(attr.get_data_type()) > 1:
            self._attr_list.set(iter_, 5, int(attr.get_data_type()[1]))
        else:
            self._attr_list.set(iter_, 5, 0)

    def _on_pk_togled(self, cellrenderertoggle, path):

        iter_attr_list = self._attr_list.get_iter(path)

        attr = self._attr_list.get_value(iter_attr_list, 9)
        attr.set_primary_key(not attr.is_primary_key())
        self._attr_list.set_value(iter_attr_list, 6, attr.is_primary_key())

    def _on_mandatory_togled(self, cellrenderertoggle, path):

        iter_attr_list = self._attr_list.get_iter(path)

        attr = self._attr_list.get_value(iter_attr_list, 9)
        attr.set_mandatory(not attr.is_mandatory())
        self._attr_list.set_value(iter_attr_list, 7, attr.is_mandatory())

    def _on_description_edited(self, cellrenderertext, path, new_text):
        iter_ = self._attr_list.get_iter(path)

        attr = self._attr_list.get_value(iter_, 9)
        attr.set_description(new_text)

        self._attr_list.set_value(iter_, 8, attr.get_description())

    def _on_new_attr_clicked(self, toolbutton):
        attr = self._control.get_new_attribute()

        #para saber si tiene datatype length
        if len(attr.get_data_type()) > 1:
            dt_length = attr.get_data_type()[1]
        else:
            dt_length = 0

        self._attr_list.append([attr.get_name(),
                                attr.get_codename(),
                                attr.get_data_type()[0],
                                self._control.logical_data_type_to_string(attr.get_data_type()[0]),
                                self._datatypes_store,
                                dt_length,
                                attr.is_primary_key(),
                                attr.is_mandatory(),
                                attr.get_description(),
                                attr])

    def _on_btn_ok_clicked(self, button):

        widget = self._wTree.get_widget("entry_name")
        self._entity.set_name(widget.get_text())

        widget = self._wTree.get_widget("entry_codename")
        self._entity.set_codename(widget.get_text())

        widget = self._wTree.get_widget("txt_description")
        buff = widget.get_buffer()
        text = buff.get_text(buff.get_start_iter(), buff.get_end_iter())
        self._entity.set_description(text)

        self._control.refresh()
        self._window.destroy()


    def _on_btn_cancel_clicked(self, button):
        pass

    def on_fill_color_set(self, colorbutton):
        pass

    def on_toolbtn_new_attribute(self, toolbutton):
        pass

    def on_toolbtn_cut_attribute(self, toolbutton):
        pass

    def on_toolbtn_copy_attribute(self, toolbutton):
        pass

    def on_toolbtn_paste_attribute(self, toolbutton):
        pass

    def on_toolbtn_delete_attribute(self, toolbutton):
        pass

    def on_primary_toggled(self, checkbutton):
        pass

    def on_mandatory_toggled(self, checkbutton):
        pass

class ViewEditRelationship:
    def __init__(self, relationship, control):
        pass

    def on_dependent1_toggled(self, checkbutton):
        pass

    def on_dependent2_toggled(self, checkbutton):
        pass

    def on_btn_ok_clicked(self, button):
        pass

    def on_btn_cancel_clicked(self, button):
        pass


class ViewEditLabel:
    def __init__(self, label, control):
        pass

    def on_font_set(self, fontbutton):
        pass

    def on_btn_ok_clicked(self, button):
        pass

    def on_btn_cancel_clicked(self, button):
        pass

class ViewEditRectangle:
    def __init__(self, rectangle, control):
        pass

    def on_line_color_set(self, colorbutton):
        pass

    def on_btn_ok_clicked(self, button):
        pass

    def on_btn_cancel_clicked(self, button):
        pass

class ViewFileDialog:
    def __init__(self, action, title, parent, filter):

        self.path = None
        self._window = gtk.FileChooserDialog(action=action,
                                             title=title,
                                             parent=parent,
                                             buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                                                      gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

        self._window.set_filter(filter)
        self._window.set_property("select-multiple", False)
        self._window.show_all()
        response = self._window.run()

        if response == gtk.RESPONSE_ACCEPT:
            self.path = self._window.get_filename()

        self._window.destroy()

class ViewAddRelationship:
    "Contiene la vista que es desplegada cuando el usuario selecciona agregar una nueva relación"
    def __init__(self, control, parent):

        self._control = control

        entities_list = self._control.get_all_entities()

        self._wTree = gtk.glade.XML(resource_filename('rascase.resources.glade',
                                                      'wndaddrelationship.glade'))

        entry = self._wTree.get_widget("entry_name")
        entry.connect("changed", self._on_entry_name_changed)

        self._window = self._wTree.get_widget("wndaddrelationship")
        self._window.set_transient_for(parent)

        entities_store = gtk.ListStore(gobject.TYPE_STRING, #name
                                       gobject.TYPE_STRING) #codename

        for x in entities_list:
            entities_store.append([x[0],x[1]])

        #combobox for entity 1
        combo = self._wTree.get_widget("combo_entity1")
        combo.set_model(entities_store)
        cell = gtk.CellRendererText()
        combo.pack_start(cell, True)
        combo.add_attribute(cell, 'text', 0)

        #dependent1
        checkbox = self._wTree.get_widget("check1_dependent")
        checkbox.connect("toggled", self._on_check_dependent_toggled)

        #combobox for entity 2
        combo = self._wTree.get_widget("combo_entity2")
        combo.set_model(entities_store)
        cell = gtk.CellRendererText()
        combo.pack_start(cell, True)
        combo.add_attribute(cell, 'text', 0)

        #dependent2
        checkbox = self._wTree.get_widget("check2_dependent")
        checkbox.connect("toggled", self._on_check_dependent_toggled)

        #combox for cardinality types
        cardinalities_store = gtk.ListStore(gobject.TYPE_STRING, #name
                                            gobject.TYPE_INT)    #code

        cardinalities_store.append(['1 a 1', 0])
        cardinalities_store.append(['1 a N', 1])
        cardinalities_store.append(['N a 1', 2])
        cardinalities_store.append(['N a N', 3])

        combo = self._wTree.get_widget("combo_cardinality")
        combo.set_model(cardinalities_store)
        cell = gtk.CellRendererText()
        combo.pack_start(cell)
        combo.add_attribute(cell, 'text', 0)
        combo.connect("changed", self._on_cardinality_changed)

        button = self._wTree.get_widget("btn_cancel")
        button.connect("clicked", self._on_btn_cancel_relationship_clicked)

        button = self._wTree.get_widget("btn_add")
        button.connect("clicked", self._on_btn_add_relationship_clicked)

        self._window.show_all()

    def _on_entry_name_changed(self, entry):
        entry_codename = self._wTree.get_widget("entry_codename")

        aux = entry.get_text().upper().replace(' ', '_')
        entry_codename.set_text(aux)

    def _on_cardinality_changed(self, combobox):
        combo_model = combobox.get_model()
        path_str = str(combobox.get_active())
        iter_cardinality = combo_model.get_iter_from_string(path_str)

        new_value = [combo_model.get_value(iter_cardinality, 0),#name
                     combo_model.get_value(iter_cardinality, 1)]#code (int)

        if new_value[1] == 0: # 1 a 1
            #TODO: configure the dialog when te user selects 1 to 1 relation
            pass

        elif new_value[1] == 1: # 1 a N
            #for entity 1
            checkbox = self._wTree.get_widget("check1_dependent")
            checkbox.set_active(False)
            checkbox.set_sensitive(False)

            checkbox = self._wTree.get_widget("check1_mandatory")
            checkbox.set_sensitive(True)

            #for entity 2
            checkbox = self._wTree.get_widget("check2_dependent")
            checkbox.set_sensitive(True)

            checkbox = self._wTree.get_widget("check2_mandatory")
            checkbox.set_active(True)
            checkbox.set_sensitive(False)


        elif new_value[1] == 2: # N a 1
            #for entity 1
            checkbox = self._wTree.get_widget("check1_dependent")
            checkbox.set_sensitive(True)

            checkbox = self._wTree.get_widget("check1_mandatory")
            checkbox.set_active(True)
            checkbox.set_sensitive(False)

            #for entity 2
            checkbox = self._wTree.get_widget("check2_dependent")
            checkbox.set_active(False)
            checkbox.set_sensitive(False)

            checkbox = self._wTree.get_widget("check2_mandatory")
            checkbox.set_sensitive(True)

        elif new_value[1] == 3: # N a N
            #for entity 1
            checkbox = self._wTree.get_widget("check1_dependent")
            checkbox.set_active(False)
            checkbox.set_sensitive(False)

            checkbox = self._wTree.get_widget("check1_mandatory")
            checkbox.set_sensitive(True)

            #for entity 2
            checkbox = self._wTree.get_widget("check2_dependent")
            checkbox.set_active(False)
            checkbox.set_sensitive(False)

            checkbox = self._wTree.get_widget("check2_mandatory")
            checkbox.set_sensitive(True)

    def _on_check_dependent_toggled(self, togglebutton):
        """Controla la habilitacion y dehabilitacion de los check button
        de la propiedad 'dependiente' para la relación
        """

        if togglebutton == self._wTree.get_widget("check1_dependent"):
            check_dependent = self._wTree.get_widget("check2_dependent")

        elif togglebutton == self._wTree.get_widget("check2_dependent"):
            check_dependent = self._wTree.get_widget("check1_dependent")
        else:
            log.error("Could not be found the checkbutton")
            return

        if togglebutton.get_active():
            check_dependent.set_active(False)
            check_dependent.set_sensitive(False)
        else:
            check_dependent.set_sensitive(True)

    def _on_btn_cancel_relationship_clicked(self, button):
        win = self._wTree.get_widget("wndaddrelationship")

        win.destroy()

    def _on_btn_add_relationship_clicked(self, button):

        # basic information of the relationship
        entry = self._wTree.get_widget("entry_name")
        name = entry.get_text()
        if name == "":
            self._show_dialog("Nombre Relación",
                              "Debe ingresar el nombre de la relación",
                              gtk.STOCK_DIALOG_WARNING)
            return

        entry = self._wTree.get_widget("entry_codename")
        codename = entry.get_text()

        if codename == "":
            self._show_dialog("Codigo Relación",
                              "Debe ingresar el codigo de la relación",
                              gtk.STOCK_DIALOG_WARNING)
            return

        txt = self._wTree.get_widget("txt_description")
        buff = txt.get_buffer()
        description = buff.get_text(buff.get_start_iter(),
                                    buff.get_end_iter())

        ####
        # entity 1
        combo = self._wTree.get_widget("combo_entity1")
        # message if not selected entity 1
        if combo.get_active() == -1:
            self._show_dialog("Seleccione Entidad",
                              "Debe seleccionar las entidades que desea relacionar",
                              gtk.STOCK_DIALOG_WARNING)
            return

        combo_model = combo.get_model()
        iter_combo= combo_model.get_iter_from_string(str(combo.get_active()))

        #get the codename of entity 1
        codename_entity1 = combo_model.get_value(iter_combo, 1)

        check_dependent = self._wTree.get_widget("check1_dependent")
        dependent1 = check_dependent.get_active()

        check_mandatory = self._wTree.get_widget("check1_mandatory")
        mandatory1 = check_mandatory.get_active()

        ####
        # entity 2
        combo = self._wTree.get_widget("combo_entity2")
        # message if not selected entity 2
        if combo.get_active() == -1:
            self._show_dialog("Seleccione Entidad",
                              "Debe seleccionar las entidades que desea relacionar",
                              gtk.STOCK_DIALOG_WARNING)
            return

        iter_combo = combo_model.get_iter_from_string(str(combo.get_active()))
        codename_entity2 = combo_model.get_value(iter_combo, 1)

        check_dependent = self._wTree.get_widget("check2_dependent")
        dependent2 = check_dependent.get_active()

        check_mandatory = self._wTree.get_widget("check2_mandatory")
        mandatory2 = check_mandatory.get_active()

        # cardinality of the relationship
        combo = self._wTree.get_widget("combo_cardinality")
        #message if not selected a cardinality
        if combo.get_active() == -1:
            self._show_dialog("Seleccione Cardinalidad",
                              "Debe seleccionar la cardinalidad para la relación",
                              gtk.STOCK_DIALOG_WARNING)
            return False

        combo_model = combo.get_model()
        iter_combo = combo_model.get_iter_from_string(str(combo.get_active()))

        cardinality = combo_model.get_value(iter_combo, 1)


        answer = self._control.add(name,
                                   codename,
                                   description,
                                   codename_entity1,
                                   dependent1,
                                   mandatory1,
                                   codename_entity2,
                                   dependent2,
                                   mandatory2,
                                   cardinality)

        #message dialog if add_relationsip returns an error
        if not answer:
            self._show_dialog("Relación",
                              """Se ha producido un error inesperado
                              No se pudo agregar la relación""",
                              gtk.STOCK_DIALOG_INFO)
            return False

        self._window.destroy()
        return True

    def _show_dialog(self, title, msg, stock_img):
        dialog = gtk.Dialog(title,
                            self._window,
                            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                            (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        hbox = gtk.HBox()

        image = gtk.Image()
        image.set_from_stock(stock_img , gtk.ICON_SIZE_DIALOG)
        hbox.pack_start(image)

        label = gtk.Label(msg)

        label.set_use_markup(True)
        hbox.pack_start(label)

        hbox.show_all()
        dialog.vbox.pack_start(hbox)
        dialog.run()
        dialog.destroy()
        return

class ViewMainWindow:
    """Vista principal

    En esta vista se despliegan los elementos más importantes del software
    como el canvas, la barra de herramientas y de menu, entre otros.

    """
    def __init__(self,control, file_=None):
        log.info('ViewMainWindow.__init__: file_=%s', file_)
        self._control = control #control que es dueño de la vista
        self.gladefile = resource_filename("rascase.resources.glade", "wndmain.glade")
        self._wTree = gtk.glade.XML(self.gladefile)

        ## widgets
        self._main_toolbar = None
        self._elements_toolbar = None
        self._menubar = None

        ## properties
        self._files_opened = list()
        self._files_list = list()
        self._canvas_list = list()
        self._selected_item = None

        # the association of the signals defined inside glade and the python methods
        signals_dic = {"on_wndmain_delete_event":self._on_delete_main_window,
                       "on_files_list_row_activated":self._on_files_list_row_activated}
        self._wTree.signal_autoconnect(signals_dic)

        # the properties of the window were defined
        self._window = self._wTree.get_widget("wndmain")
        self._window.set_default_size(600,500)
        self._window.set_title("Rascase")

        self._construct_toolbar() # we construct the toolbar

        self._window.show_all()


    # signals

    def _on_delete_main_window(self, widget, event):
        "callback conectado al evento 'delete' de la ventana principal"

        menu_option = self._uimanager.get_widget("/menubar/File/Quit")

        menu_option.activate()
        return True

    def _on_quit_selected(self, menuitem):
        "callback conectado a la opcion salir de la aplicacion"
        dialog = gtk.Dialog("Salir",
                            self._window,
                            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                            (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                             gtk.STOCK_QUIT, gtk.RESPONSE_ACCEPT))

        box = gtk.HBox()

        widget = gtk.Image()
        widget.set_from_stock(gtk.STOCK_QUIT, gtk.ICON_SIZE_DIALOG)
        box.pack_start(widget)

        widget = gtk.Label("¿Desea salir y perder todos los cambios efectuados?")
        box.pack_start(widget)

        box.show_all()
        dialog.vbox.pack_start(box)

        response = dialog.run()
        dialog.destroy()

        if response == gtk.RESPONSE_ACCEPT:
            self._control.quit()

    def _on_new_project(self, menuitem):
        self._files_list = self._control.create_new_project()
        self._reload_files_list()

    def _on_new_model(self, menuitem):
        aux = self._control.create_new_logical_model()
        if aux == None:
            statusbar = self._wTree.get_widget("statusbar")
            context_id = statusbar.get_context_id("Model not created")
            msg_id = statusbar.push(context_id, "Cancelada la creación de un nuevo modelo lógico")
            gobject.timeout_add(10000,self._remove_from_statusbar,context_id, msg_id)
        else:
            print aux
            self._files_list = aux
            self._reload_files_list()

    def _on_open_project(self, menuitem):

        # obtain the list of models associated to the project
        self._files_list = self._control.open_project(path=None)
        self._reload_files_list()

    def _on_save_project(self, menuitem):
        answer = self._control.save_project()
        statusbar = self._wTree.get_widget("statusbar")
        context_id = statusbar.get_context_id("save project")
        if answer:
            msg_id = statusbar.push(context_id, "El proyecto ha sido guardado exitosamente")
        else:
            msg_id = statusbar.push(context_id, "El proyecto no ha podido ser guardado")

        gobject.timeout_add(10000, self._remove_from_statusbar, context_id, msg_id)

    def on_open_model(self, menuitem):
        pass

    def _on_save_model(self, menuitem):
        ntbk = self._wTree.get_widget("ntbk_main")

        child = ntbk.get_nth_page(ntbk.get_current_page())
        canvas = child.get_data("canvas")

        filepath = None
        for x in self._files_opened:
            if x[1] == canvas:
                filepath = x[0]

        if filepath == None:
            log.debug("mmm trying to save a model but could not be found the modelpath")
            return

        self._control.save_model(filepath)

    def on_save_model_as(self, menuitem):
        pass

    def on_add_model_to_project(self, menuitem):
        pass

    def on_remove_model(self, menuitem): #remove the model from the project
        pass

    def on_delete_model(self, menuitem):
        pass

    #on the close of the menu
    def _on_close_file_clicked(self, menuitem):
        ntbk = self._wTree.get_widget("ntbk_main")

        page_num = ntbk.get_current_page()

        #if there is no pages a message is displayed in status bar
        if page_num == -1:
            statusbar = self._wTree.get_widget("statusbar")
            context_id = statusbar.get_context_id("no pages in notebook")
            msg_id = statusbar.push(context_id, "No hay modelo abierto")
            gobject.timeout_add(5000,self._remove_from_statusbar,context_id, msg_id)
            return

        scrolled_win =ntbk.get_nth_page(page_num)

        canvas = scrolled_win.get_data("canvas")
        closed = False
        for i in range(len(self._files_opened)):
            if self._files_opened[i][1] == canvas:
                ntbk.remove_page(page_num)
                del self._files_opened[i]
                break

        statusbar = self._wTree.get_widget("statusbar")
        context_id = statusbar.get_context_id("closing canvas")
        msg_id = statusbar.push(context_id, "Modelo cerrado")
        gobject.timeout_add(5000,self._remove_from_statusbar,context_id, msg_id)


    def _on_add_entity_clicked(self, menuitem):

        ntbk = self._wTree.get_widget("ntbk_main")
        page = ntbk.get_current_page()
        child = ntbk.get_nth_page(page)
        canvas = child.get_data("canvas")

        filepath = None
        for x in self._files_opened:
            if x[1] == canvas:
                filepath = x[0]
                break

        item = self._control.add_entity(0,0, filepath)
        canvas.add_child(item)

    def _on_add_relationship_clicked(self, menuitem):
        self._control.add_relationship()

    def on_add_inheritance_clicked(self, menuitem):
        pass

    def _on_add_label_clicked(self, menuitem):
        #self._control.add_label()
        pass

    def on_add_rectangle_clicked(self,menuitem):
        pass

    #aqui se debe chequear el tipo de componente grafico que se quiere editar
    #para luego hacer la llamada al método correspondiente
    def on_edit_component(self, item, target_item, event):
        pass

    def on_delete_component(self, item, target_item, event):
        pass

    #callbacks usados por el uimanager
    def on_delete_component_clicked(self, menuitem):
        pass

    def on_edit_component_clicked(self, menuitem):
        pass

    def on_generate_physical_model_clicked(self, menuitem):
        pass

    def on_btn_print_clicked(self, menuitem):
        pass

    def on_btn_export_clicked(self, menuitem):
        pass

    def _on_zoomin_clicked(self, menuitem):
        ntbk = self._wTree.get_widget("ntbk_main")

        child = ntbk.get_nth_page(ntbk.get_current_page())

        if child == None:
            log.error("Troubles with the zoomin callback")

        canvas = child.get_data("canvas")

        current_scale = canvas.get_property("scale")
        canvas.set_scale(current_scale + 0.1)

    def on_zoomout_clicked(self, menuitem):
        ntbk = self._wTree.get_widget("ntbk_main")

        child = ntbk.get_nth_page(ntbk.get_current_page())

        if child == None:
            log.error("Troubles with the zoomin callback")

        canvas = child.get_data("canvas")

        current_scale = canvas.get_property("scale")
        if current_scale < 0.1:
            return

        canvas.set_scale(current_scale - 0.1)

    def on_btn_send_to_back_clicked(self, menuitem):
        pass

    def on_btn_send_to_front_clicked(self, menuitem):
        pass

    def on_edit_preferences_clicked(self, menuitem):
        pass

    def on_show_help_clicked(self, menuitem):
        pass

    def on_about_clicked(self, menuitem):
        pass

    def _on_files_list_row_activated(self, treeview, path, view_column):

        ntbk = self._wTree.get_widget("ntbk_main")

        for x in self._files_opened:
            if x[0] == self._files_list[path[0]]:
                log.debug("Trying to open an already opened file")
                page_num = ntbk.page_num(x[1].scrolled_win)
                if page_num == -1:
                    log.debug("The child could not be found inside the main notebook")
                    return
                else:
                    ntbk.set_current_page(page_num)
                    return

        new_canvas = self._control.construct_model(self._files_list[path[0]])

        if new_canvas == None:
            return

        self._files_opened.append((self._files_list[path[0]],new_canvas))

        ## hbox = gtk.HBox()
        ## widget = gtk.Label(os.path.basename(self._files_list[path[0]]))
        ## hbox.pack_start(widget)

        ## button = gtk.Button()
        ## hbox.pack_start(button)
        ## img = gtk.Image()
        ## img.set_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        ## button.add(img)

        ## button.connect("clicked", self._on_btn_close_model_clicked)
        ## hbox.show_all()
        label = gtk.Label(os.path.basename(self._files_list[path[0]]))
        ntbk.append_page(new_canvas.scrolled_win, label)
        ntbk.set_current_page(-1)

    def _reload_files_list(self):
        "Debe ser llamada cada vez que la lista de archivos cambie (files_list)"
        liststore = gtk.ListStore(gobject.TYPE_STRING)
        treeview = self._wTree.get_widget("files_list")

        treeview.set_model(liststore)

        for elem in self._files_list:
            liststore.append([os.path.basename(str(elem))])

        cols = treeview.get_columns()
        for i in cols:
            treeview.remove_column(i)

        treeviewcol = gtk.TreeViewColumn("Modelos")
        treeview.append_column(treeviewcol)
        cell = gtk.CellRendererText()
        treeviewcol.pack_start(cell)
        treeviewcol.add_attribute(cell, "text", 0)

    def _remove_from_statusbar(self, context_id, msg_id):
        """Remueve el mensaje definido por context_id y msg_id.

        Retorna False para que gobject.timeout_add deje de llamar a la funcion"""
        statusbar = self._wTree.get_widget("statusbar")
        statusbar.remove(context_id, msg_id)

        return False #stop being called by gobject.timeout_add

    def _construct_toolbar(self):
        "Construye la barra de herramientas y el menu usando GtkUIManager"
        log.debug("Constructing the toolbar")

        uifile = resource_filename('rascase.resources.uidefs', 'ui.xml')

        self._uimanager = gtk.UIManager()
        accel_group = self._uimanager.get_accel_group()
        self._window.add_accel_group(accel_group)

        action_group = gtk.ActionGroup('my_actions')
        action_group.add_actions([#TODO:finish actions
            ('File', None, '_Archivo', None, None, None),
            ('NewLogicalModel', gtk.STOCK_NEW, 'Nuevo modelo lógico', '<Control>n', None,
             self._on_new_model),
            ('OpenModel', gtk.STOCK_OPEN, None, '<Control>o', None,
             self.on_open_model),
            ('Save', gtk.STOCK_SAVE, None, '<Control>s', None,
             self._on_save_model),
            ('SaveAs', gtk.STOCK_SAVE_AS, None, None, None,
             self.on_save_model_as),
            ('Print', gtk.STOCK_PRINT, None, '<Control>p', None,
             self.on_btn_print_clicked),
            ('CloseModel', gtk.STOCK_CLOSE, 'Cerrar Modelo', '<Control>w', None,
             self._on_close_file_clicked),
            ('Quit', gtk.STOCK_QUIT, None, '<Control>q', None,
             self._on_quit_selected),
            ('Project', None, '_Proyecto', None, None, None),
            ('NewProject', gtk.STOCK_NEW, None, '', 'Nuevo Proyecto',
             self._on_new_project),
            ('OpenProject', gtk.STOCK_OPEN, None, '', 'Abrir proyecto',
             self._on_open_project),
            ('SaveProject', gtk.STOCK_SAVE, None, '', 'Guardar proyecto',
             self._on_save_project),
            ('AddModel', gtk.STOCK_ADD, None, None, 'Añadir un modelo',
             self.on_add_model_to_project),
            ('RemoveModel', gtk.STOCK_REMOVE, None, None, 'Remover modelo del proyecto',
             self.on_remove_model),
            ('DeleteModel', gtk.STOCK_DELETE, None, None, 'Borrar el modelo',
             self.on_delete_model),
            ('Edit', None, '_Editar', None, None, None),
            ('EditElement', gtk.STOCK_EDIT, None, None, 'Editar el elemento seleccionado',
             self.on_edit_component_clicked),
            ('DeleteElement', gtk.STOCK_DELETE, None, None, 'Borrar el elemento seleccionado',
             self.on_delete_component_clicked),
            ('EditPreferences', gtk.STOCK_PREFERENCES, None, None, 'Editar las preferencias',
             self.on_edit_preferences_clicked),
            ('Help', None, 'A_yuda', None, None, None),
            ('ShowHelp', gtk.STOCK_HELP, None, 'F1', None,
             self.on_show_help_clicked),
            ('About', gtk.STOCK_ABOUT, None, None, None,
             self.on_about_clicked),
            ('Entity', gtk.STOCK_MISSING_IMAGE, 'Entidad', None, None,
             self._on_add_entity_clicked),
            ('Relationship', gtk.STOCK_MISSING_IMAGE, 'Relación', None, None,
             self._on_add_relationship_clicked),
            ('Inheritance', gtk.STOCK_MISSING_IMAGE, 'Herencia', None, None,
             self.on_add_inheritance_clicked),
            ('Label', gtk.STOCK_MISSING_IMAGE, 'Etiqueta', None, None,
             self._on_add_label_clicked),
            ('Rectangle', gtk.STOCK_MISSING_IMAGE, 'Rectangulo', None, None,
             self.on_add_rectangle_clicked),
            ('ZoomIn', gtk.STOCK_ZOOM_IN, None, None, None,
             self._on_zoomin_clicked),
            ('ZoomOut', gtk.STOCK_ZOOM_OUT, None, None, None,
             self.on_zoomout_clicked),
            ('SendToBack', gtk.STOCK_GO_DOWN, 'Enviar atras', None, None,
             self.on_btn_send_to_back_clicked),
            ('SendToFront', gtk.STOCK_GO_UP, 'Enviar al frente', None, None,
             self.on_btn_send_to_front_clicked)])

        self._uimanager.insert_action_group(action_group, 0)
        self._uimanager.add_ui_from_file(uifile)

        box = self._wTree.get_widget("vbox_main")
        #pack the menubar
        menubar = self._uimanager.get_widget("/menubar")
        box.pack_start(menubar, False)
        box.reorder_child(menubar, 0)
        #pack the toolbar
        toolbar = self._uimanager.get_widget("/toolbar")
        box.pack_start(toolbar, False)
        box.reorder_child(toolbar, 1)

    def get_current_path(self):

        ntbk = self._wTree.get_widget("ntbk_main")

        child = ntbk.get_nth_page(ntbk.get_current_page())

        if child == None:
            return None

        canvas = child.get_data("canvas")

        for x in self._files_opened:
            if x[1] == canvas:
                return x[0]

        return None

    def get_canvas_from_path(self, filepath):
        "Retorna el canvas asociado a un archivo"
        for x in self._files_opened:
            if x[0] == filepath:
                return x[1]

        return None

    def get_window(self):
        "retorna la ventana principal, para ser utilizada en los dialogos como ventana padre"
        return self._window

