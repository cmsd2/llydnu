use clap::{ArgMatches};
use crate::error::LlydnuError;
use tera::{Context, Tera};
use std::fs::File;
use std::io::Write;

const TEMPLATE_STR: &str = include_str!("../../../templates/infra.yaml");

pub fn template(matches: &ArgMatches) -> Result<(), LlydnuError> {
    let mut context = Context::new();

    if let Some(bucket_name) = matches.value_of("bucket") {
        context.insert("bucket_name", bucket_name);
    }

    let env_name = matches.value_of("environment").ok_or_else(|| LlydnuError::ArgError("missing environment arg".to_string()))?;
    let app_name = matches.value_of("application").ok_or_else(|| LlydnuError::ArgError("missing application arg".to_string()))?;

    context.insert("environment", env_name);
    context.insert("application", app_name);

    let cfn = Tera::one_off(TEMPLATE_STR, &context, true)?;

    if let Some(file_name) = matches.value_of("output") {
        let mut file = File::create(file_name)
            .map_err(|e| LlydnuError::TemplateFileError(e))?;
        file.write_all(cfn.as_bytes())
            .map_err(|e| LlydnuError::TemplateFileError(e))?;
    } else {
        println!("{}", cfn);
    }

    Ok(())
}