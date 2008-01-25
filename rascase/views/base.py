# coding=utf-8
##
## base.py
## Login : <freyes@yoda>
## Started on  Tue Jan 22 11:29:49 2008 Felipe Reyes
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

import goocanvas
import gtk

#Tango colors taken from 
#http://tango.freedesktop.org/Tango_Icon_Theme_Guidelines
TANGO_COLOR_BUTTER_LIGHT = int("fce94f",16)
TANGO_COLOR_BUTTER_MID = int("edd400",16)
TANGO_COLOR_BUTTER_DARK = int("c4a000",16)
TANGO_COLOR_ORANGE_LIGHT = int("fcaf3e",16)
TANGO_COLOR_ORANGE_MID = int("f57900",16)
TANGO_COLOR_ORANGE_DARK = int("ce5c00",16)
TANGO_COLOR_CHOCOLATE_LIGHT = int("e9b96e",16)
TANGO_COLOR_CHOCOLATE_MID = int("c17d11",16)
TANGO_COLOR_CHOCOLATE_DARK = int("8f5902",16)
TANGO_COLOR_CHAMELEON_LIGHT = int("8ae234",16)
TANGO_COLOR_CHAMELEON_MID = int("73d216",16)
TANGO_COLOR_CHAMELEON_DARK = int("4e9a06",16)
TANGO_COLOR_SKYBLUE_LIGHT = int("729fcfff",16)
TANGO_COLOR_SKYBLUE_MID = int("3465a4",16)
TANGO_COLOR_SKYBLUE_DARK = int("204a87",16)
TANGO_COLOR_PLUM_LIGHT = int("ad7fa8",16)
TANGO_COLOR_PLUM_MID = int("75507b",16)
TANGO_COLOR_PLUM_DARK = int("5c3566",16)
TANGO_COLOR_SCARLETRED_LIGHT = int("ef2929",16)
TANGO_COLOR_SCARLETRED_MID = int("cc0000",16)
TANGO_COLOR_SCARLETRED_DARK = int("a40000",16)
TANGO_COLOR_ALUMINIUM1_LIGHT = int("eeeeec",16)
TANGO_COLOR_ALUMINIUM1_MID = int("d3d7cf",16)
TANGO_COLOR_ALUMINIUM1_DARK = int("babdb6",16)
TANGO_COLOR_ALUMINIUM2_LIGHT = int("888a85",16)
TANGO_COLOR_ALUMINIUM2_MID = int("555753",16)
TANGO_COLOR_ALUMINIUM2_DARK = int("2e3436",16)
TRANSPARENT_COLOR = int("000000",16)

