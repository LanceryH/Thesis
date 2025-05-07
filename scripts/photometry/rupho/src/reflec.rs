use std::f64::consts::PI;
use crate::math::TrigExt;

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

fn geometry_correction(incidence: f64, emergence: f64, azimuth: f64, dzeta: f64) -> (f64, f64, f64, f64) {
    let tan_dzeta = dzeta.tan();
    let xidz = 1.0 / (1.0 + PI * tan_dzeta.powi(2)).sqrt();
    
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

fn phase_compo(b: f64, c: f64, phase: f64) -> f64 {
    (1.0 - c) * (1.0 - b.powi(2)) / (1.0 + 2.0 * b * phase.cos() + b.powi(2)).powf(1.5)
        + c * (1.0 - b.powi(2)) / (1.0 - 2.0 * b * phase.cos() + b.powi(2)).powf(1.5)
}

fn chandrasekhar(x: f64, gamma: f64) -> f64 {
    let denom = 1.0 - (1.0 - gamma.powi(2)) * x * ((1.0 - gamma) / (1.0 + gamma) + 
        (0.5 - x * (1.0 - gamma) / (1.0 + gamma)) * ((1.0 + x) / x).ln());
    1.0 / denom
}

pub fn fct_reflectance(w: f64, b: f64, c: f64, dzeta: f64, b0: f64, h: f64, incidence: f64, emergence: f64, azimuth: f64, phase: f64) -> f64 {
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
