import segno
import static_variables as const

from pathlib import Path
from loading import load_tasks
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth


def main():

    tasks = load_tasks()

    Path("qr_codes").mkdir(parents=True, exist_ok=True)
    infos = create_qr_codes(tasks)
    with open(const.QR_CODE_PATH_INFO, "w") as file:
        for info in infos:
            file.write("{}|{}\n".format(info[0], info[1]))

    create_pdf()


def create_pdf():

    with open(const.QR_CODE_PATH_INFO, "r") as file:
        data = file.readlines()

    counter = 0
    f_count = 1

    can = canvas.Canvas(const.QR_CODE_PDF_FILE.format(0), pagesize=letter)
    can.setFont(const.QR_CODE_FONT, const.QR_CODE_FONT_SIZE)

    x_start = 36
    y_start = 792
    for line in data:
        line = line.split("|")
        # page full start new one
        if counter == 12:
            counter = 0
            can.save()
            can = canvas.Canvas(const.QR_CODE_PDF_FILE.format(f_count),
                                pagesize=letter
                                )
            can.setFont(const.QR_CODE_FONT, const.QR_CODE_FONT_SIZE)
            f_count += 1
            y_start = 792

        # line full start new one
        if counter % 3 == 0:
            x_start = 36
            y_start -= 192
        img = line[0]
        txt = line[1][:-1]

        can.drawImage(img,
                      x_start,
                      y_start,
                      height=180,
                      preserveAspectRatio=True,
                      mask='auto'
                      )

        text_width = stringWidth(txt,
                                 const.QR_CODE_FONT,
                                 const.QR_CODE_FONT_SIZE
                                 )
        can.drawString((x_start + 90 - (text_width / 2.0)), y_start - 8, txt)

        x_start += 180
        counter += 1

    can.showPage()
    can.save()


def create_qr_codes(tasks):

    infos = []
    for task in tasks:
        txt = tasks[task]['name']
        path_to_file = const.QR_CODE_PATH_IMG + "{}.png".format(task)
        infos.append((path_to_file, txt))

        qrcode = segno.make_qr(
                const.QR_CODE_BASE_ADDRESS.format(task),
                )
        qrcode.save(
                path_to_file,
                scale=5,
                )
    return infos


if __name__ == '__main__':
    main()
