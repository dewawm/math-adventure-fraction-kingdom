import json, random, math
from fractions import Fraction as F
from pathlib import Path
r=random.Random(2026)
q=[]

def fs(v):
    v=F(v)
    if v.denominator==1: return str(v.numerator)
    return f'{v.numerator}/{v.denominator}'

def opts_f(v):
    v=F(v); choices={v}
    variants=[v+F(1,v.denominator),v-F(1,v.denominator),v+F(1,2),v+F(1,3),v*2,v/F(2),F(v.denominator,max(1,v.numerator)),v+1,v-F(1,2),v+F(2,3)]
    for x in variants:
        if x>=0:choices.add(x)
    step=1
    while len(choices)<4:
        choices.add(v+F(step,4));step+=1
    distractors=r.sample(sorted(choices-{v}),3); out=distractors+[v];r.shuffle(out)
    return [fs(t) for t in out],out.index(v)

def opts_int(v,suffix=''):
    nums={v}
    for d in [-4,-3,-2,-1,1,2,3,4,5,6,10,12]:
        if v+d>0: nums.add(v+d)
    ds=r.sample(sorted(nums-{v}),3); ds.append(v);r.shuffle(ds)
    return [str(x)+suffix for x in ds],ds.index(v)

def add(cat,prompt,answers,idx,why,diff='sedang'):
    q.append(dict(id=f'M{len(q)+1:03d}',category=cat,difficulty=diff,question=prompt,options=answers,answer=idx,explanation=why,points=100))

for i in range(30):
    # Multiples of denominators 2..12, distinct wording, unique numeric questions
    while True:
        a=F(r.randrange(1,10),r.randrange(2,13));b=F(r.randrange(1,9),r.randrange(2,13));addop=i%2==0
        if not addop and a<b:a,b=b,a
        result=a+b if addop else a-b
        symbol='+' if addop else '−'
        prompt=f'Hitung hasil dari {fs(a)} {symbol} {fs(b)}!'
        if prompt not in [x['question'] for x in q]:break
    options,index=opts_f(result)
    add('fraction-add',prompt,options,index,f'Samakan penyebut terlebih dahulu, lalu hitung: {fs(a)} {symbol} {fs(b)} = {fs(result)}.', 'mudah' if i<10 else 'sedang')

for i in range(30):
    while True:
        a=F(r.randrange(1,10),r.randrange(2,11));b=F(r.randrange(1,8),r.randrange(2,11));times=i%2==0
        out=a*b if times else a/b
        symbol='×' if times else '÷'
        prompt=f'Berapakah hasil {fs(a)} {symbol} {fs(b)}?'
        if prompt not in [x['question'] for x in q]:break
    op='Kalikan pembilang dan penyebut' if times else 'Balik pecahan kedua, lalu kalikan'
    choices,idx=opts_f(out)
    add('fraction-mul',prompt,choices,idx,f'{op}: {fs(a)} {symbol} {fs(b)} = {fs(out)}.', 'sedang' if i<20 else 'sulit')

for i in range(20):
    if i<10:
        whole=r.randint(1,4);num=r.randint(1,4); den=r.randint(num+1,10)
        val=F(whole*den+num,den)
        prompt=f'Ubah pecahan campuran {whole} {num}/{den} menjadi pecahan biasa!'
        explanation=f'({whole} × {den} + {num})/{den} = {fs(val)}.'
    else:
        a=r.randint(1,8);b=r.randint(1,9)
        val=F(a,10)+F(b,10)
        prompt=f'Hitung 0,{a} + 0,{b}, lalu tuliskan sebagai pecahan paling sederhana!'
        explanation=f'0,{a} + 0,{b} = {a+b}/10 = {fs(val)}.'
    choices,idx=opts_f(val)
    add('mixed',prompt,choices,idx,explanation,'sedang')

for i in range(20):
    unit=r.randint(2,9);count=r.randint(2,6);newcount=r.randint(7,14)
    while newcount==count:newcount=r.randint(7,14)
    total=count*unit; answer=newcount*unit
    if i%2==0:
        prompt=f'{count} buku seharga Rp{total*1000:,} secara keseluruhan. Berapa ribu rupiah harga {newcount} buku dengan harga satuan sama?'.replace(',','.')
        explanation=f'Harga satu buku = {total} ÷ {count} = {unit} ribu rupiah. Harga {newcount} buku = {newcount} × {unit} = {answer} ribu rupiah.'
        suffix=' ribu'
    else:
        prompt=f'Untuk membuat {count} gelas jus diperlukan {total} buah jeruk. Berapa jeruk untuk {newcount} gelas dengan takaran sama?'
        explanation=f'Setiap gelas butuh {total} ÷ {count} = {unit} jeruk. Jadi {newcount} × {unit} = {answer} jeruk.'
        suffix=''
    choices,idx=opts_int(answer,suffix)
    add('direct',prompt,choices,idx,explanation,'sedang' if i<12 else 'sulit')

for i in range(20):
    workers=r.choice([2,3,4,5,6,8,10]);more=r.choice([2,3,4]); work2=workers*more
    days=r.choice([12,16,18,20,24,30,36]);
    if days%more: days=days*more
    ans=days//more
    if i%2==0:
        prompt=f'{workers} pekerja menyelesaikan tugas dalam {days} hari. Jika jumlah pekerja menjadi {work2} orang dan kecepatan kerja sama, berapa hari diperlukan?'
    else:
        prompt=f'{workers} mesin mengemas barang dalam {days} jam. Jika dipakai {work2} mesin dengan kecepatan sama, berapa jam diperlukan?'
    explanation=f'Berbalik nilai: {workers} × {days} = {work2} × waktu, jadi waktu = {workers*days}/{work2} = {ans}.'
    choices,idx=opts_int(ans)
    add('inverse',prompt,choices,idx,explanation,'sulit')

assert len(q)==120
for item in q:
    assert len(item['options'])==4 and len(set(item['options']))==4 and 0<=item['answer']<4
Path(__file__).parent.joinpath('public','questions.json').write_text(json.dumps(q,ensure_ascii=False,indent=2),encoding='utf-8')
from collections import Counter
print('questions:',len(q),Counter(x['category'] for x in q))
