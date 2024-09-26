from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name="home"),
    path('snippets/add', views.add_snippet_page, name="add_snippet"),
    path('snippets/list', views.snippets_page, name="snippets_list"),
    #path('snippets/create', views.create_snippet, name="create_snippet"),
    path("snippet/<int:snippet_id>", views.get_snippet, name="snippet-detail"),
    path("snippet/<int:snippet_id>/edit", views.snippet_edit, name="snippet-edit"),
    path("snippet/<int:snippet_id>/delete", views.snippet_delete, name="snippet-delete"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
