use std::io::stdin;

struct Automat{
    nodes: Vec<[u32; 26]>,
    starting: Vec<u32>,
    ending: Vec<bool>,
}



fn main() {
    let input=stdin();
    let mut string=String::new();
    let mut regex=String::new();
    // a|b    or
    // a*     iterator
    // a?     0 alebo raz
    // a+     minimalne raz
    // ()
    // .      hocijaky znak
    input.read_line(&mut regex).expect("error");
    input.read_line(&mut string).expect("error");
    println!("Hello, world!");
}
