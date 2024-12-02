import inspect
from typing import Callable, Any


class CommandDispatcher(object):

	def __init__(self):
		self.commands = {}
		self.signature_cache = {}

	def register(self, name: str):

		def decorator(func: Callable):
			self.commands[name] = func
			sig = inspect.signature(func)
			param_types = {}
			has_varargs = False

			for param_name, param in sig.parameters.items():
				if param.kind == inspect.Parameter.VAR_POSITIONAL:
					has_varargs = True
				param_types[param_name] = param.annotation if param.annotation != param.empty else None

			self.signature_cache[name] = {
				'signature': sig,
				'param_types': param_types,
				'has_varargs': has_varargs,
			}
			return func

		return decorator

	def _convert_arg(self, value: str, param_type: Callable) -> Any:
		if param_type is None:
			return value
		try:
			return param_type(value)
		except (ValueError, TypeError):
			raise ValueError(f"Cannot convert '{value}' to {param_type.__name__}")

	def execute(self, command_str: str) -> Any:
		command_name, *command_args = command_str.split()
		if command_name not in self.commands:
			raise ValueError(f"Command '{command_name}' not found.")

		command_func = self.commands[command_name]
		cached_sig = self.signature_cache[command_name]

		param_types = cached_sig['param_types']
		has_varargs = cached_sig['has_varargs']

		converted_args = []
		additional_args = []

		param_names = list(param_types.keys())
		for i, arg in enumerate(command_args):
			if has_varargs and i >= len(param_names):
				additional_args.append(self._convert_arg(arg, param_types[param_names[-1]]))
			else:
				param_type = param_types[param_names[i]]
				converted_args.append(self._convert_arg(arg, param_type))

		bound_args = cached_sig['signature'].bind_partial(*converted_args, *additional_args)
		bound_args.apply_defaults()

		return command_func(*bound_args.args, **bound_args.kwargs)