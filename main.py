from Debt import Debt
while (1):
  print(
    "Podaj dane kredytu: \nwartość, miesiące, opr. roczne(%), prowizja(%) \n(oddzielone spacją, cz.dziesiętne oddzielane kropką)"
  )
  p, m, ir, c = input().split()
  d = Debt(float(p), int(m), float(ir), float(c))

  while (1):
    try:
      m, v = input("Dodaj nadpłatę(miesiąc, wartość) (Oddzielone spacją, Enter by kontynuować)").split()
    except ValueError:
      break
    else:
      d.addOverpayment(int(m), float(v))
  while (1):
    try:
      m, v = input("Dodaj zmianę oprocentowania(miesiąc, procent) (Oddzielone spacją, Enter by kontynuować)").split()
    except ValueError:
      break
    else:
      d.addInterestChange(int(m), float(v))
  d.fixedRate()
  d.variableRate()