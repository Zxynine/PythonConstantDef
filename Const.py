#I think i can remove NonInheritable or soemthing but honestly im not keen on changing the code
#for I am astonished it even functions and i dont know what i did to make it do so.
def Constant(*types):
	def TypedConstant(CallCls, *TypeCases):
		nullInstance = None
		class IterType(type):
			def __iter__(cls): return iter([cls,])
			def __eq__(null,compare): return isinstance(compare,(type(null), *TypeCases))
			def __ne__(null,compare): return not isinstance(compare,(type(null), *TypeCases))
		lambdaIdentity = lambda *args, **kwargs: nullInstance
		lambdaException = lambda ExceptionMessage: lambda *args, **kwargs: exec("raise(TypeError('"+ExceptionMessage+"'))")
		class NonInheritable(CallCls, metaclass=IterType):
			__init__ = lambdaIdentity
			__new__ = lambdaIdentity
			__call__ = lambdaIdentity
			__init_subclass__ = lambdaIdentity
		nullInstance = type(CallCls.__name__, (NonInheritable, CallCls), {})
		NonInheritable.__init_subclass__ = lambdaException(f'The parent class "{CallCls.__name__}" does not support inheritance!')
		IterType.__setattr__ = lambdaException(f'The parent class "{CallCls.__name__}" does not support assignment!')
		IterType.__getattr__ = lambdaException(f'The parent class "{CallCls.__name__}" does not allow attribute access!')
		return nullInstance
	if len(types)==0: return TypedConstant
	return lambda cls: TypedConstant(cls, *types)

@Constant(type(None))
class Null:pass

EmptyTypes = (type(None), type(Null))






if __name__ == '__main__':
	"""
	====================
	::Typed Tests::
	====================

	===== Repeat access and calls =====
	<class '__main__.TypedNull'> <class '__main__.TypedNull'>
	<class '__main__.TypedNull'> <class '__main__.TypedNull'>
	<class '__main__.TypedNull'> <class '__main__.TypedNull'>

	===== Iteration =====
	<class '__main__.TypedNull'>

	===== Own-Type equality =====
	True False
	True False

	===== None-Type equality =====
	True False
	True False
	True False

	===== Wrong-Type equality =====
	False False

	===== Non-Keyword access Blocking =====
	Caught Inheritance Exception
	Caught Assignment Exception
	Caught Attribute Access Exception


	====================
	::UnTyped Tests::
	====================

	===== Repeat access and calls =====
	<class '__main__.UnTypedNull'> <class '__main__.UnTypedNull'>
	<class '__main__.UnTypedNull'> <class '__main__.UnTypedNull'>
	<class '__main__.UnTypedNull'> <class '__main__.UnTypedNull'>

	===== Iteration =====
	<class '__main__.UnTypedNull'>

	===== Own-Type equality =====
	True False
	True False

	===== None-Type equality =====
	False True
	False True
	False True

	===== Wrong-Type equality =====
	False False

	===== Non-Keyword access Blocking =====
	Caught Inheritance Exception
	Caught Assignment Exception
	Caught Attribute Access Exception


	====================
	::Different Constants Equality::
	====================
	False

	[Done] exited with code=0 in 0.081 seconds
	"""
	def printHeader(headName): print('\n' + '='*5 + ' ' + str(headName) + ' ' + '='*5)
	@Constant()
	class UnTypedNull:pass
	
	@Constant(type(None))
	class TypedNull:pass

	print('='*20)
	print('::Typed Tests::')
	print('='*20)
	N0, N1 = TypedNull(), TypedNull
	printHeader('Repeat access and calls')
	print(N0,N1)
	print(TypedNull,TypedNull)
	print(TypedNull(),TypedNull())
	printHeader('Iteration')
	for i in TypedNull(): print(i)
	printHeader('Own-Type equality')
	print(TypedNull == TypedNull, TypedNull != TypedNull)
	print(TypedNull == TypedNull(), TypedNull() != TypedNull)
	printHeader('None-Type equality')
	print(TypedNull == None, TypedNull != None)
	print(None == TypedNull, None != TypedNull)
	print(TypedNull() == None, TypedNull() != None)
	printHeader('Wrong-Type equality')
	print(TypedNull == object, TypedNull == type)
	printHeader('Non-Keyword access Blocking')
	try: type('Inherit', (TypedNull,),{})
	except TypeError: print('Caught Inheritance Exception')
	try: TypedNull.N = None
	except TypeError: print('Caught Assignment Exception')
	try: TypedNull.N
	except TypeError: print('Caught Attribute Access Exception')
	print('\n\n' + '='*20)
	print('::UnTyped Tests::')
	print('='*20)
	N0, N1 = UnTypedNull(), UnTypedNull
	printHeader('Repeat access and calls')
	print(N0,N1)
	print(UnTypedNull,UnTypedNull)
	print(UnTypedNull(),UnTypedNull())
	printHeader('Iteration')
	for i in UnTypedNull(): print(i)
	printHeader('Own-Type equality')
	print(UnTypedNull == UnTypedNull, UnTypedNull != UnTypedNull)
	print(UnTypedNull == UnTypedNull(), UnTypedNull() != UnTypedNull)
	printHeader('None-Type equality')
	print(UnTypedNull == None, UnTypedNull != None)
	print(None == UnTypedNull, None != UnTypedNull)
	print(UnTypedNull() == None, UnTypedNull() != None)
	printHeader('Wrong-Type equality')
	print(UnTypedNull == object, UnTypedNull == type)
	printHeader('Non-Keyword access Blocking')
	try: type('Inherit', (UnTypedNull,),{})
	except TypeError: print('Caught Inheritance Exception')
	try: UnTypedNull.N = None
	except TypeError: print('Caught Assignment Exception')
	try: UnTypedNull.N
	except TypeError: print('Caught Attribute Access Exception')
	print('\n\n' + '='*20)
	print('::Different Constants Equality::')
	print('='*20)
	print(UnTypedNull == TypedNull)
