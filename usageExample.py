from MyPDF import PDF

# poniższy kod może się znaleźć w jakiejś metodzie lub funkjcji gdzie dane są
# czytane czy to z bazy danych czy z formularza aplikacji
# i wstawiane do pól obiektu klasy MyPDF

pdf = PDF()
#ustawiamy wartość pola które zdefiniowaliśmy żeby nie było x-ami
pdf.formNumber = "777/12/144"
pdf.textToPut = "Przykład"
pdf.dataToPut = ["Jest szansa, że zadziała", "Może być różnie", "Memento mori"]
pdf.generujRaportX()
pdf.output('plik.pdf')
