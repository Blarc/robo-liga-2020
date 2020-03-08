
public class PidController {

    private Float setpoint;
    private Float kp;
    private Float ki;
    private Float kd;
    private Float integralLimit;

    private Float error;
    private Long time;
    private Float integral;
    private Float value;

    public PidController(Float setpoint, Float kp, Float ki, Float kd, Float integralLimit) {
        this.setpoint = setpoint;
        this.kp = kp;
        this.ki = ki;
        this.kd = kd;
        this.integralLimit = integralLimit;
    }

    public void reset(Float setpoint, Float kp, Float ki, Float kd, Float integralLimit) {
        if (setpoint != null) {
            this.setpoint = setpoint;
        }

        if (kp != null) {
            this.kp = kp;
        }

        if (ki != null) {
            this.ki = ki;
        }

        if (kd != null) {
            this.kd = kd;
        }

        if (integralLimit != null) {
            this.integralLimit = integralLimit;
        }

        this.error = null;
        this.time = null;
        this.integral = null;
        this.value = null;
    }

    public float update(float measurement) {
        if (value == null) {
            value = measurement;
            time = System.currentTimeMillis();
            integral = 0f;
            error = setpoint - measurement;

            return kp * error;
        }
        else {
            long timeNow = System.currentTimeMillis();
            long timeDelta = timeNow - time;
            time = timeNow;

            value = measurement;

            float errorNew = setpoint - value;

            float p = kp * errorNew;

            float i;
            if (ki == null) {
                i = 0;
            }
            else {
                integral += errorNew * timeDelta;
                i = ki * integral;
                if (integralLimit != null) {
                    i = Math.max(Math.min(i, integralLimit), -integralLimit);
                }
            }

            float d;
            if (kd == null) {
                d = 0;
            }
            else {
                d = kd * (errorNew - error) / timeDelta;
            }

            error = errorNew;

            return p + i + d;
        }
    }
}
