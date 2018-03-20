import matplotlib.pyplot as plt
x = np.linspace(0.988, 1.012, 200)

y = x**7 - 7*x**6 + 21*x**5 - 35*x**4 + 35*x**3 - 21*x**2 + 7*x - 1

plt.plot(x,y)
plt.show()
