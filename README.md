# htmlmin

Minify HTML, CSS, and JavaScript. Zero dependencies.

## Usage

```bash
htmlmin minify style.css              # Print minified
htmlmin minify index.html --in-place  # Minify in place
htmlmin stats bundle.js               # Show savings
htmlmin minify file --type css        # Force type
```

## Optimizations

**HTML:** comment removal, whitespace collapse, attribute cleanup
**CSS:** comments, color shortening (#aabbcc→#abc), zero-unit removal, empty rules
**JS:** comment removal, whitespace collapse

## Requirements

- Python 3.6+ (stdlib only)
