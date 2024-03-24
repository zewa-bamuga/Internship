import enum

from a8t_tools.security.permissions import PermissionsBase


class BasePermissions(PermissionsBase):
    superusesr = enum.auto()
    authenticated = enum.auto()
