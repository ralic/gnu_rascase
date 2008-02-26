import gobject
import rascase.views
import rascase.core
import gtk
import pdb

win = gtk.Window()


canvas = rascase.views.Canvas()

#entity = rascase.views.EntityComponent(10,10,"blue","black")
for i in range(3):
	entity = rascase.views.EntityComponent("entidad"+str(i),x=10*i, y=10*i)

	attr = rascase.views.AttributeComponent("atributo1", (rascase.core.LogicalDataType.VARCHAR,10),pk=True, mandatory=True)
	entity.add_attribute(attr)
	attr = rascase.views.AttributeComponent("atributo2", (rascase.core.LogicalDataType.FLOAT,),pk=False, mandatory=False)
	entity.add_attribute(attr)
	attr = rascase.views.AttributeComponent("atributo3", (rascase.core.LogicalDataType.INTEGER,),pk=False, mandatory=True)
	entity.add_attribute(attr)
	attr = rascase.views.AttributeComponent("atributo4", (rascase.core.LogicalDataType.VARCHAR,255),pk=False, mandatory=False)
	entity.add_attribute(attr)

	canvas.add_child(entity)

win.add(canvas.scrolled_win)

win.connect("delete-event", gtk.main_quit)

win.show_all()
gtk.main()
