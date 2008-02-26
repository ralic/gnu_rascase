import gobject
import rascase.views
import rascase.core
import gtk
import pdb

win = gtk.Window()


canvas = rascase.views.Canvas()

#entity = rascase.views.EntityComponent(10,10,"blue","black")

entity1 = rascase.views.EntityComponent("entidad1",x=10, y=10)
entity2 = rascase.views.EntityComponent("entidad2",x=200, y=200)

canvas.add_child(entity1)
canvas.add_child(entity2)

relation = rascase.views.RelationshipComponent(entity1, entity2,1,False)
canvas.add_child(relation)

entity3 = rascase.views.EntityComponent("entidad3",x=10, y=100)
entity4 = rascase.views.EntityComponent("entidad4",x=200, y=300)

canvas.add_child(entity3)
canvas.add_child(entity4)

relation = rascase.views.RelationshipComponent(entity4, entity3,1,False)
canvas.add_child(relation)

win.add(canvas.scrolled_win)

win.connect("delete-event", gtk.main_quit)

win.show_all()
gtk.main()
