import segno
import yaml

from pathlib import Path
from loading import load_tasks
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth

BASE_ADDRESS = "http://192.168.178.68:5000/tasks/{}"
pdf_file = 'qr_codes/qr_codes{}.pdf'
PATH_INFO = 'qr_codes/info'
FONT = 'Helvetica'
FONT_SIZE = 21
PATH_IMG = "qr_codes/"

def main():

    tasks = load_tasks()
    tasks = tasks['no_prep'] | tasks['once_prep'] | tasks['always_prep']

    Path("qr_codes").mkdir(parents=True, exist_ok=True)
    infos = create_qr_codes(tasks)
    with open(PATH_INFO, "w") as file:
        for info in infos:
            file.write("{}|{}\n".format(info[0], info[1]))
    
    create_pdf()

def create_pdf():

    with open(PATH_INFO, "r") as file:
        data = file.readlines()

    counter = 0
    f_count = 1

    can = canvas.Canvas(pdf_file.format(0), pagesize=letter)
    can.setFont(FONT, FONT_SIZE) #choose your font type and font size

    x_start = 36
    y_start = 792
    for line in data:
        line = line.split("|")
        # page full start new one
        if counter == 12:
            counter = 0
            can.save()
            can = canvas.Canvas(pdf_file.format(f_count), pagesize=letter)
            can.setFont(FONT, FONT_SIZE) #choose your font type and font size
            f_count += 1
            y_start = 792
        
        # line full start new one
        if counter % 3 == 0:
            x_start = 36
            y_start -= 192
        img = line[0]
        txt = line[1][:-1]

        can.drawImage(img, x_start, y_start, height=180, preserveAspectRatio=True, mask='auto')
        
        text_width = stringWidth(txt, FONT, FONT_SIZE)
        can.drawString((x_start + 90 - (text_width / 2.0)), y_start - 8, txt)

        x_start += 180
        counter += 1

    can.showPage()
    can.save()

def create_qr_codes(tasks):

    infos = []
    for task in tasks:
        txt = tasks[task]['name']
        path_to_file = "qr_codes/{}.png".format(task)
        infos.append((path_to_file, txt))

        qrcode = segno.make_qr(
                BASE_ADDRESS.format(task),
                )
        qrcode.save(
                path_to_file,
                scale=5,
                )
    return infos


if __name__=='__main__':
    main()
