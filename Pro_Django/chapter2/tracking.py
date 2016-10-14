class SubclassTracker(type):
    def __init__(cls, name, bases, attrs):
        try:
            if TrackedClass not in bases:
                return
        except NameError:
            return
        TrackedClass._registry.append(cls)

class TrackedClass(object):
    __metaclass__ = SubclassTracker
    _registry = []

if __name__ == '__main__':
    class ClassOne(TrackedClass):
        pass
    assert TrackedClass._registry == [ClassOne]
    
    class ClassTwo(TrackedClass):
        pass
    assert TrackedClass._registry == [ClassOne, ClassTwo]
