struct ExampleStruct {
    1: string test_string,
    2: bool test_bool = true
}

struct InnerStruct {
    1: string some_string
}

struct ContainedStruct {
    1: i16 val,
    2: InnerStruct innerStruct
}

service ExampleService {

}
