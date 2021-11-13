#I think i can remove NonInheritable or soemthing but honestly im not keen on changing the code
#for I am astonished it even functions and i dont know what i did to make it do so.
def Constant(*types):
	def TypedConstant(CallCls, *TypeCases):
		nullInstance = None
		class IterType(type):
			def __iter__(cls): return iter([None,])
			def __next__(self): raise StopIteration
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
	===== Repeat access and calls =====
	<class '__main__.TypedNull'> <class '__main__.TypedNull'>		<class '__main__.UnTypedNull'> <class '__main__.UnTypedNull'>
	<class '__main__.TypedNull'> <class '__main__.TypedNull'>		<class '__main__.UnTypedNull'> <class '__main__.UnTypedNull'>
	<class '__main__.TypedNull'> <class '__main__.TypedNull'>		<class '__main__.UnTypedNull'> <class '__main__.UnTypedNull'>

	===== Iteration =====
	None
	None

	===== Own-Type equality =====
	True False		True False
	True False		True False

	===== None-Type equality =====
	True False		False True
	True False		False True
	True False		False True

	===== Wrong-Type equality =====
	False False		False False

	===== Non-Keyword access Blocking =====
	Caught Inheritance Exception
	Caught Assignment Exception
	Caught Attribute Access Exception
	Caught Inheritance Exception
	Caught Assignment Exception
	Caught Attribute Access Exception

	===== ::Different Constants Equality:: =====
	False

	[Done] exited with code=0 in 0.097 seconds
	"""
	def printHeader(headName): print('\n' + '='*5 + ' ' + str(headName) + ' ' + '='*5)
	def printGroups(typL,typR,utypL,utypR): print(str(typL)+' '+str(typR)+('\t'*2)+str(utypL)+' '+str(utypR))

	@Constant()
	class UnTypedNull:pass
	
	@Constant(type(None))
	class TypedNull:pass

	def FlattenIterables(items):
		if not isinstance(items, Iterable):  yield [items,]
		for x in items:
			if isinstance(items, Iterable):
				yield from FlattenIterables(x)
			else: yield x

	TN0, TN1 = TypedNull(), TypedNull
	UN0, UN1 = UnTypedNull(), UnTypedNull
	printHeader('Repeat access and calls')
	printGroups(TN0,TN1,UN0,UN1)
	printGroups(TypedNull,TypedNull,UnTypedNull,UnTypedNull)
	printGroups(TypedNull(),TypedNull(),UnTypedNull(),UnTypedNull())
	printHeader('Iteration')
	for i in TypedNull(): print(i)
	for i in UnTypedNull(): print(i)
	# print(list(FlattenIterables([TypedNull,UnTypedNull])))
	printHeader('Own-Type equality')
	printGroups(TypedNull == TypedNull, TypedNull != TypedNull, UnTypedNull == UnTypedNull, UnTypedNull != UnTypedNull)
	printGroups(TypedNull == TypedNull(), TypedNull() != TypedNull, UnTypedNull == UnTypedNull(), UnTypedNull() != UnTypedNull)
	printHeader('None-Type equality')
	printGroups(TypedNull == None, TypedNull != None, UnTypedNull == None, UnTypedNull != None)
	printGroups(None == TypedNull, None != TypedNull, None == UnTypedNull, None != UnTypedNull)
	printGroups(TypedNull() == None, TypedNull() != None, UnTypedNull() == None, UnTypedNull() != None)
	printHeader('Wrong-Type equality')
	printGroups(TypedNull == object, TypedNull == type, UnTypedNull == object, UnTypedNull == type)
	printHeader('Non-Keyword access Blocking')
	try: type('Inherit', (TypedNull,),{})
	except TypeError: print('Caught Inheritance Exception')
	try: TypedNull.N = None
	except TypeError: print('Caught Assignment Exception')
	try: TypedNull.N
	except TypeError: print('Caught Attribute Access Exception')
	try: type('Inherit', (UnTypedNull,),{})
	except TypeError: print('Caught Inheritance Exception')
	try: UnTypedNull.N = None
	except TypeError: print('Caught Assignment Exception')
	try: UnTypedNull.N
	except TypeError: print('Caught Attribute Access Exception')
	printHeader('::Different Constants Equality::')
	print(UnTypedNull == TypedNull)
