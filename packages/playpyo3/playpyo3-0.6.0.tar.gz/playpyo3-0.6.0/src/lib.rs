use pyo3::prelude::*;

/// Formats the sum of two numbers as string.
///
/// :param a: First number to add
/// :type a: int
/// :param b: Second number to add
/// :type b: int
/// :return: String representation of the sum
/// :rtype: str
#[pyfunction]
#[pyo3(signature = (a = 0, b = 0))]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn playpyo3(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    Ok(())
}
