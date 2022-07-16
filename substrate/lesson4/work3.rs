enum ShapeEnum{
    CIRCLE,
    TRIANGLE,
    RECTANGLE,
}

pub trait ShapeArea {
    fn area(&self) -> f64;
}

impl ShapeArea for ShapeEnum {
    fn area(&self) -> f64 {
        match &self {
            ShapeEnum::CIRCLE => 30.0,
            ShapeEnum::TRIANGLE => 60.0,
            ShapeEnum::RECTANGLE => 10.0,
        }
    }
}

pub fn notify<T: ShapeArea>(item: &T){
    println!("{}", item.area());
}
    

fn main() {
    let shape1 = ShapeEnum::RECTANGLE;
    notify(&shape1);
    
}
