import random

# ==== Generování náhodné mapy. ====
mapa = [['█'] * 8 for sloupec in range(8)] # Matice s rozměry 8*8.
# Umístění 32 zlounů.
umisteno_zlounu = 0
while umisteno_zlounu < 32:
  sloupec = random.randint(0, 7)
  radek = random.randint(0, 7)
  if mapa[sloupec][radek] == '█':
    mapa[sloupec][radek] = 'O'
    umisteno_zlounu += 1

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
  # Operace x & 0xF (0xF je 0b1111 binárně) ponechá první 4 bity čísla x netknuté, zbytek bitů bude 0.
  # To znamená, že pokud by x bylo 0-15, nezmění se, ale když bude negativní změní se na 16 + x.
  # Např.: 5 & 0xF = 5, 8 & 0xF = 8, -1 & 0xF = 15 a -5 & 0xFF = 11.
  # Pokud se tedy hrdina dostane mimo mapu a hrdina.pozice[smer[0]] bude 8, tak 8 & 0xF = 8.
  # Pokud však hrdina.pozice[smer[0]] bude -1 (také mimo mapu), tak -1 & 0xF = 15.
  # Jestli je to stále moc složité, podmínka "if hrdina.pozice[smer[0]] < 0 or hrdina.pozice[smer[0]] > 7" dosáhne stejného efektu.
  if hrdina.pozice[smer[0]] & 0xF > 7:
      hrdina.pozice[smer[0]] -= smer[1] # Vrácení hrdiny zpět na mapu.
  else:
    navstiveno_policek += 1
  if mapa[hrdina.pozice[0]][hrdina.pozice[1]] == '█':
    # Hrdina se dostal na prázdné políčko.
    mapa[hrdina.pozice[0]][hrdina.pozice[1]] = '░'
  elif mapa[hrdina.pozice[0]][hrdina.pozice[1]] == 'O':
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
        mapa[hrdina.pozice[0]][hrdina.pozice[1]] = '╬'
      else:
        mapa[hrdina.pozice[0]][hrdina.pozice[1]] = 'Ø'
        continue
    elif hrdina.zivoty <= 0:
      # Hrdina byl poražen.
      print("HRDINA PROHRÁL... ಥ╭╮ಥ")
      mapa[hrdina.pozice[0]][hrdina.pozice[1]] = '┼'
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
for radek in mapa:
  print(' '.join(radek))
print("==== STATISTIKY ====")
print("Počet navštívených políček: ", navstiveno_policek)
print("Počet poražených zlounů:    ", porazeno_zlounu)
