#!/usr/bin/env python
import math


class PIDController:
    def __init__(self, kp, kd, ki, min_output, max_output, min_pid_clamp, max_pid_clamp ):
        self.kp = kp
        self.kd = kd
        self.ki = ki
        self.minOutput = min_output
        self.maxOutput = max_output
        self.minPIDclamp = min_pid_clamp
        self.maxPIDclamp = max_pid_clamp
        self.previousError = 0.0
        self.previousTime = None
        self.cumulativeError = 0

    def update(self, value, target_value, time):
        error = target_value - value
        p = self.kp * error
        d = 0
        dt = 0
        if self.previousTime is not None:
            dt = time - self.previousTime
            if dt > 0:
                d = self.kd * (error - self.previousError) / dt
        output = p + d

        # TODO i portion of PID
        self.cumulativeError += self.ki * error * dt

        self.previousTime = time
        self.previousError = error
        integral_output = max(min(self.cumulativeError, self.maxPIDclamp), self.minPIDclamp)
        return max(min(output, self.maxOutput), self.minOutput) + integral_output

