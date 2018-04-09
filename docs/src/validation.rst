Validating Thrift Structs
=========================

Validating Thrift structs and their encompassing data is made easy with Django and Manifold. Simply create a subclass of
:code:`manifold.validators.ThriftValidator` that mirrors the attributes of your Thrift struct. You can then validate
any Thrift objects by instantiating the Form with the Thrift object as an argument. An example is shown below.

Our thrift declaration would be:

::

   struct JobTemplate {
       1: list<i16> some_values,
       2: optional string other_value
   }

We would then have a ``ThriftValidator`` defined somewhere:

.. code:: python

    from manifold.validators import ThriftValidator, ListField, StringField

    class JobTemplateValidator(ThriftValidator):

        # `some_values` must be int types, and the list must contain at least 1 item
        some_values = ListField(min_length=1, list_type=int)

        other_value = StringField(required=False, max_length=128)

and then we can use this in our code to provide a full Request and
Response function like so:

.. code:: python

    from manifold.handler import handler
    from validators import JobTemplateValidator

    # Map the Thrift function 'schedule' to this function
    @handler.map_function('schedule')
    def schedule_job(job):
        """Schedule a service job to run
        """
        validator = JobTemplateValidator(job)
        if not validator.is_valid():
            return False
        return True

Notice how we call ``is_valid()`` on our validator. Its very similar to
`Django Forms`_, because the validators actually are subclasses of
``django.forms``. It returns ``True`` when the passed parameters were
validated, and ``False`` otherwise.

Available Validation Fields
***************************

For validators, you can use the following validation fields, which map very closely to the Thrift types.
These can be imported from :code:`manifold.validators`. All fields can have :code:`required=True|False` passed to them, on
whether or not the field is required. Note that the default is :code:`True`. Use :code:`False` for Thrift's :code:`optional` fields.

- ``I16Field``, ``I32Field``, ``I64Field``: All three represent integers where their values must within their specific bounds.
- ``BoolField``: Represents a Thrift ``bool``. Use ``required=False`` if the value can be either True of False, else it will always need to be True.
- ``DoubleField``: Represents a Thrift ``double``. Use ``min_value`` and ``max_value`` to ensure range.
- ``StringField``: Represents a Thrift ``string``. Use ``max_length`` and ``min_length`` to ensure length.
- ``ByteField``: Represents a Thrift ``byte``. Gets represented as a Python integer between 0 and 256.
- ``ListField``: Represents a Thrift ``list<type>``. Can pass ``list_type=<Python type>`` to ensure list is of certain Python type, and ``min_length=<int>`` and ``max_length=<int>`` to ensure a certain number of values in the list.
- ``SetField``: Represents a Thrift ``set<type>``. Can pass ``set_type=<Python type>`` to ensure list is of certain Python type, and ``min_length=<int>`` and ``max_length=<int>`` to ensure a certain number of values in the list.
- ``MapField``: Represents a Thrift ``map<key_type, val_type>``. Can pass ``key_type`` and ``val_type`` to ensure type checking. Maps to a Python Dictionary.
- ``StructField``: Described under **Complex Validation**.

To retreive values from a validator, you can call ``.get(key, default=None)`` where ``key`` is the desired validator
field, and the optional ``default`` is what to return if not found. Note that you must call ``is_valid`` before
requesting any values. An example is shown below:

.. code:: python

    from manifold.handler import handler
    from validators import JobTemplateValidator

    # Map the Thrift function 'schedule' to this function
    @handler.map_function('schedule')
    def schedule_job(job):
        """Schedule a service job to run
        """
        validator = JobTemplateValidator(job)
        if not validator.is_valid():
            return False
        job_boolean = validator.get('some_bool_field', default=False)
        return job_boolean

You can also get the ``struct`` attribute on the validator to get the originally passed data/struct. Validators can take in either the Thrift structs as their Python class instance, or as a serialized dictionary.

Complex Validation
******************

If you have a situation where you have a Thrift struct that contains
another Thrift struct, you will probably want to validate at every
level. This would be when you want to use a
``manifold.validators.StructField``, which takes in a
``manifold.validators.ThriftValidator`` subclass as its first parameter.
It will verify the inner struct(s) first, before evaluating the parent.
Let’s say that you have the following somewhere in your Thrift file:

.. code:: thrift

     struct InnerStruct {
         1: i16 val
     }
    struct ContainerStruct {
        1: string some_string,
        2: InnerStruct innerStruct
    }

We see that ``ContainerStruct`` has ``InnerStruct`` inside of it. To
create a validator for this case, we can use the following:

.. code:: python

     from manifold.validators import ThriftValidator, I16Field, StringField, StructField
    class InnerStructValidator(ThriftValidator):
        val = I16Field()


    class ContainerStructValidator(ThriftValidator):
        some_string = StringField()
        innerStruct = StructF

Note how since ``InnerStructValidator`` is also a ``ThriftValidator``,
that means we can use it on it’s own to validate *just*
``InnerStruct``\ s, but we can also chain validators together into more
complex entities. Back to the example, we can then check a
``ContainerStruct`` like so:

.. code:: python

    # Validators defined above

    # Create the structs
    inner_struct = new('InnerStruct', val=123)
    container = new('ContainerStruct', innerStruct=inner_struct, some_string='example')

    # Validate `container`
    validator = ContainerStructValidator(container)
    if not validator.is_valid():
        return validator.errors.items()  # Return errors as a dict

    # Continue doing things...

.. _Django Forms: https://docs.djangoproject.com/en/2.0/topics/forms/
.. _wiki on available fields: https://github.com/acv-auctions/manifold/wiki/Validation-Available-Fields
