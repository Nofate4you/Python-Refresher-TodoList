import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import path
from django.core.wsgi import get_wsgi_application
from django.conf.urls.static import static

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", __name__)

settings.configure(
    DEBUG=True,
    SECRET_KEY="a_random_secret_key",
    ROOT_URLCONF=__name__,
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [os.path.join(BASE_DIR, "templates")],
        },
    ],
    ALLOWED_HOSTS=["*"],
    MIDDLEWARE=[
        "django.middleware.csrf.CsrfViewMiddleware",
    ],
    STATIC_URL="/static/",
    STATICFILES_DIRS=[os.path.join(BASE_DIR, "static")],
)

# List to store todo items
todos = []

# Views
def index(request):
    return render(request, "index.html", {"todos": todos})


def add(request):
    if request.method == "POST":
        todo = request.POST.get("todo")
        if todo:
            todos.append(todo)
    return redirect("/")


def delete(request, todo_id):
    if 0 <= todo_id < len(todos):
        todos.pop(todo_id)
    return redirect("/")


# URL patterns
urlpatterns = [
    path("", index, name="index"),
    path("add/", add, name="add"),
    path("delete/<int:todo_id>/", delete, name="delete"),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])  # Serve static files

# WSGI application
application = get_wsgi_application()

# Entry point
if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(["manage.py", "runserver"])
