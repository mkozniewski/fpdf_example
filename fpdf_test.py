# -*- coding: utf-8 -*-
import os
from math import ceil

from fpdf import FPDF

# ja używam tych czcionek OpenType - program je widzi kiedy plik wygląda w ten sposób
# natomist się krzaczy kiedy używam wbudowanych modułów header alfo footer

# Marcin(M): musiałem trochę zmodyfikować przykład by doprowadzić go do stanu używalności

# M: u mnie coś nie łapało czcionek więc je sobie na sztywno wrzuciłem - zmieniłem u siebie katalog
#    tylko po to żeby u mnie działało jakkolwiek
OpenSans = 'OpenSans\OpenSans-Regular.ttf'
OpenSansB = 'OpenSans\OpenSans-Bold.ttf'
OpenSansI = 'OpenSans\OpenSans-Italic.ttf'
OpenSansBI = 'OpenSans\OpenSans-Regular.ttf'


class PDF(FPDF):
    # M: meritum całego problemu znajduje się tutaj. Potrzeba utworzyć konstruktor
    #    klasy który doda czcionki przy tworzeniu obiektu PDF do tego obiektu
    #    dalej potem już tylko przeciążamy footer() i header() i powinnny działać z
    #    każdym wywołaniem add_page() na tym obiekcie
    def __init__(self, orientation = 'P', unit = 'mm', format='A4'):
        FPDF.__init__(self, orientation, unit, format)

        self.add_font('MyFont', '', OpenSans, uni=True) # M: u mnie nie chciało ładować czcionki gdy brakowało uni
        self.add_font('MyFont', 'B', OpenSansB, uni=True)
        self.add_font('MyFont', 'I', OpenSansI, uni=True)
        self.add_font('MyFont', 'BI', OpenSansBI, uni=True)

    def checker(self, checkIT, y, cell_height, cell_width):
        try:
            number_of_lines = ceil(len(checkIT) / (cell_width / 1.57))  # średnio 95 znaków w linii
            height_of_cell = ceil(number_of_lines * cell_height)
            page_height = 277  # mm
            bottom_margin = 18  # mm
            space_left = page_height - y  # // space left on page
            space_left -= bottom_margin  # // less the bottom margin
            if height_of_cell >= space_left:  # brak miejsca, buduje się nowa strona.
                return ">="
            elif height_of_cell < space_left:
                return "<"
        except:
            print("Checker ERROR")

    def raport(self):

        # Create a PDF object
        pdf = PDF('P', 'mm', 'A4')

        # Add page
        pdf.set_margins(15, 20, 15)
        pdf.set_auto_page_break(False)
        pdf.add_page()

        # to na przykład miało by być w HEADER ------------ stąd 
        pdf.set_xy(20, 12)
        pdf.set_font('MyFont', '', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(w=170, h=4, txt=f"Formularz nr xxx", align='R', border=0)
        pdf.ln(7)

        pdf.set_font('MyFont', '', 10)
        pdf.cell(w=100)
        pdf.cell(w=70, txt=f'Kuria Metropolitarna', align="L", border=0)
        pdf.ln(7)
        pdf.cell(w=100)
        pdf.cell(w=70, txt=f'w Białymstoku', align="L", border=0)
        pdf.ln(12)

        pdf.set_font('MyFont', 'B', 12)
        pdf.multi_cell(w=180, align='C', txt=f'Nagłówek', h=5)
        pdf.ln(10)

        # -------------  aż dotąd 
        
        # --------- tu zaczyna się body 
        
        line_height = pdf.font_size
        wynik = ((f'test1.1', f'test1.2', f'test1.3'),
                 (f'test2.1', f'test2.2', f'test2.3'),
                 (f'test3.1', f'test3.2', f'test3.3'),
                 (f'test4.1', f'test4.2', f'test4.3'),
                 (f'test5.1', f'test5.2', f'test5.3'),
                 )
        for dana in wynik:
            x = pdf.get_x()
            y = pdf.get_y()
            pdf.set_font('MyFont', 'I', 9)
            pdf.multi_cell(w=50, border='RTL', txt=f'', align='L', h=2)
            pdf.set_xy(x + 50, y)
            pdf.multi_cell(w=65, border='RTL', txt=f'', align='C', h=2)
            pdf.set_xy(x + 115, y)
            pdf.multi_cell(w=65, border='RTL', txt=f'', align='C', h=2)
            pdf.ln(0)
            wynik = (dana[0], dana[1], dana[2])
            x = pdf.get_x()
            y = pdf.get_y()
            pdf.set_font('MyFont', 'I', 9)
            pdf.multi_cell(w=50, border='RL', txt=f'{wynik[0]}', align='L', h=line_height + 2)
            h1 = pdf.get_y() - y
            pdf.set_xy(x + 50, y)
            pdf.set_font('MyFont', 'B', 11)
            pdf.multi_cell(w=65, border='RL', txt=f'{wynik[1]}', align='C', h=line_height + 2)
            h2 = pdf.get_y() - y
            pdf.set_xy(x + 115, y)
            pdf.set_font('MyFont', 'B', 11)
            pdf.multi_cell(w=65, border='RL', txt=f'{wynik[2]}', align='C', h=line_height + 2)
            h3 = pdf.get_y() - y
            pdf.ln(0)
            new_h = max(h1, h2, h3) + 4
            pdf.set_xy(x, y)
            pdf.set_font('MyFont', 'I', 7)
            pdf.multi_cell(w=50, border='RBL', txt='', align='L', h=new_h - 1)
            pdf.set_xy(x + 50, y)
            pdf.multi_cell(w=65, border='RBL', txt='', align='C', h=new_h - 1)
            pdf.set_xy(x + 115, y)
            pdf.multi_cell(w=65, border='RBL', txt='', align='C', h=new_h - 1)
            pdf.ln(0)

        pdf.ln(line_height / 2)

        # Uzasadnienie prośby, cz. 1
        y = pdf.get_y()
        test = "Z Teleskopu Webba na Ziemię zaczęły trafiać pierwsze zdjęcia przestrzeni kosmicznej oraz dane spektroskopowe. Gdy będziemy oglądać fascynujące obrazy warto pamiętać, " \
               "że pochodzą one z urządzenia, które znajduje się niemal 3000 razy dalej od Ziemi niż Teleskop Hubble'a. Warto więc dowiedzieć się,... "
        if PDF.checker(self, test, y, 5, 150) == ">=":
            pdf.set_y(-18)
            pdf.set_font('MyFont', '', 8)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(w=180, txt=f'NupT 1.0 ® © by xmslyz', align='R')
            pdf.set_text_color(0)
            pdf.add_page()  # // page break.
            pdf.set_font('MyFont', '', 7)
            pdf.cell(w=180, h=5, border=0, align="R", txt=f'Formularz XXX [strona {pdf.page_no()} z {pdf.pages_count}]')
            pdf.ln(10)
            pdf.set_font('MyFont', '', 11)
            pdf.multi_cell(w=180, border=0, txt=f'{test}', align='J', h=line_height + 2)
            pdf.ln(2)
        else:
            pdf.set_font('MyFont', '', 11)
            pdf.multi_cell(w=180, border=0, txt=f'{test}', align='J', h=line_height + 2)
            pdf.ln(2)
        
        # - ---------- koniec body

        # M: Footer wyniosłem do przeciążonej metody footer()
        # ---- początek footera
        
        #pdf.set_y(-18)
        #pdf.set_font('MyFont', '', 8)
        #pdf.set_text_color(100, 100, 100)
        #pdf.cell(w=180, txt=f'NupT 1.0 ® © by xmslyz', align='R')

        # M: dodaję kilka stron dla demonstracji
        pdf.add_page()
        pdf.add_page()

        # no i hop, rób plik
    
        # M: zdejmuje osłonkę, żeby zobaczyć na co narzeka przy generowaniu PDFa
        #try:
        pdf.output('FORM.pdf')
        #except:
            #print("Nie wyszło")

    # M: przeciążona metoda footer() wywoływana podczas wywołania add_page()
    def footer(self):
        # ---- początek footera

        self.set_y(-18)
        self.set_font('MyFont', '', 8)
        self.set_text_color(100, 100, 100)
        self.cell(w=180, txt=f'NupT 1.0 ® © by xmslyz', align='R')

# M: cokolwiek co wygeneruje mi przykładowy raport
#    najpierw tworzymy obiekt PDF
pdf = PDF('P', 'mm', 'A4')
# M: generujemy raport
pdf.raport()

