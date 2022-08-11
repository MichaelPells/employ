class Class:
	def __init__(self):
		s = 2
		def t():
			return s*3
		
		self.__setattr__("s",s)
		self.__setattr__("t",t)

	
print(Class().t())
