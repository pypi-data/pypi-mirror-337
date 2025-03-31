#aps2d(vel,nt=1501,dt=0.001,ax=[0,20,81],az=[0,20,81],ns=2,sx=[30,40],sz=[30,40],f=[10,10],t=[0.2,0.35],A=[1,2],nbt=30,ct=0.01,jsnap=4,abc=True,ifsnaps=False,ps=True,tri=False,dat=None,verb=True):
import numpy as np
from pfwicfun import *

def pfwi(vel,q,wav,src,data=None,mode=1,media=1,inv=0,verb=1,nb=60,coef=0.005,acq=1,ss=[0,0.2,1],f0=10,waterz=-30,niter=30,conv_e=0.01,par=None):
	'''
	pfwi: inverting for velocity ( and source ) using passive data
	
	INPUT
	vel: velocity model (2D)
	q: quality factor model (2D)
	wav: source wavelet (1D)
	src: source position,time,index (4D, nz*nx*nt*ns) (to be inverted)
	data: input data (nt*nx*ns)
	mode: 1modeling2FWI3RTM4PFWI (if mode=1, input data=None;)
	media: media type (1: acoustic (default); 2: visco-acoustic)
	inv: inversion flag 
	verb: verbosity
	
	
	OUTPUT
	data,vinv,grad,src,mwt (intuitively)
	
	mode=4;inv=0: only Data, others: None
	mode=4;inv=1: Source, others: None
	
	'''
	
	par=fillpar(par) #fill blank keywords using default values

	if mode==1:		#modeling
			print('start modeling in python')
			vel=vel.flatten(order='F').astype(np.float32);
			q=q.flatten(order='F').astype(np.float32);
			wav=wav.flatten(order='F').astype(np.float32);
# 			datasrc=src.flatten(order='F').astype(np.float32);  #combined datasrc
			print('data flattening done in python')
			#if mwt (model weight) is not considered right now

			pararray=np.array([
			par['nz'],
			par['nx'],
			par['dz'],
			par['dx'],
			par['oz'],
			par['ox'],
			par['nt'],
			par['dt'],
			par['ot'],
			par['inv'],
			par['ns'],
			par['ds'],
			par['os'],
			par['sz'],
			par['nb'],				#boundary width
			par['coef'],			#absorbing boundary coefficient
			par['f0'],				#reference frequency
			par['acqui_type'],		#1, fixed acquisition; 
			par['interval'],		#wavefield storing interval
			par['niter']			#number of inversion iterations
			],dtype=np.float32)
			
			print('par:',par)
			print('len(pararray)',len(pararray))
			
# 			data=lstric(vel, q, wav, datasrc, pararray); #modeling, #array can be constructed internally
# 			data=lstric(pararray); #modeling, #array can be constructed internally
		
			if media==1:
				data=forward_modeling_ac(vel, q, wav, pararray);
			else: 
				data=forward_modelingc(vel, q, wav, pararray);
		
			data=data.reshape(par['nt'],par['nx'],par['ns'],order='F')
			vinv=[];grad=[];mwt=[];src=[];
		
	elif mode==2:
			print('start FWI in python')
			vel=vel.flatten(order='F').astype(np.float32); #vel is smoothed velocity
			q=q.flatten(order='F').astype(np.float32);
			wav=wav.flatten(order='F').astype(np.float32);
			data=data.flatten(order='F').astype(np.float32);  #combined datasrc
			print('data flattening done in python')
			#if mwt (model weight) is not considered right now

			pararray=np.array([
			par['nz'],
			par['nx'],
			par['dz'],
			par['dx'],
			par['oz'],
			par['ox'],
			par['nt'],
			par['dt'],
			par['ot'],
			par['inv'],
			par['ns'],
			par['ds'],
			par['os'],
			par['sz'],
			par['nb'],				#boundary width
			par['coef'],			#absorbing boundary coefficient
			par['f0'],				#reference frequency
			par['acqui_type'],		#1, fixed acquisition; 
			par['interval'],		#wavefield storing interval
			par['niter']			#number of inversion iterations
			],dtype=np.float32)
			
			print('par:',par)
			print('len(pararray)',len(pararray))
			vinv=fwic(vel, q, wav, data, pararray); #in this case, vel is the smoothed model
			vinv=vinv.reshape(par['nz'],par['nx'],par['niter'],order='F')
			src=None;mwt=None;grad=None;
	elif mode==3:  #RTM
		pass
# 		if media==1: 
# 			rtm_ac(Fdat, Fimg, &mpipar, soupar, acpar, array, verb);
# 		else: 
# 			rtmc(Fdat, Fimg, &mpipar, soupar, acpar, array, verb);
		
	elif mode==4:
		if par['inv']==True:
			if par['onlysrc']==True:
				print('start source inversion in python')
				vel=vel.flatten(order='F').astype(np.float32);
				q=q.flatten(order='F').astype(np.float32);
				wav=wav.flatten(order='F').astype(np.float32);
				datasrc=data.flatten(order='F').astype(np.float32);  #combined datasrc
				print('data flattening done in python')
			#if mwt (model weight) is not considered right now
			
				par['inv']=1;
				
				pararray=np.array([
				par['nz'],
				par['nx'],
				par['dz'],
				par['dx'],
				par['oz'],
				par['ox'],
				par['nt'],
				par['dt'],
				par['ot'],
				par['inv'],
				par['ns'],
				par['ds'],
				par['os'],
				par['sz'],
				par['nb'],				#boundary width
				par['coef'],			#absorbing boundary coefficient
				par['f0'],				#reference frequency
				par['acqui_type'],		#1, fixed acquisition; 
				par['interval'],		#wavefield storing interval
				par['niter']			#number of inversion iterations
				],dtype=np.float32)
			
				print('par:',par)
				print('len(pararray)',len(pararray))
			
				src=lstric(vel, q, wav, datasrc, pararray); #modeling, #array can be constructed internally
