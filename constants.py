from typing import Any, Iterator, Sequence, Union, overload, _T


class _ConstantClass(): ...


class _ConstantDict():
    @overload
    def __init__(self, values: dict = {}):
        self._consts = {}
        for k, v in values.items():
            
            #Key must be a string
            if not isinstance(k, str):
                raise TypeError("Constant keys must be of type 'str'")
            
            if isinstance(v, dict):
                self._consts[k] = _Constant(v)
            elif isinstance(v, list):
                self._consts[k] = tuple(v)
            else:
                self._consts[k] = v
        
        self._dict = {}
        for k, v in self._consts:
            if isinstance(v, _Constant):
                v = dict(_Constant)
            self._dict[k] = v
    
    @overload
    def __init__(self, *args: Union[list[Sequence[str, Any]], tuple[Sequence[str, Any]]]):
        self.__init__(dict(args))

    @overload
    def __getitem__(self, name: str) -> Any:
        return self._consts[name]

    @overload
    def __getitem__(self, name: tuple[str]) -> Any:
        if len(name) == 1:
            return self[name[0]]
        return self[name[0]][name[1:]]

    def __dict__(self) -> dict:
        return self._dict

    def __iter__(self) -> Iterator:
        return self.__dict__().items()

    def __str__(self) -> Any:
        return str(self._consts)

    def __getattr__(self, name: str) -> Any:
        return self[name]

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError('Constants cannot be changed')
    
    def __setitem__(self, name: str, value: Any) -> None:
        raise AttributeError('Constants cannot be changed')
    
    def __delitem__(self, name: str) -> None:
        raise AttributeError('Constants cannot be deleted')

    def __contains__(self, name: str) -> Any:
        return name in self.__dict__()
    
    def __repr__(self) -> str:
        return str(self.__dict__())
    
    def __eq__(self, other: Any):
        if isinstance(other, dict):
            return self.__dict__() == other
        if isinstance(other, _Constant):
            return self.__dict__() == other.__dict__()


#https://www.codeproject.com/Articles/1227368/Python-Readonly-Attributes-Complete-Solution
class _ReadonlyMetaclass(type):
    def __new__(mcls, clsname, bases, clsdict: dict):
        def getMclsAttr(attr):
            return lambda cls: type(cls)._attributeContainer[attr]
        readonlyAttrs = {}
        readonlyProperties = {}
        for name, value in dict(clsdict).items():
            if value[:2] == '__' or value[:len(clsname) + 3] == f'_{clsname}__':
                continue
            if value == '_attributeContainer':
                raise ValueError("'_attributeContainer' is a reserved key name")
            readonlyAttrs[name] = value
            readonlyProperties[name] = property(getMclsAttr(name))
            try: 
                clsdict.pop(name)
            except KeyError:
                pass
        childClassName = '_ReadonlyMetaclassChild'
        localQualname = '.'.join(getMclsAttr.__qualname__.split('.')[:-2])
        childQualname = f'{localQualname}.{childClassName}'
        returnQualname = f'{childQualname}.{clsname}'
        return type.__new__(
            type(
                childClassName,
                (mcls,),
                {
                    '_attributeContainer': readonlyAttrs,
                    '__qualname__': childClassName,
                    **readonlyProperties
                },
            ),
            clsname, 
            bases, 
            {
                '__qualname__': returnQualname,
                **clsdict,
            },
        )


class _ReadonlyBaseClass(metaclass=_ReadonlyMetaclass): ...

'''
class Readonly(type):

    class Attribute(object):
        def __init__(self, value):
            self.value = value
    
    def __new__(metaclass, classname, bases, classdict):
        class NewMetaclass(metaclass):
            attributeContainer = {}
        def getAttrFromMetaclass(attr):
            return lambda cls: type(cls).attributeContainer[attr]
        clone = dict(classdict)
        for name, value in clone.items():
            if not isinstance(value, metaclass.Attribute):
                continue;
            NewMetaclass.attributeContainerName[name] = value.value
            aProperty = property(getAttrFromMetaclass(name))
            setattr(NewMetaclass, name, aProperty)
            classdict[name] = aProperty
            classdict.pop(name, None)               
        return type.__new__(NewMetaclass, classname, bases, classdict)
# '''

class _BaseConstant(_ReadonlyBaseClass):
    
    def __new__(cls: Any) -> None:
        """Prevent constants classes from being instantiated"""

        raise TypeError('Constant cannot be instantiated')
    
    def __setattr__(self, name: str, value: Any) -> None:
        pass


class _Constant():
    def __init__(self, value):
        self._value = value
    
    def __get__(self, obj, objtype=None):
        return self._value

    def __set__(self, obj, value):
        raise AttributeError('Constants cannot be changed')


def _ConstantClass(cls) -> _BaseConstant:
    default_dict = type('', (), {}).__dict__.keys()
    unique_attrs = [attr for attr in cls.__dict__.keys() if attr not in default_dict]
    
    

    return type(
        cls.__name__,
        (_BaseConstant,),
        {attr: _Constant(getattr(cls, attr)) for attr in unique_attrs},
    )()


def Static(cls) -> object:
    return cls()


@_ConstantClass
class Interface():
    kDriverControllerPort = 0
    kManipControllerPort = 1

@_ConstantClass
class Drivetrain():
    kLeftMotorIDs = ()
    kRightMotorIDs = ()

@_ConstantClass
class Elevator():
    kMotorIDs = ()
    kPIDConstants = {'Kp': 0, 'Ki': 0, 'Kd': 0}


if __name__ == '__main__':
    #Static instance (final)
    #Nonfinal values
    #Able to add attributes
    @Static
    class A():
        a = 2
        b = 3
    
    #Static instance (final)
    #Final values
    #Unable to add values
    B = _ConstantDict({
        'a': 2,
        'b': 3,
    })

    #Equivalent to B
    C = _ConstantDict({
        ('a', 2),
        ['b', 3],
    })

    #Static class (nonfinal)
    #Final values
    #Able to add values
    class D(metaclass=_ReadonlyMetaclass):
        a = 2
        b = 3
    
    #Equivalent to D
    class E(_ReadonlyBaseClass):
        a = 2
        b = 3
