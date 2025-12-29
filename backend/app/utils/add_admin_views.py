from inspect import isclass
from app.api.admin import views
from sqladmin import ModelView
from typing import Callable

def add_views(add_view: Callable):
    for name, obj in views.__dict__.items():
        if isclass(obj) and issubclass(obj, ModelView) and obj is not ModelView:
            add_view(obj)