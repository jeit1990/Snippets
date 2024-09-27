from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.index_page, name="home"),
    path('snippets/add', views.add_snippet_page, name="add_snippet"),
    path('snippets/list', views.snippets_page, name="snippets_list"),
    path('snippets/list/<str:user_name>', views.snippets_page_user, name="snippets_list_user"),
    #path('snippets/create', views.create_snippet, name="create_snippet"),
    path("snippet/<int:snippet_id>", views.get_snippet, name="snippet-detail"),
    path("snippet/<int:snippet_id>/edit", views.snippet_edit, name="snippet-edit"),
    path("snippet/<int:snippet_id>/delete", views.snippet_delete, name="snippet-delete"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('register', views.create_user, name="register"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
