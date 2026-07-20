//! Fixed-width toy backend for the P5.4 p=11 SvdW suite.
//!
//! This is an auditable experiment, not a production cryptographic library.

const P: u64 = 11;

#[repr(C)]
#[derive(Clone, Copy, Debug)]
pub struct Point {
    pub x: u64,
    pub y: u64,
    pub infinity: u64,
}

#[inline(always)]
fn ct_eq(left: u64, right: u64) -> u64 {
    let difference = left ^ right;
    ((difference | difference.wrapping_neg()) >> 63) ^ 1
}

#[inline(always)]
fn cmov(false_value: u64, true_value: u64, selector: u64) -> u64 {
    let mask = 0_u64.wrapping_sub(selector);
    false_value ^ (mask & (false_value ^ true_value))
}

#[inline(always)]
fn point_cmov(false_value: Point, true_value: Point, selector: u64) -> Point {
    Point {
        x: cmov(false_value.x, true_value.x, selector),
        y: cmov(false_value.y, true_value.y, selector),
        infinity: cmov(false_value.infinity, true_value.infinity, selector),
    }
}

#[inline(always)]
fn fadd(left: u64, right: u64) -> u64 {
    (left + right) % P
}

#[inline(always)]
fn fsub(left: u64, right: u64) -> u64 {
    (left + P - right) % P
}

#[inline(always)]
fn fneg(value: u64) -> u64 {
    (P - value) % P
}

#[inline(always)]
fn fmul(left: u64, right: u64) -> u64 {
    (left * right) % P
}

#[inline(always)]
fn fsquare(value: u64) -> u64 {
    fmul(value, value)
}

#[inline(always)]
fn fpow(value: u64, exponent: u64) -> u64 {
    let mut result = 1_u64;
    for bit_index in (0..64).rev() {
        result = fsquare(result);
        let multiplied = fmul(result, value);
        result = cmov(result, multiplied, (exponent >> bit_index) & 1);
    }
    result
}

#[inline(always)]
fn inv0(value: u64) -> u64 {
    fpow(value, P - 2)
}

#[inline(always)]
fn is_square(value: u64) -> u64 {
    ct_eq(value, 0) | ct_eq(fpow(value, (P - 1) / 2), 1)
}

#[inline(always)]
fn fsqrt(value: u64) -> u64 {
    fpow(value, (P + 1) / 4)
}

#[inline(always)]
fn curve_rhs(x: u64) -> u64 {
    fadd(fmul(fsquare(x), x), 1)
}

/// RFC 9380 Appendix F.1 with compile-time E: y^2=x^3+1 and Z=1.
#[unsafe(no_mangle)]
#[inline(never)]
pub extern "C" fn map_svdw_p11(input: u64) -> Point {
    let u = input % P;
    let z = 1_u64;
    let gz = curve_rhs(z);
    let numerator = fadd(fmul(3, fsquare(z)), 0);
    let c2 = fneg(fmul(z, inv0(2)));
    let mut c3 = fsqrt(fneg(fmul(gz, numerator)));
    c3 = cmov(c3, fneg(c3), c3 & 1);
    let c4 = fneg(fmul(fmul(4, gz), inv0(numerator)));

    let tv1_initial = fmul(fsquare(u), gz);
    let tv2 = fadd(1, tv1_initial);
    let tv1 = fsub(1, tv1_initial);
    let tv3 = inv0(fmul(tv1, tv2));
    let tv4 = fmul(fmul(fmul(u, tv1), tv3), c3);
    let x1 = fsub(c2, tv4);
    let gx1 = curve_rhs(x1);
    let e1 = is_square(gx1);
    let x2 = fadd(c2, tv4);
    let gx2 = curve_rhs(x2);
    let e2 = is_square(gx2) & (e1 ^ 1);
    let x3_base = fmul(fsquare(tv2), tv3);
    let x3 = fadd(fmul(fsquare(x3_base), c4), z);
    let gx3 = curve_rhs(x3);
    let x = cmov(cmov(x3, x1, e1), x2, e2);
    let gx = cmov(cmov(gx3, gx1, e1), gx2, e2);
    let mut y = fsqrt(gx);
    y = cmov(fneg(y), y, ct_eq(y & 1, u & 1));
    Point { x, y, infinity: 0 }
}

