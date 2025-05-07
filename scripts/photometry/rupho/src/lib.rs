mod math;
mod reflec;

use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use numpy::{IntoPyArray, PyArray1};
use rayon::prelude::*;
use reflec::fct_reflectance;

#[pyfunction]
fn reflectance(
    py: Python<'_>,
    w: f64, b: f64, c: f64,
    z: f64, o: f64, h: f64,
    incidence: Vec<f64>,
    emergence: Vec<f64>,
    azimuth: Vec<f64>,
    phase: Vec<f64>) -> Py<PyArray1<f64>> {

    let n = incidence.len();
    let mut results = vec![0.0; n];

    results.par_iter_mut().enumerate().for_each(|(i, res)| {
        let incidence_rad = incidence[i].to_radians();
        let emergence_rad = emergence[i].to_radians();
        let azimuth_rad = azimuth[i].to_radians();
        let phase_rad = phase[i].to_radians();
        let z_rad = z.to_radians();

        *res = fct_reflectance(
            w, b, c, z_rad, o, h,
            incidence_rad, emergence_rad, azimuth_rad, phase_rad
        );
    });

    results.into_pyarray(py).into()
}

#[pymodule]
fn rupho(_py: Python, m: &Bound<PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(reflectance, m)?)?;
    Ok(())
}
