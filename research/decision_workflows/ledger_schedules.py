"""Five stipulated ledger schedules retained from the initial demonstrator."""
BITS=[[int(c) for c in f'{i:04b}'] for i in range(16)]
TARGET=[1,0,1,1]
RANK=[11,10,3,15,9,7,2,14,1,13,8,6,5,0,12,4]
def distribution(m,g):
    weights=[]
    for idx,a in enumerate(BITS):
        eq=[x==y for x,y in zip(a,TARGET)];w=1.
        if m==1:
            if g==1:w=.8 if eq[0] else .2
            if g>=2:w=float(all(eq[:g-1]))
        elif m==2:
            if g==1:w=(.8 if eq[0] else .2)*(.8 if eq[1] else .2)
            if g>=2:w=float(all(eq[:2]))
            if g==3:w*=.8 if eq[2] else .2
            if g>=4:w*=eq[2]
            if g==5:w*=eq[3]
        elif m==3:
            if g>=1:w=.8 if eq[0] else .2
            if g>=2:w*=a[1]==1-a[0]
            if g>=3:w*=a[2]==a[0]
            if g>=4:w*=eq[0]
            if g==5:w*=eq[3]
        elif m==4:
            if g<5:
                q=4**g/(1+4**g);w=q**sum(eq)*(1-q)**(4-sum(eq))
            else:w=float(all(eq))
        else:w=float(idx in RANK[:[16,12,8,4,2,1][g]])
        weights.append(w)
    z=sum(weights);return [v/z for v in weights]

