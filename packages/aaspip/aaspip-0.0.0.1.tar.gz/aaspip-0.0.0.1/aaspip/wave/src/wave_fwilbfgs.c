/* L-BFGS optimization and line search based on Wolfe condition */

#include <stdio.h>
#include <stdbool.h>
#include "wave_alloc.h"
#include "wave_fwiutil.h"
/*^*/

void lbfgs_save(int n, float *x, float *grad, float **sk, float **yk, np_optim opt)
/*< save current model and gradient >*/
{
	int i;
	if(opt->ipair < opt->npair){
		copy(n, x, sk[opt->ipair]);
		copy(n, grad, yk[opt->ipair]);
		opt->ipair += 1;
	}else{
		for(i=0; i<opt->npair-1; i++){
			copy(n, sk[i+1], sk[i]);
			copy(n, yk[i+1], yk[i]);
		}
		copy(n, x, sk[opt->npair-1]);
		copy(n, grad, yk[opt->npair-1]);
	}
}

void lbfgs_update(int n, float *x, float *grad, float **sk, float **yk, np_optim opt)
/*< update current sk and yk >*/
{
	int i, j;
	j=opt->ipair-1;
	for(i=0; i<n; i++){
		sk[j][i]=x[i]-sk[j][i];
		yk[j][i]=grad[i]-yk[j][i];
	}
}

void lbfgs_direction(int n, float *grad, float *r, float **sk, float **yk, np_optim opt)
/*< calculate search direction >*/
{
	int i, j;
	float *rho, *q, *alpha, tmp, tmp1, gamma, beta;

	// safeguard
	l2norm(n, sk[opt->ipair-1], &tmp);
	l2norm(n, yk[opt->ipair-1], &tmp1);
	if(tmp==0. || tmp1==0.){
		reverse(n, grad, r);
		return;
	}
	
	q=np_floatalloc(n);
	rho=np_floatalloc(opt->ipair);
	alpha=np_floatalloc(opt->ipair);

	copy(n, grad, q);
	
	// first loop
	for(i=opt->ipair-1; i>=0; i--){
		
		// calculate rho
		dot_product(n, yk[i], sk[i], &tmp);  
		rho[i]=1./tmp;

		dot_product(n, sk[i], q, &tmp);
		alpha[i]=rho[i]*tmp;
		for(j=0; j<n; j++)
			q[j] -= alpha[i]*yk[i][j];
	}

	// initial Hessian
	dot_product(n, yk[opt->ipair-1], yk[opt->ipair-1], &tmp);
	gamma=1./tmp/rho[opt->ipair-1];
	for (j=0; j<n; j++){
		r[j]=gamma*q[j];
	}

	// second loop
	for(i=0; i<opt->ipair; i++){
		dot_product(n, yk[i], r, &tmp);
		beta=tmp*rho[i];
		tmp=alpha[i]-beta;
		for(j=0; j<n; j++)
			r[j] += tmp*sk[i][j];
	}

	// opposite direction of H^(-1)*grad(f)
	for(j=0; j<n; j++)
		r[j]=-r[j];

	// deallocate variables
	free(q);
	free(alpha);
	free(rho);
}

void clip(float *x, int n, float min, float max)
/*< clip data >*/
{
    int i;

    for(i=0; i<n; i++){
        if(x[i]<min) x[i]=min;
        if(x[i]>max) x[i]=max;
    }
}

void line_search(int n, float *x, float *grad, float *direction, np_gradient gradient, np_optim opt, int *flag)
/*< line search (Wolfe condition) >*/
/*In the unconstrained minimization problem, the Wolfe conditions are a set of inequalities for performing inexact line search, especially in quasi-Newton methods, first published by Philip Wolfe in 1969.[1][2]*/
{
	int i, j;
	float m1, m2, m3, fcost, alpha1=0., alpha2=0.;
	float *xk;

	xk=np_floatalloc(n);
	copy(n, x, xk);
	dot_product(n, grad, direction, &m1);
	m2=m1*opt->c2;
	m1=m1*opt->c1;
	
	for(i=0; i<opt->nls; i++){
		
		opt->ils += 1;
		for(j=0; j<n; j++)
			x[j] =xk[j] + opt->alpha*direction[j];

                clip(x, n, opt->v1, opt->v2);

		gradient(x, &fcost, grad);
		opt->igrad += 1;
		dot_product(n, grad, direction, &m3);
		

		printf("line search i=%d\n",i+1);
		printf("alpha1=%g alpha2=%g alpha=%g\n",alpha1, alpha2, opt->alpha);
		printf("fcost=%g fk=%g fk+c1*alpha*m1=%g m3=%g c2*m1=%g\n",fcost, opt->fk, opt->fk+opt->alpha*m1, m3, m2);


		if(fcost <= opt->fk + opt->alpha*m1 && m3 >= m2){
			opt->fk=fcost;
			*flag=0;
			break;
		}else if (fcost > opt->fk + opt->alpha*m1){
			alpha2=opt->alpha;
			opt->alpha=0.5*(alpha1+alpha2);
		}else{
			alpha1=opt->alpha;
			if(alpha2 == 0.)
				opt->alpha *= opt->factor;
			else
				opt->alpha = 0.5*(alpha1+alpha2);
		}

	}
	
	if(i==opt->nls){
		if(fcost <= opt->fk)
			*flag=1;
		else
			*flag=2;
	}

	free(xk);
}
