//! Foundation behavior tests for the server binary scaffold.

use std::process::Command;

#[test]
fn foundation_binary_is_explicitly_nonfunctional() -> Result<(), Box<dyn std::error::Error>> {
    let output = Command::new(env!("CARGO_BIN_EXE_gjallarbru")).output()?;
    assert!(output.status.success());
    let stdout = String::from_utf8(output.stdout)?;
    assert!(stdout.contains("repository foundation"));
    assert!(stdout.contains("STUN/TURN service not implemented"));
    Ok(())
}
