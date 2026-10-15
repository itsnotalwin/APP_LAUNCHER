#!/usr/bin/env python3
"""Launchpad app icons from the same procedural blob artwork. Run after generate_blobs.py."""
from PIL import Image, ImageDraw
from generate_blobs import make, HERO

def art():
    S = 1024; L = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for i in range(8):
        for j in range(8): d.ellipse((130+i*54-6.5, 140+j*54-6.5, 130+i*54+6.5, 140+j*54+6.5), fill=(11, 11, 11, 150))
    b = make(HERO, (1000, 860), 640, 31); L.alpha_composite(b, (300, 330))
    A = Image.new('RGBA', (S*3, S*3), (0, 0, 0, 0)); a = ImageDraw.Draw(A); k = 3; w = 46*k
    for pts in [[(570, 690), (715, 545)], [(610, 545), (715, 545), (715, 650)]]:
        P = [(x*k, y*k) for x, y in pts]; a.line(P, fill=(255, 255, 255, 255), width=w, joint='curve')
        for x, y in P: a.ellipse((x-w/2, y-w/2, x+w/2, y+w/2), fill=(255, 255, 255, 255))
    L.alpha_composite(A.resize((S, S), Image.LANCZOS)); return L

def compose(kind):
    S = 1024; A = art()
    if kind == 'any':
        base = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(base)
        d.rounded_rectangle((2, 2, S-3, S-3), 224, fill=(255, 255, 255, 255), outline=(217, 217, 217, 255), width=4); base.alpha_composite(A); return base
    f = .8 if kind == 'maskable' else .9
    base = Image.new('RGBA', (S, S), (255, 255, 255, 255)); n = int(S*f)
    base.alpha_composite(A.resize((n, n), Image.LANCZOS), ((S-n)//2, (S-n)//2)); return base

for name, kind, size in [('icon-192.png', 'any', 192), ('icon-512.png', 'any', 512), ('icon-maskable.png', 'maskable', 512), ('apple-touch-icon.png', 'apple', 180)]:
    compose(kind).resize((size, size), Image.LANCZOS).save('../'+name, optimize=True)
