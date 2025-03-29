use std::collections::{HashMap, HashSet};
use pyo3::{exceptions::PyException, prelude::{pyfunction, pymodule, wrap_pyfunction, Bound, PyModule, PyModuleMethods as _, PyResult}};

use ::parquet_to_excel::{parq_file_to_csv, parq_folder_to_csv};
use ::parquet_to_excel::{parq_file_to_xlsx, parq_folder_to_xlsx};


#[pyfunction]
#[pyo3(signature = (source, destination, header_labels=HashMap::new(), select_columns=HashSet::new()))]
fn parquet_file_to_csv(source: String, destination: String, header_labels: HashMap<String, String>, select_columns: HashSet<String>) -> PyResult<()> {
    match parq_file_to_csv(source, destination, &header_labels, &select_columns) {
        Ok(_) => {
            Ok(())
        },
        Err(e) => {
            Err(PyException::new_err(e.to_string()))
        }
    }
}


#[pyfunction]
#[pyo3(signature = (source, destination, header_labels=HashMap::new(), select_columns=HashSet::new()))]
fn parquet_files_to_csv(source: String, destination: String, header_labels: HashMap<String, String>, select_columns: HashSet<String>) -> PyResult<()> {
    match parq_folder_to_csv(source, destination, &header_labels, &select_columns) {
        Ok(_) => {
            Ok(())
        },
        Err(e) => {
            Err(PyException::new_err(e.to_string()))
        }
    }
}


#[pyfunction]
#[pyo3(signature = (source, destination, sheet_name=None, sheet_column=None, header_labels=HashMap::new(), select_columns=HashSet::new()))]
fn parquet_file_to_xlsx(source: String, destination: String, sheet_name: Option<String>, sheet_column: Option<String>, header_labels: HashMap<String, String>, select_columns: HashSet<String>) -> PyResult<()> {
    match parq_file_to_xlsx(source, destination, sheet_name, sheet_column, &header_labels, &select_columns) {
        Ok(_) => {
            Ok(())
        },
        Err(e) => {
            Err(PyException::new_err(e.to_string()))
        }
    }
}


#[pyfunction]
#[pyo3(signature = (source, destination, sheet_name=None, sheet_column=None, header_labels=HashMap::new(), select_columns=HashSet::new()))]
fn parquet_files_to_xlsx(source: String, destination: String, sheet_name: Option<String>, sheet_column: Option<String>, header_labels: HashMap<String, String>, select_columns: HashSet<String>) -> PyResult<()> {
    match parq_folder_to_xlsx(source, destination, sheet_name, sheet_column, &header_labels, &select_columns) {
        Ok(_) => {
            Ok(())
        },
        Err(e) => {
            Err(PyException::new_err(e.to_string()))
        }
    }
}


/// A Python module implemented in Rust.
#[pymodule]
fn parquet_to_excel(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parquet_file_to_csv, m)?)?;
    m.add_function(wrap_pyfunction!(parquet_files_to_csv, m)?)?;
    m.add_function(wrap_pyfunction!(parquet_file_to_xlsx, m)?)?;
    m.add_function(wrap_pyfunction!(parquet_files_to_xlsx, m)?)?;
    Ok(())
}


// development build
// maturin develop --release
// publish to pypi
// maturin publish --username __token__  --release