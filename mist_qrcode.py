import qrcode

def generate_qrcode(ssid, psk):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data("WIFI:T:WPA;S:{0};P:{1};;".format(ssid, psk))
    qr.make(fit=True)
    return qr.get_matrix()