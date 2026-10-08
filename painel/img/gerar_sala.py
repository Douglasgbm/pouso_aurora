"""Gera sala.png a partir de sala.jpg com o vidro da janela transparente.

O canvas do painel fica atrás da imagem e aparece pelo vidro; a moldura e o
monitor da mesa continuam na frente. Coordenadas em pixels da arte (1344x768).
"""
from pathlib import Path
from PIL import Image, ImageDraw

AQUI = Path(__file__).parent
VIDRO = (374, 170, 961, 467)  # retângulo interno da janela
RAIO = 22
MONITOR = [(471, 470), (471, 432), (480, 424), (488, 419),
           (630, 417), (636, 424), (636, 470)]

arte = Image.open(AQUI / "sala.jpg").convert("RGBA")
mascara = Image.new("L", arte.size, 255)
d = ImageDraw.Draw(mascara)
d.rounded_rectangle(VIDRO, radius=RAIO, fill=0)
d.polygon(MONITOR, fill=255)
arte.putalpha(mascara)
arte.save(AQUI / "sala.png", optimize=True)
print("sala.png:", arte.size)
