import random

# ==== Generování náhodné mapy. ====
mapa = list("████████████████████████████████OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
random.shuffle(mapa)
# mapa.insert(0, '█')

# ==== Definice globálních proměnných. ====
class chlapek:
  pozice = random.sample(range(0, 7), 2) # [0, 0]
  def __init__(self, sila, zivoty, odolnost):
    self.sila = sila
    self.zivoty = zivoty
    self.odolnost = odolnost
hrdina = chlapek(random.randint(1, 19), random.randint(100, 1000), random.randint(1, 19))
navstiveno_policek = 0
porazeno_zlounu = 0

# ==== Hlavní herní smyčka. ====
while True:
  smer = random.choice([[0, -1], [0, 1], [1, -1], [1, 1]])
  hrdina.pozice[smer[0]] += smer[1]
  if hrdina.pozice[smer[0]] & 0xFFFFFFFF > 7:
      hrdina.pozice[smer[0]] -= smer[1]
  else:
    navstiveno_policek += 1
  policko = hrdina.pozice[0] * 8 + hrdina.pozice[1]
  if mapa[policko] == '█':
    mapa[policko] = '░'
  if mapa[policko] == 'O':
    zloun = chlapek(random.randint(1, 19), random.randint(1, 100), random.randint(1, 19))
    souperi = [hrdina, zloun] # Opravdu nevím jak pojmenovat tuto proměnou.
    # random.shuffle(souperi) # Bez tohoto řádku bude vždy útočit nejdříve zloun.
    while hrdina.zivoty * zloun.zivoty > 0:
      if souperi[0].odolnost < random.randint(1, 20):
        souperi[0].zivoty -= random.random() * souperi[1].sila
      souperi[0], souperi[1] = souperi[1], souperi[0]
  else:
    continue
  if zloun.zivoty <= 0:
    porazeno_zlounu += 1
    if porazeno_zlounu == 32:
      print("HRDINA VYHRÁL!!! ƪ(˘⌣˘)ʃ")
      mapa[policko] = '╬'
    else:
      mapa[policko] = 'Ø'
      continue
  elif hrdina.zivoty <= 0:
    print("HRDINA PROHRÁL... ಥ╭╮ಥ")
    mapa[policko] = '┼'
  break 

# ==== Zobrazení mapy a statistik. ====
print("""==== VYSVĚTLIVKY ====
█ = prázdné pole
░ = prázdné pole, které navštívil hrdina
╬ = hrdina
┼ = poražený hrdina
O = zloun
Ø = poražený zloun
==== MAPA ====""")
for x in range(8):
  for y in range(8):
    print(mapa[x * 8 + y], end = ' ')
  print()
print("==== STATISTIKY ====")
print("Počet navštívených políček: ", navstiveno_policek)
print("Počet poražených zlounů:    ", porazeno_zlounu)
