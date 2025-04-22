import matplotlib.pyplot as plt
import io
import qrcode
import base64

# 1. Create a Matplotlib figure
fig, ax = plt.subplots()
ax.plot([0, 1], [0, 1])
ax.set_title("Sample SVG Plot")

# 2. Save it as SVG in memory
svg_io = io.StringIO()
fig.savefig(svg_io, format='svg')
svg_data = svg_io.getvalue()
plt.close(fig)

# 3. Convert SVG to base64 and create a data URI
svg_base64 = base64.b64encode(svg_data.encode('utf-8')).decode('utf-8')
data_uri = f"data:image/svg+xml;base64,{svg_base64}"

# 4. Generate QR code
qr = qrcode.make(data_uri)

# 5. Save or show QR code
qr.save("svg_qrcode.png")
qr.show()
