#!/usr/bin/env python3
"""Convert an Android VectorDrawable XML file to SVG.

Usage: vector-to-svg.py INPUT.xml OUTPUT.svg [--background COLOR] [--padding FRACTION]
Supports paths, groups (translate/scale/rotate/pivot), clip-paths and aapt linear/radial gradients.
"""
import argparse
import xml.etree.ElementTree as ET
from xml.sax.saxutils import quoteattr

A = '{http://schemas.android.com/apk/res/android}'
AAPT = '{http://schemas.android.com/aapt}'


def color(value):
    """Android #AARRGGBB / #RGB → (css colour, opacity)."""
    if not value or not value.startswith('#'):
        return value or 'none', 1.0
    h = value[1:]
    if len(h) in (3, 4):
        h = ''.join(c * 2 for c in h)
    if len(h) == 8:
        return '#' + h[2:], int(h[:2], 16) / 255
    return '#' + h, 1.0


class Converter:
    def __init__(self):
        self.defs, self.ids = [], 0

    def new_id(self, prefix):
        self.ids += 1
        return f'{prefix}{self.ids}'

    def gradient(self, g):
        gid = self.new_id('g')
        kind = g.get(A + 'type', 'linear')
        stops = []
        items = g.findall('item')
        if items:
            for item in items:
                c, o = color(item.get(A + 'color'))
                stops.append((item.get(A + 'offset', '0'), c, o))
        else:
            pairs = [('0', g.get(A + 'startColor'))]
            if g.get(A + 'centerColor'):
                pairs.append(('0.5', g.get(A + 'centerColor')))
            pairs.append(('1', g.get(A + 'endColor')))
            stops = [(off, *color(c)) for off, c in pairs]
        stop_xml = ''.join(f'<stop offset="{off}" stop-color="{c}"' + (f' stop-opacity="{o:.3f}"' if o < 1 else '') + '/>' for off, c, o in stops)
        if kind == 'radial':
            attrs = f'cx="{g.get(A + "centerX", 0)}" cy="{g.get(A + "centerY", 0)}" r="{g.get(A + "gradientRadius", 0)}"'
            self.defs.append(f'<radialGradient id="{gid}" gradientUnits="userSpaceOnUse" {attrs}>{stop_xml}</radialGradient>')
        else:
            attrs = ' '.join(f'{k}="{g.get(A + v, 0)}"' for k, v in (('x1', 'startX'), ('y1', 'startY'), ('x2', 'endX'), ('y2', 'endY')))
            self.defs.append(f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" {attrs}>{stop_xml}</linearGradient>')
        return f'url(#{gid})'

    def paint(self, el, attr):
        for aapt in el.findall(AAPT + 'attr'):
            if aapt.get('name') == 'android:' + attr:
                g = aapt.find('gradient')
                if g is not None:
                    return self.gradient(g), 1.0
        value = el.get(A + attr)
        return color(value) if value else ('none', 1.0)

    def path(self, el):
        fill, fill_o = self.paint(el, 'fillColor')
        stroke, stroke_o = self.paint(el, 'strokeColor')
        fill_o *= float(el.get(A + 'fillAlpha', 1))
        stroke_o *= float(el.get(A + 'strokeAlpha', 1))
        out = [f'd={quoteattr(el.get(A + "pathData", ""))}', f'fill="{fill}"']
        if fill_o < 1:
            out.append(f'fill-opacity="{fill_o:.3f}"')
        if el.get(A + 'fillType') == 'evenOdd':
            out.append('fill-rule="evenodd"')
        if stroke != 'none':
            out.append(f'stroke="{stroke}" stroke-width="{el.get(A + "strokeWidth", 0)}"')
            if stroke_o < 1:
                out.append(f'stroke-opacity="{stroke_o:.3f}"')
            if el.get(A + 'strokeLineCap'):
                out.append(f'stroke-linecap="{el.get(A + "strokeLineCap")}"')
            if el.get(A + 'strokeLineJoin'):
                out.append(f'stroke-linejoin="{el.get(A + "strokeLineJoin")}"')
        return f'<path {" ".join(out)}/>'

    def children(self, parent):
        out, clip = [], None
        for el in parent:
            tag = el.tag
            if tag == 'path':
                out.append(self.path(el))
            elif tag == 'group':
                out.append(self.group(el))
            elif tag == 'clip-path':
                clip = self.new_id('c')
                self.defs.append(f'<clipPath id="{clip}"><path d={quoteattr(el.get(A + "pathData", ""))}/></clipPath>')
        body = ''.join(out)
        return f'<g clip-path="url(#{clip})">{body}</g>' if clip else body

    def group(self, el):
        f = lambda k, d=0.0: float(el.get(A + k, d))
        px, py = f('pivotX'), f('pivotY')
        transform = f'translate({f("translateX") + px} {f("translateY") + py}) rotate({f("rotation")}) scale({f("scaleX", 1)} {f("scaleY", 1)}) translate({-px} {-py})'
        return f'<g transform="{transform}">{self.children(el)}</g>'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input'); parser.add_argument('output')
    parser.add_argument('--background'); parser.add_argument('--padding', type=float, default=0)
    args = parser.parse_args()
    root = ET.parse(args.input).getroot()
    w, h = float(root.get(A + 'viewportWidth')), float(root.get(A + 'viewportHeight'))
    conv = Converter()
    body = conv.children(root)
    pad = args.padding * w
    if pad:
        body = f'<g transform="translate({pad} {pad}) scale({(w - 2 * pad) / w})">{body}</g>'
    if args.background:
        body = f'<rect width="{w}" height="{h}" fill="{args.background}"/>' + body
    defs = f'<defs>{"".join(conv.defs)}</defs>' if conv.defs else ''
    with open(args.output, 'w') as fh:
        fh.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}">{defs}{body}</svg>\n')


if __name__ == '__main__':
    main()
