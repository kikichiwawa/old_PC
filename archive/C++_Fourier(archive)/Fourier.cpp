#include "Fourier.h"
#include <iostream>
#include <complex>
#include "some_exception.h"

#define PI 3.14159265358979323846

Fourier::Fourier() {

}

unsigned int Fourier::bit_invert(unsigned int N, int keta) {
	N = (N & 0x55555555) << 1 | (N >> 1) & 0x55555555;
	N = (N & 0x33333333) << 2 | (N >> 2) & 0x33333333;
	N = (N & 0x0F0F0F0F) << 4 | (N >> 4) & 0x0F0F0F0F;
	N = (N << 24) | ((N & 0xFF00) << 8) |
		((N >> 8) & 0xFF00) | (N >> 24);
	N = N >> (32 - keta);
	return N;
}

void printb(unsigned int v) {
	unsigned int mask = (int)1 << (sizeof(v) * CHAR_BIT - 1);
	do putchar(mask & v ? '1' : '0');
	while (mask >>= 1);
}

void putb(unsigned int v) {
	putchar('0'), putchar('b'), printb(v), putchar('\n');
}


void Fourier::FFT(FILE* rfp, FILE* wfp, int N, double f_0, int data_number, int start_N) {
	int keta = NULL;
	int NN;
	for (int a = 1; a < 32; a++) {
		NN = pow(2, a);
		if (N <= NN ) {
			keta = a;
			break;
		}
	}
	unsigned N_;
	if (keta == NULL) {
		throw some_exception("オーバーフローが発生しました");
	}
	else {
		N_ = pow(2, keta);
	}
	printf("N_ = %d\n", N_);
	char* buf_str;
	double* f;
	if (!(buf_str = (char*)malloc(sizeof(char) * 40))) {
		throw some_exception("メモリの確保に失敗しました");
	}
	if (!(f = (double*)calloc(N_, sizeof(double)))){
		free(buf_str);
		buf_str = NULL;
		throw some_exception("メモリの確保に失敗しました");
	}
	std::cout << sizeof(f) << "f\n";
	printf("three:%d\n",keta);
	//データのバッファへの書き出し
	char buf_f[10];
	buf_f[9] = '\0';
	fseek(rfp, 20 * start_N, SEEK_SET);
	unsigned int n;
	printf("N:%d\n", N);
	for (unsigned int j = 0; j < N; j++) {
		if (!(fgets(buf_str, 40, rfp))) {
			std::cout << j << "\n";
			throw some_exception("読み込みに失敗しました");
		}
		for (int k = 0; k < 8; k++) {
			buf_f[k] = buf_str[k + 9];
		}
		buf_f[8] = buf_str[17];

		n = Fourier::bit_invert(j, keta);
		f[n] = atof(buf_f);
	}
	free(buf_str);
	buf_str = NULL;

	//FFTに用いるWの計算
	std::complex<double>* W;
	if (!(W = (std::complex<double>*)malloc(sizeof(std::complex<double>) * ((long)keta + 1)))) {
		free(f);
		f = NULL;
		throw some_exception("メモリの確保に失敗しました");
	}

	std::complex<double> c = (0,0);
	double d = -2.0 * PI / N_;
	for (int i = 0; i <= keta; i++) {
		c.imag(d * pow(2, i));
		W[keta  -i] = exp(c);
	}

	std::complex<double> *F;
	unsigned int size = N_ * sizeof(std::complex<double>);
	if (!(F = (std::complex<double>*)malloc(size))) {
		free(f);
		f = NULL;
		free(W);
		W = NULL;
		throw some_exception("メモリの確保に失敗しました");
	}
	std::complex<double> buf_even = (0, 0);
	std::complex<double> buf_odd = (0, 0);
	//1回目はfよりFにうつす

	int i_max = N_ * 0.5, k_m_half = 1, even_index, odd_index;
	for (int i = 0; i < i_max; i++) {
		even_index = 2 * i * k_m_half + 0;//k = 0
		odd_index = even_index + k_m_half;
		buf_even.real(*(f + even_index));
		buf_odd.real(*(f + odd_index));

		*(F + even_index) = buf_even + buf_odd * pow(W[1],0);
		*(F + odd_index) = buf_even + buf_odd * pow(W[1],1);
	}


	printf("%d:%d\n", i_max, k_m_half * 2);
	for (int a = 1; a < keta; a++) {
		i_max *= 0.5;
		k_m_half *= 2;
		for (int i = 0; i < i_max; i++) {
			for (int k = 0; k < k_m_half; k++) {
				even_index = 2 * i * k_m_half + k;
				odd_index = even_index + k_m_half;
				buf_even = *(F + even_index);
				buf_odd = *(F + odd_index);

				*(F + even_index) = buf_even + buf_odd * pow(W[a + 1], k);
				*(F + odd_index) = buf_even + buf_odd * pow(W[a + 1], k + k_m_half);
			}
		}
		printf("%d:%d\n", i_max, k_m_half * 2);
	}

	//2回目以降はbuf_F自身に対して移す
	double freq;
	int k_max2 = N_ * 0.5;
	double buf_F;
	for(int k = 0; k < k_max2; k++){
		buf_F = abs(F[k]);
		freq = (double)k * f_0;
		fprintf(wfp, "%f\t%f\n", freq, buf_F);
	}

	free(f);
	f = NULL;
	free(W);
	W = NULL;
	free(F);
	F = NULL;
}


void Fourier::DFT(FILE* rfp, FILE* wfp, int N, double f_0, int data_number, int start_N) {
	int f_times = N / 2;
	char* buf_str;
	buf_str = (char*)malloc(sizeof(char)*40);
	char  buf_f[10];
	buf_f[9] = '\0';

	double *f;
	f = (double*)malloc(sizeof(double)*N);

	if (!(f && buf_str)) {
		throw some_exception("メモリ確保に失敗しました");
	}

	std::complex<double> buf_c;

	//データのバッファへの書き出し
	fseek(rfp, 20 * start_N, SEEK_SET);
	for (int j = 0; j < N; j++) {
		fgets(buf_str, 40, rfp);
		for (int k = 0; k < 9; k++) {
			buf_f[k] = buf_str[k + 9];
		}
		f[j] = atof(buf_f);

	}

	//フーリエ係数の計算

	std::complex<double> a = (0.0, 0.0);
	int check = 0;
	double b = 2 * PI / (double)N;
	printf("%f\n", f_0);
	for (int i = 0; i < f_times; i++) {	
		buf_c = (0.0, 0.0);
		for (int j = 0; j < N; j++) {
			a.imag(b * i * j);
			buf_c += f[j] * exp(a);
		}
		double freq = i * f_0;
		fprintf(wfp, "%f\t%2.6f\n", freq, std::abs(buf_c));

		if (check == 100) {
			printf("w:%d\n", i);
			check = 0;
		}
		check++;
	}
	free(buf_str);
	free(f);
}