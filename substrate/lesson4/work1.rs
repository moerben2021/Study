enum TrafficLight{
    Red,
    Green,
    Yellow,
}

fn timeInLight(light: TrafficLight) -> u8 {
    match light {
        TrafficLight::Red => 30,
        TrafficLight::Green => 60,
        TrafficLight::Yellow => 10,
    }
}
fn main() {
    let light1 = TrafficLight::Red;
    let time1 = timeInLight( light1 );
    println!("time is: {}", time1);
    
    let light2 = TrafficLight::Green;
    let time2 = timeInLight( light2 );
    println!("time is: {}", time2);
    
    let light3 = TrafficLight::Yellow;
    let time3 = timeInLight( light3 );
    println!("time is: {}", time3);
}