class RectBaseComponent:
    def __init__(self, bodytype='rect'):
        self._body = None
        self._dragbox = None
        pass

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
        self.connect("button_press_event",self.on_button_press)
        self.connect("button_release_event",self.on_button_release)
        self.connect("motion_notify_event",self.on_motion)
        self.connect("enter_notify_event",self.on_enter_notify)
        self.connect("leave_notify_event",self.on_leave_notify)


    def is_dragging(self):
        if self._dragging == True:
            return True
        else:
            return False
        
    #senales
    def on_button_press(self,item,target,event):
        
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
        self._dragging = False
        canvas = item.get_canvas ()
        canvas.pointer_ungrab(item, event.time)
            
        return True
        
    def on_enter_notify(self,item,target,event):
        item.props.fill_color = "yellow"
        
    def on_leave_notify(self,item,target,event):
        item.props.fill_color = "black"
        
    def on_motion(self,item,target,event):
        canvas = item.get_canvas ()

        if not (event.state == gtk.gdk.BUTTON1_MASK) and not self._dragging:
            return False
        
        new_x = event.x
        new_y = event.y
        if item.name == 'N':
            dif = new_y - self.drag_y
            item.translate(0,dif)

            item.get_parent().get_body().props.height = \
                item.get_parent().get_body().props.height - dif

            item.get_parent().get_body().translate(0,dif)

            #make the dragbox follow the corners of the square
            item.get_parent().dragbox['NW'].translate (0,dif)
            item.get_parent().dragbox['NE'].translate (0,dif)
            item.get_parent().dragbox['W'].translate (0,dif/2)
            item.get_parent().dragbox['E'].translate (0,dif/2)

        elif item.name == 'NE':
            dif_x = new_x - self.drag_x
            dif_y = new_y - self.drag_y
            item.translate(dif_x, dif_y)

            item.get_parent().get_body().props.width = \
                item.get_parent().get_body().props.width + dif_x
            
            item.get_parent().get_body().props.height = \
                item.get_parent().get_body().props.height - dif_y

            item.get_parent().get_body().translate(0, dif_y)

            #make the dragbox follow the corner
            item.get_parent().dragbox['NW'].translate(0, dif_y)
            item.get_parent().dragbox['N'].translate(dif_x/2, dif_y)
            item.get_parent().dragbox['E'].translate(dif_x, dif_y/2)
            item.get_parent().dragbox['SE'].translate(dif_x, 0)

        elif item.name == 'E':
            dif = new_x - self.drag_x
            item.translate(dif,0)
           
            item.get_parent().get_body().props.width = \
                item.get_parent().get_body().props.width + dif

            #make the dragbox
            item.get_parent().dragbox['NE'].translate (dif, 0)
            item.get_parent().dragbox['SE'].translate (dif, 0)
            item.get_parent().dragbox['N'].translate (dif/2, 0)
            item.get_parent().dragbox['S'].translate (dif/2, 0)

        elif item.name == 'SE':
            dif_x = new_x - self.drag_x
            dif_y = new_y - self.drag_y
            item.translate(dif_x, dif_y)
            
            item.get_parent().get_body().props.width = \
                item.get_parent().get_body().props.width + dif_x

            item.get_parent().get_body().props.height = \
                item.get_parent().get_body().props.height + dif_y

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
            
            item.get_parent().get_body().props.height = \
                item.get_parent().get_body().props.height + dif

            #move the dragbox
            item.get_parent().dragbox['W'].translate (0, dif/2)
            item.get_parent().dragbox['SW'].translate (0, dif)
            item.get_parent().dragbox['SE'].translate (0, dif)
            item.get_parent().dragbox['E'].translate (0, dif/2)

        elif item.name == 'SW':
            dif_x = new_x - self.drag_x
            dif_y = new_y - self.drag_y
            item.translate(dif_x,dif_y)

            item.get_parent().get_body().props.height = \
                item.get_parent().get_body().props.height + dif_y

            item.get_parent().get_body().props.width = \
                item.get_parent().get_body().props.width - dif_x

            item.get_parent().get_body().translate(dif_x,0)

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

            item.get_parent().get_body().props.width = \
                item.get_parent().get_body().props.width - dif

            item.get_parent().get_body().translate(dif,0)

            #move the dragbox
            item.get_parent().dragbox['N'].translate (dif/2, 0)
            item.get_parent().dragbox['NW'].translate (dif, 0)
            item.get_parent().dragbox['SW'].translate (dif, 0)
            item.get_parent().dragbox['S'].translate (dif/2, 0)

        elif item.name == 'NW':
            dif_x = new_x - self.drag_x
            dif_y = new_y - self.drag_y
            item.translate(dif_x,dif_y)
            item.get_parent().get_body().props.height = \
                item.get_parent().get_body().props.height - dif_y

            item.get_parent().get_body().props.width = \
                item.get_parent().get_body().props.width - dif_x

            item.get_parent().get_body().translate(dif_x,dif_y)

            #move the dragbox
            item.get_parent().dragbox['E'].translate (0, dif_y/2)
            item.get_parent().dragbox['NE'].translate (0, dif_y)
            item.get_parent().dragbox['N'].translate (dif_x/2, dif_y)
            item.get_parent().dragbox['W'].translate (dif_x, dif_y/2)
            item.get_parent().dragbox['SW'].translate (dif_x, 0)
            item.get_parent().dragbox['S'].translate (dif_x/2, 0)


class RectangleComponent(RectBaseComponent):
    def __init__(self):
        RectBaseComponent.__init__(self)
        self._transparency = 0.0

    def set_transparency(self, opacity):
        pass

class LabelComponent(RectBaseComponent):
    def __init__(self):
        RectBaseComponent
