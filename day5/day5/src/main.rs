use std::{collections::HashMap, fs};
#[derive(Debug)]
struct Ordering {
    left: i32,
    right: i32,
}

fn load_file(filename: &str) -> String {
    let file = fs::read_to_string(filename).expect("Opening file and reading to string");
    return file.trim().to_string();
}

fn orderings_from_file(file: &String) -> Vec<Ordering> {
    let mut orderings: Vec<Ordering> = Vec::new();

    for (_i, line) in file
        .split("\n\n")
        .nth(0)
        .unwrap()
        .split("\n")
        .into_iter()
        .enumerate()
    {
        let left_right: Vec<&str> = line.split("|").collect();
        let left: i32 = left_right[0].parse().expect("Integer");
        let right: i32 = left_right[1].parse().expect("Integer");
        let order = Ordering { left, right };
        orderings.push(order);
    }
    orderings
}

fn pages_from_file(file: &String) -> Vec<Vec<i32>> {
    let mut pages: Vec<Vec<i32>> = Vec::new();

    for (_i, line) in file
        .split("\n\n")
        .nth(1)
        .unwrap()
        .split("\n")
        .into_iter()
        .enumerate()
    {
        let mut page: Vec<i32> = vec![];
        let nums: Vec<&str> = line.split(",").collect();

        for num in nums.iter() {
            let num: i32 = num.parse().expect("Integer");
            page.push(num);
        }
        pages.push(page);
    }
    pages
}

fn check_ordering(page: &Vec<i32>, ordermap: &HashMap<i32, Vec<i32>>) -> (bool, Vec<i32>) {
    let mut seen_nums: Vec<i32> = Vec::new();

    for (_idx, num) in page.iter().enumerate() {
        let rules = match ordermap.get(num) {
            Some(v) => v,
            None => &Vec::<i32>::new(),
        };

        let mut violations = Vec::new();
        for num in seen_nums.iter() {
            let num_violations = rules.iter().map(|x| (x == num) as i32).sum();
            violations.push(num_violations);
        }

        if violations.iter().sum::<i32>() > 0 {
            return (false, violations);
        }
        //println!("{num} {rules:?}");
        seen_nums.push(*num);
    }
    (true, Vec::<i32>::new())
}

fn get_reordered_page(page: &Vec<i32>, ordermap: &HashMap<i32, Vec<i32>>, depth: i32) -> Vec<i32> {
    let mut reordered_page = page.clone();

    let (valid, violations) = check_ordering(&reordered_page, &ordermap);
    if valid {
        return reordered_page;
    }
    let swap_index = violations.len();
    let violation_index = violations.partition_point(|&x| x < 1);
    reordered_page[violation_index] = page[swap_index];
    reordered_page[swap_index] = page[violation_index];

    return get_reordered_page(&reordered_page, ordermap, depth + 1);
}

fn get_middle_number(numbers: &Vec<i32>) -> i32 {
    let middle_num = numbers[numbers.len() / 2];
    middle_num
}

fn main() {
    let filename = "../inputs.txt";
    let file = load_file(filename);
    let orderings = orderings_from_file(&file);
    let pages = pages_from_file(&file);

    let mut ordermap: HashMap<i32, Vec<i32>> = HashMap::new();

    for ordering in &orderings {
        let left = ordering.left;
        let right = ordering.right;
        //println!("l:{left}, r:{right}");
        let vec = ordermap.entry(left).or_insert(vec![]);
        vec.push(right);
        //println!("{vec:?}");
    }

    //println!("\nordermap:\n{ordermap:?}\n");

    let mut res = 0;
    for page in pages.iter() {
        //println!("page: {page:?}");
        let (valid, _idx) = check_ordering(&page, &ordermap);
        //println!("{valid} {idx:?}\n");
        if valid {
            res += get_middle_number(&page);
        }
    }
    println!("res part 1: {res}");

    let mut res = 0;
    for page in pages.iter() {
        //println!("page: {page:?}");
        let (valid, _idx) = check_ordering(&page, &ordermap);
        //println!("{valid} {idx:?}\n");
        if !valid {
            let reordered_page = get_reordered_page(&page, &ordermap, 0);
            res += get_middle_number(&reordered_page);
        }
    }
    println!("res part 2: {res}");
}
