
def test1():
    class Color:
        def __init__(self):
            self.name = 'Green' # overwritte
            self.obj_type = 'Color' # shared with inner class
            self.lg = self.Lightgreen(self)

        def show(self):
            print ('Name:', self.name)
 

        class Lightgreen:
            def __init__(self, color_obj):
                # Overwrite outer class attribute
                self.name = 'Light Green'
                # Access outer class attribute
                self.obj_type = color_obj.obj_type
                # Create new attribute
                self.code = '024avc'
        
            # @staticmethod
            # @classmethod
            def display(self):
                print ('Name:', self.name)
                print ('Code:', self.code)
            
            # @classmethod
            def display_obj_type(self):
                print ('Object type:', self.obj_type)


    outer = Color()
    g = outer.lg 
    g.display()
    g.display_obj_type()

    return


def test2():
    # create outer class
    class Doctors:
        def __init__(self):
            self.name = 'Doctor'
            self.den = self.Dentist()
            self.car = self.Cardiologist()
    
        def show(self):
            print('In outer class')
            print('Name:', self.name)
    
        # create a 1st Inner class
        class Dentist:
            def __init__(self):
                self.name = 'Dr. Savita'
                self.degree = 'BDS'
    
            def display(self):
                print("Name:", self.name)
                print("Degree:", self.degree)
    
        # create a 2nd Inner class
        class Cardiologist:
            def __init__(self):
                self.name = 'Dr. Amit'
                self.degree = 'DM'
    
            def display(self):
                print("Name:", self.name)
                print("Degree:", self.degree)
    
    
    # create a object
    # of outer class
    outer = Doctors()
    outer.show()
    
    # create a object
    # of 1st inner class
    d1 = outer.den
    
    # create a object
    # of 2nd inner class
    d2 = outer.car
    print()
    d1.display()
    print()
    d2.display()

    return


def test3():
    """Inner class which receives outer class instance as argument"""
    class Outer(object):

        def createInner(self):
            return Outer.Inner(self)

        class Inner(object):
            def __init__(self, outer_instance):
                self.outer_instance = outer_instance
                self.outer_instance.somemethod()

            def inner_method(self):
                self.outer_instance.anothermethod()


test1()
# test2()