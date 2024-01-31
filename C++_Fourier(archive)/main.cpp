#include <iostream>
#include "Wavdata.h"
#include "gnuplot.h"


int main(){
	/*
	std::string filename = "test.wav";

	Wavdata twav(filename, false);
	twav.getinfo();
	twav.FFT();
	*/
	std::string filename = "test.wav";

	Wavdata twav(filename, true);
	twav.getinfo();
	twav.FFT();
	twav.DFT();
}