# 				data=lstric(pararray); #modeling, #array can be constructed internally
				vinv=[];grad=[];mwt=[];src=src.reshape(par['nz'],par['nx'],par['nt'],par['ns'],order='F')
# 				data=data.reshape(par['nt'],par['nx'],par['ns'],order='F')
				data=[];
# 				pass
# 				datasrc=data.flatten(order='F').astype(np.float32);  #combined datasrc
# 				src=lstric(datasrc, acpar, paspar, verb); #[src,mwt]=
			else:
				vel=vel.flatten(order='F').astype(np.float32);
				q=q.flatten(order='F').astype(np.float32);
				wav=wav.flatten(order='F').astype(np.float32);
				
				par['inv']=1;
				
				pararray=np.array([
				par['nz'],
				par['nx'],
				par['dz'],
				par['dx'],
				par['oz'],
				par['ox'],
				par['nt'],
				par['dt'],
				par['ot'],
				par['inv'],
				par['ns'],
				par['ds'],
				par['os'],
				par['sz'],
				par['nb'],				#boundary width
				par['coef'],			#absorbing boundary coefficient
				par['f0'],				#reference frequency
				par['acqui_type'],		#1, fixed acquisition; 
				par['interval'],		#wavefield storing interval
				par['niter']			#number of inversion iterations
				],dtype=np.float32)
# 				vinv,grad,src,mwt]=pfwic(data, vel, [], src, [], soupar, acpar, array, fwipar, optpar, paspar, verb);
				data=data.flatten(order='F').astype(np.float32);  #combined datasrc
				src=src.flatten(order='F').astype(np.float32);  #combined datasrc
				print(par)
				print(data.shape,src.shape)
				datasrc=np.concatenate([data,src],axis=0)
				vinv=pfwic(vel, q, wav, datasrc, pararray); #in this case, vel is the smoothed model
				vinv=vinv.reshape(par['nz'],par['nx'],par['niter'],order='F')
			if par['onlysrc']==True:	   #only src
				vinv=None;grad=None;
			else:
				if par['onlyvel']==True:   #only vel
					src=None;mwt=None;grad=None;
# 			data=None
			
		else:
			print('start modeling in python')
			vel=vel.flatten(order='F').astype(np.float32);
			q=q.flatten(order='F').astype(np.float32);
			wav=wav.flatten(order='F').astype(np.float32);
			datasrc=src.flatten(order='F').astype(np.float32);  #combined datasrc
			print('data flattening done in python')
			#if mwt (model weight) is not considered right now

			pararray=np.array([
			par['nz'],
			par['nx'],
			par['dz'],
			par['dx'],
			par['oz'],
			par['ox'],
			par['nt'],
			par['dt'],
			par['ot'],
			par['inv'],
			par['ns'],
			par['ds'],
			par['os'],
			par['sz'],
			par['nb'],				#boundary width
			par['coef'],			#absorbing boundary coefficient
			par['f0'],				#reference frequency
			par['acqui_type'],		#1, fixed acquisition; 
			par['interval'],		#wavefield storing interval
			par['niter']			#number of inversion iterations
			],dtype=np.float32)
			
			print('par:',par)
			print('len(pararray)',len(pararray))
			
			data=lstric(vel, q, wav, datasrc, pararray); #modeling, #array can be constructed internally
# 			data=lstric(pararray); #modeling, #array can be constructed internally
			vinv=[];grad=[];mwt=[];src=[];
			data=data.reshape(par['nt'],par['nx'],par['ns'],order='F')

	else:
	
		print("Wrong mode")
		return 0
		

	
	return data,vinv,grad,src,mwt
	
	
def fillpar(par):
	'''
	fillpar: fill blank keywords using default values
	
	INPUT
	par: input parameter dictionary
	
	OUTPUT
	par: filled parameter dictionary
	
	'''
	
	kw = {
	'f0': 10,
	'nb': 100,
	'coef': 0.003,
	'acqui_type': 1,	#1, fixed acquisition; if 2, marine acquisition; if 3, symmetric acquisition
	'interval': 1, 		#wavefield storing interval
	'ns':1,
	'ds':0.2,
	'os':0.0,
	'sz':5,
	'nx':100,
	'nz':100,
	'nr':par['nx'],
	'dr':par['dx'],
	'r0':par['ox'],
	'fhi':0.5/par['dt'],
	'flo':0,
	'onlysrc': True,
	'onlyvel': False,
	'inv': False,
	'niter': 10
	}
	
	kw.update(par)
	
	par=kw;

	return par





	
	