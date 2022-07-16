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


  
  
