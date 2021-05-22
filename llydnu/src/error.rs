use std::error::Error;
use thiserror::Error;
use std::io;

pub type BoxError = Box<dyn Error>;

#[derive(Error, Debug)]
pub enum LlydnuError {
    #[error("template error")]
    TemplateError(#[from] tera::Error),
    #[error("template file error")]
    TemplateFileError(io::Error),
    #[error("arg error")]
    ArgError(String),
}