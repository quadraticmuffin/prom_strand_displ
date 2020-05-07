import scipy.optimize as so
import scipy.integrate as si 
from openpyxl import load_workbook
import matplotlib.pyplot as plt
from scipy.integrate._ivp.ivp import OdeResult

# TODO Add Jacobian Matrix
# TODO try new methods in Curve_fit
# think about objective function

workbook = load_workbook("kinetics_b2_b2-b3.xlsx") # May have to use full file path
sheet = workbook.active
t_data = [cell.value for cell in sheet['A']][2:]
l_data = [cell.value for cell in sheet['B']][2:]

TMAX = t_data[-1]

I0 = 50 # nM
F0 = 50 # nM
V0 = 600 # microL

def func1(t, o, a):
    return a * (I0 - o) * (F0 - o) # initial concentrations 50 nM; I=input, F=fuel

def func2(t, a, b, T0, L0, e):
    ans = b * si.solve_ivp(lambda t,o: func1(t,o,a), (T0, TMAX), [L0/b], vectorized=True, dense_output=True).sol(t)[0]
    # Background fluorescence
    ans = [i + L0 for i in ans]
    i = 0
    while t[i] < T0:
        ans[i] = L0
        i+= 1
    
    # Increased concentration due to evaporation
    for i in range(len(t)):
        ans[i] *= V0/(V0-e*t[i])

    return ans

params = so.curve_fit(func2, t_data, l_data, p0=[0.0001, 30, 600, 50, 0.001])[0]

print([round(num, 5) for num in params])

plt.plot(t_data, l_data, 'b-', label='data')
# plt.plot(t_data, func2(t_data, 0.0001, 25, 600, 50, 0.001), 'g.', label='ideal')
plt.plot(t_data, func2(t_data, *params), 'r-', label='model')

plt.xlim(0, TMAX)
plt.legend()
plt.show()

