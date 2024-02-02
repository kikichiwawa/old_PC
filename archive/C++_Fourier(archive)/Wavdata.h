#pragma once
#include <iostream>

class Wavdata //�񈳏k��WAV�t�@�C���݂̂�ΏۂƂ���
{
private:
	FILE *fp;
	std::string filename;
	int file_size, head_size, format_size, subc_size, d_point, data_size, freq, plot_num;
	short chunnel, BperS, Bsize;
	double k;
	void check();//RIFF�CWAVE�Cfmt���ʎq�̃`�F�b�N���񈳏k�t�@�C���ł��邱�Ƃ̊m�F����
	void initialize();//�e��f�[�^�T�C�Y�C�`���l�����C�T���v�����O���g���C�T���v���r�b�g��������
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