#!/usr/bin/env python3

from modules.console_ui import draw_coloured_line, get_validated_input

ANTIG_EMP_P = 0.06
ANTIG_EMP_M = 0.05
HORAS_EMP_P = 4
HORAS_EMP_M = 8

dias_emp_p = get_validated_input(
    msg="Introduzca la cantidad de dias trabajados de la empleada P",
    return_type="int",
)
dias_emp_m = get_validated_input(
    msg="Introduzca la cantidad de dias trabajados de la empleada M",
    return_type="int",
)
remun_mes = float(input("Introduzca el monto por hora para quinta categoría con retiro: "))

horas_mensuales_emp_p = dias_emp_p * HORAS_EMP_P
horas_mensuales_emp_m = dias_emp_m * HORAS_EMP_M

basico_emp_p = round(horas_mensuales_emp_p * remun_mes, 2)
antig_emp_p = round(basico_emp_p * ANTIG_EMP_P, 2)

basico_emp_m = round(horas_mensuales_emp_m * remun_mes, 2)
antig_emp_m = round(basico_emp_m * ANTIG_EMP_M, 2)

titulo_emp_p = "Valores de la empleada P"
print(f"\n{titulo_emp_p}")
draw_coloured_line(length=len(titulo_emp_p))
print(f"Horas trabajadas: {horas_mensuales_emp_p} horas")
print(f"Básico: {basico_emp_p}")
print(f"Antiguedad: {antig_emp_p}")

titulo_emp_m = "Valores de la empleada M"
print(f"\n{titulo_emp_m}")
draw_coloured_line(length=len(titulo_emp_m))
print(f"Horas trabajadas: {horas_mensuales_emp_m} horas")
print(f"Básico: {basico_emp_m}")
print(f"Antiguedad: {antig_emp_m}")
