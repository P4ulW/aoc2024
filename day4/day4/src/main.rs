use std::fs;

static TARGET: &'static str = "XMAS";
static TARGET_REV: &'static str = "SAMX";

fn load_file(filename: &str) -> String {
    let file = fs::read_to_string(filename).unwrap();
    return file.trim().to_string();
}

fn check_lines_horizontal(lines: &Vec<&str>) -> i32 {
    let mut matches = 0;

    for line in lines {
        for i in 0..(line.len() - 3) {
            let pattern = &line[i..(i + 4)];
            if pattern == TARGET || pattern == TARGET_REV {
                matches += 1;
            }
        }
    }
    return matches;
}

fn check_lines_vertical(lines: &Vec<&str>) -> i32 {
    let height = lines.len();
    let width = lines.first().unwrap().len();

    let mut matches = 0;

    for col in 0..width {
        for row in 0..(width - 3) {
            let mut pattern = String::new();
            for i in 0..4 {
                let char = lines[row + i].chars().nth(col).unwrap();
                pattern.push(char);
            }

            if pattern == TARGET || pattern == TARGET_REV {
                matches += 1;
            }
        }
    }

    return matches;
}

fn check_lines_diagonal_pos(lines: &Vec<&str>) -> i32 {
    let height = lines.len();
    let width = lines.first().unwrap().len();

    let mut matches = 0;

    for col in 0..(width - 3) {
        for row in 0..(height - 3) {
            let mut pattern = String::new();
            for i in 0..4 {
                let char = lines[row + i].chars().nth(col + i).unwrap();
                pattern.push(char);
            }

            if pattern == TARGET || pattern == TARGET_REV {
                matches += 1;
            }
        }
    }

    return matches;
}

fn check_lines_diagonal_neg(lines: &Vec<&str>) -> i32 {
    let height = lines.len();
    let width = lines.first().unwrap().len();

    let mut matches = 0;

    for col in 3..(width) {
        for row in 0..(height - 3) {
            let mut pattern = String::new();
            for i in 0..4 {
                let char = lines[row + i].chars().nth(col - i).unwrap();
                pattern.push(char);
            }

            if pattern == TARGET || pattern == TARGET_REV {
                matches += 1;
            }
        }
    }

    return matches;
}

fn main() {
    let filename = "../inputs.txt";
    let file = load_file(filename);
    let lines: Vec<&str> = file.split("\n").map(|c| c).collect();

    let mut matches = 0;
    matches += check_lines_horizontal(&lines);
    matches += check_lines_vertical(&lines);
    matches += check_lines_diagonal_pos(&lines);
    matches += check_lines_diagonal_neg(&lines);
    println!("{matches}");
}
