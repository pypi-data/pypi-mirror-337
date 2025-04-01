use std::collections::{HashMap, HashSet};
use std::fs;
use std::fs::File;
use std::io::{BufReader, Read};
use std::iter::zip;
use std::path::Path;
use csv::Reader;
use flate2::bufread::GzDecoder;
use log::{debug, error, info};
use pyo3::prelude::*;
use regex::Regex;
use yaml_rust2::YamlLoader;
use crate::Validation::{RegularExpression};

const MAX_SAMPLE_SIZE:u16 = 10;

#[derive(Debug, Clone)]
enum Validation {
    RegularExpression(String),
    Min(f64),
    Max(f64),
    None
}

struct ColumnValidations {
    column_name: String,
    validations: Vec<Validation>
}

struct ValidationSummary {
    validation: Validation,
    wrong_rows: usize,
    wrong_values_sample: Vec<String>
}

struct ColumnValidationsSummary {
    column_name: String,
    validation_summaries: Vec<ValidationSummary>
}

/// Validate that CSV file complies with validations definition
#[pyfunction]
fn validate(path: &str, definition_path: &str) -> PyResult<bool> {
    info!("Validating file {} against definition {}", path, definition_path);

    let validations = get_validations(definition_path);

    // Pre-Compile and save all Regex expressions to save time in execution
    let mut regex_map = HashMap::new();
    for column_validation in &validations {
        for validation in &column_validation.validations {
            match validation {
                RegularExpression(regex) => {
                    regex_map.insert(regex, Regex::new(regex.as_str()).unwrap());
                },
                _ => continue
            }
        }
    }

    // Build the CSV reader
    let mut rdr = get_reader_from(path);

    // First validation: Ensure column names and order are exactly as expected
    if validate_column_names(&mut rdr, &validations) {
        info!("Columns names and order are correct");
    }
    else {
        error!("Expected columns != Real columns");
        return Ok(false);
    }

    // Second validation: If column names match, check if also the values match the validations
    let mut validation_summaries_map = build_validation_summaries_map(&validations);
    let mut is_valid_file = true;
    for result in rdr.records() {
        let record = result.unwrap();
        for next_column in zip(record.iter(), validations.iter()) {
            let value = next_column.0;
            let _column_name = &next_column.1.column_name;
            for validation in &next_column.1.validations {
                let valid = apply_validation(value, validation, &regex_map);
                if !valid {
                    let validation_summary_list = validation_summaries_map.get_mut(_column_name).unwrap();
                    let validation_summary = validation_summary_list
                            .iter_mut()
                            .find(|val_sum|
                                std::mem::discriminant(&val_sum.validation) == std::mem::discriminant(validation)).unwrap();
                    validation_summary.wrong_rows += 1;
                    if validation_summary.wrong_values_sample.len() < MAX_SAMPLE_SIZE as usize {
                        validation_summary.wrong_values_sample.push(value.to_string());
                    }
                }
                is_valid_file = is_valid_file && valid;
            }
        }
    }

    // Fill the ColumnValidationSummary for each column
    let mut column_validation_summaries = Vec::new();
    for column_validation in &validations {
        let validation_summary_for_column =
            validation_summaries_map.remove(&column_validation.column_name).unwrap();
        let column_validation_summary = ColumnValidationsSummary {
            column_name: column_validation.column_name.clone(),
            validation_summaries: validation_summary_for_column
        };
        column_validation_summaries.push(column_validation_summary);
    }

    debug!("VALIDATIONS SUMMARY");
    debug!("==================================================================================");
    for column_validation_summary in column_validation_summaries {
        debug!("Column: '{}'", column_validation_summary.column_name);
        for validation_summary in column_validation_summary.validation_summaries {
            debug!("\tValidation {:?} => Wrong Rows: {} | Wrong Values Sample: {:?}", &validation_summary.validation,
                &validation_summary.wrong_rows, &validation_summary.wrong_values_sample);
        }
    }

    if is_valid_file {
        info!("OK: File matches the validations");
    }
    else {
        info!("NO OK: File DOESN'T match validations");
    }
    Ok(is_valid_file)
}

fn build_validation_summaries_map(validations: &Vec<ColumnValidations>) -> HashMap<String, Vec<ValidationSummary>> {
    let mut validation_summaries_map = HashMap::new();
    for validation in validations {
        let mut validation_summaries = Vec::new();
        for column_validation in &validation.validations {
            let validation_summary =
                ValidationSummary{validation: (*column_validation).clone(), wrong_rows: 0, wrong_values_sample: Vec::new()};
            validation_summaries.push(validation_summary);
        }
        validation_summaries_map.insert(validation.column_name.clone(), validation_summaries);
    }

    validation_summaries_map
}

