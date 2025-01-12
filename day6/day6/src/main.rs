use std::fs;

fn load_file(filename: &str) -> String {
    let file = fs::read_to_string(filename).expect("Valid File");
    return file.trim().to_string();
}

fn main() {
    let filename = "../test_inputs.txt";
    let file = load_file(filename);
    let map: Vec<&str> = file.split("\n").collect();
    let mut warehouse: Vec<Vec<i32>> = Vec::new();
    for line in map.iter() {
        let mut converted_line: Vec<i32> = vec![];
        for char in line.chars() {
            let x = match char {
                '.' => 0,
                '#' => 1,
                '^' => 2,
                _ => -1,
            };
            converted_line.push(x);
        }
        warehouse.push(converted_line);
    }
    println!("{map:?}");
    println!("{warehouse:?}");
}
