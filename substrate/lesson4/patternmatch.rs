fn main() {
    let five = Some(5);
    let six = five.map(|i| i+1);
    println!("six: {:?}",six);
    
    let none: Option<i32> = None;
    let none_result = none.map(|i| i+1);
    println!("none: {:?}", none_result);
}
