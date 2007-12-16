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
        self.dragging = False

        print type(self.props.fill_color)
        
        #conexion de senales
        self.connect("button_press_event",self.on_button_press)
        self.connect("button_release_event",self.on_button_release)
        self.connect("motion_notify_event",self.on_motion)
        self.connect("enter_notify_event",self.on_enter_notify)
        self.connect("leave_notify_event",self.on_leave_notify)

    #senales
    def on_button_press(self,item,target,event):
        
        self.dragging = True
        fleur = gtk.gdk.Cursor(gtk.gdk.FLEUR)
        canvas = item.get_canvas ()
        canvas.pointer_grab(item, 
                        gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.BUTTON_RELEASE_MASK,
                        fleur, event.time)
        self.drag_x = event.x
        self.drag_y = event.y
        return True
    
    def on_button_release(self,item,target,event):
        self.dragging = False
        canvas = item.get_canvas ()
        canvas.pointer_ungrab(item, event.time)
            
        return True
        
    def on_enter_notify(self,item,target,event):
        item.props.fill_color = "yellow"
        
    def on_leave_notify(self,item,target,event):
        item.props.fill_color = "black"
        
    def on_motion(self,item,target,event):
        canvas = item.get_canvas ()

        if not (event.state == gtk.gdk.BUTTON1_MASK) and not self.dragging:
            return False
        
        new_x = event.x
        new_y = event.y
        if item.name == 'N':
            dif = new_y - self.drag_y
            item.translate(0,dif)
            item.get_parent().cuerpo.props.height = item.get_parent().cuerpo.props.height - dif
            item.get_parent().cuerpo.translate(0,dif)

            #make the dragbox follow the corners of the square
            item.get_parent().dragbox['NW'].translate (0,dif)
            item.get_parent().dragbox['NE'].translate (0,dif)
            item.get_parent().dragbox['W'].translate (0,dif/2)
            item.get_parent().dragbox['E'].translate (0,dif/2)

        elif item.name == 'NE':
            dif_x = new_x - self.drag_x
            dif_y = new_y - self.drag_y
            item.translate(dif_x, dif_y)
            item.get_parent().cuerpo.props.width = item.get_parent().cuerpo.props.width + dif_x
            item.get_parent().cuerpo.props.height = item.get_parent().cuerpo.props.height - dif_y
            item.get_parent().cuerpo.translate(0, dif_y)

            #make the dragbox follow the corner
            item.get_parent().dragbox['NW'].translate(0, dif_y)
            item.get_parent().dragbox['N'].translate(dif_x/2, dif_y)
            item.get_parent().dragbox['E'].translate(dif_x, dif_y/2)
            item.get_parent().dragbox['SE'].translate(dif_x, 0)

        elif item.name == 'E':
            dif = new_x - self.drag_x
            item.translate(dif,0)
            item.get_parent().cuerpo.props.width = item.get_parent().cuerpo.props.width + dif

            #make the dragbox
            item.get_parent().dragbox['NE'].translate (dif, 0)
            item.get_parent().dragbox['SE'].translate (dif, 0)
            item.get_parent().dragbox['N'].translate (dif/2, 0)
            item.get_parent().dragbox['S'].translate (dif/2, 0)

        elif item.name == 'SE':
            dif_x = new_x - self.drag_x
            dif_y = new_y - self.drag_y
            item.translate(dif_x, dif_y)
            item.get_parent().cuerpo.props.width = item.get_parent().cuerpo.props.width + dif_x
            item.get_parent().cuerpo.props.height = item.get_parent().cuerpo.props.height + dif_y

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
            item.get_parent().cuerpo.props.height = item.get_parent().cuerpo.props.height + dif

            #move the dragbox
            item.get_parent().dragbox['W'].translate (0, dif/2)
            item.get_parent().dragbox['SW'].translate (0, dif)
            item.get_parent().dragbox['SE'].translate (0, dif)
            item.get_parent().dragbox['E'].translate (0, dif/2)

        elif item.name == 'SW':
            dif_x = new_x - self.drag_x
            dif_y = new_y - self.drag_y
            item.translate(dif_x,dif_y)
            item.get_parent().cuerpo.props.height = item.get_parent().cuerpo.props.height + dif_y
            item.get_parent().cuerpo.props.width = item.get_parent().cuerpo.props.width - dif_x
            item.get_parent().cuerpo.translate(dif_x,0)

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
            item.get_parent().cuerpo.props.width = item.get_parent().cuerpo.props.width - dif
            item.get_parent().cuerpo.translate(dif,0)

            #move the dragbox
            item.get_parent().dragbox['N'].translate (dif/2, 0)
            item.get_parent().dragbox['NW'].translate (dif, 0)
            item.get_parent().dragbox['SW'].translate (dif, 0)
            item.get_parent().dragbox['S'].translate (dif/2, 0)

        elif item.name == 'NW':
            dif_x = new_x - self.drag_x
            dif_y = new_y - self.drag_y
            item.translate(dif_x,dif_y)
            item.get_parent().cuerpo.props.height = item.get_parent().cuerpo.props.height - dif_y
            item.get_parent().cuerpo.props.width = item.get_parent().cuerpo.props.width - dif_x
            item.get_parent().cuerpo.translate(dif_x,dif_y)

            #move the dragbox
            item.get_parent().dragbox['E'].translate (0, dif_y/2)
            item.get_parent().dragbox['NE'].translate (0, dif_y)
            item.get_parent().dragbox['N'].translate (dif_x/2, dif_y)
            item.get_parent().dragbox['W'].translate (dif_x, dif_y/2)
            item.get_parent().dragbox['SW'].translate (dif_x, 0)
            item.get_parent().dragbox['S'].translate (dif_x/2, 0)


