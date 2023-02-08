

def test1():
  class A:
    def __init__(self, i='parent'): 
      self.i=i
    

  class B(A): 
    def __init__(self, j='child'):
      A.__init__(self)
      self.j=j 


  b=B()
  print('In child, variable from', b.j)
  print('In child variable from', b.i)


def test2():
  class A:
    def __init__(self, i='parent'): 
      self.i=i
      
    
  class B(A): 
    def __init__(self, j='child'):
      super().__init__()
      self.j=j 
    
    
  b=B(i='parent2')
  print('In child, variable from', b.j)
  print('In child variable from', b.i)


def test3():
  class A(object):
    def __init__(self, parent_var1, parent_var2):
      self.parent_var1 = parent_var1
      self.parent_var2 = parent_var2

  class B(A):
    def __init__(self, parent_var1, parent_var2, child_var1):
      A.__init__(self, parent_var1, parent_var2)
      self.child_var1 = child_var1

  parent_obj = A('John', 'Teacher')
  child_obj = B('John', 'Teacher', 'Maths')
  print(parent_obj.parent_var1)
  print(child_obj.parent_var1)

test1()
test2()
test3()