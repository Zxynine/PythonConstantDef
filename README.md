# PythonConstantDef
This repo documents my custom constant decorator that allows the creation of constants which block subclassing, and getting/setting attributes. Additionally, the constants are a singleton that implements some special cases that are not provided by base python constants like the 'None' obj.



Definitions: 
	Constant<Decorator>:
		The constant decorator. See `Null`.


	Null<Constant>:
		The Null object is the entire reason for creating this file. Null behaves very similar to pythons singleton/constant `None`,
		of which it was intended to replace. None is limited in a few special cases and this has been the focus of the design. To start,
		if you were to have a situation where you expect a method/lambda back from a method, however, in special cases you may want to 
		have the method return an object that will represent 'doing nothing'. Its ideal to be able to maybe loop through and call each returned
		lambda imedietly since more often than not it will work. None will not work for this as if you pass it back you either will call it and
		raise an exception saying None is not callable, or you have to check each return if it equals none to call it when you know it will work.
		With Null, that is not a problem as it implements a call dunder that just returns the singleton class. This means you can now check the 
		return of the call if it is Null and potentially combine that with the other called method returns for a seamless transition. Additionaly,
		If you ever find a Null in a loop(or generator) that is expecting iterables, there is no worry as Nulls iter dunder returns an iter over 
		a length 1 array contaning the Null singleton. 
	
		TODO: prevent recursive iterable calls from causing infinate recursion with next dunder
			and variable that tracks multiple iter calls. 2 will return no iterable, 3 calls will raise a stop iteration.

	EmptyTypes<Tuple of Types>
		The `EmptyTypes` object provides easy access to both `Null` and `None` in a tuple for instance checking.
		This is more than likley to be depricated as the constant type is now passed alternate types during each 
		declaration, thus you can now easily check its equality to both Null and/or None through Null == None
