class employ:
	import sys as __sys__
	import os as __os__
	import threading as __thread__
	import requests as __requests__
	import urllib.parse as __parser__
	from zipfile import ZipFile as __zip__
	__PATH__ = __sys__.path

	modules = {}            

	class __classify__: pass
	
	def __init__(__self__, __name__="", **__params__):
	
		__self__.__ready__ = False
		
		class __sync__(__self__.__thread__.Thread):
			def run(self, __self__=__self__, __name__=__name__, __params__=__params__):
				del self
				
				if __name__.endswith(".py"): __name__ = __name__[0:__name__.find(".py")]
						
				if "." not in __name__: __filename__ = __name__+".py"
				else: __filename__ = __name__
				
				if "url" in __params__ and (__params__["url"].startswith("http://") or __params__["url"].startswith("https://")) and "path" not in __params__:
					__source__ = "remote"
					__url__ = __params__["url"]
					__join__ = __self__.__parser__.urljoin
					__file__ = __join__(__url__+"/", "__init__.py")
					if "getoptions" in __params__: __getoptions__ = __params__["getoptions"]
					else: __getoptions__ = {"allow_redirects": True, "timeout": 30}
					def __fetch__(url, **options):
						try:
							io = __self__.__requests__.get(url, **options)
							if io.status_code // 100 != 2:
								raise AssertionError
							return io
						except AssertionError: raise AssertionError("No module found in remote repository")
						except: raise AssertionError("Module could not be fetched")
					def __isdir__(url, **options):
						try:
							io = __self__.__requests__.get(url, **options)
							if io.status_code // 100 == 2: return True
							else: return False
						except: raise AssertionError("Module could not be fetched")
						
					try:
						if not __isdir__(__file__, **__getoptions__):
							__isdir__ = False
							__io__ = __fetch__(__url__, **__getoptions__)

							__io__.name = __url__
							
						else:
							__isdir__ = True
							__items__ = []
							__modules__ = {}
							__children__ = __self__.__classify__()
						
							__filename__ = __name__+"/__init__.py"
							__io__ = __fetch__(__file__, **__getoptions__)

							__io__.name = __file__
						del __fetch__
					except Exception as e:
						raise ModuleNotFoundError(e)
				else:
					__source__ = "local"
					if "path" in __params__: __self__.__PATH__ = [__params__["path"]]
					
					for __path__ in __self__.__PATH__:
						try:
							if not __path__.endswith(".zip"):
								if __path__ != "" and not __path__.endswith("/"): __dir__ = __path__+"/"
								else: __dir__ = __path__
								
								if not __self__.__os__.path.isdir(__dir__+__name__):
									__isdir__ = False
									__io__ = open(__dir__+__filename__)
									
								else:
									__isdir__ = True
									__items__ = __self__.__os__.listdir(__dir__+__name__)
									if "__init__.py" in __items__:
										__items__.remove("__init__.py")
										__modules__ = {}
										__children__ = __self__.__classify__()
									
										__filename__ = __name__+"/__init__.py"
										__io__ = open(__dir__+__filename__)
									else: raise Exception
							else:
								__io__ = __self__.__zip__(__path__).open(__filename__)

							break
						except:
							if __self__.__PATH__.index(__path__) < len(__self__.__PATH__)-1: continue
							else: raise ModuleNotFoundError("No module named '"+__name__+"'")
				
				__self__.__setattr__("__os__",None)
				__self__.__setattr__("__zip__",None)
				__self__.__setattr__("__PATH__",[])
				__self__.__setattr__("__requests__",None)
				__self__.__setattr__("__parser__",None)
				
				if "name" in __params__:
					__name__ = __params__["name"]

				if "family" in __params__:
					__family__ = __params__["family"]

				if "level" not in __params__ or __params__["level"] != "private":
					if "res" in __params__: __global__ = __params__["res"]
					else: __global__ = globals()

				if "univ" in __params__:
					__univ__ = __params__["univ"]
				elif __isdir__: __univ__ = __self__.__classify__()
				__self__.__setattr__("__classify__",None)
				
				if __source__ == "local": __script__ = __io__.read()
				elif __source__ == "remote": __script__ = __io__.content
				if type(__script__) == bytes: __script__ = __script__.decode()
				try: __io__.close()
				except: pass
				
				__env__ = locals()
				if not __isdir__ and "only" in __params__: __oldenv__ = dict(__env__) # Snapshots the current environment
				elif __isdir__: __oldenv__ = dict(__env__) # Snapshots the current environment
				__env__.pop("__self__")
				exec(__script__, __env__)
				if not __isdir__ and "only" in __params__:
					__newenv__ = __env__ # Snapshots the new environment
					__env__ = __oldenv__ # Restores the old environment
					for __req__ in __params__["only"]: __env__.update({__req__: __newenv__[__req__]}) # Adds desired variables to old from new environment
					del __oldenv__, __newenv__, __req__
				elif __isdir__:
					for __new__ in __env__:
						if __new__ not in __oldenv__: __univ__.__setattr__(__new__, __env__[__new__])
						del __new__


				if "__items__" in locals():
					try: __items__ = __env__["__index__"]
					except: pass

					if "shared" not in __params__ or __params__["shared"] == "time":
						for __item__ in __items__:
							if __item__.endswith(".py"): __item__ = __item__[0:__item__.find(".py")]
							if "only" not in __params__ or __item__ in __params__["only"]:
								try:
									if __source__ == "local": __child__ = employ(__item__, path=__dir__+__name__, level="private", univ=__univ__, family=__children__)
									elif __source__ == "remote": __child__ = employ(__item__, url=__join__(__url__+"/", __item__+".py"), level="private", univ=__univ__, family=__children__)

									__modules__.update({__item__: __child__})
									__children__.__setattr__(__item__, __child__)
									del __child__
								except: pass
							del __item__
					elif __params__["shared"] == "memory":
						__childdict__ = {}
						for __item__ in __items__:
							if __item__.endswith(".py"): __item__ = __item__[0:__item__.find(".py")]
							__childdict__[__item__] = None
						class __createchild__(__self__.__thread__.Thread):
							def __init__(self, item):
								__self__.__thread__.Thread.__init__(self)
								self.item = item
							def run(self):
								try:
									if __source__ == "local": __childdict__[self.item] = employ(self.item, path=__dir__+__name__, level="private", univ=__univ__, family=__children__)
									elif __source__ == "remote": __childdict__[self.item] = employ(self.item, url=__join__(__url__+"/", self.item+".py"), level="private", univ=__univ__, family=__children__)
								except: del __childdict__[self.item]
						for __item__ in __items__:
							if __item__.endswith(".py"): __item__ = __item__[0:__item__.find(".py")]
							if "only" not in __params__ or __item__ in __params__["only"]:
								__createchild__(__item__).start()

						while None in __childdict__.values(): pass
						else:
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
					
				
				__file__ = __io__.name

				__methods__ = locals()

				if "on" not in __params__ or ("on" in __params__ and __params__["on"] == "sub"):
					for __obj__ in __methods__:
						if (__obj__.startswith("__") and __obj__.endswith("__")) or "only" not in __params__ or __obj__ in __params__["only"]:
							__self__.__setattr__(__obj__,__methods__[__obj__])
							
					if "__modules__" in __methods__:
						for __mod__ in __modules__: __self__.__setattr__(__mod__,__modules__[__mod__])
				
				elif "on" in __params__ and __params__["on"] == "main":
					for __obj__ in __methods__:
						if __obj__.startswith("__") and __obj__.endswith("__"):
							__self__.__setattr__(__obj__, __methods__[__obj__])
						else:
							if "only" not in __params__ or __obj__ in __params__["only"]:
								__global__[__obj__] = __methods__[__obj__]
								
					if "__modules__" in __methods__:
						for __mod__ in __modules__: __global__[__mod__] = __modules__[__mod__]


				if "level" not in __params__ or __params__["level"] != "private":       
					__self__.modules.update({__name__:__self__})
					__self__.__sys__.modules.update({__name__:__self__})
				
				__self__.__setattr__("modules",{})
				__self__.__setattr__("__sys__",None)

				if "name" in __params__:
					__global__[__params__["name"]] = __self__

				__self__.__ready__ = True


		if "sync" in __params__ and __params__["sync"] == False: __sync__().start()
		else: __sync__().run()
