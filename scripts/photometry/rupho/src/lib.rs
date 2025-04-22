mod other;
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use std::f64::consts::PI;
use other::TrigExt;
use numpy::{IntoPyArray, PyArray1}; 
use rayon::prelude::*;

/// Computes the exponential of the cotangent terms
fn e1(dzeta: f64, x: f64) -> f64 {
    let cot_dzeta = dzeta.cotan();
    let cot_x = x.cotan();
    (-2.0 / PI * cot_dzeta * cot_x).exp()
}

fn e2(dzeta: f64, x: f64) -> f64 {
    let cot_dzeta_sq = dzeta.cotan().powi(2);
    let cot_x_sq = x.cotan().powi(2);
    (-1.0 / PI * cot_dzeta_sq * cot_x_sq).exp()
}

/// Computes the geometric correction factors for reflectance.
fn geometry_correction(incidence: f64, emergence: f64, azimuth: f64, dzeta: f64) -> (f64, f64, f64, f64) {
    let tan_dzeta = dzeta.tan();
    let xidz = 1.0 / (1.0 + PI * tan_dzeta.powi(2)).sqrt();
    
    // Normalize azimuth angle
    let azimuth = azimuth.rem_euclid(2.0 * PI);

    let muo_b = (incidence.cos() + incidence.sin() * tan_dzeta * e2(dzeta, incidence) / (2.0 - e1(dzeta, incidence))) * xidz;
    let mu_b = (emergence.cos() + emergence.sin() * tan_dzeta * e2(dzeta, emergence) / (2.0 - e1(dzeta, emergence))) * xidz;

    let (muo, mu) = if incidence <= emergence {
        let muo = (incidence.cos() + incidence.sin() * tan_dzeta * 
            (azimuth.cos() * e2(dzeta, emergence) + azimuth.sin().powi(2) * e2(dzeta, incidence)) /
            (2.0 - e1(dzeta, emergence) - (azimuth / PI) * e1(dzeta, incidence))) * xidz;
        let mu = (emergence.cos() + emergence.sin() * tan_dzeta *
            (e2(dzeta, emergence) - azimuth.sin().powi(2) * e2(dzeta, incidence)) /
            (2.0 - e1(dzeta, emergence) - (azimuth / PI) * e1(dzeta, incidence))) * xidz;
        (muo, mu)
    } else {
        let muo = (incidence.cos() + incidence.sin() * tan_dzeta *
            (e2(dzeta, incidence) - azimuth.sin().powi(2) * e2(dzeta, emergence)) /
            (2.0 - e1(dzeta, incidence) - (azimuth / PI) * e1(dzeta, emergence))) * xidz;
        let mu = (emergence.cos() + emergence.sin() * tan_dzeta *
            (azimuth.cos() * e2(dzeta, incidence) + azimuth.sin().powi(2) * e2(dzeta, emergence)) /
            (2.0 - e1(dzeta, incidence) - (azimuth / PI) * e1(dzeta, emergence))) * xidz;
        (muo, mu)
    };

    (muo, mu, muo_b, mu_b)
}

/// Computes the shadowing factor using Hapke's model.
fn shadowing(incidence: f64, emergence: f64, mu: f64, muo_b: f64, mu_b: f64, azimuth: f64, dzeta: f64) -> f64 {
    let f = if azimuth.abs() == PI {
        0.0
    } else {
        (-2.0 * (azimuth / 2.0).tan()).exp()
    };

    let xidz = 1.0 / (1.0 + PI * dzeta.tan().powi(2)).sqrt();
    let temp = if incidence <= emergence {
        mu_b * muo_b * (1.0 - f + f * xidz * incidence.cos() / muo_b)
    } else {
        mu_b * muo_b * (1.0 - f + f * xidz * emergence.cos() / mu_b)
    };

    mu * incidence.cos() * xidz / temp
}

/// Computes the phase function component of reflectance.
fn phase_compo(b: f64, c: f64, phase: f64) -> f64 {
    (1.0 - c) * (1.0 - b.powi(2)) / (1.0 + 2.0 * b * phase.cos() + b.powi(2)).powf(1.5)
        + c * (1.0 - b.powi(2)) / (1.0 - 2.0 * b * phase.cos() + b.powi(2)).powf(1.5)
}

/// Computes the Chandrasekhar function used in reflectance modeling.
fn chandrasekhar(x: f64, gamma: f64) -> f64 {
    let denom = 1.0 - (1.0 - gamma.powi(2)) * x * ((1.0 - gamma) / (1.0 + gamma) + 
        (0.5 - x * (1.0 - gamma) / (1.0 + gamma)) * ((1.0 + x) / x).ln());
    1.0 / denom
}

/// Computes the reflectance function.
fn fct_reflectance(w: f64, b: f64, c: f64, dzeta: f64, b0: f64, h: f64, incidence: f64, emergence: f64, azimuth: f64, phase: f64) -> f64 {
    let mu = emergence.cos();
    let muo = incidence.cos();
    let gamma = (1.0 - w).sqrt();

    let (muo, mu, muo_b, mu_b) = if dzeta > 0.0 {
        geometry_correction(incidence, emergence, azimuth, dzeta)
    } else {
        (muo, mu, muo, mu)
    };

    let phase_factor = phase_compo(b, c, phase);
    let shadow_correction = if dzeta > 0.0 {
        shadowing(incidence, emergence, mu, muo_b, mu_b, azimuth, dzeta)
    } else {
        1.0
    };

    w * muo / (4.0 * (mu + muo) * incidence.cos()) * 
        ( (1.0 + (b0 / (1.0 + (1.0 / h) * (phase / 2.0).tan()))) * phase_factor
        + chandrasekhar(muo, gamma) * chandrasekhar(mu, gamma) - 1.0 ) * shadow_correction
}

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


    // Return the results as a Python array
    results.into_pyarray(py).into()
}

#[pymodule]
fn rupho(_py: Python, m: &Bound<PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(reflectance, m)?)?;
    Ok(())
}