fn apply_validation(value: &str, validation: &Validation, regex_map: &HashMap<&String, Regex>) -> bool {
    match validation {
        RegularExpression(regex) => {
            let regex = regex_map.get(regex).unwrap();
            regex.is_match(value)
        },
        Validation::Min(min) => {
            match value.parse::<f64>() {
                Ok(value) => value >= *min,
                Err(_) => false
            }
        },
        Validation::Max(max) => {
            match value.parse::<f64>() {
                Ok(value) => value <= *max,
                Err(_) => false
            }
        },
        Validation::None => panic!("None validation cannot be applied")
    }
}

/// Infers the file compression type and returns the corresponding buffered reader
fn get_reader_from(path: &str) -> Reader<Box<dyn Read>> {
    let buf_reader = BufReader::new(File::open(Path::new(path)).unwrap());
    if is_gzip_file(path) {
        debug!("File is gzipped");
        let read_capacity = 10 * 1024_usize.pow(2);
        let reader = BufReader::with_capacity(read_capacity, GzDecoder::new(buf_reader));
        Reader::from_reader(Box::new(reader))
    }
    else {
        Reader::from_reader(Box::new(buf_reader))
    }
}

fn is_gzip_file(path: &str) -> bool {
    let mut bytes = [0u8; 2];
    File::open(Path::new(path)).unwrap().read_exact(&mut bytes).unwrap();
    bytes[0] == 0x1f && bytes[1] == 0x8b
}

fn get_validations(definition_path: &str) -> Vec<ColumnValidations> {
    // Read the YAML definition with the validations
    let config =
        YamlLoader::load_from_str(fs::read_to_string(definition_path).unwrap().as_str()).unwrap();
    // Get the column names list and each associated validation
    let columns = &config[0]["columns"];
    let mut column_names = vec![];
    let mut column_validations = vec![];
    for column in columns.as_vec().unwrap() {
        let column_def = column.as_hash().unwrap();
        let mut name = "";
        let mut validations = vec![];
        for validation_definition in column_def.iter() {
            let key = validation_definition.0.as_str().unwrap();
            let value = validation_definition.1;
            let mut validation: Validation = Validation::None;
            match key {
                "name" => { name = value.as_str().unwrap(); column_names.push(name); }
                "regex" => { validation = Validation::RegularExpression(String::from(value.as_str().unwrap())); }
                "min" => { validation = Validation::Min(value.as_i64().unwrap() as f64); }
                "max" => { validation = Validation::Max(value.as_i64().unwrap() as f64); }
                _ => panic!("Unknown validation: {key}")
            }

            if key != "name" {
                validations.push(validation);
            }

        }
        let new_validations = ColumnValidations { column_name: name.to_string(), validations: validations };
        column_validations.push(new_validations);
    }

    column_validations
}

fn validate_column_names(reader: &mut Reader<Box<dyn Read>>, validations: &Vec<ColumnValidations>) -> bool {
    let expected_column_names = validations.iter()
        .map(|v| v.column_name.clone())
        .collect::<Vec<String>>();
    debug!("Expected Column Names: {:?}", expected_column_names);

    let headers: Vec<String> = reader.headers().unwrap().iter().map(|s| String::from(s) ).collect();
    debug!("Actual Column Names: {:?}", headers);

    if expected_column_names != headers {
        if expected_column_names.len() != headers.len() {
            let expected_columns_set: HashSet<String> = expected_column_names.iter().cloned().collect();
            let headers_set: HashSet<String> = headers.iter().cloned().collect();
            debug!("File headers not in expected columns: {:?}", headers_set.difference(&expected_columns_set));
            debug!("Columns in expected columns not in file headers: {:?}", expected_columns_set.difference(&headers_set));
        }
        else {
            for (expected_column, header) in zip(expected_column_names, headers) {
                if expected_column != header {
                    debug!("{:?} != {:?}", expected_column, header);
                }
            }
        }
        return false
    }
    true
}

/// A Python module implemented in Rust.
#[pymodule]
fn csv_validation(m: &Bound<'_, PyModule>) -> PyResult<()> {
    pyo3_log::init();
    m.add_function(wrap_pyfunction!(validate, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use simple_logger::SimpleLogger;
    use crate::validate;

    #[test]
    fn init_logger() {
        SimpleLogger::new().init().unwrap();
    }

    #[test]
    fn test_validate_csv() {
        assert!(validate("test/test_file.csv", "test/test_validations.yml").unwrap());
    }

    #[test]
    fn test_validate_csv_gz() {
        assert!(validate("test/test_file.csv.gz", "test/test_validations.yml").unwrap());
    }

    #[test]
    fn test_wrong_headers() {
        assert!(!validate("test/test_file.csv", "test/test_validations_wrong_headers.yml").unwrap());
    }
}