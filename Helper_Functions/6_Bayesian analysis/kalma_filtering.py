from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple, Optional
import numpy as np


# =========================
# 1D Kalman Filter
# =========================

@dataclass
class KalmanFilter1D:
    """
    1D Kalman Filter for a scalar state (position only).
    Model:
      predict: x <- x + u,  P <- P + Q
      update:  fuse measurement z with variance R
    """
    x: float = 0.0              # mean
    P: float = 500.0            # variance
    Q: float = 2.0              # process (motion) variance
    R: float = 3.0              # measurement variance

    def predict(self, u: float = 0.0) -> Tuple[float, float]:
        """Prediction step: apply motion u."""
        self.x = self.x + u
        self.P = self.P + self.Q
        return self.x, self.P

    def update(self, z: float, R: Optional[float] = None) -> Tuple[float, float]:
        """Measurement update: fuse measurement z."""
        R = self.R if R is None else float(R)

        # Basic guards (keeps filter sane)
        if self.P <= 0 or R <= 0:
            raise ValueError(f"Variances must be positive. Got P={self.P}, R={R}")

        # Kalman gain for scalar case:
        # K = P / (P + R)
        S = self.P + R
        K = self.P / S

        # Updated mean/variance
        self.x = self.x + K * (z - self.x)
        self.P = (1.0 - K) * self.P

        return self.x, self.P

    def step(self, z: float, u: float = 0.0, R: Optional[float] = None) -> Tuple[float, float]:
        """Convenience: predict then update."""
        self.predict(u=u)
        return self.update(z=z, R=R)


def demo_kf_1d():
    sensor_readings = [5.0, 6.0, 8.0, 9.0]
    motions_applied = [1.0, 2.0, 2.0, 1.0]

    kf = KalmanFilter1D(x=0.0, P=500.0, Q=2.0, R=3.0)

    print("=== 1D Kalman Filter Demo ===")
    for i, (z, u) in enumerate(zip(sensor_readings, motions_applied), start=1):
        x_pred, P_pred = kf.predict(u=u)
        x_upd, P_upd = kf.update(z=z)

        print(f"\n--- Step {i} ---")
        print(f"After predict: position={x_pred:.2f}, uncertainty={P_pred:.2f}")
        print(f"After update : position={x_upd:.2f}, uncertainty={P_upd:.2f}")

    print("\n=== Final Estimate ===")
    print(f"Position: {kf.x:.2f} ± {np.sqrt(kf.P):.2f} (std dev)")


# =========================
# 2D Kalman Filter (CV model)
# =========================

class KalmanFilter2D:
    """
    2D constant-velocity Kalman Filter
    State: [x, y, vx, vy]^T
    Measurements: [x, y]^T
    """

    def __init__(
        self,
        dt: float = 1.0,
        x0: Optional[Sequence[float]] = None,
        P0: float = 1000.0,
        R_pos: float = 1.0,
        Q_scale: float = 0.01,
    ):
        self.dt = float(dt)

        # State vector
        if x0 is None:
            self.x = np.zeros((4, 1), dtype=float)
        else:
            arr = np.asarray(x0, dtype=float).reshape(4, 1)
            self.x = arr

        # Covariance
        self.P = np.eye(4, dtype=float) * float(P0)

        dt = self.dt
        self.F = np.array(
            [[1, 0, dt, 0],
             [0, 1, 0, dt],
             [0, 0, 1,  0],
             [0, 0, 0,  1]],
            dtype=float
        )

        self.H = np.array(
            [[1, 0, 0, 0],
             [0, 1, 0, 0]],
            dtype=float
        )

        self.R = np.eye(2, dtype=float) * float(R_pos)
        self.Q = np.eye(4, dtype=float) * float(Q_scale)

        self.I = np.eye(4, dtype=float)

        # Reusable buffers (minor speed + less garbage)
        self._y = np.zeros((2, 1), dtype=float)
        self._S = np.zeros((2, 2), dtype=float)

    def predict(self) -> np.ndarray:
        """Prediction step."""
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q
        return self.x[:2, 0].copy()

    def update(self, z: Sequence[float]) -> np.ndarray:
        """Measurement update using z=[meas_x, meas_y]."""
        z = np.asarray(z, dtype=float).reshape(2, 1)

        # Innovation: y = z - Hx
        self._y[:] = z - (self.H @ self.x)

        # S = HPH^T + R
        self._S[:] = self.H @ self.P @ self.H.T + self.R

        # Kalman gain: K = P H^T S^{-1}
        # Avoid explicit inverse: solve(S^T, (PH^T)^T)^T
        PHt = self.P @ self.H.T  # 4x2
        K = np.linalg.solve(self._S.T, PHt.T).T  # 4x2

        # Update state/covariance
        self.x = self.x + K @ self._y
        self.P = (self.I - K @ self.H) @ self.P

        return self.x[:, 0].copy()

    def step(self, z: Sequence[float]) -> np.ndarray:
        """Convenience: predict then update."""
        self.predict()
        return self.update(z)


def demo_kf_2d():
    kf = KalmanFilter2D(dt=1.0, P0=1000.0, R_pos=1.0, Q_scale=0.01)

    # True trajectory: constant velocity (vx=2, vy=1)
    true_states = np.array([[t * 2.0, t * 1.0, 2.0, 1.0] for t in range(10)], dtype=float)

    # Noisy measurements
    rng = np.random.default_rng(42)
    measurements = true_states[:, :2] + rng.normal(0.0, 1.5, size=(10, 2))

    print("=== 2D Kalman Filter Demo ===\n")
    print("Time | True Position | Noisy Measurement | Kalman Estimate (pos) | Estimated Velocity")
    print("-" * 78)

    for t in range(len(measurements)):
        state = kf.step(measurements[t])

        true_x, true_y = true_states[t, 0], true_states[t, 1]
        meas_x, meas_y = measurements[t, 0], measurements[t, 1]
        est_x, est_y, est_vx, est_vy = state

        print(
            f"t={t:2d} | ({true_x:5.1f},{true_y:5.1f}) | "
            f"({meas_x:6.2f},{meas_y:6.2f}) | "
            f"({est_x:6.2f},{est_y:6.2f}) | "
            f"v=({est_vx:5.2f},{est_vy:5.2f})"
        )

    print("\n=== Analysis ===")
    print("Even with noticeable measurement noise, the estimated trajectory stays smooth.")
    print("And although we only measure position, the filter also estimates velocity.")


# =========================
# Run demos
# =========================

if __name__ == "__main__":
    demo_kf_1d()
    print("\n")
    demo_kf_2d()
