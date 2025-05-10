use crate::trigo::TrigExt;
use std::f64::consts::PI;

fn e1(z: f64, x: f64) -> f64 {
    (-2.0 / PI * z.cotan() * x.cotan()).exp()
}

fn e2(z: f64, x: f64) -> f64 {
    (-1.0 / PI * z.cotan().powi(2) * x.cotan().powi(2)).exp()
}

fn geometry_correction(incidence: f64, emergence: f64, azimuth: f64, z: f64) -> (f64, f64, f64, f64) {
    let tan_z = z.tan();
    let xidz = 1.0 / (1.0 + PI * tan_z.powi(2)).sqrt();
    //azimuth.rem_euclid(2.0 * PI);
    let azimuth = if azimuth >= PI {
        2.0 * PI - azimuth
    } else {
        azimuth
    };

    let muo_b = (incidence.cos() + incidence.sin() * tan_z * e2(z, incidence) / (2.0 - e1(z, incidence))) * xidz;
    let mu_b = (emergence.cos() + emergence.sin() * tan_z * e2(z, emergence) / (2.0 - e1(z, emergence))) * xidz;

    let (muo, mu) = if incidence <= emergence {
        let muo = (incidence.cos() + incidence.sin() * tan_z * 
            (azimuth.cos() * e2(z, emergence) + (azimuth / 2.0).sin().powi(2) * e2(z, incidence)) /
            (2.0 - e1(z, emergence) - (azimuth / PI) * e1(z, incidence))) * xidz;
        let mu = (emergence.cos() + emergence.sin() * tan_z *
            (e2(z, emergence) - (azimuth / 2.0).sin().powi(2) * e2(z, incidence)) /
            (2.0 - e1(z, emergence) - (azimuth / PI) * e1(z, incidence))) * xidz;
        (muo, mu)
    } else {
        let muo = (incidence.cos() + incidence.sin() * tan_z *
            (e2(z, incidence) - (azimuth / 2.0).sin().powi(2) * e2(z, emergence)) /
            (2.0 - e1(z, incidence) - (azimuth / PI) * e1(z, emergence))) * xidz;
        let mu = (emergence.cos() + emergence.sin() * tan_z *
            (azimuth.cos() * e2(z, incidence) + (azimuth / 2.0).sin().powi(2) * e2(z, emergence)) /
            (2.0 - e1(z, incidence) - (azimuth / PI) * e1(z, emergence))) * xidz;
        (muo, mu)
    };

    (muo, mu, muo_b, mu_b)
}

fn shadowing(incidence: f64, emergence: f64, mu: f64, muo_b: f64, mu_b: f64, azimuth: f64, z: f64) -> f64 {
    let f = if azimuth.abs() == PI {
        0.0
    } else {
        (-2.0 * (azimuth / 2.0).tan()).exp()
    };

    let xidz = 1.0 / (1.0 + PI * z.tan().powi(2)).sqrt();
    let temp = if incidence <= emergence {
        mu_b * muo_b * (1.0 - f + f * xidz * incidence.cos() / muo_b)   
    } else {
        mu_b * muo_b * (1.0 - f + f * xidz * emergence.cos() / mu_b)
    };

    mu * incidence.cos() * xidz / temp
}

fn phase_compo(b: f64, c: f64, phase: f64) -> f64 {
    (1.0 - c) * (1.0 - b.powi(2)) / (1.0 + 2.0 * b * phase.cos() + b.powi(2)).powf(1.5)
        + c * (1.0 - b.powi(2)) / (1.0 - 2.0 * b * phase.cos() + b.powi(2)).powf(1.5)
}

fn chandrasekhar(x: f64, gamma: f64) -> f64 {
    1.0/ (1.0 - (1.0 - gamma.powi(2)) * x * ((1.0 - gamma) / (1.0 + gamma) + 
        (0.5 - x * (1.0 - gamma) / (1.0 + gamma)) * ((1.0 + x) / x).ln()))
}

pub fn fct_reflectance(w: f64, b: f64, c: f64, z: f64, o: f64, h: f64, incidence: f64, emergence: f64, azimuth: f64, phase: f64) -> f64 {
    let mu = emergence.cos();
    let muo = incidence.cos();
    let gamma = (1.0 - w).sqrt();

    let (muo, mu, muo_b, mu_b) = if z > 0.0 {
        geometry_correction(incidence, emergence, azimuth, z)
    } else {
        (muo, mu, muo, mu)
    };

    let shadow_correction = if z > 0.0 {
        shadowing(incidence, emergence, mu, muo_b, mu_b, azimuth, z)
    } else {
        1.0
    };

    w * muo / (4.0 * (mu + muo) * incidence.cos()) * 
        ( (1.0 + (o / (1.0 + (1.0 / h) * (phase / 2.0).tan()))) * phase_compo(b, c, phase)
        + chandrasekhar(muo, gamma) * chandrasekhar(mu, gamma) - 1.0 ) * shadow_correction
}
