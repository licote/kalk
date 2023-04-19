def calculateInstallment(principal: float, months: int, rate: float):
  #principal, months, interest rate
  #returns an installment of a fixed-rate loan
  #https://pl.wikipedia.org/wiki/Raty_r%C3%B3wne
  denom = 0.0
  for i in range(1, months + 1):
    denom += pow((1 + rate / 12), -i)
  return principal / denom

def fixedRate(principal: float, months: int, rate: float):  #rata stała
  #principal, months, interest rate
  #returns an array of (principal, interest) parts of each fixed-rate installment
  #https://www.bankoweabc.pl/2021/04/05/jak-obliczyc-rate-kredytu/
  #https://www.allianz.pl/pl_PL/poradniki/dom-i-mieszkanie/jak-obliczyc-rate-kredytu-hipotecznego.html
  arrayOfInstallments = []
  totalCost = 0.0 #koszt całkowity
  debtBalance = 0.0 #saldo kredytu
  installment = calculateInstallment(principal, months, rate)
  for month in range(1, months + 1):
    if (month == 25):  #nadpłata
      overpayment = 5000
      principal -= overpayment
      installment = calculateInstallment(principal, months + 1 - month, rate)
      print("OVERPAYMENT - " + str(overpayment))
    if (month == 35):  #zmiana oprocentowania
      oldrate = rate
      rate = 0.03
      installment = calculateInstallment(principal, months + 1 - month, rate)
      print("INTEREST RATE CHANGE  - " + str(oldrate) + " --> " + str(rate))
    interestSide = principal * rate * 1 / 12  #cz. odsetkowa
    principalSide = installment - interestSide  #cz. kapitalowa
    totalCost += interestSide + principalSide #koszt całkowity
    debtBalance += principalSide #saldo kredytu
    principal *= 1 + rate / 12
    principal -= interestSide + principalSide
    #arrayOfInstallments.append(["{:.2f}".format(principalSide), "{:.2f}".format(interest)])
    print("{:.2f}".format(principalSide) + "  "\
        + "{:.2f}".format(interestSide) + "    "\
        + "{:.2f}".format(interestSide+principalSide) + "    "\
        + str(month))
  print("Saldo kredytu: " + "{:.2f}".format(debtBalance))
  print("Koszt całkowity: " + "{:.2f}".format(totalCost))
  return (arrayOfInstallments)


def variableRate(principal: float, months: int, rate: float):
  #principal, months, interest rate
  #returns an array of (principal, interest) parts of each variable-rate installment
  #https://www.bankoweabc.pl/2021/04/05/jak-obliczyc-rate-kredytu/
  arrayOfInstallments = []
  totalCost = 0.0 #koszt całkowity
  debtBalance = 0.0 #saldo kredytu
  principalSide = principal / months  #cz. kapitałowa
  for month in range(1, months + 1):
    if (month == 250 or month == 350):  #nadpłata
      overpayment = 5000
      principal -= overpayment
      principalSide = calculateInstallment(principal, months + 1 - month, 0.0)
      print("OVERPAYMENT - " + str(overpayment))
    '''  
    Faster
    if (month == 25):  #nadpłata
      principal -= 5000
      principalSide = principal / (months + 1 - month)
      print("---")
    '''
    interestSide = principalSide - principal / (months + 1 - month) + rate * principal / 12  #cz. odsetkowa
    totalCost += interestSide + principalSide #koszt całkowity
    debtBalance += principalSide #saldo kredytu
    principal *= 1 + rate / 12
    principal -= interestSide + principalSide
    #arrayOfInstallments.append(["{:.2f}".format(principalSide), "{:.2f}".format(interest)])
    print("{:.2f}".format(principalSide) + "  "\
        + "{:.2f}".format(interestSide) + "    "\
        + "{:.2f}".format(interestSide+principalSide) + "    "\
        + str(month))
  print("Saldo kredytu: " + "{:.2f}".format(debtBalance))
  print("Koszt całkowity: " + "{:.2f}".format(totalCost))
  return arrayOfInstallments


variableRate(50000, 60, 0.072)
fixedRate(50000, 60, 0.072)
