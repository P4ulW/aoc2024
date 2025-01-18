use std::{collections::HashMap, fs};

fn load_file(filename: &str) -> String {
    let file = fs::read_to_string(filename).expect("Valid File");
    return file.trim().to_string();
}

fn get_guard_pos(warehouse: &Vec<Vec<i32>>) -> Option<(i32, i32)> {
    for (r, row) in warehouse.iter().enumerate() {
        for (c, num) in row.iter().enumerate() {
            if *num == 2 {
                return Some((r as i32, c as i32));
            }
        }
    }
    None
}

fn is_out_of_bounds(row: i32, col: i32, warehouse: &Vec<Vec<i32>>) -> bool {
    if row < 0 || col < 0 {
        return true;
    }
    let height = warehouse.len() as i32;
    let width = warehouse[0].len() as i32;
    if col >= height || row >= width {
        return true;
    }
    false
}

fn is_box(row: i32, col: i32, warehouse: &Vec<Vec<i32>>) -> bool {
    if warehouse[row as usize][col as usize] == 1 {
        return true;
    } else {
        false
    }
}

fn rotate_direction(direction: (i32, i32)) -> (i32, i32) {
    return (direction.1, -direction.0);
}

fn main() {
    let filename = "../inputs.txt";
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

    let (mut row, mut col) = get_guard_pos(&warehouse).expect("Guard on board");
    let mut direction = (-1, 0);
    let mut visited: HashMap<(i32, i32), i32> = HashMap::new();
    loop {
        let mut num_visited = *visited.entry((row, col)).or_insert(0);
        num_visited += 1;
        visited.insert((row, col), num_visited);
        let (next_row, next_col) = (row + direction.0, col + direction.1);
        if is_out_of_bounds(next_row, next_col, &warehouse) {
            break;
        }
        if is_box(next_row, next_col, &warehouse) {
            //println!("There is a box at {next_row},{next_col}");
            direction = rotate_direction(direction);
            continue;
        }
        (row, col) = (next_row, next_col);
    }
    println!("sol part 1: {}", visited.len());
    //println!("{visited:?}");

    //part 2
    let mut loop_positions = Vec::<(i32, i32)>::new();
    for (obstacle_row, obstacle_col) in visited.keys() {
        let (mut row, mut col) = get_guard_pos(&warehouse).expect("Guard on board");
        let mut direction = (-1, 0);
        if (row, col) == (*obstacle_row, *obstacle_col) {
            //println!("skipped start pos!");
            continue;
        }

        //println!("placing obstacle at {obstacle_row} {obstacle_col}");
        let mut temp_warehouse = warehouse.clone();
        temp_warehouse[*obstacle_row as usize][*obstacle_col as usize] = 1;
        let mut temp_visited: HashMap<(i32, i32), i32> = HashMap::new();

        loop {
            let mut num_visited = *temp_visited.entry((row, col)).or_insert(0);
            num_visited += 1;
            if num_visited > 4 {
                //println!("found loop");
                loop_positions.push((*obstacle_row, *obstacle_row));
                break;
            }
            temp_visited.insert((row, col), num_visited);

            let (next_row, next_col) = (row + direction.0, col + direction.1);
            if is_out_of_bounds(next_row, next_col, &temp_warehouse) {
                break;
            }

            if is_box(next_row, next_col, &temp_warehouse) {
                //println!("There is a box at {next_row},{next_col}");
                direction = rotate_direction(direction);
                continue;
            }

            (row, col) = (next_row, next_col);
        }
    }
    println!("sol part 2: {}", loop_positions.len());

    //println!("{row} {col}");
    //println!("{map:?}");
    //println!("{loop_positions:?}");
    //println!("{warehouse:?}");
}
