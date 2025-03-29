use pyo3::prelude::*;

/// sum_as_string(a: int, b: int) -> str
///
/// Returns the sum of two numbers as a string.
///
/// Args:
///     a: First integer
///     b: Second integer
///
/// Returns:
///     String representation of the sum
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn playpyo3(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    Ok(())
}
