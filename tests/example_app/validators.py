from manifold.validators import ThriftValidator, StringField, StructField,\
                                I16Field


class InnerStructValidator(ThriftValidator):

    val = I16Field(required=True)


class ComplexValidator(ThriftValidator):

    innerStruct = StructField(InnerStructValidator)

    some_string = StringField()
