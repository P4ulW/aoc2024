use std::fs;

static XMAS: &'static str = "XMAS";
static SAMX: &'static str = "SAMX";

static MAS: &'static str = "MAS";
static SAM: &'static str = "SAM";

fn load_file(filename: &str) -> String {
    let file = fs::read_to_string(filename).unwrap();
    return file.trim().to_string();
}

fn check_lines_horizontal(lines: &Vec<&str>) -> i32 {
    let mut matches = 0;

    for line in lines {
        for i in 0..(line.len() - 3) {
            let pattern = &line[i..(i + 4)];
            if pattern == XMAS || pattern == SAMX {
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

            if pattern == XMAS || pattern == SAMX {
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

            if pattern == XMAS || pattern == SAMX {
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

            if pattern == XMAS || pattern == SAMX {
                matches += 1;
            }
        }
    }

    return matches;
}

fn check_xmax(lines: &Vec<&str>) -> i32 {
    let height = lines.len();
    let width = lines.first().unwrap().len();

    let mut matches = 0;

    for col in 0..(width - 2) {
        for row in 0..(height - 2) {
            let mut diag1 = String::new();
            let mut diag2 = String::new();
            for i in 0..3 {
                let char = lines[row + i].chars().nth(col + i).unwrap();
                diag1.push(char);

                let char = lines[row + i].chars().nth(col + 2 - i).unwrap();
                diag2.push(char);
            }

            if (diag1 == MAS || diag1 == SAM) && (diag2 == MAS || diag2 == SAM) {
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

    //part 1
    let mut matches = 0;
    matches += check_lines_horizontal(&lines);
    matches += check_lines_vertical(&lines);
    matches += check_lines_diagonal_pos(&lines);
    matches += check_lines_diagonal_neg(&lines);
    println!("res part 1: {matches}");

    //part 2
    let matches = check_xmax(&lines);
    println!("res part 2: {matches}");
}
