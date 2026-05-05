#ifndef DATE_H
#define DATE_H
#include <iostream>
#include <string>
#include <sstream>
using namespace std;

class Date {
private:
    int month;
    int day;
    int year;
public:
    Date();
    Date(string date);
    string to_string();
    void print_date(string style = "Month D, YYYY");
    bool operator==(const Date& rhs);
    bool operator!=(const Date& rhs);
};

#endif