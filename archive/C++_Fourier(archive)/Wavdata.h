#pragma once
#include <iostream>

class Wavdata //非圧縮のWAVファイルのみを対象とする
{
private:
	FILE *fp;
	std::string filename;
	int file_size, head_size, format_size, subc_size, d_point, data_size, freq, plot_num;
	short chunnel, BperS, Bsize;
	double k;
	void check();//RIFF，WAVE，fmt識別子のチェック＆非圧縮ファイルであることの確認する
	void initialize();//各種データサイズ，チャネル数，サンプリング周波数，サンプルビットを初期化
	void ex_initialize();
	void getdata(FILE *wfp);

public:
	Wavdata(std::string filename, bool show = true);
	~Wavdata();
	
	void getinfo();
	void wdata();
	void DFT();
	void FFT(int chunnel = 1);
	void makepitch(std::string wfilename);
};