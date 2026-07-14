#![forbid(unsafe_code)]

//! Gjallarbru server application entry point.

fn main() {
    println!(
        "gjallarbru {} (repository foundation; STUN/TURN service not implemented)",
        env!("CARGO_PKG_VERSION")
    );
}
