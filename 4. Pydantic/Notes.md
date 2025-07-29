# Why Pydantic is needed?
- As we know Python is a dynamic langauge i.e. under one variable, multiple types of data types can be there and due to this there is at all no restrictions on what kind of data you want to achieve and is it actually matching with the data you insert or no. There is at all no type validation process to check this flaw in Python.
- One way to visualize what kind of data a method needs is done by Type Hinting. In this, we are specifically hinting during the making of the method on what data type you have to give data to the method.
    - For example: def insert_patient(name:str, age:int):
                        pass
    - As you can see we are hinting about the datatype of the particular variable. But stil there is a problem. Even though we have given a hint about the datatype, it will still take any kind of data when used.
    - Type hinting is only used to give information rather than type validation. It doesn't produce any kind of error.    
- Another way is to use **Type()**. What it does is, it checks the data type of the variable inside the parenthesis and with a combination of if statement you can check whether the data type entered is correct or no. But the only thing that makes this approach bad is that its not scallable. In production level code you can't write this type of code all the time just to check data type of every single variable out there.
- The same goes for data validation. By data validation, it means checking certain constraints of the particular data such that it doesnt create unchecked errors. 

- Pydantic is smart enough to convert the required data type from one data type to another for example - string to int if needed. Its called Type Coercion.
- Sometimes this coversion can lead to misleading data conversion which can result in issues. So, to prevent this kind of automatic conversion, we can supress it by using the Strict parameter to True.

# Nested Models:
- Somtimes there will be fields which contains multiple type of data in itself, in these situations, it becomes very hard to validate the data as well as the type.
- So, to resolve this issue, the concept of Nested Models are used. In simple terms, we just create another class which is inherited from Pydantic and then declare the particular fields which were once summed up in a single field. After that we can create a object of that class to the value of the necessary key and now we are able to do all basic operations to validate data and type.