class EntityComponent(goocanvas.Group):
    __gsignals__ = {
        'on-movement': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ())
        }
    
    ANCHO = 100
    ALTO = 200
    ANCHO_LINEA = 1.0
    COLOR_RELLENO = "#729fcf"
    
    def __init__(self,x,y):
        goocanvas.Group.__init__(self, can_focus = True)
        
        self.cuerpo = goocanvas.Rect(x=x,y=y,
            width=self.ANCHO,
            height=self.ALTO,
            line_width=self.ANCHO_LINEA,
            fill_color=self.COLOR_RELLENO)
            
        self.add_child(self.cuerpo)
        self.dragging= False
        
        self.dragbox = {
            'NW': DragBox('NW',x-5,y-5),
            'N' : DragBox('N',(x+self.ANCHO)/2,y-5),
            'NE': DragBox('NE',(x+self.ANCHO)-5,y-5),
            'E' : DragBox('E',(x+self.ANCHO)-5,(y+self.ALTO)/2),
            'SE': DragBox('SE',(x+self.ANCHO)-5,(y+self.ALTO)-5),
            'S' : DragBox('S',(x+self.ANCHO)/2,(y+self.ALTO)-5),
            'SW': DragBox('SW',x-5,(y+self.ALTO)-5),
            'W' : DragBox('W',x-5,(y+self.ALTO)/2)
            }
        for item in self.dragbox.keys():
            self.add_child(self.dragbox[item])
            

        #signals del foco
        self.connect("focus_in_event", self.on_focus_in)
        self.connect("focus_out_event", self.on_focus_out)
        self.connect("button_press_event", self.on_double_click_press)
        self.connect("button_press_event",self.on_button_press)
        self.connect("button_release_event",self.on_button_release)
        self.connect("motion_notify_event",self.on_motion)
        self.connect("enter_notify_event",self.on_enter_notify)
        self.connect("leave_notify_event",self.on_leave_notify)
        
        

    

    #reescritura de metodos
    
    #senales
    def on_double_click_press(self,item,target,event):
        if event.type == gtk.gdk._2BUTTON_PRESS:
            print "*** se hizo doble click", type(target)
            if target is __main__.entidad:
                print "es entidad :D"
            else:
                print "buu, no es entidad"

            
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
            if self.dragbox[aux].dragging:
                return True
            
        self.dragging = True
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
            if self.dragbox[aux].dragging:
                return True

        self.dragging = False
        canvas = item.get_canvas ()
        canvas.pointer_ungrab(item, event.time)
        return True
        
    def on_enter_notify(self,item,target,event):
        pass
        
    def on_leave_notify(self,item,target,event):
        pass
        
    def on_motion(self,item,target,event):
        for aux in self.dragbox.keys():
            if self.dragbox[aux].dragging:
                return True
         
        canvas = item.get_canvas ()

        if not (event.state == gtk.gdk.BUTTON1_MASK) and not self.dragging:
            return False
        
        new_x = event.x
        new_y = event.y
        item.translate (new_x - self.drag_x, new_y - self.drag_y)
        self.emit('on-movement')
        

def cs(item):
    print "on motion: ", item

        
def main():
    window = gtk.Window()
    window.set_default_size(300, 300)
    window.set_position(gtk.WIN_POS_CENTER)
    
    window.show()
    window.connect("destroy", lambda w: gtk.main_quit())
    
    scrolled_win = gtk.ScrolledWindow()
    scrolled_win.set_shadow_type(gtk.SHADOW_IN)
    scrolled_win.show()
    window.add(scrolled_win)
    
    canvas = goocanvas.Canvas()
    canvas.set_flags(gtk.CAN_FOCUS)
    canvas.set_size_request(300, 300)
    canvas.set_bounds(0, 0, 600, 600)

    root = canvas.get_root_item()
    
    item = entidad(0,40)
    root.add_child(item)

    item = entidad(50,50)
    item.connect("on-movement",cs)
    root.add_child(item)
    
    item = goocanvas.Table(width=100, height=100, fill_color="red")
    root.add_child(item)
    hijo = goocanvas.Text(parent=item, text="Factura", anchor=gtk.ANCHOR_SE, fill_color = "blue")
    item.set_child_properties(hijo, row=0, column=0)
    #item.add_child(hijo)
    hijo = goocanvas.Text(parent=item, text="atributo1", anchor=gtk.ANCHOR_SE, fill_color = "yellow")
    item.set_child_properties(hijo, row=1, column=0)
    #item.add_child(hijo)
    hijo = goocanvas.Text(parent=item, text="atributo2", anchor=gtk.ANCHOR_SE, fill_color = "yellow")
    item.set_child_properties(hijo, row=2, column=0)
    #item.add_child(hijo)
    
    
    canvas.set_root_item(root)
    canvas.show()
    
    scrolled_win.add(canvas)
    

    gtk.main()
    

