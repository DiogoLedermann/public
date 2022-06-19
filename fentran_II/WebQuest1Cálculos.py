from numpy import pi

# Arbitrados
Tf = 300  # Temperatura do fluido longe da superfície (K)
V = 5  # Velocidade do fluido (m/s)

Ts = 373  # Temperatura da superfície (K)
L = 0.02  # Comprimento de referência (diâmetro) (m)
x = 0.1  # Altura do cilindro (m)

# Dados
Cpf = 4186  # Calor específico da água (J / kg K)
kf = 0.609  # Condutividade térmica da água (W / m K)
ro = 996.5  # Massa específica da água a 300 K (kg / m³)
mi = 0.000852  # Viscosidade dinâmica da água a 300 K (N s / m²)

Cps = 393  # Calor específico do cobre (J / kg K)
ks = 393  # Condutividade térmica do cobre a 373 K (W / m K)

deltaT = Ts - Tf
A = (2 * (pi * (L / 2) ** 2)) + ((2 * pi * (L / 2)) * x)  # Área total = 2 x Abase + Alateral = 2πr² + 2πrh

Re = V * L * ro / mi  # Reynolds

if 1 <= Re <= 40:
    C = 0.75
    m = 0.4
elif 40 < Re <= 1_000:
    C = 0.51
    m = 0.5
elif 10 ** 3 < Re <= 2 * 10 ** 5:
    C = 0.26
    m = 0.6
elif 2 * 10 ** 5 < Re <= 10 ** 6:
    C = 0.076
    m = 0.7

Prf = Cpf * mi / kf  # Prandlt do fluido
Prs = Cps * mi / ks  # Prandlt da superfície

Nu = C * Re ** m * Prf ** 0.37 * (Prf / Prs) ** (1 / 4)

h = Nu * kf / L
q = h * A * deltaT

print(f'ΔT = {deltaT} °C\n'
      f'Área de contato = {A} m²\n'
      f'Reynolds = {Re}\n'
      f'C = {C}\n'
      f'm = {m}\n'
      f'Prandtl do fluido = {Prf}\n'
      f'Prandtl da superfície = {Prs}\n'
      f'Nusselt = {Nu}\n'
      f'h = {h} ≈ {round(h)} W / m² °C\n'
      f'q = {q} ≈ {round(q)} W\n')
