class employ:
	"""
	Make programmatic, dynamic, and robust import for local or remote Python module or library.
	"""
	import sys as __eMPloY_sys__
	import os as __eMPloY_os__
	import threading as __eMPloY_thread__
	import requests as __eMPloY_requests__
	import urllib.parse as __eMPloY_parser__
	from zipfile import ZipFile as __eMPloY_zip__
	__eMPloY_PATH__ = __eMPloY_sys__.path

	modules = {}            

	class __objectify__:
		"""Create an attributable container (that is, object)."""
		pass
	
	def __init__(__self__, __name__="", **__params__):
		"""
		Creates an `employ` object (that is, module).

		name
			_Optional_. Module, or file name of module.

		path
			_Optional_. Path to local module (or package).

		url
			_Optional_. URL to remote module (or package).

		getoptions
			_Optional_. Kwargs for `requests.get`'s optional parameters. Only applicable to remote modules.

		on = "sub" | "main"
			_Optional_. Scope of module. Default is `"sub"`.
			`"sub"`: module is imported as a submodule (similar to `import module`). All attributes and methods are registered to the `employ` object.
			`"main"`: module is imported as a main module (similar to `from module import *`). All, except special attributes and methods, are registered to the global namespace.

		level = "public" | "private"
			_Optional_. Level of module. Default is `"public"`.
			`"public"`: module has access to environment (as controlled by `res` parameter), and is registered to `sys.modules` and `employ.modules`.
			`"private"`: module is not visible, and has no access, to the environment. Useful for importing child modules or dependencies of a module that would not be exposed globally.

		res
			_Optional_. Connection between module and existing environment (for instance, `globals()`), or a shared resource (for instance, a dictionary) between module and environment. If not specified, `globals()` is used.
			Only applicable to public modules (that is, modules with `level="public"` parameter).

		sync = True | False
			_Optional_. Boolean indicating mode of execution for module import. Default is `True`.
			`True`: Import module synchronously, blocking the main thread until the module is fully imported.
			`False`: Import module asynchronously (in a separate thread), allowing the main thread to continue executing while the module is being imported. Useful for large modules, or modules with blocking, non-terminating code (for instance, a module that runs a server). Main thread must use the `join()` method of the exposed `__thread__` attribute (`threading.Thread` object) to wait for the module to be fully imported before accessing its attributes or methods.

		only
			_Optional_. List of attributes and methods to import. If not specified, all attributes and methods are imported.

		shared = "time" | "memory"
			_Optional_. Mode of execution for child imports. Default is `"time"`. Only applicable to packages.
			`"time"`: Child modules are imported synchronously.
			`"memory"`: Child modules are imported asynchronously (in separate threads). Useful for large packages, or packages with blocking, non-terminating child modules (for instance, a child module that runs a server).

		univ
			_Optional_. Simulated universal environment (an object) to share variables across parent and child modules.

		family
			_Optional_. Common object to share resources across, or allow communication between, sister modules (for instance, modules in the same package). Much useful when paired with `shared="memory"` parameter, where communication is required between non-terminating sister modules (for instance, a client-server application).

		"""

		__self__.__ready__ = False
		
		class __sync__(__self__.__eMPloY_thread__.Thread):
			"""Subclass of `threading.Thread`. Allow both synchronous and asynchronous imports."""

			def run(self, __self__=__self__, __name__=__name__, __params__=__params__):
				"""
				Overrides the `threading.Thread`'s `run()` method. Executes either synchronous and asynchronous imports
				depending on whether it is called directly, or through `threading.Thread`'s `start()` method.
				"""

				del self

				if __name__.endswith(".py"): __name__ = __name__[0:__name__.find(".py")]

				if "url" in __params__ and (__params__["url"].startswith("http://") or __params__["url"].startswith("https://")) and "path" not in __params__:
				# For remote modules:
					__source__ = "remote"
					__url__ = __params__["url"]
					__join__ = __self__.__eMPloY_parser__.urljoin
					__file__ = __join__(__url__+"/", "__init__.py")
					if "getoptions" in __params__: __getoptions__ = __params__["getoptions"]
					else: __getoptions__ = {"allow_redirects": True, "timeout": 30}

					def __fetch__(url, **options):
						"""
						Downloads remote module or library. Returns an HTTP Response object.

						url
							URL of module.
						options
							_Optional_. Kwargs for `requests.get`'s optional parameters.
						"""

						try:
							io = __self__.__eMPloY_requests__.get(url, **options)
							if io.status_code // 100 != 2:
								raise AssertionError
							return io
						except AssertionError: raise AssertionError("No module found in remote repository")
						except: raise AssertionError("Module could not be fetched")

					def __isdir__(url, **options):
						"""
						Checks if remote module is a package (that is, a folder with `__init__.py`).
						Basically checks if a remote resource is available. Returns `True` or `False`.

						url
							URL of module.
						options
							_Optional_. Kwargs for `requests.get`'s optional parameters.
						"""

						try:
							io = __self__.__eMPloY_requests__.get(url, **options)
							if io.status_code // 100 == 2: return True
							else: return False
						except: raise AssertionError("Module could not be fetched")
						
					try:
						if not __isdir__(__file__, **__getoptions__):
						# For remote modules that are not packages (that is, a single `.py` file):
							__isdir__ = False
							__io__ = __fetch__(__url__, **__getoptions__)

							__filename__ = __name__+".py"
							__io__.name = __url__
							
						else:
						# For remote modules that are packages (that is, a folder with `__init__.py`):
							__isdir__ = True
							__items__ = []
							__modules__ = {}
							__children__ = __self__.__objectify__()
						
							__filename__ = __name__+"/__init__.py"
							__io__ = __fetch__(__file__, **__getoptions__)

							__io__.name = __file__
						del __fetch__
					except Exception as e:
					# For remote modules that are not found:
						raise ModuleNotFoundError(e)
				else:
				# For local modules:
					__source__ = "local"
					if "path" in __params__: __self__.__eMPloY_PATH__ = [__params__["path"]]
					
					for __path__ in __self__.__eMPloY_PATH__:
					# For each path in the module search paths:
						try:
							if not __path__.endswith(".zip"):
							# For regular local modules (that are NOT in a zip file):
								if __path__ != "" and not __path__.endswith("/"): __dir__ = __path__+"/"
								else: __dir__ = __path__
								
								if not __self__.__eMPloY_os__.path.isdir(__dir__+__name__):
									__isdir__ = False

									__filename__ = __name__+".py"
									__io__ = open(__dir__+__filename__)
									
								else:
									__isdir__ = True
									__items__ = __self__.__eMPloY_os__.listdir(__dir__+__name__)
									if "__init__.py" in __items__:
										__items__.remove("__init__.py")
										__modules__ = {}
										__children__ = __self__.__objectify__()
									
										__filename__ = __name__+"/__init__.py"
										__io__ = open(__dir__+__filename__)
									else: raise Exception
							else:
							# For local modules that are in a zip file:
								# __isdir__ = False -- Revisit this LATER. For now, assume that all modules in zip files are not packages (that is, a single `.py` file).
								__io__ = __self__.__eMPloY_zip__(__path__).open(__filename__)

							break
						except:
						# When module is not found in the current path, continue to the next path.
						# If no more paths are available, raise `ModuleNotFoundError`.
							if __self__.__eMPloY_PATH__.index(__path__) < len(__self__.__eMPloY_PATH__)-1: continue
							else: raise ModuleNotFoundError("No module named '"+__name__+"'")

				# Clear `employ` object attributes to avoid namespace pollution and potential conflicts with imported module's attributes.
				# LATER: Check if these attributes are garbage collected.
				__self__.__setattr__("__eMPloY_os__",None)
				__self__.__setattr__("__eMPloY_zip__",None)
				__self__.__setattr__("__eMPloY_PATH__",[])
				__self__.__setattr__("__eMPloY_requests__",None)
				__self__.__setattr__("__eMPloY_parser__",None)

				# Allow for custom module name via the `name` parameter.
				# Useful for avoiding naming conflicts when importing modules with the same file name.
				if "name" in __params__:
					__name__ = __params__["name"]

				# Allow shared access to variables across sister modules (for instance, modules in the same package) via  the `__family__` object. 
				if "family" in __params__:
					__family__ = __params__["family"]

				# Allow access to existing environment via the `res` parameter, or via the default `globals()` object,
				# if module is imported as a public module:
				# LATER: Should this be done for private modules too? For now, no. Private modules are not visible to the environment, and should not have access to it.
				if "level" not in __params__ or __params__["level"] != "private":
					if "res" in __params__: __global__ = __params__["res"]
					else: __global__ = globals()

				# Allow child modules to access variables from the parent module's environment via the `__univ__` object.
				if "univ" in __params__:
					__univ__ = __params__["univ"]
				elif __isdir__: __univ__ = __self__.__objectify__()
				__self__.__setattr__("__objectify__",None)

				# Read the module's script.
				if __source__ == "local": __script__ = __io__.read()
				elif __source__ == "remote": __script__ = __io__.content
				if type(__script__) == bytes: __script__ = __script__.decode()
				try: __io__.close()
				except: pass

				# Create a new environment for the module's script to execute in, and execute the script in that environment.
				__env__ = locals()
				if not __isdir__ and "only" in __params__: __oldenv__ = dict(__env__) # Snapshots the current environment
				elif __isdir__: __oldenv__ = dict(__env__) # Snapshots the current environment
				__env__.pop("__self__")
				exec(__script__, __env__)
				if not __isdir__ and "only" in __params__:
				# Perform selective addition of variables from the new environment to the old environment, based on the `only` parameter.
					__newenv__ = __env__ # Snapshots the new environment
					__env__ = __oldenv__ # Restores the old environment
					for __req__ in __params__["only"]: __env__.update({__req__: __newenv__[__req__]}) # Adds desired variables to old from new environment
					del __oldenv__, __newenv__, __req__
				elif __isdir__:
				# Register new variables from the new environment to the `__univ__` object.
					for __new__ in __env__:
						if __new__ not in __oldenv__: __univ__.__setattr__(__new__, __env__[__new__])
						del __new__


				if "__items__" in locals():
				# Basically, if the module is a package (that is, a folder with `__init__.py`), import its child modules.
					# Limit child modules to be imported to those specified in the `__index__` variable,
					# if it exists in the module's environment (that is, in `__init__.py`).
					try: __items__ = __env__["__index__"]
					except: pass

					if "shared" not in __params__ or __params__["shared"] == "time":
					# If child modules would be imported synchronously (as indicated by the `shared` parameter):
						for __item__ in __items__: # Iterate over the child modules.
							if __item__.endswith(".py"): __item__ = __item__[0:__item__.find(".py")]

							if "only" not in __params__ or __item__ in __params__["only"]:
							# If the child module is specified in the `only` parameter, or the `only` parameter is not specified:
								# Quietly import child module, and register in `__modules__` dictionary and `__children__` object.
								try:
									if __source__ == "local": __child__ = employ(__item__, path=__dir__+__name__, level="private", univ=__univ__, family=__children__)
									elif __source__ == "remote": __child__ = employ(__item__, url=__join__(__url__+"/", __item__+".py"), level="private", univ=__univ__, family=__children__)

									__modules__.update({__item__: __child__})
									__children__.__setattr__(__item__, __child__)
									del __child__
								except: pass
							del __item__
					elif __params__["shared"] == "memory":
					# If child modules would be imported asynchronously (as indicated by the `shared` parameter):
						__childdict__ = {}
						for __item__ in __items__: # Iterate over the child modules.
							if __item__.endswith(".py"): __item__ = __item__[0:__item__.find(".py")]
							__childdict__[__item__] = None

						class __createchild__(__self__.__eMPloY_thread__.Thread):
							"""Subclass of `threading.Thread`. Allow asynchronous import of child modules."""

							def __init__(self, item):
								"""
								Initializes child module creation routine.

								item
									Name of child module.
								"""

								__self__.__eMPloY_thread__.Thread.__init__(self)
								self.item = item
							def run(self):
								"""Overrides the `threading.Thread`'s `run()` method. Imports child module, and stores in `__childdict__`."""

								# Quietly import child module, and store in `__childdict__` dictionary.
								try:
									if __source__ == "local": __childdict__[self.item] = employ(self.item, path=__dir__+__name__, level="private", univ=__univ__, family=__children__)
									elif __source__ == "remote": __childdict__[self.item] = employ(self.item, url=__join__(__url__+"/", self.item+".py"), level="private", univ=__univ__, family=__children__)
								except: del __childdict__[self.item]

						# Start asynchronous import of child modules, and wait for all child modules to be imported before proceeding.
						for __item__ in __items__:
							if "only" not in __params__ or __item__ in __params__["only"]:
							# If the child module is specified in the `only` parameter, or the `only` parameter is not specified:
								__createchild__(__item__).start()

						while None in __childdict__.values(): pass
						else:
							# Register child modules in `__modules__` dictionary and `__children__` object.
							for __item__ in __childdict__:
								__child__ = __childdict__[__item__]
								__modules__.update({__item__: __child__})
								__children__.__setattr__(__item__, __child__)
								del __child__
								del __item__
							del __childdict__
					else: raise AssertionError("Unknown resource specified in 'shared' parameter. shared is either 'time' or 'memory' (not '"+__params__["shared"]+"').")
					if __source__ == "remote": del __join__
					del __children__
					

				__file__ = __io__.name # Set the module's `__file__` attribute to the module's authentic file name or URL.

				# Register module's attributes and methods for user access, based on specific conditions.
				__methods__ = locals()

				if "on" not in __params__ or ("on" in __params__ and __params__["on"] == "sub"):
				# If the module is imported as a submodule:
					# Register all module's attributes and methods to the `employ` object. Similar to `import module` statement.
					for __obj__ in __methods__:
						if (__obj__.startswith("__") and __obj__.endswith("__")) or "only" not in __params__ or __obj__ in __params__["only"]:
							__self__.__setattr__(__obj__,__methods__[__obj__])

					# Register all child modules to the `employ` object. Similar to `import module` statement.	
					if "__modules__" in __methods__:
						for __mod__ in __modules__: __self__.__setattr__(__mod__,__modules__[__mod__])
				
				elif "on" in __params__ and __params__["on"] == "main":
				# If the module is imported as a main module:
					# Register only module's main attributes and methods to the global namespace. Similar to `from module import *` statement.
					for __obj__ in __methods__:
						if __obj__.startswith("__") and __obj__.endswith("__"):
							__self__.__setattr__(__obj__, __methods__[__obj__])
						else:
							if "only" not in __params__ or __obj__ in __params__["only"]:
								__global__[__obj__] = __methods__[__obj__]

					# Register all child modules to the global namespace. Similar to `from module import *` statement.
					if "__modules__" in __methods__:
						for __mod__ in __modules__: __global__[__mod__] = __modules__[__mod__]


				# Register imported module to the general `employ` class and to `sys.modules`,
				# if module is imported as a public module.
				if "level" not in __params__ or __params__["level"] != "private":
					__self__.modules.update({__name__:__self__})
					__self__.__eMPloY_sys__.modules.update({__name__:__self__})

				# Clear `employ` object attributes to avoid namespace pollution and potential conflicts with imported module's attributes.
				__self__.__setattr__("modules",{})
				__self__.__setattr__("__eMPloY_sys__",None)

				# Register the `employ` object to the global namespace, if `name` parameter is specified.
				if "name" in __params__:
					__global__[__params__["name"]] = __self__

				__self__.__ready__ = True


		# Start the import process, either synchronously or asynchronously, based on the `sync` parameter.
		__self__.__thread__ = __sync__()
		if "sync" in __params__ and __params__["sync"] == False: __self__.__thread__.start()
		else: __self__.__thread__.run()
