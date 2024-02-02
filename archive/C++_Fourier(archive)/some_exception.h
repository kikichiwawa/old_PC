#pragma once
class some_exception
{
private:
	const char* msg;

public:
	some_exception(const char* msg);
	const char* what();
};

