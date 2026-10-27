import re
p='index.html'
h=open(p,encoding='utf-8').read()
old='''    <div class="marquee" aria-hidden="true">
      <div class="marquee__track">
        <span>Charcoal</span><span class="marquee__dot"></span>
        <span>Coastal spice</span><span class="marquee__dot"></span>
        <span>Open hearth</span><span class="marquee__dot"></span>
        <span>Seasonal menu</span><span class="marquee__dot"></span>
        <span>Shoreditch</span><span class="marquee__dot"></span>
        <span>Charcoal</span><span class="marquee__dot"></span>
        <span>Coastal spice</span><span class="marquee__dot"></span>
        <span>Open hearth</span><span class="marquee__dot"></span>
        <span>Seasonal menu</span><span class="marquee__dot"></span>
        <span>Shoreditch</span><span class="marquee__dot"></span>
      </div>
      <p class="sr-only">Charcoal, coastal spice, open hearth, seasonal menu, Shoreditch.</p>
    </div>'''
new='''    <div class="marquee" aria-hidden="true">
      <div class="marquee__track">
        <div class="marquee__group">
          <span>Charcoal</span><span class="marquee__dot"></span>
          <span>Coastal spice</span><span class="marquee__dot"></span>
          <span>Open hearth</span><span class="marquee__dot"></span>
          <span>Seasonal menu</span><span class="marquee__dot"></span>
          <span>Shoreditch</span><span class="marquee__dot"></span>
        </div>
        <div class="marquee__group">
          <span>Charcoal</span><span class="marquee__dot"></span>
          <span>Coastal spice</span><span class="marquee__dot"></span>
          <span>Open hearth</span><span class="marquee__dot"></span>
          <span>Seasonal menu</span><span class="marquee__dot"></span>
          <span>Shoreditch</span><span class="marquee__dot"></span>
        </div>
      </div>
    </div>'''
assert old in h
h=h.replace(old,new)
h=h.replace('<svg class="brand__mark" aria-hidden="true">','<svg class="brand__mark" viewBox="0 0 24 24" aria-hidden="true">')
h=h.replace('<svg class="icon"','<svg class="icon" viewBox="0 0 24 24"')
open(p,'w',encoding='utf-8',newline='\n').write(h)
print('updated', len(h))
