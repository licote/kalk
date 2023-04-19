class Debt:
  def __init__(self, principal, months, rate):
    self.principal = principal
    self.months = months
    self.rate = rate/100
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
    arrayOfInstallments = []
    totalCost = 0.0  #koszt całkowity
    debtBalance = 0.0  #saldo kredytu
    installment = self.calculateInstallment(self.principal, self.months, self.rate)
    for month in range(1, self.months + 1):
      for overpayment in self.overpayments:
        if month == overpayment[0]:
          self.principal -= overpayment[1]
          installment = self.calculateInstallment(self.principal, self.months + 1 - month, self.rate)
          print("Nadpłata - " + str(overpayment[1]))
      for ic in self.interestChanges:
        if month == ic[0]:
          oldrate = self.rate
          self.rate = ic[1]
          installment = self.calculateInstallment(self.principal, self.months + 1 - month, self.rate)
          print("Zmiana oprocentowania  - " + str(oldrate) + " --> " + str(self.rate))
      interestSide = self.principal * self.rate * 1 / 12  #cz. odsetkowa
      principalSide = installment - interestSide  #cz. kapitalowa
      totalCost += interestSide + principalSide  #koszt całkowity
      debtBalance += principalSide  #saldo kredytu
      self.principal *= 1 + self.rate / 12
      self.principal -= interestSide + principalSide
      #arrayOfInstallments.append(["{:.2f}".format(principalSide), "{:.2f}".format(interest)])
      print("{:.2f}".format(principalSide) + "  "\
          + "{:.2f}".format(interestSide) + "    "\
          + "{:.2f}".format(interestSide+principalSide) + "    "\
          + str(month))
    print("Saldo kredytu: " + "{:.2f}".format(debtBalance))
    print("Koszt całkowity:  " + "{:.2f}".format(totalCost) +"\n")
    return (arrayOfInstallments)

  def variableRate(self):
    #principal, months, interest rate
    #returns an array of (principal, interest) parts of each variable-rate installment
    #https://www.bankoweabc.pl/2021/04/05/jak-obliczyc-rate-kredytu/
    arrayOfInstallments = []
    totalCost = 0.0  #koszt całkowity
    debtBalance = 0.0  #saldo kredytu
    principalSide = self.principal / self.months  #cz. kapitałowa
    for month in range(1, self.months + 1):
      for overpayment in self.overpayments:
        if month == overpayment[0]:
          self.principal -= overpayment[1]
          principalSide = self.calculateInstallment(self.principal, self.months + 1 - month, 0)
          print("Nadpłata - " + str(overpayment[1]))
      '''
      Faster
      for overpayment in self.overpayments:
        if month == overpayment[0]:
          self.principal -= overpayment[1]
          principalSide = self.principal / (self.months + 1 - month)
          print("OVERPAYMENT - " + str(overpayment[1]))
      '''
      interestSide = principalSide - self.principal / (self.months + 1 -month) + self.rate * self.principal / 12  #cz. odsetkowa
      totalCost += interestSide + principalSide  #koszt całkowity
      debtBalance += principalSide  #saldo kredytu
      self.principal *= 1 + self.rate / 12
      self.principal -= interestSide + principalSide
      #arrayOfInstallments.append(["{:.2f}".format(principalSide), "{:.2f}".format(interest)])
      print("{:.2f}".format(principalSide) + "  "\
          + "{:.2f}".format(interestSide) + "    "\
          + "{:.2f}".format(interestSide+principalSide) + "    "\
          + str(month))
    print("Saldo kredytu: " + "{:.2f}".format(debtBalance))
    print("Koszt całkowity: " + "{:.2f}".format(totalCost) + "\n")
    return arrayOfInstallments

  def addOverpayment(self, month, amount):
    self.overpayments.append([month, amount])

  def addInterestChange(self, month, amount):
    self.interestChanges.append([month, amount])
