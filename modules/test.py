import qrcode

# Data to be encoded
data = "https://mole-pretty-primarily.ngrok-free.app/"

# Create a QR code instance
qr = qrcode.QRCode(
    version=1,  # Control the size of the QR Code (1-40)
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
    box_size=10,  # Size of each box in the QR code
    border=4,  # Border thickness
)

# Add data
qr.add_data(data)
qr.make(fit=True)

# Create and save the image
img = qr.make_image(fill="black", back_color="white")
img.save("qrcode.png")

# Show the QR code
img.show()
