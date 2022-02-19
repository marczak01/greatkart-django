from category.models import Category

#function which is putting all category names into the list
#called "links". We use python dict() fnc to convert it into the list
def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)