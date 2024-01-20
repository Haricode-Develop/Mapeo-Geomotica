import pandas as pd

# Leer los archivos Excel
excel1 = pd.read_excel('C:\\Users\\jmanc\\Downloads\\Result_208.xlsx')
excel2 = pd.read_excel('C:\\Users\\jmanc\\Downloads\\ReporteOperaciones_20231208_173400.xlsx', header=6)
print(excel2.columns)

# Asegúrate de que los nombres de las columnas coincidan exactamente con los de los archivos Excel
columna_excel1 = excel1["ID_CONVERSACION"]  # Si este es el nombre correcto en el primer Excel
columna_excel2 = excel2["ID_CONVERSACION"]  # Si este es el nombre correcto en el segundo Excel

# Encontrar las diferencias
diferencias = columna_excel1[~columna_excel1.isin(columna_excel2)]

# Mostrar las diferencias
print(diferencias)
# O puedes guardar los resultados en un nuevo archivo Excel
# diferencias.to_excel('diferencias.xlsx')
