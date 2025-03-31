use cbindgen::Config;
use std::env;
use std::path::PathBuf;

fn main() {
    // Tell Cargo to re-run this if any of these files change
    println!("cargo:rerun-if-changed=src/lib.rs");
    println!("cargo:rerun-if-changed=src/python.rs");
    println!("cargo:rerun-if-changed=build.rs");

    // Set up PyO3
    pyo3_build_config::add_extension_module_link_args();

    // Generate C header
    let crate_dir = env::var("CARGO_MANIFEST_DIR").unwrap();
    let config = Config {
        language: cbindgen::Language::C,
        ..Default::default()
    };
    
    let header_path = PathBuf::from(&crate_dir)
        .join("target")
        .join("gitomator.h");
        
    cbindgen::generate_with_config(&crate_dir, config)
        .unwrap()
        .write_to_file(header_path);
} 