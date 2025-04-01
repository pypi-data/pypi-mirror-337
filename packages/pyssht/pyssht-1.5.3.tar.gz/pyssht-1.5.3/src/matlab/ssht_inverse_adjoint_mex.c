// SSHT package to perform spin spherical harmonic transforms
// Copyright (C) 2011  Jason McEwen
// See LICENSE.txt for license details


#include <ssht.h>
#include "ssht_mex.h"
#include <string.h>
#include "mex.h"


/**
 * Compute inverse adjoint transform.
 *
 * Usage: 
 *   flm = ssht_inverse_adjoint_mex(f, L, method, spin, reality, ...
 *                                  southPoleSampleExists, ...
 *                                  southPoleSample, southPolePhi, ...
 *                                  northPoleSampleExists, ...
 *                                  northPoleSample, northPolePhi);
 *
 * \author Jason McEwen
 */
void mexFunction( int nlhs, mxArray *plhs[],
                  int nrhs, const mxArray *prhs[])
{

  ssht_dl_method_t dl_method = SSHT_DL_TRAPANI;
  int i, L, spin, reality, verbosity=0, f_m, f_n;
  int f_is_complex, fsp_is_complex, fnp_is_complex;
  int south_pole_exists, north_pole_exists;
  double *flm_real = NULL, *flm_imag = NULL;
  double *f_real = NULL, *f_imag = NULL;
  double *fr = NULL;
  complex double *flm = NULL, *f = NULL;
  double *fsp_real = NULL, *fsp_imag = NULL;
  double *fnp_real = NULL, *fnp_imag = NULL;
  double fspr = 0.0, fnpr = 0.0;
  complex double fsp = 0.0, fnp = 0.0;
  double phi_sp = 0.0, phi_np = 0.0;
  int ntheta, nphi, t, p;
  int len, iin = 0, iout = 0;
  char method[SSHT_STRING_LEN];

  /* Check number of arguments. */
  if(nrhs!=11) {
    mexErrMsgIdAndTxt("ssht_inverse_adjoint_mex:InvalidInput:nrhs",
		      "Require five inputs.");
  }
  if(nlhs!=1) {
    mexErrMsgIdAndTxt("ssht_inverse_adjoint_mex:InvalidOutput:nlhs",
		      "Require one output.");
  }

  /* Parse reality. */
  iin = 4;
  if( !mxIsLogicalScalar(prhs[iin]) )
    mexErrMsgIdAndTxt("ssht_inverse_adjoint_mex:InvalidInput:reality",
		      "Reality flag must be logical.");
  reality = mxIsLogicalScalarTrue(prhs[iin]);

  /* Parse function samples f. */
  iin = 0;
  if( !mxIsDouble(prhs[iin]) ) {
    mexErrMsgIdAndTxt("ssht_inverse_adjoint_mex:InvalidInput:f",
		      "Function values must be doubles.");
  }
  f_m = mxGetM(prhs[iin]);
  f_n = mxGetN(prhs[iin]);  
  f_real = mxGetPr(prhs[iin]);  
  f_is_complex = mxIsComplex(prhs[iin]);
  f_imag = f_is_complex ? mxGetPi(prhs[iin]) : NULL;
  if (reality) {
    fr = (double*)malloc(f_m * f_n * sizeof(double));
    for(t=0; t<f_m; t++)
      for(p=0; p<f_n; p++)
	fr[t*f_n + p] = f_real[p*f_m + t];
  }
  else {
    f = (complex double*)malloc(f_m * f_n * sizeof(complex double));
    for(t=0; t<f_m; t++)
      for(p=0; p<f_n; p++)
	f[t*f_n + p] = f_real[p*f_m + t] 
	  + I * (f_is_complex ? f_imag[p*f_m + t] : 0.0);
  }
  if (f_is_complex && reality)
    mexWarnMsgTxt("Running real transform but input appears to be complex (ignoring imaginary component).");
  if (!f_is_complex && !reality)
    mexWarnMsgTxt("Running complex transform on real signal (set reality flag to improve performance).");

  /* Parse harmonic band-limit L. */
  iin = 1;
  if( !mxIsDouble(prhs[iin]) || 
      mxIsComplex(prhs[iin]) || 
      mxGetNumberOfElements(prhs[iin])!=1 ) {
    mexErrMsgIdAndTxt("ssht_inverse_adjoint_mex:InvalidInput:bandLimit",
		      "Harmonic band-limit must be integer.");
  }
  L = (int)mxGetScalar(prhs[iin]);
  if (mxGetScalar(prhs[iin]) > (double)L || L <= 0)
    mexErrMsgIdAndTxt("ssht_inverse_adjoint_mex:InvalidInput:bandLimitNonInt",
		      "Harmonic band-limit must be positive integer.");

  /* Parse method. */
  iin = 2;
  if( !mxIsChar(prhs[iin]) ) {
    mexErrMsgIdAndTxt("ssht_inverse_adjoint_mex:InvalidInput:methodChar",
		      "Method must be string.");
  }
  len = (mxGetM(prhs[iin]) * mxGetN(prhs[iin])) + 1;
  if (len >= SSHT_STRING_LEN) 
    mexErrMsgIdAndTxt("ssht_inverse_adjoint_mex:InvalidInput:methodTooLong",
		      "Method exceeds string length.");
  mxGetString(prhs[iin], method, len);

  /* Parse spin. */
  iin = 3;
  if( !mxIsDouble(prhs[iin]) || 
      mxIsComplex(prhs[iin]) || 
      mxGetNumberOfElements(prhs[iin])!=1 ) {
    mexErrMsgIdAndTxt("ssht_inverse_adjoint_mex:InvalidInput:spin",
		      "Spin number must be integer.");
  }
  spin = (int)mxGetScalar(prhs[iin]);
  if (mxGetScalar(prhs[iin]) > (double)spin)
    mexErrMsgIdAndTxt("ssht_inverse_adjoint_mex:InvalidInput:spinNonInt",
		      "Spin number must be integer.");
  if (spin >= L)
    mexErrMsgIdAndTxt("ssht_inverse_adjoint_mex:InvalidInput:spinInvalid",
		      "Spin number must be strictly less than band-limit."); 
  if (spin != 0 && reality)
    mexErrMsgIdAndTxt("ssht_inverse_adjoint_mex:InvalidInput:spinReality",
		      "A spin function on the sphere cannot be real."); 

  /* Parse South pole flag. */
  iin = 5;
  if( !mxIsLogicalScalar(prhs[iin]) )
    mexErrMsgIdAndTxt("ssht_inverse_adjoint_mex:InvalidInput:southPoleExists",
		      "South pole flag must be logical.");
  south_pole_exists = mxIsLogicalScalarTrue(prhs[iin]);

  /* Parse South pole sample. */
  iin = 6;
  if( !mxIsDouble(prhs[iin]) || 
      mxGetNumberOfElements(prhs[iin])!=1 ) {
    mexErrMsgIdAndTxt("ssht_inverse_adjoint_mex:InvalidInput:southPoleSample",
		      "South pole sample must be double.");
  }
  fsp_is_complex = mxIsComplex(prhs[iin]);
  fsp_real = mxGetPr(prhs[iin]);  
  fsp_imag = fsp_is_complex ? mxGetPi(prhs[iin]) : NULL;
  if (reality)
    fspr = fsp_real[0];
  else
    fsp = fsp_real[0] 
      + I * (fsp_is_complex ? fsp_imag[0] : 0.0);
  if (fsp_is_complex && reality)
    mexWarnMsgTxt("Running real transform but South pole sample appears to be complex (ignoring imaginary component).");

  /* Parse South pole phi. */
  iin = 7;
  if( !mxIsDouble(prhs[iin]) || 
      mxIsComplex(prhs[iin]) || 
      mxGetNumberOfElements(prhs[iin])!=1 ) {
    mexErrMsgIdAndTxt("ssht_inverse_adjoint_mex:InvalidInput:southPolePhi",
		      "South pole phi must be real double.");
  }
  phi_sp = mxGetScalar(prhs[iin]);

  /* Parse North pole flag. */
  iin = 8;
  if( !mxIsLogicalScalar(prhs[iin]) )
    mexErrMsgIdAndTxt("ssht_inverse_adjoint_mex:InvalidInput:northPoleExists",
		      "North pole flag must be logical.");
  north_pole_exists = mxIsLogicalScalarTrue(prhs[iin]);

  /* Parse North pole sample. */
  iin = 9;
  if( !mxIsDouble(prhs[iin]) || 
      mxGetNumberOfElements(prhs[iin])!=1 ) {
    mexErrMsgIdAndTxt("ssht_inverse_adjoint_mex:InvalidInput:northPoleSample",
		      "North pole sample must be double.");
  }
  fnp_is_complex = mxIsComplex(prhs[iin]);
  fnp_real = mxGetPr(prhs[iin]);  
  fnp_imag = fnp_is_complex ? mxGetPi(prhs[iin]) : NULL;
  if (reality)
    fnpr = fnp_real[0];
  else
    fnp = fnp_real[0] 
      + I * (fnp_is_complex ? fnp_imag[0] : 0.0);
  if (fnp_is_complex && reality)
    mexWarnMsgTxt("Running real transform but North pole sample appears to be complex (ignoring imaginary component).");

  /* Parse North pole phi. */
  iin = 10;
  if( !mxIsDouble(prhs[iin]) || 
      mxIsComplex(prhs[iin]) || 
      mxGetNumberOfElements(prhs[iin])!=1 ) {
    mexErrMsgIdAndTxt("ssht_inverse_adjoint_mex:InvalidInput:northPolePhi",
		      "North pole phi must be real double.");
  }
  phi_np = mxGetScalar(prhs[iin]);

  /* Check polar interface usage valid. */
  if (south_pole_exists || north_pole_exists) {

    if (strcmp(method, SSHT_SAMPLING_MW) != 0 &&
	strcmp(method, SSHT_SAMPLING_MWSS) != 0) 
      mexErrMsgIdAndTxt("ssht_inverse_adjoint_mex:InvalidInput:poleWithInvalidMethod",
			"Polar interfaces only supported by MW or MWSS methods.");

    if (!south_pole_exists)
      mexErrMsgIdAndTxt("ssht_inverse_adjoint_mex:InvalidInput:noSouthPole",
			"South pole sample must be specified if North pole is.");

    if (south_pole_exists && !north_pole_exists)
      if (strcmp(method, SSHT_SAMPLING_MW) != 0)
	mexErrMsgIdAndTxt("ssht_inverse_adjoint_mex:InvalidInput:noNorthPole",
			  "North pole must be specified for MWSS method.");

    if (south_pole_exists && north_pole_exists)
      if (strcmp(method, SSHT_SAMPLING_MWSS) != 0)
	mexErrMsgIdAndTxt("ssht_inverse_adjoint_mex:InvalidInput:northPoleWithInvalidMethod",
			  "North pole must not be specified for MW method.");

  }

  /* Compute adjoint inverse transform. */
  if (strcmp(method, SSHT_SAMPLING_MW) == 0) {

    ntheta = ssht_sampling_mw_ntheta(L);
    nphi = ssht_sampling_mw_nphi(L);
    if (south_pole_exists) {
      if (ntheta-1 != f_m || nphi != f_n)
	mexErrMsgIdAndTxt("ssht_inverse_adjoint_mex:InvalidInput:inconsistentSizesMWpole",
          "Number of function samples inconsistent with method and band-limit.");
    }
    else {
      if (ntheta != f_m || nphi != f_n)
	mexErrMsgIdAndTxt("ssht_inverse_adjoint_mex:InvalidInput:inconsistentSizesMW",
          "Number of function samples inconsistent with method and band-limit.");
    }

    flm = (complex double*)calloc(L*L, sizeof(complex double));

    if (south_pole_exists) {
      if (reality)
	ssht_adjoint_mw_inverse_sov_sym_real_pole(flm, 
						  fr, fspr,
						  L, 
						  dl_method, verbosity);
      else
	ssht_adjoint_mw_inverse_sov_sym_pole(flm, 
					     f, fsp, phi_sp, 
					     L, spin, 
					     dl_method, verbosity);
    }
    else {
      if (reality)
	ssht_adjoint_mw_inverse_sov_sym_real(flm, fr, L, 
					     dl_method, verbosity);
      else
	ssht_adjoint_mw_inverse_sov_sym(flm, f, L, spin, 
					dl_method, verbosity);
    }

    /* mexPrintf("flm_m = %d; flm_n = %d\n", flm_m, flm_n); */
    /* mexPrintf("ntheta = %d; nphi = %d\n", ntheta, nphi); */
    /* mexPrintf("L = %d; spin = %d; reality = %d; verbosity = %d\n",  */
    /* 	      L, spin, reality, verbosity); */

  }
  else if (strcmp(method, SSHT_SAMPLING_MWSS) == 0) {
      
    ntheta = ssht_sampling_mw_ss_ntheta(L);
    nphi = ssht_sampling_mw_ss_nphi(L);
    if (south_pole_exists) {
      if (ntheta-2 != f_m || nphi != f_n)
	mexErrMsgIdAndTxt("ssht_inverse_adjoint_mex:InvalidInput:inconsistentSizesMWSSPole",
          "Number of function samples inconsistent with method and band-limit.");
    }
    else {
      if (ntheta != f_m || nphi != f_n)
	mexErrMsgIdAndTxt("ssht_inverse_adjoint_mex:InvalidInput:inconsistentSizesMWSS",
          "Number of function samples inconsistent with method and band-limit.");
    }

    flm = (complex double*)calloc(L*L, sizeof(complex double));

    if (south_pole_exists) {
      if (reality)
	ssht_adjoint_mw_inverse_sov_sym_ss_real_pole(flm, 
						     fr, fnpr, fspr,
						     L, 
						     dl_method, verbosity);   
      else
	ssht_adjoint_mw_inverse_sov_sym_ss_pole(flm, 
						f, fnp, phi_np, fsp, phi_sp,
						L, spin, 
						dl_method, verbosity);   
    }
    else {
      if (reality)
	ssht_adjoint_mw_inverse_sov_sym_ss_real(flm, fr, L, 
						dl_method, verbosity);
      else
	ssht_adjoint_mw_inverse_sov_sym_ss(flm, f, L, spin, 
					   dl_method, verbosity);
    }

  }
  else {

    mexErrMsgIdAndTxt("ssht_inverse_adjoint_mex:InvalidInput:method",
		      "Method invalid.");

  } 

  /* Copy flm to output. */
  plhs[iout] = mxCreateDoubleMatrix(L*L, 1, mxCOMPLEX);
  flm_real = mxGetPr(plhs[iout]);
  flm_imag = mxGetPi(plhs[iout]);
  for (i=0; i<L*L; i++) {
    flm_real[i] = creal(flm[i]);
    flm_imag[i] = cimag(flm[i]);;
  }

  /* Free memory. */
  free(flm);
  if (reality)
    free(fr);
  else
    free(f);
}
