import math

def read_positive_number(prompt):
    try:
        value = float(input(prompt))
    except ValueError:
        raise ValueError("输入无效：请输入数字。") from None
    if not math.isfinite(value) or value <= 0:
        raise ValueError("输入无效：所有数值输入必须是有限正数（大于 0）。")
    return value


def check_calculation_range(*values):
    if not all(math.isfinite(value) and value > 0 for value in values):
        raise ValueError("数值超出浮点计算范围，请调整输入。")


def calculate_once():
    print("1. 计算模式：已知 L 计算电感电流纹波 ΔIL")
    print("2. 设计模式：根据目标 ΔIL 反推电感 L")
    try:
        mode = input("请选择模式（1/2，回车默认为 1）: ").strip() or "1"
        if mode not in ("1", "2"):
            raise ValueError("模式无效：请选择 1 或 2。")

        vin = read_positive_number("请输入输入电压 Vin (V): ")
        vout = read_positive_number("请输入输出电压 Vout (V): ")
        if vout >= vin:
            raise ValueError("Vout >= Vin，不符合基础理想 Buck 降压条件。")

        if mode == "1":
            inductance_uh = read_positive_number("请输入电感 L (uH): ")
        switching_frequency_khz = read_positive_number("请输入开关频率 fs (kHz): ")
        if mode == "2":
            inductor_ripple = read_positive_number("请输入目标电感电流纹波 ΔIL (A，峰峰值): ")

        duty_cycle = vout / vin
        switching_frequency_hz = switching_frequency_khz * 1e3
        numerator = (vin - vout) * duty_cycle
        check_calculation_range(duty_cycle, switching_frequency_hz, numerator)

        # 理想 Buck 稳态连续导通模式：ΔIL = (Vin - Vout) * D / (L * fs)。
        if mode == "1":
            inductance_h = inductance_uh * 1e-6
            denominator = inductance_h * switching_frequency_hz
            check_calculation_range(inductance_h, denominator)
            inductor_ripple = numerator / denominator
            check_calculation_range(inductor_ripple)
        else:
            # 移项得到 L = (Vin - Vout) * D / (ΔIL * fs)，结果单位为 H。
            denominator = inductor_ripple * switching_frequency_hz
            check_calculation_range(denominator)
            inductance_h = numerator / denominator
            inductance_uh = inductance_h * 1e6
            check_calculation_range(inductance_h, inductance_uh)

        print("Input voltage:", vin, "V")
        print("Output voltage:", vout, "V")
        print("Duty cycle:", duty_cycle)
        print("Duty cycle (%):", duty_cycle * 100)
        print("Inductor current ripple (peak-to-peak):", inductor_ripple, "A")
        if mode == "2":
            print(f"Required inductance: {inductance_h:.12g} H = {inductance_uh:.12g} uH")
    except ValueError as error:
        print(error)


def main():
    try:
        while True:
            calculate_once()
            while True:
                answer = input("是否继续计算？（y/yes 继续，n/no 退出）: ").strip().lower()
                if answer in ("y", "yes"):
                    break
                if answer in ("n", "no"):
                    return
                print("输入无效：请输入 y/yes 或 n/no。")
    except EOFError:
        print("输入中断：未提供完整参数。")


if __name__ == "__main__":
    main()
