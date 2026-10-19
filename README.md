# Demos - Programming for the people
*Demos is a Greek term referring to the ruling body of free citizens in ancient Greek city-states (like Athens), and as such is the primary root of the word "democracy".* - [Wikipedia](https://en.wikipedia.org/wiki/Demos)

Demos is a language centered around 4 important values:
- The language must make programming easier and simpler
- The language must be fast to write
- The programmer is the priority
- The language can be compiled and interpreted

## What it means
The Demos programming language is not solely focused on a single paradigm, strictness or safety. Rather, it is focused on completing the most important duty of a programming language: making the programmer work less for more. Not only that, but it is also important that the language is fun to use. For those reasons, most features in this language are not about making professional-grade code, but rather making the code necessary to accomplish your goals shorter and tasty. What I mean by tasty, is that the code is to your taste. Yes, in Demos, you can choose how you write your code. Strict syntaxes are offputting for people of different taste, making a language unfun for those who strongly disagree with the syntax, regardless of the ease of use or features that the language provides. In Demos, apart from strictly necessary syntax like operators and such, most syntax provides alternatives that won't affect your code if you don't use them. Moreover, Demos combines multiple paradigms, because it is unreasonable to limit a language to a single way of thinking. Although, it is impossible to combine all paradigms together obviously.

## Examples
**C example**
```c
int main(void){
    int age;
    
    printf("Enter your age: ");
    scanf("%u", &age);

    printf("You are %d years old!\n");

    if(age < 18)
        printf("You are a minor\n");
    else if(age < 50)
        printf("You are %d years away from your midlife crisis\n", 50 - age);
    else
        printf("You are old and crinkly\n");
    
    return age;
}
```

**Demos equivalent**
```
fn main() : int {
    age : int
    input("Enter your age: {}", age)

    println("You are {} years old", age)

    // Optional indented blocks
    // Curly braces also work
    switch age:
        < 18:
            println("You are a minor")
        < 50:
            println("You are {} years away from your midlife crisis", 50 - age)
        else:
            println("You are old and crinkly")

    return age
}
```
As you can see, there are no semicolons, no fn or var keywords and also indented blocks. The indented blocks are optional; the default is {} like most languages.

**C++ example**
```c++
struct Shape {
    virtual int area() = 0;
    virtual int perimeter() = 0;
};

struct Box : Shape {
    int width, height;
    
    Box(int width, int height) : width(width), height(height) {}

    virtual int area() override {
        return this->width * this->height;
    }

    virtual int perimeter() override {
        return 2 * (this->width + this->height);
    }
};
```

**Demos equivalent**
```
// Abstract class
// poly = virtual, stands for polymorphic
abstract Shape = 
    abstract poly area() : int
    abstract poly perimeter() : int

// Child class of shape
class Box from Shape {
    pub:
    width, height : int

    // Both parameters are of type int
    ctor(width, height : int) =
        me.[width, height] = width, height
    
    // ovr = override
    ovr area() = width * height
    ovr perimeter() = 2 * (width + height)
}
```

**Rust example**
```rust
trait Animal {
    fn get_description(&self) -> String;
    fn make_sound(&self);
}

struct Dog<'a> {
    name : &'a str
}

impl Animal for Dog<'_> {
    fn get_description(&self) -> String {
        format!("Dog named {}", self.name)
    }
    
    fn make_sound(&self){
        println!("Woof Woof");
    }
}

struct Chihuahua<'a> {
    name : &'a str
}

impl Animal for Chihuahua<'_> {
    fn get_description(&self) -> String {
        format!("Dog named {}", self.name)
    }
    
    fn make_sound(&self){
        println!("Waf Waf Waf Waf Waf");
    }
}

fn main() {
    let dog = Dog{name: "Max"};
    println!("{}", dog.get_description());
    dog.make_sound();
    
    let chihuahua = Chihuahua{name: "Terry"};
    println!("{}", chihuahua.get_description());
    chihuahua.make_sound();
}
```

**Demos equivalent**
```
trait Animal {
    getter description : str
    make_sound() : none
}

class Dog =
    name : str

    trait Animal:
    // Types are already known, no need to repeat
    
    getter description = "Dog named {}".format(name)
    
    make_sound() =
        println("Woof Woof")

class Chihuahua from Dog =
    trait Animal:
    
    make_sound() =
        println("Waf Waf Waf")

fn main() {
    dog := Dog{"Max"}
    println("{}", dog.description)
    dog.make_sound()

    chihuahua = Chihuahua{"Terry"}
    println("{}", chihuahua.description)
    chihuahua.make_sound()
}
```

**Rust example**
```rust
#[derive(Debug)]
enum Value<'a> {
    Int(i64),
    Float(f64),
    Bool(bool),
    Char(char),
    Text(&'a str),
    None,
}

fn get_number(v: &Value) -> Option<f64> {
    match v {
        Value::Int(x) => Some(*x as f64),
        Value::Float(x) => Some(*x),
        _ => None,
    }
}

fn main() {
    let v = Value::Int(5);
    println!("v = {:?}", v);

    let result: Value = match v {
        Value::Int(x) => Value::Int(x + 10i64),
        Value::Float(x) => Value::Float(x / 5.2f64),
        Value::Bool(x) => Value::Bool(!x),
        Value::Char(x) => Value::Char(x),
        Value::Text(x) => Value::Text(x),
        Value::None => Value::Text("I have nothing to hide"),
    };
    println!("result = {:?}", result);

    let number = get_number(&v);
    if number.is_some() {
        println!("number = {}", number.unwrap());
    }
}
```

**Demos equivalent**
```
// Tagged union
type Value = i64 | f64 | bool | char | str | none

// format would have default implementation that would use
// the current value's implementation
trait format for Value {
    format(fmt) =
        fmt.write("{}({})", me.type.name, me.value)
}

get_number(v : Value &r) : f64? {
    match v {
        i64 | f64:
            ret (f64) v,
        else:
            ret none
    }
}

// To make get_number() a read-only property:
impl Value {
  getter number = get_number(me)
}

fn main() {
    v : Value = 5
    println("v = {}", v)

    result : Value
    match v {
        i64(x):
          result = x + 10
        f64(x):
          result = x / 5.2
        bool(x):
          result = not x
        char | text:
          result = v
        none:
          result = "I have nothing to hide"
    }
    println("result = {}", result)

    number := get_number(v)
    if number? {
        println("number = {}", number)
    }
}
```

## Varied and flexible syntax
```
// PlantUML-like class definition
class my_class {
    + x : int           // public
    # y : float         // protected
    - z : [int | float] // private

    ctor(x : int, y : float, z : [int | float]){
      self.[x, y, z] = x, y, z
    }
    
    + get_info() : str
    - get_private_info() : hashmap<int, float>
    + global get_global_info() : tuple<bool, str>
}

// is the same as
class MyClass {
    public x : int
    protected y : float
    private z : array<int | float>

    MyClass(x : int, y : float, z : array<int | float>){
        this.x = x
        this.y = y
        this.z = z
    }

    public getInfo() : str
    private getPrivateInfo() : hashmap<int, float>
    public static getGlobalInfo() : tuple<bool, str>
}

// and is the same as
class my_cls =
    pub x : int
    prot y : float
    priv z : [int | float]

    ctor(x, y, z) =
      me.[x, y, z] = x, y, z

    pub getter info : str
    priv getter priv_info : {int: float}
    pub global getter global_info : (bool, str)
```
Multiple ways of writing the same thing, essentially giving the programmer the freedom to write code as they want. Rest assured, if syntax can be rewritten in another way, that alternative will never be too strange to understand.

## Scope syntax
In the code shown above, it might seem confusing to see `{}`, `=` and `:` being used varyingly. Let me clear it up:
```
// For all declarative statements, so those
// who create or define something, like a
// function declaration, you can use either
// {} or =.

// For example:
fn my_func() = ...

// is the same as 
fn my_func(){ ... }

// But it's not correct to write
if condition = ...
// since an if statement does not create or define anything

// For the other statements, that are non-declarative,
// like if, for or while statements, you can use either
// {} or :.

// For example:
if condition: ...

// is the same as
if condition { ... }

// One thing that is important is that = and : are used
// for indented blocks, so when you use them, you need to
// make sure that every line inside the block has the same
// spacing from the start of the line.
```

## Basic types
- `i8`, `i16`, `i32` (aka `int`), `i64` : Signed integer types
- `u8`, `u16`, `u32` (aka `uint`), `u64` : Unsigned integer types
- `ssize`, `usize` : Signed and unsigned pointer sized integers
- `float` or `f32`, `double` or `f64` : Single / double precision floating point numbers
- `bool` : Boolean values (`true`/`yes` or `false`/`no`)
- `none` : Nothing (can only be given the value `none`)
- `str` : Allocated ASCII string
- `char` : ASCII character
- `wstr` : Allocated UTF-8 string
- `wchar` : UTF-8 codepoint (4 bytes big)
- `array` : Array list data structure (syntaxic sugar is `[element]`)
- ``
- `tuple` : Predefined sequence of types (syntaxic sugar is `(a, b, ...)`)
- `hashmap` : Hashmap data structure (syntaxic sugar is `{key, value}`)
- `union` : Tagged union (syntaxic sugar is `a | b | ...`)
- `option` : Optional value (syntaxic sugar is `type?`)
- `any` : For typeless pointers, arrays or variable arguments (`any*`).

*Note that integer types can also be written in the form of `int` / `uint` + the number of bits like `uint8` or `int64`.*

## OOP and traits (interfaces)
Object Oriented Programming is a controversial paradigm - for good reason. It is slow, restrictive and lacks some flexibility in most implementations. However, I think the devil is in the implementation, not the paradigm itself. Instead of avoiding the paradigm altogether, Demos's implementation of OOP is flexible and permissive. In addition, some shortcuts are given to the user to make OOP development less repetitive in encapsulation intensive situations. On the other hand, there is interfaces (also known as traits in Rust, which I think sounds better). Interfaces are very useful in a lot of situations, which is why it's surpising to see that many programming languages don't integrate them natively. For example, if we wanted to have a unified system to convert a value into an integer, we could create a `IntLike` trait that every value convertible to an integer could implement. For a language without traits, the equivalent would be to create a parent class that has all the necessary properties and methods. However, if our child class also needs to inherit from another class, we get multiple inheritance, which sucks and complexifies a simple problem. That is why interfaces are so important; avoiding multiple inheritance and giving us tools to make unified systems.

Almost every type in Demos is considered an *object*, so something that can have attributes, properties and methods. For example, a simple int may have a method `is_null()` to check if its value is 0. I think this is important, because any value of any type should be able to do what it's supposed to do without accessing anything outside. However, there is a catch. Only classes can have polymorphic abilities by themselves, because other types cannot afford to add a virtual pointer at the start of their data. For that reason, traits allow for many polymorphic-like practices to make that process easier. In addition, a non-class declared type (types that are "user-declared", like *structs*, *traits* or *enums*) can also use inheritance where possible.

Inherited attributes, properties and methods can be "deleted" (made unreachable from the child, but still usable from the parent). For example, if you were to create a 2D vector, that inherits from a 3D vector, and would want to remove the third component `z`, you could write `delete z` in the 2D vector's definition. Deleting a polymorphic method will remove its overhead when the child class will be used by itself or by its children.

"Wrappers" are surface level additions to a type, but that creates a new distinct type. For example, if we wanted to have a dedicated `hex` type for hexadecimal numbers, that only changes the way the number is printed, we could create a wrapper for the generic `int` type.

## Parametric types
Parametric types are types that need extra parameters to ensure correct or extended function. This is called type templates or generic types in other languages. For example, the `array`, `tuple`, `hashmap`, `union` and `option` types are parametric. Parametric types are often used for data structures that can hold any type. 

Using a parametric type follows this syntax: `type<a, b, ...>`. For example, an `array` that holds `bool`s is denoted as `array<bool>`. The `array` knows what type it holds via its parameter. Parametric types can also have a variable number of parameters, like the `union` and `tuple` types, which accepts any number of parameters, but must at least have one.


## Pointers and references
#### Pointers
A pointer is a memory address that contains data. For pointers, the "underlying type" of a pointer is the type of data inside the memory address that the pointer holds. Creating a pointer type follows this syntax `type *`, where `type` is the underlying type.

A pointer's main use is to be able to read / write a value you don't have direct access to. To access the value "pointed to" by the pointer, you use the dereference operator (`*`) like so: `*pointer`.

A pointer can also be "typeless" if necessary, if the underlying type is `any`. Typeless pointers can point to any type of data in memory, but that also means that the underlying data cannot be handled normally since it does not have a size.

To get the pointer of a value, but only if the value is actually contained in memory (i.e. is inside a variable or data structure), you can use the reference operator (`&`) like so: `&value`. In case you want to explicit permissions for a pointer, you can add `r`or `w` to make it read-only or  explicitly writable (is already writable by default) respectively.

A pointer's size depends on the architecture it will run on, but will always be the same size as `usize` and `ssize`. Never assume a pointer's size, for compatibility's sake.

*Examples:*
* `bool *r` : Read-only pointer to a `bool` (no writing allowed)
* `hashmap<int, bool>*` : Pointer to a `hashmap` with `int` keys and `bool` values
* `int *w` : Pointer to an explicitly written to `int`
```
my_var : int = 0
my_ptr : int* = &my_var
*my_ptr = 5
println("my_var = {}", *my_ptr)
// -> my_var = 5
```

*Note: Pointers in Demos point to only one value and cannot be used like arrays!*

#### References
A reference is a similar concept to a pointer, but is different in a few ways. First, a reference is a pointer in disguise, but if used in a function parameter, passing a variable as its value will automatically take its pointer. Second, it will act as a normal value, but will access the value it is currently pointing to. Third, the pointer behind the reference cannot be changed. Finally, a reference cannot be `nul`. Note that there are no typeless references in consequence of the second point; `any` does not have a size.

A reference type is created using the following syntax: `type &`. Like pointers, you can optionally append `r` or `w` after `&` to explicit permissions. Also, since a reference cannot be `nul`, you must declare its value on creation.

A reference is implicitly taken when its value is assigned. For example, in the example `my_ref : int& = my_var`, `my_ref` will automatically take the reference to `my_var`. Same thing applies to function arguments.

*Examples:*
* `int &w` : A reference to an explicitly written to `int`
* `bool&` : A reference to a `bool`
* `float &r` : A read-only reference to a `float`
```
fn add_one(count : int&) =
    count += 1

x := 1
add_one(x)
println("x = {}", x)
// -> x = 2
```

## Arrays
Arrays are useful for holding multiple values in a certain order. Arrays are contiguous blocks of memory treated as a bundle of multiple elements of the same type placed one after the other. An array is, under the hood, literally a pointer, but is treated differently. Arrays can be either fixed, of known size or of unknown size. Arrays can be of a single dimension, or of multiple dimensions (multidimensional array). Demos *should* support array-wide vectorized operations. An array's size is the number of elements it can hold at maximum capacity.

#### Fixed arrays
*Fixed arrays are actually stored as a solid memory block. So, assigning to a fixed array is copying data into it.*

Fixed arrays are the easiest to use. They hold a constant amount of elements, so they also have a constant size. A fixed array must hold elements of known size, so they should not hold `any` elements, because `any` does not have an actual size. Fixed arrays are passed in arguments as pointers behind the scenes, without providing their size since it is already known. A fixed array's size is accessed using `array.size`. If a fixed array is multidimensional, its size will be a tuple. You can also check if an index is in bounds using `array.in_bounds(index, ...)`, where additional indexes are to be provided in case of multi-dimensional arrays. Both of these can be evaluated at compile-time where possible.

**Examples:** 
- `int[64]` : *a fixed array of 64 integers.*
- `float*[16]` : *a fixed array of 16 pointers of floats.*
- `bool[10, 20]` : *a 10 rows x 20 columns array of booleans.*

#### Arrays of known size (aka slice)
*Arrays of known size (slices) are a bundle of a pointer + integers of pointer size. So assigning to a slice is changing its pointer and size.*

A slice would be an array that is not fixed size, but refers to a number of elements that we know of. But that number is not constant, so not necessarily known at compile-time. If the array holds elements of `any` type, the number of elements (size of the array) should be the number of bytes that the array takes up. Arrays of known size are passed in arguments as a pointer followed by the number of elements, in an integer of a pointer's size. Fixed arrays are automatically converted into a pair of pointer + size when passed as an array of known size. A slice's size is accessed using `slice.size`. If a slice is multi-dimensional, its size will be a tuple. You can also check if an index is in bounds is in bounds using `slice.in_bounds(index, ...)`, where additional indexes are to be provided in case of multi-dimensional arrays. Both of these can be evaluated at compile-time only if the slice is non-volatile and the size is already known.

Note that if an array of known size is two-dimensional or more, it will pass its size as a series of 2 or more integers of a pointer's size.

**Examples:**
- `int[:]` : *an array of known size of integers.*
- `float*[:]` : *an array of known size of pointers of floats.*
- `bool[:, 3]` : *an array of known rows x 3 columns of booleans.*

#### Arrays of unknown size (aka naive array)
*Arrays of unknown size are simply pointers. So assigning to naive array is to change value of the pointer.*

Arrays of unknown size are useful in cases where we hold memory that we do not know the size of, but have to handle. The catch with these mysterious arrays is that we cannot know if an index is in bounds (is inside the memory block), and therefore cannot catch any memory errors before they happen. The usual result is a terrifying `Segmentation fault`. **Use arrays of unknown size carefully, only when strictly necessary.** For example, when interacting explicitly with C code, arrays of unknown size will often need to be handled.
An array of unknown size is passed as an argument as a single pointer. These arrays cannot be passed / converted as arrays of fixed / known size. An array of unknown size can only be of one dimensions. Only in arrays of unknown size can `any` be used as the element type and will be the size of 1 byte exceptionally for ease of manipulation.

**Examples:**
- `int[]` : *an array of unknown size of integers.*
- `float*[]` : *a naive array of pointers of floats.*

#### Dynamic arrays (aka *vector* in C++, `array` type)
*Dynamic arrays are complex classes that represent an array that can grow according to its needs. Its memory is on the heap and it only holds a pointer to it. It will allocate memory when it is needed and free memory when it is no longer needed. So, assigning to a dynamic array might free memory and allocate new memory.*

Dynamic arrays are more complicated than the aforementionned ones, because it handles varying amounts of memory, without necessarily knowing how much it needs. However, its implementation is given by the standard library, so don't sweat to much. It is represented by the built-in `array` type. Dynamic arrays have a size and capacity. Size is the current number of elements, capacity is the maximum number of elements that the data-structure can hold. 

Dynamic arrays can be multi-dimensional, but the number of dimensions must remain constant. Dynamic arrays are 1D by default. When multi-dimensional, their size is represented as an array of integers, where each number is the number of rows, columns, etc. Indexing a dynamic array is the same as fixed arrays and slices.

**Examples:**
- `array<int>` : *a dynamic array of integers.*
- `array<float*>` : *a dynamic array of pointers of floats.*
- `array<float, 2>` : *a dynamic 2D array of floats.*
- `[float]` : *a dynamic array of floats, but written in syntaxic sugar.*
- `[float, 2]` : *a dynamic 2D array of floats, but written in syntaxic sugar.*

#### Array indexing, slicing and operations
Arrays can be handled in very cool and efficient ways in Demos. Long gone are the days of tedious for loops and pointer math. The programmer will be impressed when he can do a bunch of things in a single line. This is the Demos programming language's time to shine.

Firstly, array indexing adheres to the Python list indexing: arrays start at index `0` and negative indices are evaluated as `array.size + i`. So, for example, `array[-4]` is the same as `array[array.size - 4]`. The greater part of the standard library also follows these indexing conventions.

Secondly, slicing lets you take a part of an array and use it as a single block. For example, if we want to pass only the 5 first elements of an array in a function, we could write: `array[:5]`. If we wanted the elements from index 2 to 10 we could write: `array[2:11]` (the second index is excluded). Negative indexes can also be used to create slices. Slicing results in an array of known size. Slicing in multiple dimensions is a little bit different:
`array[:, :3]` gives us a slice of all rows, but with only the first 3 columns. `array[0, :]` or `array[0]` gives us the first row of the array. `array[2:-1, :-3]` gives us the second and following rows except the last one, with each excluding the last 3 rows.

Finally, array operations can be divided into 3 categories: arithmetic, repetition and restructuring.

- Arithmetic operations are usually repeated operations done on large amounts of data. For example, adding a row to another row looks like: `array[0, :] + array[1, :]`. These operations will give fixed arrays if the sizes of the data handled is known, otherwise, either a dynamic array will be automatically created using the required amount of data or a small amount of stack memory will be allocated if the number of elements is low. If the result of arithmetic is directly stored into a fitting array, the operations will preferably be done in-place to reduce memory usage. Usually, arithmetic is done with numbers, but any object types capable of compatible operations will be fit. For more powerful usage of indexing, it is possible to also use the `::` operator, which will iterate through all included indices. So, `array1[1:-1:, :] += array2` will go through all rows except the first and last ones and will add array2 to each one. By default, the iteration will be done for all indices in the range. When a third value is introduced, the operator iterates through the indices with a specified step (default is 1). `array[-1::-1]` will step through all elements, but in reverse order.

- Repetition is doing a bunch of operations on all elements, like calling a function for each element, where the element is an argument. For example, if we have an array of type `str[256]` and we want to replace the word `hello` with `bye` in each element, instead of using a pesky for loop with iterators and whatnot, we can use `array[:].replace("hello", "bye")`. It is pretty useful. Note that if the method, attribute or property of the elements is the same as one provided by the array itself, the array will have the priority.

- Restructuring is making a new array from other arrays by gluing them together. For example, if we want to put together a 100 element array and a 99 x 100 array, we could do `array1 _> array2`. The `_>` operator acts as a "join underneath" operator and will add array1 as the final row of array2 in the result. The opposite operation, "join on top", is represented with the operator `^>`. Furthermore, there is also "join horzontally", represented by `><` (like sticking stuff together). Joining a 1D array with a 2D array will treat it as a column. There is also the transpose operator, `^T`, which rearranges the matrix horizontally and vertically. For example, a 100x200 matrix transposed gives us a 200x100 matrix. These operations are very useful for 2D arrays, but for more dimensions, these operators are rather useless. Instead, methods are provided with additional parameters and details.

## Structures
Structures are basic data structures where all members are public. They cannot use polymorphism, but can use basic inheritance. Like Rust, they can have methods and implement traits. That's pretty much all they can do, and their simplicity is intentional. A struct can provide a constructor, but not a destructor. They can provide operator overloads as well. Properties are not allowed.

```
struct Vehicle {
    name : str
    speed : float = 0.0 // m/s
    registration : LicensePlate? = none
    price : uint64 // USD

    ctor(name, speed, price) =
        me.[name, speed, price] = name, speed, price
        me.registration = none 
}

struct Engine {
    cylinders : u16
    displacement : float // L
    turbo : bool = no

    is_legal() : bool = not turbo
}

fn search_car(name : str, brand : CarBrand) : (uint64, float, Engine)

struct Car from Vehicle {
    brand : CarBrand
    engine : Engine
    windows_tinted : bool = no

    is_legal() : bool =
        engine.is_legal() and registration? and not windows_tinted
    
    ctor(name, brand, registration) =
        me.[name, brand, registration] = name, brand, registration
        me.[price, speed, engine] = search_car(name, brand)
}
```

## One-liner utilities
A one-liner master is someone that appreciates the complexity of what you can do in a single line of code. For languages like Python, where a line is limited and a strict building block, a one-liner-slinger will know when their chance is there. There are tales of a one-line slinger from the North, that has furnished and finished a functional singular line of code capable of running the entire game of life in Python. That greatness is to be expected for every Demos user, because this language makes one-line-slinging easier than ever. Firstly, methods on a single object can be chained:
```
// : calls the method, drops the return and keeps the object instead
my_form:fill_name("DioDogHater"):fill_status("Unemployed").sign()

// can be used to call a method, then return the object itself
println("My form with a fake name: {}", my_form:fill_name("Quandale"))

// ; calls the method, keeps the return in a tuple, but reuses the object
name, status = my_form;get_name();get_status().archive()
```
Now, I know the code is not very readable since these operators are usually used differently, but to be fair, if you're a one-line freak, you don't care about code clarity. Well, the operator isn't that confusing either; just remember what they're used for and you'll be alright.

Similarly, we can also chain attribute / property modification:
```
// Like in Python, but no need to repeat the object multiple times
my_form.[name, status, archived] = "DioDogHater", "Unemployed", true

// Another way of doing it:
my_form[.name = "DioDogHater", .status = "Unemployed", .archived = true]

// Doing the same operation on multiple attributes / properties
my_form.[age, networth, life_expenctancy] *= 2

// Or you could also just "reinitialize" the object
// (keeps the other members intact)
my_form = {
  phone_number = "123-4567",
  address = "1234 Programming Rd, Listenburg"
}

// But, if you want to use my_form later
// (like if you wanted to print it after modifying it)
println("My completed form: {}", (my_form = {completed = true}))
```
Now, what you've seen in the last part is exactly what I'm about to show next:
creating or assigning to a variable inside an expression.
```
pi := 1.25 // wrong!

println("pi = {}", (pi = 3.1415))
// Whew, saved at the last moment

println("x = {}", (x := 220))
println("x * 2 = {}", x * 2)
println("x /= 10", (x /= 10))
// Wow, what's my x doing here?
```
Cool, right? Now, what about some more array stuff? Let's add more array stuff in there just in case you nerds complain.
```
// Create an array with a for loop (like in Python)
my_array := [x for x in 0..100 if x % 2 == 0] // even numbers in [0, 99]
// or
my_array = [x for x = 0; x < 100; x++ if x % 2 == 0]

// Create an array of powers of 2
two_powers = [2**i for i in 1..=64] // from 2^1 to 2^64

// Create an array with a range
my_range := [0..=100] // 0 to 100

// Create a 2D array based on their indices
my_matrix := [[i * j for i in 0..16] for j in 0..16]
```
Now, what if we wanted to generate elements of an array that depend on the last elements?
```
// Normally, _ is like a trash bin, where a value is discarded.
// However, _ is the current structure we are defining in this case.
my_array := [1, 2, 3, x - _[-1] for 0..10]

// Fibonacci sequence, in an array expression?
fibo := [0, 1, _[-1] + _[-2] for 0..10]

// So for example, let's create a structure
@optimize // rearranges the structure to minimize padding
struct integers {
  a : i32
  b : i64
  c : i8
}

// 1e6 = 1 * 10^6
x := integers{a = 1e6, b = _.a / 2, c = _.a & 0xFF}
```
We can also do some cool things with loops:
```
// Count number of digits in x
x := 1510232
digits := count for i = x; i > 0; i /= 10

// Sum all even numbers between 0 and 100
even_sum := sum x for x in 0..=100 if x % 0 == 0

// Get the factorial of 5
// Multiply all whole numbers under 5 and above 0 to 5
five_facto := mult x for x in 1..=5
```