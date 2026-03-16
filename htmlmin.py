#!/usr/bin/env python3
"""htmlmin - Minify HTML, CSS, and JavaScript. Zero deps."""
import sys, re, os

def minify_html(html):
    # Remove HTML comments (keep conditionals)
    html = re.sub(r'<!--(?!\[if).*?-->', '', html, flags=re.DOTALL)
    # Collapse whitespace between tags
    html = re.sub(r'>\s+<', '><', html)
    # Collapse internal whitespace
    html = re.sub(r'\s{2,}', ' ', html)
    # Remove whitespace around = in attributes
    html = re.sub(r'\s*=\s*', '=', html)
    # Strip leading/trailing
    return html.strip()

def minify_css(css):
    # Remove comments
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
    # Remove whitespace around symbols
    css = re.sub(r'\s*([{}:;,>~+])\s*', r'\1', css)
    # Collapse whitespace
    css = re.sub(r'\s{2,}', ' ', css)
    # Remove trailing semicolons before }
    css = re.sub(r';}', '}', css)
    # Remove empty rules
    css = re.sub(r'[^{}]+\{\}', '', css)
    # Shorten colors
    css = re.sub(r'#([0-9a-fA-F])\1([0-9a-fA-F])\2([0-9a-fA-F])\3', r'#\1\2\3', css)
    # Remove units from zero
    css = re.sub(r'(?<=[\s:])0(px|em|rem|%|pt|ex|ch|vw|vh|vmin|vmax)', '0', css)
    return css.strip()

def minify_js(js):
    # Remove single-line comments (careful with URLs)
    js = re.sub(r'(?<!:)//[^\n]*', '', js)
    # Remove multi-line comments
    js = re.sub(r'/\*.*?\*/', '', js, flags=re.DOTALL)
    # Collapse whitespace (careful with strings)
    lines = js.splitlines()
    result = []
    for line in lines:
        stripped = line.strip()
        if stripped:
            result.append(stripped)
    js = ' '.join(result)
    # Remove unnecessary spaces around operators
    js = re.sub(r'\s*([{}();,=+\-*/<>!&|?:])\s*', r'\1', js)
    # Restore needed spaces (keywords)
    for kw in ['var ','let ','const ','return ','function ','typeof ','instanceof ','new ','delete ','throw ','case ','in ','of ','else ','export ','import ','from ','class ','extends ','yield ','async ','await ']:
        js = js.replace(kw.rstrip(), kw.rstrip() + ' ') if kw.rstrip() + '{' not in js else js
    return js.strip()

def cmd_minify(args):
    if not args: print("Usage: htmlmin minify <file> [--type html|css|js]"); sys.exit(1)
    
    ftype = None
    for i, a in enumerate(args):
        if a == "--type" and i+1 < len(args):
            ftype = args[i+1]; args = args[:i] + args[i+2:]; break
    
    inplace = "--in-place" in args
    args = [a for a in args if not a.startswith("-")]
    path = args[0]
    
    if not ftype:
        ext = os.path.splitext(path)[1].lower()
        ftype = {"html":"html",".htm":"html",".css":"css",".js":"js"}.get(ext, "html")
    
    with open(path) as f: content = f.read()
    original = len(content)
    
    if ftype == "html": result = minify_html(content)
    elif ftype == "css": result = minify_css(content)
    elif ftype == "js": result = minify_js(content)
    else: result = minify_html(content)
    
    minified = len(result)
    saved = original - minified
    pct = (saved / original * 100) if original else 0
    
    if inplace:
        with open(path, "w") as f: f.write(result)
        print(f"✅ {path}: {original:,} → {minified:,} bytes ({pct:.1f}% saved)")
    else:
        print(result)
        print(f"\n/* {original:,} → {minified:,} bytes ({pct:.1f}% reduction) */", file=sys.stderr)

def cmd_stats(args):
    if not args: print("Usage: htmlmin stats <file>"); sys.exit(1)
    with open(args[0]) as f: content = f.read()
    ext = os.path.splitext(args[0])[1].lower()
    ftype = {".html":"html",".htm":"html",".css":"css",".js":"js"}.get(ext, "html")
    
    if ftype == "html": minified = minify_html(content)
    elif ftype == "css": minified = minify_css(content)
    else: minified = minify_js(content)
    
    orig = len(content); mini = len(minified); saved = orig - mini
    print(f"📊 {args[0]}")
    print(f"  Original:  {orig:>10,} bytes")
    print(f"  Minified:  {mini:>10,} bytes")
    print(f"  Saved:     {saved:>10,} bytes ({saved/orig*100:.1f}%)")

CMDS = {"minify":cmd_minify,"min":cmd_minify,"m":cmd_minify,"stats":cmd_stats,"s":cmd_stats}

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] in ("-h","--help"):
        print("htmlmin - Minify HTML, CSS, and JavaScript")
        print("Commands: minify <file> [--type html|css|js] [--in-place], stats <file>")
        sys.exit(0)
    cmd = args[0]
    if cmd not in CMDS: print(f"Unknown: {cmd}"); sys.exit(1)
    CMDS[cmd](args[1:])
