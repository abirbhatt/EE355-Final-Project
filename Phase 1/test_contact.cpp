#include "contact.h"

int main() {
    Email e("Work", "julia@wh.com");
    e.print();   // expect: (Work) julia@wh.com

    Phone p("Home", "310-192-2011");
    p.print();   // expect: (Home) 310-192-2011

    Phone p2("Cell", "3101922011");  // no dashes
    p2.print();  // expect: (Cell) 310-192-2011

    return 0;
}