# Gera o og.jpg (1200x630) a partir do index.html. Uso: python3 gerar-og.py index.html og.jpg
# Requer: pip install playwright && playwright install chromium; fontes: npm i @fontsource/pinyon-script @fontsource/cormorant-garamond @fontsource/jost (ajuste a variavel F)
import sys, asyncio
from playwright.async_api import async_playwright
F='/home/claude/fonts/node_modules/@fontsource'
FONTS=f"""
@font-face{{font-family:"Pinyon Script";src:url(file://{F}/pinyon-script/files/pinyon-script-latin-400-normal.woff2)}}
@font-face{{font-family:"Cormorant Garamond";font-weight:400;src:url(file://{F}/cormorant-garamond/files/cormorant-garamond-latin-400-normal.woff2)}}
@font-face{{font-family:"Cormorant Garamond";font-weight:500;src:url(file://{F}/cormorant-garamond/files/cormorant-garamond-latin-500-normal.woff2)}}
@font-face{{font-family:"Cormorant Garamond";font-style:italic;font-weight:400;src:url(file://{F}/cormorant-garamond/files/cormorant-garamond-latin-400-italic.woff2)}}
@font-face{{font-family:"Cormorant Garamond";font-style:italic;font-weight:500;src:url(file://{F}/cormorant-garamond/files/cormorant-garamond-latin-500-italic.woff2)}}
@font-face{{font-family:Jost;font-weight:300;src:url(file://{F}/jost/files/jost-latin-300-normal.woff2)}}
@font-face{{font-family:Jost;font-weight:400;src:url(file://{F}/jost/files/jost-latin-400-normal.woff2)}}
"""
CSS="""
html,body{overflow:hidden}
.hero{flex-direction:row;gap:64px;min-height:630px;height:630px;padding:0 64px}
.kicker,.hint{display:none}.seal{animation:none}
#og{width:540px;text-align:center;color:#f6edd2}
#og p{margin:0;font:italic 400 32px/1.2 "Cormorant Garamond",serif;color:#e9d49a}
#og h2{margin:14px 0 18px;font:400 98px/1.02 "Pinyon Script",cursive;color:#f8f0d8}
#og h2 i{display:block;font:italic 400 52px/1 "Cormorant Garamond",serif;color:#e0c37a;margin:4px 0}
#og .d{display:inline-block;padding:12px 26px;border-block:1px solid rgba(233,212,154,.55);font:300 25px/1.3 Jost,sans-serif;color:#efe0b0}
#og .l{margin-top:14px;font:300 21px/1.3 Jost,sans-serif;color:#cdbf92}
"""
JS="""() => {
  const g = k => document.querySelector('[data-k='+k+']').textContent;
  document.documentElement.style.setProperty('--S','470px');
  const og = document.createElement('div'); og.id='og';
  og.innerHTML = `<p>Você recebeu um convite</p><h2>${g('noiva')}<i>&amp;</i>${g('noivo')}</h2>
    <div class="d">${g('dia')} de ${g('mesano')}</div><div class="l">${g('local')}</div>`;
  document.getElementById('hero').appendChild(og);
}"""
async def main(src, out):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width':1200,'height':630})
        await pg.route('**/fonts.googleapis.com/**', lambda r: r.abort())
        await pg.goto('file://'+src)
        await pg.add_style_tag(content=FONTS+CSS)
        await pg.evaluate(JS)
        await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(600)
        await pg.screenshot(path=out, type='jpeg', quality=86)
        await b.close()
if __name__=='__main__': asyncio.run(main(sys.argv[1], sys.argv[2]))
