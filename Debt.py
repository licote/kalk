class en:
    MONTH = 0
    AMOUNT = 1

class Debt:
  def __init__(self, principal, months, rate, commission): #wartość, miesiące, oprocentowanie, prowizja
    self.principal = principal
    self.months = months
    self.rate = rate/100
    self.commission = commission/100
    self.overpayments = []
    self.interestChanges = []

  def calculateInstallment(self, principal, months, rate):
    #principal, months, interest rate
    #returns an installment of a fixed-rate loan
    #https://pl.wikipedia.org/wiki/Raty_r%C3%B3wne
    denominator = 0.0
    for i in range(1, months + 1):
      denominator += pow((1 + rate / 12), -i)
    return principal / denominator

  def fixedRate(self):  #rata stała
    #returns an array of (principal, interest) parts of each fixed-rate installment
    #https://www.bankoweabc.pl/2021/04/05/jak-obliczyc-rate-kredytu/
    #https://www.allianz.pl/pl_PL/poradniki/dom-i-mieszkanie/jak-obliczyc-rate-kredytu-hipotecznego.html
    principal = self.principal
    months = self.months
    rate = self.rate
    commission = self.commission
    arrayOfInstallments = []
    totalCost = 0.0  #koszt całkowity
    debtBalance = 0.0  #saldo kredytu
    installment = self.calculateInstallment(principal, months, rate)
    print("--- \n Raty stałe \n--- \n")
    print("kapit.   ods.      całk.     nr raty")
    for month in range(1, months + 1):
      for op in self.overpayments: #nadpłaty
        if month == op[en.MONTH]:
          principal -= op[en.AMOUNT]
          installment = self.calculateInstallment(principal, months + 1 - month, rate)
          print("Nadpłata - " + str(op[en.AMOUNT]))
      for ic in self.interestChanges: #zmiany oprocentowania
        if month == ic[en.MONTH]:
          oldrate = rate
          rate = ic[en.AMOUNT]/100
          installment = self.calculateInstallment(principal, months + 1 - month, rate)  
          print("Zmiana oprocentowania  - " + str(round(oldrate,4)) + " --> " + str(rate))
      interestSide = principal * rate * 1 / 12  #cz. odsetkowa
      principalSide = installment - interestSide  #cz. kapitalowa
      totalCost += interestSide + principalSide  #koszt całkowity
      debtBalance += principalSide  #saldo kredytu
      principal *= 1 + rate / 12
      principal -= interestSide + principalSide
      #arrayOfInstallments.append(["{:.2f}".format(principalSide), "{:.2f}".format(interest)])
      print("{:.2f}".format(principalSide) + "  "\
          + "{:.2f}".format(interestSide) + "    "\
          + "{:.2f}".format(interestSide+principalSide) + "    "\
          + str(month))
    print("Saldo kredytu: " + "{:.2f}".format(debtBalance))
    print("Koszt całkowity:  " + "{:.2f}".format(totalCost) + " (+ " + "{:.2f}".format(debtBalance*(commission)) +" prowizji)\n")
    return (arrayOfInstallments)

  def variableRate(self):
    #principal, months, interest rate
    #returns an array of (principal, interest) parts of each variable-rate installment
    #https://www.bankoweabc.pl/2021/04/05/jak-obliczyc-rate-kredytu/
    principal = self.principal
    months = self.months
    rate = self.rate
    commission = self.commission
    arrayOfInstallments = []
    totalCost = 0.0  #koszt całkowity
    debtBalance = 0.0  #saldo kredytu
    principalSide = principal / months  #cz. kapitałowa
    print("--- \n Raty malejące \n--- \n")
    print("kapit.   ods.      całk.     nr raty")
    for month in range(1, months + 1):
      for overpayment in self.overpayments:  #nadpłaty
        if month == overpayment[en.MONTH]:
          principal -= overpayment[en.AMOUNT]
          principalSide = self.calculateInstallment(principal, months + 1 - month, 0)
          print("Nadpłata - " + str(overpayment[en.AMOUNT]))
      for ic in self.interestChanges: #zmiany oprocentowania
        if month == ic[en.MONTH]:
          oldrate = rate
          rate = ic[en.AMOUNT]/100
          print("Zmiana oprocentowania  - " + str(round(oldrate,4)) + " --> " + str(rate))
      '''
      Faster
      for overpayment in self.overpayments:
        if month == overpayment[0]:
          principal -= overpayment[1]
          principalSide = principal / (months + 1 - month)
          print("OVERPAYMENT - " + str(overpayment[1]))
      '''
      interestSide = principalSide - principal / (months + 1 -month) + rate * principal / 12  #cz. odsetkowa
      totalCost += interestSide + principalSide  #koszt całkowity
      debtBalance += principalSide  #saldo kredytu
      principal *= 1 + rate / 12
      principal -= interestSide + principalSide
      #arrayOfInstallments.append(["{:.2f}".format(principalSide), "{:.2f}".format(interest)])
      print("{:.2f}".format(principalSide) + "  "\
          + "{:.2f}".format(interestSide) + "    "\
          + "{:.2f}".format(interestSide+principalSide) + "    "\
          + str(month))
    print("Saldo kredytu: " + "{:.2f}".format(debtBalance))
    print("Koszt całkowity:  " + "{:.2f}".format(totalCost) + " (+ " + "{:.2f}".format(debtBalance*(commission)) +" prowizji)\n")
    return arrayOfInstallments

  def addOverpayment(self, month, amount):
    self.overpayments.append([month, amount])

  def addInterestChange(self, month, amount):
    self.interestChanges.append([month, amount])
