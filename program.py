import random

# ==== Generování náhodné mapy. ====
# Podle mě nejjednodušší způsob jak vygenerovat 8*8 matci s 32 náhodně rozmístěnými zlouny je...
# předdefinovat matici s 32 prázdnými místy ('█') a 32 zlouny ('O') a pomocí funkce random.shuffle() ji náhodně zamíchat.
# Tento přístup má ovšem jednu nevýhodu: random.shuffle() neumí míchat vícedimenzionální matice.
# Proto je nutné přeměnit 2D matici s rozměry 8*8 na 1D matici s rozměry 1*64, a jen předstírat že je 2D.
# Indexování pak funguje takto: mat1D[x + y * 8] = mat2D[y][x] což znamená: mat1D[0...7] = mat2D[0][0...7], mat1D[8...15] = mat2D[1][0...7] atd.
# Také není nutné, aby mapa (vygenerovaná matice) ukládala u zlounů jejich sílu, počet živoutů a odolnost, protože...
# hrdina vždy bojuje maximálně s jedním za kolo a tyto vlastnosti mohou být vygenerovány až před bojem.
mapa = list("████████████████████████████████OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO") # Definice matice s rozměry 1*64.
random.shuffle(mapa) # Zamíchání matice.
# mapa.insert(0, '█')

# ==== Definice globálních proměnných. ====
# Hrdina a zloun budou instance této třídy.
class chlapek:
  # Pozice je důležitá jen u hrdiny, protože vždy existuje jen jeden zloun, nevadí že pozici také ukládá.
  # Hrdina začíná na náhodných souřadnicích ne na zadaných (0, 0).
  pozice = random.sample(range(0, 7), 2) # [0, 0]
  def __init__(self, sila, zivoty, odolnost):
    self.sila = sila
    self.zivoty = zivoty
    self.odolnost = odolnost
hrdina = chlapek(random.randint(1, 19), random.randint(100, 1000), random.randint(1, 19)) # Hrdina má 100-1000 životy, místo zadaných 1-100.
navstiveno_policek = 0
porazeno_zlounu = 0

# ==== Hlavní herní smyčka. ====
while True:
  # Směr je náhodná 1*2 matice, kde 1. element je po jaké ose se bude hrdina pohybovat (0 = x, 1 = y) a...
  # 2. element je jestli se bude pohybovat k mínusu nebo k plusu.
  smer = random.choice([[0, -1], [0, 1], [1, -1], [1, 1]])
  hrdina.pozice[smer[0]] += smer[1]
  # Tato podmínka zkontroluje zda se hrdina nedostal mimu mapu.
  # Funguje stejně jako: "if hrdina.pozice[smer[0]] < 0 or hrdina.pozice[smer[0]] > 7", jen udělá o operaci méně.
  # (Opravdu se mi nechce vysvětlovat jak to přesně funguje.)
  if hrdina.pozice[smer[0]] & 0xFFFFFFFF > 7:
      hrdina.pozice[smer[0]] -= smer[1] # Vrácení hrdiny zpět na mapu.
  else:
    navstiveno_policek += 1
  policko = hrdina.pozice[0] + hrdina.pozice[1] * 8 # Viz řádek 8.
  if mapa[policko] == '█':
    # Hrdina se dostal na prázdné políčko.
    mapa[policko] = '░'
  elif mapa[policko] == 'O':
    # Hrdina se dostal na políčko se zlounem.
    zloun = chlapek(random.randint(1, 19), random.randint(1, 100), random.randint(1, 19)) # Generování vlastností zlouna.
    souperi = [hrdina, zloun] # souperi = [obránce, útočník]
    # random.shuffle(souperi) # Bez tohoto řádku bude vždy útočit nejdříve zloun.
    # Smyčka, která běží dokud nezemře buď hrdina nebo zloun.
    while hrdina.zivoty * zloun.zivoty > 0:
      # Boj.
      if souperi[0].odolnost < random.randint(1, 20):
        souperi[0].zivoty -= random.random() * souperi[1].sila
      souperi[0], souperi[1] = souperi[1], souperi[0] # Obránce se stává útocňíkem a útočník obráncem. 
    if zloun.zivoty <= 0:
      # Zloun byl poražen.
      porazeno_zlounu += 1
      if porazeno_zlounu == 32:
        # Hrdina porazil všech 32 zlounů.
        print("HRDINA VYHRÁL!!! ƪ(˘⌣˘)ʃ")
        mapa[policko] = '╬'
      else:
        mapa[policko] = 'Ø'
        continue
    elif hrdina.zivoty <= 0:
      # Hrdina byl poražen.
      print("HRDINA PROHRÁL... ಥ╭╮ಥ")
      mapa[policko] = '┼'
    break 

# ==== Zobrazení mapy a statistik. ====
# Tohle je snad vše jasné.
print("""==== VYSVĚTLIVKY ====
█ = prázdné pole
░ = prázdné pole, které navštívil hrdina
╬ = hrdina
┼ = poražený hrdina
O = zloun
Ø = poražený zloun
==== MAPA ====""")
for y in range(8):
  for x in range(8):
    print(mapa[x + y * 8], end = ' ')
  print()
print("==== STATISTIKY ====")
print("Počet navštívených políček: ", navstiveno_policek)
print("Počet poražených zlounů:    ", porazeno_zlounu)
