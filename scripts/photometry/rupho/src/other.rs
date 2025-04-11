// src/trig_ext.rs
pub trait TrigExt {
    fn cotan(self) -> f64;
}

impl TrigExt for f64 {
    fn cotan(self) -> f64 {
        self.cos() / self.sin()
    }
}
