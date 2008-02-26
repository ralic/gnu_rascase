import gobject
import rascase.views
import gtk
import pdb

win = gtk.Window()


canvas = rascase.views.Canvas()

#entity = rascase.views.EntityComponent(10,10,"blue","black")
for i in range(3):
	entity = rascase.views.EntityComponent("entidad"+str(i),x=10*i, y=10*i)

	canvas.add_child(entity)

win.add(canvas.scrolled_win)

win.connect("delete-event", gtk.main_quit)

win.show_all()
gtk.main()
