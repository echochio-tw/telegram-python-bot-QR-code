#!/usr/bin/python
import qrcode,sys

qr = qrcode.QRCode(
    version = 1,
    error_correction = qrcode.constants.ERROR_CORRECT_H,
    box_size = 10,
    border = 4,
)

host=sys.argv[1]
qr.add_data(host)
qr.make(fit=True)
img = qr.make_image()
img.save("/tmp/photo.png")
