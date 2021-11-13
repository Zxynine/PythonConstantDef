class StaticType(type):
	def __setattr__(*args, **kwargs): raise(TypeError('The Constant class does not support assignment!'))
	def __getattr__(*args, **kwargs): raise(TypeError('The Constant class does not allow attribute access!'))

#I think i can remove NonInheritable or soemthing but honestly im not keen on changing the code
#for I am astonished it even functions and i dont know what i did to make it do so.
class Constant(metaclass=StaticType):
	def __new__(cls, *types):
		def TypedConstant(CallCls, *TypeCases, default=Constant):
			nullInstance = None
			lambdaIdentity = lambda *args, **kwargs: nullInstance
			lambdaException = lambda ExceptionMessage: lambda *args, **kwargs: exec("raise(TypeError('"+ExceptionMessage+"'))")
			class IterType(type):
				def __new__(self,name,bases,attrs,**kwargs): return super().__new__(self,name,bases,attrs,**kwargs)
				def __next__(self): raise StopIteration
				def __iter__(cls): return iter([TypeCases[0] if len(TypeCases) != 0 else default,])
				def __eq__(to,compare): return isinstance(compare,(type(to), *TypeCases)) or compare is default
				def __ne__(to,compare): return not (isinstance(compare,(type(to), *TypeCases)) or compare is default)
			class NonInheritable(CallCls):
				__init__ = lambdaIdentity
				__new__ = lambdaIdentity
				__call__ = lambdaIdentity
			nullInstance = IterType(CallCls.__name__, (NonInheritable, CallCls), {})
			nullInstance.__init_subclass__ = lambdaException(f'The parent class "{CallCls.__name__}" does not support inheritance!')
			IterType.__setattr__ = lambdaException(f'The parent class "{CallCls.__name__}" does not support assignment!')
			IterType.__getattr__ = lambdaException(f'The parent class "{CallCls.__name__}" does not allow attribute access!')
			return nullInstance
		if len(types)==0: return TypedConstant
		return lambda cls: TypedConstant(cls, *types)
	def __init_subclass__(*args, **kwargs): raise TypeError('The Constant class does not allow inheritance!')

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
	<class 'NoneType'> <class '__main__.Constant'>
	<class 'NoneType'> <class '__main__.Constant'>

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
	Caught Inheritance Exception | Caught Inheritance Exception
	Caught Assignment Exception | Caught Assignment Exception
	Caught Attribute Access Exception | Caught Attribute Access Exception

	===== Generic Constant Equality =====
	True True

	===== Different Constants Equality =====
	False

	[Done] exited with code=0 in 0.099 seconds
	"""
	def printHeader(headName): print('\n' + '='*5 + ' ' + str(headName) + ' ' + '='*5)
	def printGroups(typL,typR,utypL,utypR): print(str(typL)+' '+str(typR)+('\t'*2)+str(utypL)+' '+str(utypR))
	from typing import Iterable
	@Constant()
	class UnTypedNull:pass
	
	@Constant(type(None))
	class TypedNull:pass

	GENERIC = [i for i in UnTypedNull][0]

	def FlattenIterables(items):
		if not isinstance(items, Iterable): yield items; return
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
	print(*[i for i in TypedNull], *[i for i in UnTypedNull])
	print(*list(FlattenIterables([TypedNull, UnTypedNull])))
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
	inheritance, assignment, attrAccess= [None,None], [None,None], [None,None]
	try: inheritance[0] = type('Inherit', (TypedNull,),{})
	except TypeError: inheritance[0] = ('Caught Inheritance Exception')
	try: assignment[0] = TypedNull.N = None
	except TypeError: assignment[0] = ('Caught Assignment Exception')
	try: attrAccess[0] = TypedNull.N
	except TypeError: attrAccess[0] = ('Caught Attribute Access Exception')
	try: inheritance[1] = type('Inherit', (UnTypedNull,),{})
	except TypeError: inheritance[1] = ('Caught Inheritance Exception')
	try: assignment[1] = UnTypedNull.N = None
	except TypeError: assignment[1] = ('Caught Assignment Exception')
	try: attrAccess[1] = UnTypedNull.N
	except TypeError: attrAccess[1] = ('Caught Attribute Access Exception')
	print(*inheritance, sep= ' | ')
	print(*assignment, sep= ' | ')
	print(*attrAccess, sep= ' | ')
	printHeader('Generic Constant Equality')
	print(UnTypedNull == GENERIC, TypedNull == GENERIC)
	printHeader('Different Constants Equality')
	print(UnTypedNull == TypedNull)
