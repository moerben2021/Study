

fn main() {
    let number_list = vec![34, 50, 25, 100, 65];
    let result = sum(&number_list);
    println!("The largest number is {}", result);
    
}


fn sum(list: &[u32]) -> Option(u32){
    let mut total = &list[0];
    for item in list {
        total += item;
    }
    Some(total)
    
}
