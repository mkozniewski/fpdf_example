# -*- coding: utf-8 -*-

from math import ceil
from fpdf import FPDF

OpenSans = 'OpenSans\OpenSans-Regular.ttf'
OpenSansB = 'OpenSans\OpenSans-Bold.ttf'
OpenSansI = 'OpenSans\OpenSans-Italic.ttf'
OpenSansBI = 'OpenSans\OpenSans-Regular.ttf'

# takie klasy można potworzyć dla każdego rodzaju formularza
# lub różne metody raportów
class PDF(FPDF):
    # M: meritum całego problemu znajduje się tutaj. Potrzeba utworzyć konstruktor
    #    klasy który doda czcionki przy tworzeniu obiektu PDF do tego obiektu
    #    dalej potem już tylko przeciążamy footer() i header() i powinnny działać z
    #    każdym wywołaniem add_page() na tym obiekcie
    #    ustawiamy też domyślne parametry wiec łątiwej generować bedzie nowy obiekt PDF
    def __init__(self, orientation = 'P', unit = 'mm', format='A4'):
        FPDF.__init__(self, orientation, unit, format)

        self.add_font('MyFont', '', OpenSans, uni=True) # M: u mnie nie chciało ładować czcionki gdy brakowało uni
        self.add_font('MyFont', 'B', OpenSansB, uni=True)
        self.add_font('MyFont', 'I', OpenSansI, uni=True)
        self.add_font('MyFont', 'BI', OpenSansBI, uni=True)

        # proponuje dodać pola do klasy jak ponieżej i później je modyfikować w zależności czego
        # wymaga formularz
        self.formNumber = "XXX/XX/XXX"
        self.textToPut = "Vacua"
        self.dataToPut = ["Vacua"]

    def header(self):
        self.set_xy(20, 12)
        self.set_font('MyFont', '', 10)
        self.set_text_color(0, 0, 0)
        self.cell(w=170, h=4, txt=f"Formularz nr {self.formNumber}", align='R', border=0)
        self.ln(7)

    def footer(self):
        self.set_y(-18)
        self.set_font('MyFont', '', 8)
        self.set_text_color(100, 100, 100)
        self.cell(w=180, txt=f'Teścik 1.0 ® © by dobrzy ludzie', align='R')

    def generujRaportX(self):
        # zamiast na obiekcie (który tworzymy) działamy na self
        self.set_margins(15, 20, 15)
        self.set_auto_page_break(False)
        self.add_page()

        # coś dodaję
        self.set_xy(10, 15)
        self.set_font('MyFont', '', 10)
        self.set_text_color(0, 0, 0)
        self.cell(w=170, h=4, txt=f'{self.textToPut}', align='L', border=0)
        self.ln(7)

        for i in range(len(self.dataToPut)):
            self.cell(w=170, h=4, txt=f'{self.dataToPut[i]}', align='L', border=0)
            if i>0:
                self.add_page()
                self.set_xy(10, 22)

