pub trait TrigExt {
    fn cotan(self) -> f64;
}

impl TrigExt for f64 {
    fn cotan(self) -> f64 {
        if self.sin() == 0.0 {
            f64::INFINITY
        } else {
            self.cos() / self.sin()
        }
    }
}
