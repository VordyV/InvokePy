#
# InvokePy library to simplify the implementation of console commands.
# The usual import is done like this `from invokepy import dispatcher`.
# `dispatcher` is the main handler, but if an additional one is required, a separate instance can be created.
#
from ._command_dispatcher import CommandDispatcher

__all__ = [
	"CommandDispatcher"
]

dispatcher = CommandDispatcher()