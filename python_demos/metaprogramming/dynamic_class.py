
# class Person:

#     def __init__(self, fn, ln):
#         self.fn = fn
#         self.ln = ln

#     def fullname(self):
#         return self.fn + ' ' + self.ln

def constructor(self, fn, ln):
    self.fn = fn
    self.ln = ln

def fullname(self):
    return self.fn + ' ' + self.ln    

Person = type("Person", (object,), {
    "__init__": constructor,
    "fullname": fullname
})


p = Person('Bob', 'Smith')
print(p.fullname())

