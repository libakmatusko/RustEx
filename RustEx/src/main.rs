use std::io::stdin;

struct Automat{
    nodes: Vec<[u32; 26]>,
    starting: Vec<u32>,
    ending: Vec<bool>,
}

fn main() {
    let input=stdin();
    let mut string=String::new();

    input.read_line(&mut string).expect("error");
    println!("Hello, world!");
}
