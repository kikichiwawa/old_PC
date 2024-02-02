#pragma once
#include <iostream>
#include <complex>

class Fourier
{
private:
	static unsigned int bit_invert(unsigned int N, int keta);//
public:
	Fourier();
	static void DFT(FILE* rfp, FILE* wfp, int N, double f_0, int data_number = 1, int start_N = 0);
	static void FFT(FILE* rfp, FILE* wfp, int N, double f_0, int data_number = 1, int start_N = 0);//データ数Nを2^aでうえから抑えてFFTを行う
};