enum TrafficLight{
    Red,
    Green,
    Yellow,
}

pub trait TrafficTime {
    fn time(&self) -> u8;
}

impl TrafficTime for TrafficLight {
    fn time(&self) -> u8 {
        match &self {
            TrafficLight::Red => 30,
            TrafficLight::Green => 60,
            TrafficLight::Yellow => 10,
        }
    }
}

pub fn notify<T: TrafficTime>(item: &T){
    println!("{}", item.time());
}
    

fn main() {
    let light1 = TrafficLight::Red;
    notify(&light1);
    
    let light2 = TrafficLight::Green;
    notify(&light2);
    
    let light3 = TrafficLight::Yellow;
    notify(&light3);
    
}
