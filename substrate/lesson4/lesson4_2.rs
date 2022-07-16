example1:
fn main() {
    let s1 = String::from("hello");
    let s2 = s1.clone();
    println!("s1 = {}, s2 = {}", s1, s2);
}

example2:
fn main() {
    let x = vec![1,2];
    let y = x;
//    println!("y: {:?}",y);
    println!("y: {:?}",y);
}

example3:
fn main() {
    let my_string = String::from("hello world");
    let word = first_word(&my_string[..]);
    println!("result: {}", word);
}

fn first_word(s: &str) -> &str {
    let bytes = s.as_bytes();
    
    for( i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return &s[0..i];
        }
    }
    
    &s[..]
}