/// Exception-complete masked affine addition for valid points on this curve.
#[unsafe(no_mangle)]
#[inline(never)]
pub extern "C" fn point_add_complete_p11(left: Point, right: Point) -> Point {
    let dx = fsub(right.x, left.x);
    let dy = fsub(right.y, left.y);
    let generic_slope = fmul(dy, inv0(dx));
    let generic_x = fsub(fsub(fsquare(generic_slope), left.x), right.x);
    let generic_y = fsub(fmul(generic_slope, fsub(left.x, generic_x)), left.y);
    let generic = Point { x: generic_x, y: generic_y, infinity: 0 };

    let double_numerator = fmul(3, fsquare(left.x));
    let double_denominator = fmul(2, left.y);
    let double_slope = fmul(double_numerator, inv0(double_denominator));
    let double_x = fsub(fsquare(double_slope), fmul(2, left.x));
    let double_y = fsub(fmul(double_slope, fsub(left.x, double_x)), left.y);
    let doubled = Point { x: double_x, y: double_y, infinity: 0 };
    let infinity = Point { x: 0, y: 0, infinity: 1 };

    let same_x = ct_eq(left.x, right.x);
    let same_y = ct_eq(left.y, right.y);
    let left_y_nonzero = ct_eq(left.y, 0) ^ 1;
    let use_double = same_x & same_y & left_y_nonzero;
    let use_infinity = same_x & (use_double ^ 1);
    let mut result = point_cmov(generic, doubled, use_double);
    result = point_cmov(result, infinity, use_infinity);
    result = point_cmov(result, right, left.infinity);
    point_cmov(result, left, right.infinity)
}

#[unsafe(no_mangle)]
#[inline(never)]
pub extern "C" fn hash_field_pair_p11(u0: u64, u1: u64) -> Point {
    let q0 = map_svdw_p11(u0);
    let q1 = map_svdw_p11(u1);
    let sum = point_add_complete_p11(q0, q1);
    let twice = point_add_complete_p11(sum, sum);
    point_add_complete_p11(twice, twice)
}

fn run_tables() {
    println!("kind,left,right,x,y,infinity");
    for u in 0..P {
        let point = map_svdw_p11(u);
        println!("map,{u},0,{},{},{}", point.x, point.y, point.infinity);
    }
    for u0 in 0..P {
        for u1 in 0..P {
            let point = hash_field_pair_p11(u0, u1);
            println!("hash,{u0},{u1},{},{},{}", point.x, point.y, point.infinity);
        }
    }
    let points = [
        Point { x: 0, y: 1, infinity: 0 },
        Point { x: 0, y: 10, infinity: 0 },
        Point { x: 2, y: 3, infinity: 0 },
        Point { x: 2, y: 8, infinity: 0 },
        Point { x: 5, y: 4, infinity: 0 },
        Point { x: 5, y: 7, infinity: 0 },
        Point { x: 7, y: 5, infinity: 0 },
        Point { x: 7, y: 6, infinity: 0 },
        Point { x: 9, y: 9, infinity: 0 },
        Point { x: 9, y: 2, infinity: 0 },
        Point { x: 10, y: 0, infinity: 0 },
        Point { x: 0, y: 0, infinity: 1 },
    ];
    for left in 0..points.len() {
        for right in 0..points.len() {
            let point = point_add_complete_p11(points[left], points[right]);
            println!("add,{left},{right},{},{},{}", point.x, point.y, point.infinity);
        }
    }
}

fn measure_pair(u0: u64, u1: u64, batch: u64) -> u128 {
    use std::hint::black_box;
    use std::time::Instant;

    let started = Instant::now();
    for _ in 0..batch {
        let point = hash_field_pair_p11(black_box(u0), black_box(u1));
        black_box(point);
    }
    started.elapsed().as_nanos()
}

fn run_timing(rounds: u64, batch: u64) {
    let mut state = 5_409_u64;
    println!("round,class_a_ns,class_b_ns,a_first,batch");
    for round in 0..rounds {
        state = state.wrapping_mul(6_364_136_223_846_793_005).wrapping_add(1);
        let a_first = (state >> 63) & 1;
        let first = measure_pair(
            cmov(1, 0, a_first),
            cmov(2, 0, a_first),
            batch,
        );
        let second = measure_pair(
            cmov(0, 1, a_first),
            cmov(0, 2, a_first),
            batch,
        );
        let class_a = cmov(second as u64, first as u64, a_first);
        let class_b = cmov(first as u64, second as u64, a_first);
        println!("{round},{class_a},{class_b},{a_first},{batch}");
    }
}

fn main() {
    let arguments: Vec<String> = std::env::args().collect();
    if arguments.get(1).map(String::as_str) == Some("--timing") {
        let rounds = arguments.get(2).and_then(|value| value.parse().ok()).unwrap_or(400);
        let batch = arguments.get(3).and_then(|value| value.parse().ok()).unwrap_or(1_000);
        run_timing(rounds, batch);
    } else {
        run_tables();
    }
}
