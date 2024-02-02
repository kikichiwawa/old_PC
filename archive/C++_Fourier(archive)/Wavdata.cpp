#include <iostream>
#include <regex>
#include "Wavdata.h"
#include "some_exception.h"
#include "gnuplot.h"
#include "Fourier.h"


constexpr auto WAV = ".wav";
constexpr auto DAT = ".dat";

inline void freade(void* address, unsigned __int64 size, int times, FILE* fp) {
	if (!(fread(address, size, times, fp))) {
		throw some_exception("読み取りエラー");
	}
}

Wavdata::Wavdata(std::string gfilename, bool show) {
	size_t i = gfilename.rfind(".");
	if (i == std::string::npos) {
		filename = gfilename;
	}
	else {
		filename = gfilename.substr(0, i);
	}

	try {
		if ((fopen_s(&fp, (filename + WAV).c_str(), "rb")) != 0) {
			std::cout << (filename + WAV).c_str() << "\n";
			throw some_exception("ファイルが開けません");
		}
		check();
	}
	catch (some_exception e) {
		std::cout << e.what() <<"\n";
		ex_initialize();
	}

	initialize();
	if (show) {
		wdata();
	}

}

Wavdata::~Wavdata() {
	fclose(fp);
}

void Wavdata::initialize(){
	fseek(fp, 4, SEEK_SET);
	freade(&file_size, sizeof(int), 1, fp);
	file_size += 8;

	head_size = 20;

	fseek(fp, 8, SEEK_CUR);
	freade(&format_size, sizeof(int), 1, fp);

	subc_size = 8;

	data_size = file_size - head_size - format_size - subc_size;

	fseek(fp, 2, SEEK_CUR);
	freade(&chunnel, sizeof(short), 1, fp);

	freade(&freq, sizeof(int), 1, fp);

	fseek(fp, 4, SEEK_CUR);
	freade(&Bsize, sizeof(short), 1, fp);

	freade(&BperS, sizeof(short), 1, fp);
	
	d_point = head_size + format_size + subc_size;

	plot_num = data_size * 8 / BperS / chunnel;

	k = 1.0 / freq;
}

void Wavdata::ex_initialize() {
	file_size = head_size = format_size = data_size = chunnel = freq = Bsize = BperS = k =0;
}

void Wavdata::getinfo() {
	printf("file_size  : %d\n", file_size);
	printf("head_size  : %d\n", head_size);
	printf("format_size: %d\n", format_size);
	printf("subc_size  : %d\n", subc_size);
	printf("deta_point : %d\n\n", d_point);

	printf("data_size  : %d\n\n", data_size);

	printf("chunnel    : %d\n", chunnel);
	printf("freqency   : %d\n", freq);
	printf("k          : %f\n", k);
	printf("bits / s   : %d\n", BperS);
	printf("deta_point : %d\n", d_point);
	printf("plot num   : %d\n", plot_num);
}

void Wavdata::wdata() {
	FILE* wfp = 0;
	try {
		if ((fopen_s(&wfp, (filename + ".dat").c_str(), "w")) != 0) {
			throw some_exception("書き出しファイルを作成できません");
		}

		getdata(wfp);

	}catch (some_exception e) {
		std::cout << e.what() << "\n";
	}

	if (wfp != 0) {
		fclose(wfp);
	}
	try {
		gnuplot::file_plot((filename + DAT).c_str());
	}
	catch(some_exception e) {
		std::cout << e.what() << "\n";
	}
}

