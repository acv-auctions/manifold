struct ExampleStruct {
    1: string test_string,
    2: bool test_bool = true
}

struct InnerStruct {
    1: i16 val
}

struct ContainedStruct {
    1: string some_string,
    2: InnerStruct innerStruct
}

service ExampleService {

}
