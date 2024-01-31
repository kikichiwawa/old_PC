#include "some_exception.h"

some_exception::some_exception(const char* get_msg) {
	msg = get_msg;
}

const char* some_exception::what() { 
	return msg;
}
