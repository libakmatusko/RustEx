use std::io::stdin;

struct Automat{
    nodes: Vec<[u32; 26]>,
    starting: Vec<u32>,
    ending: Vec<bool>,
}

struct Strom {
    hodnota: char, // pokial ' ' tak to nie je list
    operator: char,
    listy: Vec::<Strom>,
}

fn or_parser(regex:&str) -> Strom {
    println!("{}", regex);
    let mut sub_regex = Vec::new();
    let mut zatvorky = 0;
    let mut zaciatok = 0;
    for (i, c) in regex.char_indices() {
        match c {
            "(" => {zatvorky += 1},
            ")" => {zatvorky -= 1},
            "|" => {
                if zatvorky == 0 {
                    join_parser(regex[zaciatok::i]);
                    zaciatok = i+1;
                }
            },
            _ => {},
        }
        if zatvorky == 0 {
            join_parser(regex[zaciatok::i+1]);
            zaciatok = i+1;
        }
    };

    let mut s = Strom {
        hodnota: ' ';
        operator: '|';
        listy: ![]
    };
    return s
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

    let _Strom = or_parser(&regex);
    println!("Hello, world!");
}
