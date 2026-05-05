#include "date.h"

Date::Date() : month(0), day(0), year(0) {}

Date::Date(string date) {
    stringstream ss(date);
    char slash;
    ss >> month >> slash >> day >> slash >> year;
}
void Date::print_date(string style) {
    string months[] = {"January", "February", "March", "April", "May", "June","July", "August", "September", "October", "November", "December"};
    if (style == "Month D, YYYY") {
        cout << months[month - 1] << " " << day << ", " << year << endl;
    } else {
        cout << month << "/" << day << "/" << year << endl;
    }
}
bool Date::operator==(const Date& rhs) {
    return (month == rhs.month && day == rhs.day && year == rhs.year);
}
bool Date::operator!=(const Date& rhs) {
    return !(*this == rhs);
}

string Date::to_string() {
    stringstream ss;
    ss << month << "/" << day << "/" << year;
    return ss.str();
}