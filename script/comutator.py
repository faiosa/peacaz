#This is main.py scripts running on RP2040 to handle comutator
import machine as mch,time,select,sys
BS=3
BO='big'
def fba(bt):
 global BS,BO
 return [int.from_bytes(bt[i*BS:(i+1)*BS],BO) for i in range(len(bt)//BS)]
p_o=select.poll()
p_o.register(sys.stdin, 1)
while True:
 try:
  if p_o.poll(0):
   c=sys.stdin.read(BS*2).encode()
   m=fba(c)
   d=fba(sys.stdin.read(m[1]).encode())
   for i in range(len(d)//2):
    p=mch.Pin(d[i*2],mch.Pin.OUT)
    if d[i*2+1]:
     p.high()
    else:
     p.low()
  time.sleep(0.1)
 except Exception as e:
  mch.soft_reset()