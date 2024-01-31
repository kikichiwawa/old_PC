#pragma once
#include <string>

class gnuplot
{
private:
	static void open_gnuplot(FILE* gp);
	static void show(FILE* gp, std::string filename);
public:
	static void file_plot(std::string filename);
	//void file_plot(std::string filename, int* x_min = nullptr, int* y_range[]);
};

