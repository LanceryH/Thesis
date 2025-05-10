use numpy::{IntoPyArray, PyArray1};
use reflec::fct_reflectance;
use pyo3::wrap_pyfunction;
use pyo3::prelude::*;

mod trigo;
mod reflec;


#[pyfunction]
fn reflectance(
    py: Python<'_>,
    microtext: Vec<f64>,
    incidence: Vec<f64>,
    emergence: Vec<f64>,
    azimuth: Vec<f64>,
    phase: Vec<f64>) -> Py<PyArray1<f64>> {

    let n = incidence.len();
    let mut results = vec![0.0; n];
    let w = microtext[0];
    let b = microtext[1];
    let c = microtext[2];
    let z = microtext[3] * 45.0;
    let o = microtext[4];
    let h = microtext[5];

    for i in 0..n {
        let incidence_rad = incidence[i].to_radians();
        let emergence_rad = emergence[i].to_radians();
        let azimuth_rad = azimuth[i].abs().to_radians();
        let phase_rad = phase[i].to_radians();
        let z_rad = z.to_radians();

        results[i] = fct_reflectance(
            w, b, c, z_rad, o, h,
            incidence_rad, emergence_rad,
            azimuth_rad, phase_rad
        );
    }
    results.into_pyarray(py).into()
}

#[pymodule]
fn rupho(_py: Python, m: &Bound<PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(reflectance, m)?)?;
    Ok(())
}
