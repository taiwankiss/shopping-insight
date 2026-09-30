# Shopping Insight

**Everything I Bought.** A long-scroll, single-page report on nine and a half years of Taobao orders (2017.01 – 2026.09): 732 orders, 895 items, NT$428,904.

A gunmetal wire shopping cart, modelled in Blender, rotates, explodes, turns into line work and gets sliced by year as you scroll through eight chapters: overview, categories, price bands, years, outliers, sale days, category shifts and a closing summary.

## Stack

- [Three.js](https://threejs.org) r160 for the cart, the glowing question mark and the light burst
- [GSAP](https://gsap.com) ScrollTrigger + [Lenis](https://lenis.darkroom.engineering) for the scroll-driven timeline
- Plain HTML/CSS, no build step

## Files

| File | What it is |
| --- | --- |
| `index.html` | The whole page |
| `cart_wire.glb` | The cart model (10 parts), loaded first |
| `cart_wire.glb.txt` | Base64 copy of the model, used where `.glb` cannot be served |
| `blender/cart_wire.py` | Blender script that builds and exports the model |
| `favicon.png`, `apple-touch-icon.png`, `icon-512.png` | Icons |

## Run locally

```bash
python3 -m http.server 8765
```

Then open http://localhost:8765.

## Rebuild the model

```bash
/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python blender/cart_wire.py -- cart_wire.glb
base64 -i cart_wire.glb -o cart_wire.glb.txt
```

Amounts are converted at 1 CNY = 4.65 TWD and exclude cancelled orders.
