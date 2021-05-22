use clap::{Arg, ArgMatches, App, SubCommand};
use anyhow::Result;

fn main() -> Result<()> {
    println!("Hello, world!");

    let matches = App::new("llydnu")
        .version("1.0")
        .arg(Arg::with_name("environment")
            .help("environment string for namespacing, tagging and locating resources")
            .global(true)
            .long("environment")
            .short("e")
            .required(false)
            .default_value("prod")
            .value_name("ENV")
        )
        .arg(Arg::with_name("application")
            .hidden(true)
            .global(true)
            .long("application")
            .required(false)
            .default_value("llydnu")
            .value_name("APP")
        )
        .subcommand(SubCommand::with_name("rustc")
            .about("rustc wrapper")
            .version("1.0")
        )
        .subcommand(SubCommand::with_name("cfn")
            .about("cloudformation bootstrap template")
            .version("1.0")
            .arg(Arg::with_name("bucket")
                .help("bucket to use to store build files")
                .long("bucket")
                .value_name("NAME")
                .required(false)
            )
            .arg(Arg::with_name("output")
                .help("file to write cloudformation template to")
                .long("output")
                .value_name("FILE")
                .required(false)
            )
        )
        .get_matches();
    
    if let Some(matches) = matches.subcommand_matches("rustc") {
        cmd_rustc(matches)?;
    }

    if let Some(matches) = matches.subcommand_matches("cfn") {
        cmd_cfn(matches)?;
    }

    Ok(())
}

fn cmd_rustc(matches: &ArgMatches) -> Result<()> {
    todo!()
}

fn cmd_cfn(matches: &ArgMatches) -> Result<()> {
    llydnu::cfn::template(matches)?;

    Ok(())
}