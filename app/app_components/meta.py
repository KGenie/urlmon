import sys, inspect, app_globals
from response import JinjaResponse
from service import Service
from util import get_controller_actions, get_controller_services


def _declare_actions(cls, name, bases, attrs):
    actions = get_controller_actions(attrs)
    attrs['_actions'] = actions


def _declare_services(cls, name, bases, attrs):
    services = get_controller_services(attrs)
    attrs['_services'] = services


class WebMonitorControllerMetaclass(type):

    def __new__(cls, name, bases, attrs):
        _declare_actions(cls, name, bases, attrs)
        _declare_services(cls, name, bases, attrs)

        return super(WebMonitorControllerMetaclass, cls).__new__(cls, name, bases, attrs)
