use std::fs;

fn load_file(filename: &str) -> String {
    let file = fs::read_to_string(filename).expect("Error reading file");
    file
}

fn check_report(report: Vec<&str>) -> bool {
    //println!("{report:?}");
    let mut prev: i32 = report[0].parse().unwrap();
    let mut ordering = 0;

    for num in &report[1..] {
        let current_num: i32 = num.parse().unwrap();
        let difference = current_num - prev;
        //println!("{prev} {current_num} {difference}");

        if difference == 0 {
            return false;
        }
        if difference.abs() > 3 {
            return false;
        }

        let current_sign = difference / difference.abs();

        if ordering == 0 {
            ordering = current_sign;
        }
        if current_sign != ordering {
            return false;
        }

        prev = current_num;
    }
    return true;
}

fn check_report_dampened(report: Vec<&str>) -> bool {
    for (i, _) in report.iter().enumerate() {
        let mut damped_report: Vec<&str> = Vec::new();

        for (j, num) in report.iter().enumerate() {
            if i == j {
                continue;
            }
            damped_report.push(num);
        }
        //println!("{damped_report:?}");
        if check_report(damped_report) {
            return true;
        }
    }
    //println!("report {report:?} is unsafe");
    return false;
}

fn main() {
    let filename = "./inputs.txt";
    let file = load_file(filename);
    let mut reports = Vec::new();
    for line in file.trim().split("\n") {
        reports.push(line)
    }

    let mut res = 0;
    for report in reports.iter() {
        let report: Vec<&str> = report.split(" ").collect();
        //println!("{report:?}");
        //println!("{}\n", check_report(report));
        if check_report(report) {
            res += 1;
        }
    }
    println!("res par 1: {res}");

    let mut res = 0;
    for report in reports.iter() {
        let report: Vec<&str> = report.split(" ").collect();
        //println!("{report:?}");
        //println!("{}\n", check_report(report));
        if check_report_dampened(report) {
            res += 1;
        }
    }
    println!("res par 2: {res}");
}
