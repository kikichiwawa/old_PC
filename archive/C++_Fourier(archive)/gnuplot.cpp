#include "gnuplot.h"
#include <iostream>
#include "some_exception.h"


constexpr auto GNUPLOT_PATH = "C:/PROGRA~1/gnuplot/bin/gnuplot.exe"; //gnuplot.exeへのPATH
constexpr auto HERE_PATH = "C:/Users/nishi/pp-C&C++/testprojects/tpr1/tpr1/";

void gnuplot::open_gnuplot(FILE* gp) {

}

void gnuplot::show(FILE* gp, std::string filename) {
	fprintf(gp, "plot \"%s\" with lines linetype 1 \n", filename.c_str());
	fflush(gp);

	std::cout << "範囲を指定して表示し直しますか？（Y / その他の入力）\n";

	std::string s;
	getline(std::cin, s);
	if ((s == "Y") || (s == "y")) {
		std::cout << "x軸の範囲を指定してください．（最小値，スペース，最大値）\n";
		double x_min, x_max;
		std::cin >> x_min >> x_max;
		if (std::cin.good() != 0) {
			fprintf(gp, "set xrange [%f:%f]\n", x_min, x_max);
		}

		std::cout << "y軸の範囲を指定してください．（最小値，スペース，最大値）\n";
		double y_min, y_max;
		std::cin >> y_min >> y_max;
		if (std::cin.good() != 0) {
			fprintf(gp, "set yrange [%f:%f]\n", y_min, y_max);
		}

		getline(std::cin, s);
		gnuplot::show(gp, filename);
	}
}

void gnuplot::file_plot(std::string gfilename) {
	std::string filename = HERE_PATH + gfilename;
	FILE* gp = 0;

	if (!(gp = _popen(GNUPLOT_PATH, "w"))) {	// gnuplotをパイプで起動
		throw some_exception("gnuplotを開けません");
	}
	gnuplot::open_gnuplot(gp);

	gnuplot::show(gp, filename);
	_pclose(gp);
}