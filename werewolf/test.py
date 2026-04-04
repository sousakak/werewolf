from abc import ABC, abstractmethod

class Parent(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    # ここでsetterを定義しても何も変わらない
    #  setterのみのデコレータで子孫クラスで定義しないと、セットできない
    #  setterとabstractmethodの両方のデコレータのとき、子孫クラスでsetterを定義しなくてもエラーはおきない
        
class Child(Parent):
    def __init__(self):
        self.a = "あ"
        
    @property
    def name(self):
        return "子供"
        
    @name.setter
    def name(self, value):
        self.name = value

child = Child()
print(child.name)
child.name = "こども"
print(child.name)

##################################################################
# これなら動く

class Parent(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @name.setter
    def name(self, value):
        self._name_setter(value)

    @abstractmethod
    def _name_setter(self, value):
        pass
