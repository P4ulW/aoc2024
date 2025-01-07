use regex::Regex;
use std::fs;

fn load_file(filename: &str) -> String {
    let file = fs::read_to_string(filename).expect("unable to read file!");
    return file;
}

fn main() {
    let filename = "../inputs.txt";
    let reg_mul = Regex::new(r"mul\(\d+,\d+\)|do\(\)|don't\(\)?").unwrap();
    let file = load_file(filename);

    //let mut results = vec![];
    let mut sum = 0;
    let mut mul = true;
    for r in reg_mul.find_iter(&file).map(|m| m.as_str()) {
        let res = r;
        println!("{res}");
        if res.contains("mul") {
            let res = res.strip_prefix("mul(").unwrap();
            let res = res.strip_suffix(")").unwrap();
            let res: Vec<&str> = res.split(",").collect();
            println!("{}, {}", res[0], res[1]);
            let res: i32 = res[0].parse::<i32>().unwrap() * res[1].parse::<i32>().unwrap();
            if mul {
                sum += res;
            }
            println!("{res:?}");
        }

        if res.contains("do()") {
            mul = true;
        }

        if res.contains("don't()") {
            mul = false;
        }
    }
    println!("{sum}");
}
