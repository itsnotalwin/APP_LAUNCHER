#!/usr/bin/env python3
"""Procedural distressed-black blob artwork for Launchpad (original work, no external imagery).
Run: python3 generate_blobs.py   ->  blob-hero.webp, blob-detail.webp, pale-paths.txt"""
import numpy as np, math
from PIL import Image, ImageDraw
from scipy.ndimage import gaussian_filter, distance_transform_edt

def spline(pts, n=48):
    P = np.array(pts, float); N = len(P); out = []
    for i in range(N):
        p0, p1, p2, p3 = P[i-1], P[i], P[(i+1) % N], P[(i+2) % N]
        for t in np.linspace(0, 1, n, endpoint=False):
            out.append(.5*(2*p1 + (-p0+p2)*t + (2*p0-5*p1+4*p2-p3)*t*t + (-p0+3*p1-3*p2+p3)*t**3))
    return np.array(out)

def silhouette(pts, W, H, ss=3):
    im = Image.new('L', (W*ss, H*ss), 0)
    ImageDraw.Draw(im).polygon([tuple(p*ss) for p in spline(pts)], fill=255)
    return np.asarray(im.resize((W, H), Image.LANCZOS), float)/255

def chalk(W, H, m, seed, scratches=1200, dust=.011):
    r = np.random.default_rng(seed)
    nz = lambda s: (lambda n: n/n.std())(gaussian_filter(r.standard_normal((H, W)), s))
    v = 21 + nz(W*.09)*3.6 + nz(W*.03)*2.8 + nz(W*.012)*3.4 + nz(W*.006)*2.6 + r.standard_normal((H, W))*4.6 + gaussian_filter(r.standard_normal((H, W)), 1.1)*12
    v += np.clip(nz(W*.045)-.2, 0, None)*8.0
    dens = np.clip(.45 + .55*np.clip(nz(W*.06), -.8, 1.6), .05, None)
    wear = np.exp(-distance_transform_edt(m > .5)/(W*.05))
    ys, xs = np.nonzero(r.random((H, W)) < dust*dens*(1 + 1.4*wear))
    S = np.zeros((H, W)); S[ys, xs] = np.minimum(26 + r.pareto(1.6, len(ys))*24, 150)
    v += gaussian_filter(S, .85)*2.9
    ss = 2; sc = Image.new('L', (W*ss, H*ss), 0); d = ImageDraw.Draw(sc)
    th0 = r.uniform(0, math.pi); flat = np.flatnonzero((m > .5).ravel())
    for _ in range(scratches*2):
        y, x = divmod(int(r.choice(flat)), W)
        if r.random() > dens[y, x]/1.2: continue
        th = th0 + r.normal(0, .5) if r.random() < .65 else r.uniform(0, math.pi)
        L = float(np.clip(r.lognormal(2.2, .5), 4, 40)); bend = r.normal(0, L*.12)
        dx, dy = math.cos(th)*L/2, math.sin(th)*L/2
        mx, my = x - math.sin(th)*bend, y + math.cos(th)*bend
        d.line([((x-dx)*ss, (y-dy)*ss), (mx*ss, my*ss), ((x+dx)*ss, (y+dy)*ss)],
               fill=int(r.uniform(22, 70)), width=1 if r.random() < .8 else 2)
    v += np.asarray(sc.resize((W, H), Image.LANCZOS), float)*.9
    yy, xx = np.mgrid[:H, :W]
    v += 4*np.exp(-(((xx-W*.32)/(W*.35))**2 + ((yy-H*.28)/(H*.35))**2))
    g = np.clip(v, 0, 255).astype(np.uint8)
    return Image.fromarray(np.dstack([g, g, g, (m*255).astype(np.uint8)]), 'RGBA')

HERO = [(640,55),(850,70),(985,230),(1000,430),(930,640),(760,770),(540,820),(320,790),(150,680),(55,520),(70,390),(190,310),(290,285),(360,215),(450,120),(540,65)]
DETAIL = [(150,170),(260,70),(400,50),(500,88),(575,118),(655,82),(790,70),(880,160),(870,300),(780,420),(600,480),(400,500),(220,460),(90,370),(50,260)]

def make(pts, base, W, seed, **kw):
    k = W/base[0]; m = silhouette([(x*k, y*k) for x, y in pts], W, int(base[1]*k), 3)
    return chalk(W, m.shape[0], m, seed, **kw)

def pale_path(cx, cy, R, seed, n=8):
    r = np.random.default_rng(seed)
    P = [(cx+R*(1+r.uniform(-.14, .14))*math.cos(2*math.pi*i/n+r.uniform(-.12, .12)),
          cy+R*(1+r.uniform(-.14, .14))*math.sin(2*math.pi*i/n+r.uniform(-.12, .12))) for i in range(n)]
    P = np.array(P); d = f"M{P[0][0]:.0f} {P[0][1]:.0f}"
    for i in range(n):
        p0, p1, p2, p3 = P[i-1], P[i], P[(i+1) % n], P[(i+2) % n]
        a, b = p1+(p2-p0)/6, p2-(p3-p1)/6
        d += f"C{a[0]:.0f} {a[1]:.0f} {b[0]:.0f} {b[1]:.0f} {p2[0]:.0f} {p2[1]:.0f}"
    return d+"Z"

if __name__ == '__main__':
    make(HERO, (1000, 860), 1000, 11).save('blob-hero.webp', 'WEBP', quality=80, method=6)
    make(DETAIL, (900, 520), 800, 23, scratches=800).save('blob-detail.webp', 'WEBP', quality=80, method=6)
    open('pale-paths.txt', 'w').write(f"hero {pale_path(200,200,170,5)}\ndetail {pale_path(200,200,170,9)}\n")
