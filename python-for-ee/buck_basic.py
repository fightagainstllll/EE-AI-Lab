import math

try:
    vin = float(input("请输入输入电压 Vin (V): "))
    vout = float(input("请输入输出电压 Vout (V): "))
except ValueError:
    print("输入无效：请输入数字。")
else:
    if not math.isfinite(vin) or not math.isfinite(vout):
        print("输入无效：电压必须是有限数字。")
    elif vin <= 0 or vout < 0:
        print("输入无效：Vin 必须大于 0，Vout 不能小于 0。")
    elif vout >= vin:
        print("Vout >= Vin，不符合基础理想 Buck 降压条件。")
    else:
        duty_cycle = vout / vin

        print("Input voltage:", vin, "V")
        print("Output voltage:", vout, "V")
        print("Duty cycle:", duty_cycle)
        print("Duty cycle (%):", duty_cycle * 100)
