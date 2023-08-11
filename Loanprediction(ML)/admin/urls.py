
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Django Task"
admin.site.site_title = "Django Task Admin Portal"
admin.site.index_title = "Welcome to Django Task Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls'))

]
