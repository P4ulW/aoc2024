use std::collections::HashMap;
use std::fs;
fn load_inputs(filename: &str) -> String {
    let file = fs::read_to_string(filename).expect("Could not read file");
    return file;
}

fn main() -> () {
    let filename = "./inputs.txt";

    let file = load_inputs(filename);
    println!("{file}");

    let mut left_list: Vec<i32> = Vec::new();
    let mut right_list: Vec<i32> = Vec::new();

    for line in file.lines() {
        for (i, number_str) in line.split_whitespace().enumerate() {
            match i {
                0 => left_list.push(number_str.parse().unwrap()),
                1 => right_list.push(number_str.parse().unwrap()),
                _ => continue,
            }
        }
    }

    left_list.sort();
    right_list.sort();

    //println!("{left_list:?}");
    //println!("{right_list:?}");

    let mut sum: u32 = 0;
    for (i, num) in left_list.iter().enumerate() {
        sum += (num - right_list[i]).abs() as u32;
    }
    println!("result part 1: {sum}\n");

    let mut occurences: HashMap<i32, u32> = HashMap::new();
    for num in right_list.iter() {
        //println!("{num}");
        //occurences.insert(*num, 1);
        match occurences.get(num) {
            Some(val) => occurences.insert(*num, val + 1),
            None => occurences.insert(*num, 1),
        };
    }
    //println!("{occurences:?}");

    let mut sum: u32 = 0;
    for num in left_list.iter() {
        //println!("{num}");
        match occurences.get(num) {
            Some(val) => sum += val * *num as u32,
            None => sum += 0,
        }
    }

    println!("result part 2: {sum}\n");

    return;
}
