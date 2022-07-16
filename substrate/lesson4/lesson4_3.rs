1
struct Point<T>{
    x:T,
    y:T,
}

impl<T> Point<T>{
    fn x(&self) -> &T {
        &self.x
    }
}

fn main() {
    let integer = Point{ x:5, y:10 };
    let float = Point{ x:1.0, y:4.0 };
}


2
fn main() {
    let number_list = vec![34, 50, 25, 100, 65];
    let result = largest(&number_list);
    println!("The largest number is {}", result);
    
    let char_list = vec!['y','m', 'a', 'q'];
    let result = largest(&char_list);
    println!("The largest char is {}", result);
}

fn largest<T: PartialOrd>(list: &[T]) -> &T {
    let mut largest = &list[0];
    
    for item in list {
        if item > largest {
            largest = item;
        }
    }    
    largest
}

3
fn main() {
    let tweet = Tweet {
        author: String::from("Kaichao"),
        text: String::from("hello world"),
    };
    
    notify( &tweet );
}

pub trait Summary {
    fn summarize(&self) -> String;
}

struct Tweet {
    author: String,
    text: String,
}

impl Summary for Tweet {
    fn summarize(&self) -> String {
        return format!("{}, {}", self.author, self.text);
    }
}

pub fn notify<T: Summary>(item: &T) {
    println!("{}", item.summarize());
}


