# Procedural sound design for "Relative" (numpy only). Writes sfx.wav (12 s, mono).
import numpy as np, wave
sr=44100; T=12.0; n=int(sr*T); t=np.arange(n)/sr
rng=np.random.default_rng(1); out=np.zeros(n)
ft=168/24; fs=192/24
seg=t<ft
f=60*(15**((t/ft)**2)); ph=2*np.pi*np.cumsum(f)/sr            # engine: exponential sweep
eng=(np.sin(ph)+0.4*np.sin(2*ph)+0.2*np.sin(3*ph))*np.clip(t/0.5,0,1)
env=np.where(seg,0.25+0.35*(t/ft),np.exp(-(t-ft)*6)*0.6); out+=eng*env*0.5
noise=rng.standard_normal(n); wind=np.convolve(noise,np.ones(30)/30,'same')*3   # wind
out+=wind*np.where(seg,(t/ft)**2*0.5,0)
br=(t>=ft)&(t<fs+0.2); fsr=2400+300*np.sin(2*np.pi*31*t)                         # brake screech
out+=np.sin(2*np.pi*np.cumsum(fsr)/sr)*br*0.18*np.exp(-np.clip(t-ft,0,None)*2)
for start,f0,f1,dur,a in [(236/24,300,500,0.5,0.35),(252/24,90,70,1.4,0.35)]:     # boing + tuba
    m=(t>=start)&(t<start+dur); tt=t-start
    ff=f0+(f1-f0)*np.clip(tt/dur,0,1); p=2*np.pi*np.cumsum(ff*m)/sr
    out+=np.sin(p)*m*a*np.exp(-np.clip(tt,0,None)*2.5)
out/=np.max(np.abs(out))*1.1
w=wave.open('sfx.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
