from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = "tutorial"

urlpatterns = [
    path(
        "mine/",
        login_required(views.ManageCourseListView.as_view()),
        name="manage_course_list",
    ),
    path(
        "create/",
        login_required(views.CourseCreateView.as_view()),
        name="course_create",
    ),
    path(
        "<pk>/edit/",
        login_required(views.CourseUpdateView.as_view()),
        name="course_edit",
    ),
    path(
        "<pk>/delete/",
        login_required(views.CourseDeleteView.as_view()),
        name="course_delete",
    ),
    path(
        "<pk>/module/",
        login_required(views.CourseModuleUpdateView.as_view()),
        name="course_module_update",
    ),
    path(
        "module/<int:module_id>/content/<model_name>/create/",
        login_required(views.ContentCreateUpdateView.as_view()),
        name="module_content_create",
    ),
    path(
        "module/<int:module_id>/content/<model_name>/<id>/",
        login_required(views.ContentCreateUpdateView.as_view()),
        name="module_content_update",
    ),
    path(
        "content/<int:id>/delete/",
        login_required(views.ContentDeleteView.as_view()),
        name="module_content_delete",
    ),
    path(
        "module/<int:module_id>/",
        login_required(views.ModuleContentListView.as_view()),
        name="module_content_list",
    ),
    path(
        "module/order/",
        login_required(views.ModuleOrderView.as_view()),
        name="module_order",
    ),
    path(
        "content/order/",
        login_required(views.ContentOrderView.as_view()),
        name="content_order",
    ),
    path(
        "subject/<slug:subject>/",
        login_required(views.CourseListView.as_view()),
        name="course_list_subject",
    ),
    path(
        "<slug:slug>/",
        login_required(views.CourseDetailView.as_view()),
        name="course_detail",
    ),
]
