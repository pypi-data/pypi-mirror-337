import numpy as np
from afdcfun import *

def afd3d(vel,nt=1501,dt=0.001,ax=[0,20,81],ay=[0,20,81],az=[0,20,81],ns=3,sx=[30,40,50],sy=[30,40,50],sz=[30,40,50],f=[10,10,10],t=[0.2,0.35,0.5],A=[1,2,2],nbt=30,ct=0.01,jsnap=4,abc=True,ifsnaps=False,ps=True,tri=False,dat=None,verb=True):
	'''
	aps3d: 3D acoustic wavefield modeling using the pseudo-spectral method  
	
	INPUT
	vel: velocity model [nz,nx,ny]
	nt: number of samples
	dt: temporal sampling (time interval)
	ax: axis x [ox,dx,nx]
	ay: axis y [oy,dy,ny]
	az: axis z [oz,dz,nz]
	nbt: 	size of ABC layers
	ct:		ABCparameter
	jsnap:	output wavefield interval
	abc:	if abc (default: True)
	ifsnaps:if output wavefield (default False)
	ps: if pseudo-spectral
	tri: if choose time reversal imaging (True: TRI; False: Forward modeling)
	verb: verbosity flag
	
	#below is for synthetic parameters
	ns:		number of shots
	sx:		source x vector in samples
	sy:		source y vector in samples
	sz:		source z vector in samples
	f:		source freq vector in Hz
	t:		source time vector in sec
	A:		source amplitude
	
	OUTPUT
	data
	[wfd] if jsnap>0
	
	EXAMPLE
	demos/test_mod3d.py
	
	HISTORY
	Original version by Yangkang Chen, Oct 31, 2024
	
	REFERENCE
	Chen, Y., O.M. Saad, M. Bai, X. Liu, and S. Fomel, 2021, A compact program for 3D passive seismic source-location imaging, Seismological Research Letters, 92(5), 3187–3201.
	
	See the original Madagascar version with documentation at
	https://github.com/chenyk1990/passive_imaging/blob/main/mod3d.c
	
	'''
	vel=vel.flatten(order='F').astype(np.float32)
	ox=ax[0];dx=ax[1];nx=ax[2];
	oy=ay[0];dy=ay[1];ny=ay[2];
	oz=az[0];dz=az[1];nz=az[2];
	
	sx=np.array(sx);
	sy=np.array(sy);
	sz=np.array(sz);
	f=np.array(f);
	t=np.array(t);
	A=np.array(A);
	
# 	vel=vel.flatten(order='F',dtype='float32')

	if tri:
# 		if dat=='None':
# 			print('Need input data')
		print('Time-reversal imaging')
		print('dat.shape',dat.shape)
		source=dat.flatten(order='F').astype(np.float32); 
		tri=1;
	else:
		source=np.concatenate([sx,sy,sz,f,t,A],axis=0,dtype='float32'); #remember: source size is ns*6
	
	print(source)
	print(nt,nx,ny,nz)
	print(tri)
	dout=afd3dc(vel,source,tri,nt,nx,ny,nz,ns,verb,jsnap,ifsnaps,abc,nbt,ct,dt,ox,dx,oy,dy,oz,dz);
	
	if jsnap>0:
	
		ntsnap=0;
		if jsnap:
			for it in range(nt):
				if np.mod(it,jsnap)==0:
					ntsnap=ntsnap+1;
		print('ntsnap=',ntsnap);
		wfd=dout[nt*nx*ny:].reshape(nz,nx,ny,ntsnap,order='F'); #[x,y,z]
		dout=dout[0:nt*nx*ny].reshape(nt,nx,ny,order='F'); #[x,y,z]
		# tri,&nt,&nx,&ny,&nz,&ns,&verb,&jsnap,&ifsnaps,&abs,&nbt,ct,dt,ox,dx,oy,dy,oz,dz);

	if jsnap>0:
		return dout,wfd
	else:
		return dout


