
class EntityDoesNotExist(Exception):
    """Raised when entity was not found in database."""


class DuplicatedIdentityKey(Exception):
    """Raised when new entity has duplicated identity information with existing one"""