void Wavdata::getdata(FILE *wfp) {
	fseek(fp, d_point, SEEK_SET);
	fseek(wfp, 0, SEEK_SET);
	
	if (BperS == 8) {
		double ratio = 1.0 / 128;
		if (chunnel == 1) {
			char buf;

			for (int i = 0; i < plot_num; i++) {
				freade(&buf, sizeof(char), 1, fp);
				fprintf(wfp, "%f\t%f\n", i * k, buf * ratio);
			}
		}
		else if (chunnel == 2) {
			char buf[2];
			for (int i = 0; i < plot_num; i++) {
				freade(buf, sizeof(char), 2, fp);
				fprintf(wfp, "%f\t%f\t%f\n", i * k, buf[0] * ratio, buf[1] * ratio);
			}
		}
		else {
			throw some_exception("予期せぬファイル構造です");
		}
	}else if(BperS == 16) {
		double ratio = 1.0 / 32767;
		if (chunnel == 1) {
			short buf;
			for (int i = 0; i < plot_num; i++) {
				freade(&buf, sizeof(short), 1, fp);
				fprintf(wfp, "%f\t%2.6f", i * k, buf * ratio);
				if (buf < 0) {
					fprintf(wfp, "\n");
				}
				else {
					fprintf(wfp, " \n");
				}
			}
		}
		else if (chunnel == 2) {
			short buf[2];
			for (int i = 0; i < plot_num; i++) {
				freade(buf, sizeof(short), 2, fp);
				fprintf(wfp, "%f\t%f\t%f\n", i * k, buf[0] * ratio, buf[1] * ratio);
			}
		}
		else {
			throw some_exception("予期せぬファイル構造です");
		}
	}else {
		throw some_exception("予期せぬファイル構造です");
	}
}

void Wavdata::check() //RIFF，WAVE，fmt識別子のチェック＆非圧縮ファイルであることの確認する

{
	char RIFF[4], WAV[4], FMT[4];
	char RIFF2[] = "RIFF", WAV2[] = "WAVE", FMT2[] = "fmt ";
	short buf_format;
	fseek(fp, 0, SEEK_SET);

	freade(RIFF, sizeof(char), 4, fp);

	fseek(fp, 4, SEEK_CUR);
	freade(WAV, sizeof(char), 4, fp);

	freade(FMT, sizeof(char), 4, fp);

	fseek(fp, 4, SEEK_CUR);
	freade(&buf_format, sizeof(short), 1, fp);

	for (int i = 0; i < 4; i++) {
		if ((RIFF[i] != RIFF2[i]) || (WAV[i] != WAV2[i]) || (FMT[i] != FMT2[i])) {
			throw some_exception("形式がWAVと一致しません");
		}
	}
	if (buf_format != 1) {
		throw some_exception("圧縮形式です");
	}
}

void Wavdata::DFT() {
	FILE* rfp=0;
	FILE* wfp=0;
	try {
		if ((fopen_s(&rfp, (filename + ".dat").c_str(), "r")) != 0) {
			throw some_exception("書き出しファイルを作成できません");
		}
		if ((fopen_s(&wfp, (filename + "_DFT.dat").c_str(), "w")) != 0) {
			throw some_exception("書き出しファイルを作成できません");
		}

		double f_0 = (double)freq / (double)plot_num;
		Fourier::DFT(rfp, wfp, plot_num , f_0);
	}
	catch (some_exception e) {
		std::cout << e.what() << "\n";
	}
	if (wfp != 0) {
		fclose(wfp);
	}
	try {
		gnuplot::file_plot((filename + "_DFT.dat").c_str());
	}
	catch (some_exception e) {
		std::cout << e.what() << "\n";
	}
}

void Wavdata::FFT(int chunnel) {
	FILE* rfp = 0;
	FILE* wfp = 0;
	try {
		if ((fopen_s(&rfp, (filename + ".dat").c_str(), "r")) != 0) {
			throw some_exception("書き出しファイルを作成できません");
		}
		if ((fopen_s(&wfp, (filename + "_FFT.dat").c_str(), "w")) != 0) {
			throw some_exception("書き出しファイルを作成できません");
		}

		double f_0 = (double)freq / (double)plot_num;
		Fourier::FFT(rfp, wfp, plot_num, f_0, chunnel, 0);
		//Fourier::FFT(rfp, wfp, 65536, f_0);
	}
	catch (some_exception e) {
		std::cout << e.what() << "\n";
	}
	if (wfp != 0) {
		fclose(wfp);
	}
	try {
		gnuplot::file_plot((filename + "_FFT.dat").c_str());
	}
	catch (some_exception e) {
		std::cout << e.what() << "\n";
	}
}

void Wavdata::makepitch(std::string wfilename) {
	FILE* wfp;
	try {
		if ((fopen_s(&wfp, (filename + ".dat").c_str(), "w")) != 0) {
			throw some_exception("書き出しファイルを作成できません");
		}
	}
	catch (some_exception e) {
		std::cout << e.what() << "\n";
	}
}