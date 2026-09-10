import math

try:
    vin = float(input("请输入输入电压 Vin (V): "))
    vout = float(input("请输入输出电压 Vout (V): "))
    inductance_uh = float(input("请输入电感 L (uH): "))
    switching_frequency_khz = float(input("请输入开关频率 fs (kHz): "))
except ValueError:
    print("输入无效：请输入数字。")
else:
    inputs = (vin, vout, inductance_uh, switching_frequency_khz)
    if not all(math.isfinite(value) for value in inputs):
        print("输入无效：Vin、Vout、L 和 fs 必须是有限数字。")
    elif any(value <= 0 for value in inputs):
        print("输入无效：Vin、Vout、L 和 fs 必须大于 0。")
    elif vout >= vin:
        print("Vout >= Vin，不符合基础理想 Buck 降压条件。")
    else:
        duty_cycle = vout / vin

        # 将 uH 转换为 H，将 kHz 转换为 Hz。
        inductance_h = inductance_uh * 1e-6
        switching_frequency_hz = switching_frequency_khz * 1e3
        # 理想 Buck 连续导通模式下的电感电流峰峰值纹波，单位为 A。
        inductor_ripple = (vin - vout) * duty_cycle / (
            inductance_h * switching_frequency_hz
        )

        print("Input voltage:", vin, "V")
        print("Output voltage:", vout, "V")
        print("Duty cycle:", duty_cycle)
        print("Duty cycle (%):", duty_cycle * 100)
        print("Inductor current ripple (peak-to-peak):", inductor_ripple, "A")
