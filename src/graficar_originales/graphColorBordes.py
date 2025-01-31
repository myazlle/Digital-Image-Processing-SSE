import pandas as pd           ###librería para manipular tablas de datos
import seaborn as sns         ###librería para hacer gráficos
import numpy as np            ###librería de cálculo numérico
from scipy import stats       ###librería de estadística
import seaborn_qqplot as sqp  ###librería complementaria a seaborn para hacer qqplots
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages



colorBordesC0 = pd.read_csv('./build/ColorBordes.csv', header=None, sep=',')
colorBordesC2 = pd.read_csv('./build2/ColorBordes.csv', header=None, sep=',')
colorBordesC3 = pd.read_csv('./build3/ColorBordes.csv', header=None, sep=',')
tamaños = np.array([512,2048,8192,32768,120000,131072,480000,1920000])
tamañosASM = {"512":[],"2048":[],"8192":[],"32768":[],"120000":[],"131072":[],"480000":[],"1920000":[]}
tamañosC0 = {"512":[],"2048":[],"8192":[],"32768":[],"120000":[],"131072":[],"480000":[],"1920000":[]}
tamañosC2 = {"512":[],"2048":[],"8192":[],"32768":[],"120000":[],"131072":[],"480000":[],"1920000":[]}
tamañosC3 = {"512":[],"2048":[],"8192":[],"32768":[],"120000":[],"131072":[],"480000":[],"1920000":[]}

implementacion=1
tamaño=2
ciclos=3
for index, row in colorBordesC0.iterrows():
    if row[implementacion]=="ASM":
        tamañosASM[str(row[tamaño])].append(row[ciclos])
    else:
        tamañosC0[str(row[tamaño])].append(row[ciclos])

for index, row in colorBordesC2.iterrows():
    if row[implementacion]=="C":
        tamañosC2[str(row[tamaño])].append(row[ciclos])
    
for index, row in colorBordesC3.iterrows():
    if row[implementacion]=="C":
        tamañosC3[str(row[tamaño])].append(row[ciclos])


resASM=[]
resC0=[]
resC2=[]
resC3=[]

for index, x in enumerate(tamañosC0):
    snsArray = pd.Series(tamañosC0[x])
    tamañosC0[x] = snsArray[snsArray.between(snsArray.quantile(.10), snsArray.quantile(.90))]

for index, x in enumerate(tamañosC2):
    snsArray = pd.Series(tamañosC2[x])
    tamañosC2[x] = snsArray[snsArray.between(snsArray.quantile(.10), snsArray.quantile(.90))]

for index, x in enumerate(tamañosC3):
    snsArray = pd.Series(tamañosC3[x])
    tamañosC3[x] = snsArray[snsArray.between(snsArray.quantile(.10), snsArray.quantile(.90))]


for index, x in enumerate(tamañosASM):
    snsArray = pd.Series(tamañosASM[x])
    tamañosASM[x] = snsArray[snsArray.between(snsArray.quantile(.10), snsArray.quantile(.90))]

for index, x in enumerate(tamañosASM):
    npArray = np.array(tamañosASM[x])
    #tamañosASM[x] = tamañosASM[x].mean()
    resASM.append(tamañosASM[x].mean())


for index, x in enumerate(tamañosC0):
    npArray = np.array(tamañosC0[x])
    #tamañosC0[x] = tamañosC0[x].mean()
    resC0.append(tamañosC0[x].mean())

for index, x in enumerate(tamañosC2):
    npArray = np.array(tamañosC2[x])
    #tamañosC0[x] = tamañosC0[x].mean()
    resC2.append(tamañosC2[x].mean())

for index, x in enumerate(tamañosC3):
    npArray = np.array(tamañosC3[x])
    #tamañosC0[x] = tamañosC0[x].mean()
    resC3.append(tamañosC3[x].mean())



with PdfPages('ColorBordes_C_vs_ASM.pdf') as pdf:
    fig, ax= plt.subplots()
    ax.plot(tamaños, resASM, label="ASM", marker=".")
    ax.plot(tamaños, resC0, label="O0", marker=".")
    ax.plot(tamaños, resC2, label="O2", marker=".")
    ax.plot(tamaños, resC3, label="O3", marker=".")
    ax.legend(['ASM','O0','O2','O3'], loc='upper left')
    plt.xlabel("Cantidad de pixeles")
    plt.ylabel("Ciclos de clock")
    plt.title("Color Bordes")
    ax.ticklabel_format(style='plain')
    ax.axis([0, 2000000, 0, 180000000])
    plt.grid( linestyle='-', linewidth=1)
    for tick in ax.get_xticklabels():
        tick.set_rotation(55)
    #plt.show()
    pdf.savefig(bbox_inches='tight')
    plt.close()

with PdfPages('ColoresBordes_x_tamaño.pdf') as pdf:
    plt.figure(figsize=(7, 5))
    labels = 'ASM', 'O3', 'O2', 'O0'
    barValues = [resASM[7],resC3[7],resC2[7], resC0[7]]
    x = [1,2,3,4]
    fig, ax = plt.subplots()
    rects1 = ax.bar(x, barValues,0.7, label='')
    plt.ylabel('')
    plt.xlabel("Implementaciones")
    plt.ylabel("Ciclos de clock")
    plt.title("Color Bordes 1600x1200")
    ax.ticklabel_format(style='plain')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    plt.grid(linestyle='-', linewidth=1, axis='y')
    pdf.savefig(bbox_inches='tight')
    plt.close()



def calcularPorcentaje(asm, c):
    return int((asm*100)/c)


asm_vs_o3 = calcularPorcentaje(resASM[7], resC3[7])
asm_vs_o2 = calcularPorcentaje(resASM[7], resC2[7])
asm_vs_o0 = calcularPorcentaje(resASM[7], resC0[7])

print("colorBordes_asm_vs_O0: " + str(asm_vs_o0) + " %")
print("colorBordes_asm_vs_O2: " + str(asm_vs_o2) + " %")
print("colorBordes_asm_vs_O3: " + str(asm_vs_o3) + " %" + "\n")

#Hace el de ticks divido por millon y label Ticks (Millones)

#colorBordesAsm.set_index('Tamaño')
#media = colorBordesAsm['Ciclos'].mean()
#desviacionStandard = colorBordesAsm['Ciclos'].std()
#aproximacionNormal = np.random.normal(media, desviacionStandard, len(colorBordesAsm['Ciclos']))
#
#
#
#    fig, ax = plt.subplots()
#    ax.plot(colorBordesAsm, label='ASM')
#    # ax.plot(sizes, res_imagen_fantasma_c_O0, label="O0")
#    # ax.plot(sizes, res_imagen_fantasma_c_O1, label="O1")
#    # ax.plot(sizes, res_imagen_fantasma_c_O2, label="O2")
#    # ax.plot(sizes, res_imagen_fantasma_c_O3,  label="O3")
#    legend = ax.legend(loc='upper right', shadow=True)
#    ax.ticklabel_format(style='plain')
#    plt.title('Rendimiento')
#    plt.xlabel('Tamaño')
#    plt.ylabel('Ciclos')
#    legend.get_frame()
#    pdf.savefig()
#    plt.close()
#    plt.show()
