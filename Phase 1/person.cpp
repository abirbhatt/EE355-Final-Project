
#include "person.h"
#include "misc.h"

Person::Person(){
    // I'm already done! 
    set_person();
}


Person::~Person(){
    delete birthdate;
    // TODO: complete the method!
    delete email;
    delete phone;
}


Person::Person(string f_name, string l_name, string b_date, string email, string phone){
    // TODO: Complete this method!
    // phone and email strings are in full version
    this->f_name = f_name;
    this->l_name = l_name;
    this->birthdate = new Date(b_date);
    size_t eOpen  = email.find('(');
    size_t eClose = email.find(')');
    string eType  = email.substr(eOpen + 1, eClose - eOpen - 1);
    string eVal   = email.substr(eClose + 1);
    while (!eVal.empty() && eVal[0] == ' ') eVal.erase(0, 1);
    this->email = new Email(eType, eVal);

    size_t pOpen  = phone.find('(');
    size_t pClose = phone.find(')');
    string pType  = phone.substr(pOpen + 1, pClose - pOpen - 1);
    string pVal   = phone.substr(pClose + 1);
    while (!pVal.empty() && pVal[0] == ' ') pVal.erase(0, 1);
    this->phone = new Phone(pType, pVal);

    next = NULL;
    prev = NULL;
    
}


Person::Person(string filename){
    set_person(filename);
}


void Person::set_person(){
    // prompts for the information of the user from the terminal
    // first/last name can have spaces!
    // date format must be "M/D/YYYY"
    // We are sure user enters info in correct format.
    // TODO: complete this method!
    
    string temp;
    string type;

    cout << "First Name: ";
    // pay attention to how we read first name, as it can have spaces!
    std::getline(std::cin,f_name);

	cout << "Last Name: ";
    std::getline(std::cin,l_name);

    cout << "Birthdate (M/D/YYYY): ";
    std::getline(std::cin,temp);
    // pay attention to how we passed argument to the constructor of a new object created dynamically using new command
    birthdate = new Date(temp); 

    cout << "Type of email address: ";
    // code here
    string eType, eAddr;
    std::getline(std::cin, eType);
    cout << "Email address: ";
    // code here
    std::getline(std::cin, eAddr);
    email = new Email(eType, eAddr);

    cout << "Type of phone number: ";
    // code here
    string pType, pNum;
    std::getline(std::cin, pType);
    cout << "Phone number: ";
    // code here
    std::getline(std::cin, pNum);
    // code here
    phone = new Phone(pType, pNum);

    next = NULL;
    prev = NULL;
}


void Person::set_person(string filename){
    // reads a Person from a file
    // Look at person_template files as examples.     
    // Phone number in files can have '-' or not.
    // TODO: Complete this method!
    ifstream fin(filename.c_str());
    string bdateLine, line4, line5;
    std::getline(fin, f_name);
    std::getline(fin, l_name);
    std::getline(fin, bdateLine);
    birthdate = new Date(bdateLine);
    std::getline(fin, line4);
    std::getline(fin, line5);
    string emailLine, phoneLine;
    if (line4.find('@') != string::npos) {
        emailLine = line4;
        phoneLine = line5;
    } else {
        phoneLine = line4;
        emailLine = line5;
    }
    size_t eOpen  = emailLine.find('(');
    size_t eClose = emailLine.find(')');
    string eType  = emailLine.substr(eOpen + 1, eClose - eOpen - 1);
    string eVal   = emailLine.substr(eClose + 1);
    while (!eVal.empty() && eVal[0] == ' ') eVal.erase(0, 1);
    email = new Email(eType, eVal);

    size_t pOpen  = phoneLine.find('(');
    size_t pClose = phoneLine.find(')');
    string pType  = phoneLine.substr(pOpen + 1, pClose - pOpen - 1);
    string pVal   = phoneLine.substr(pClose + 1);
    while (!pVal.empty() && pVal[0] == ' ') pVal.erase(0, 1);
    phone = new Phone(pType, pVal);

    next = NULL;
    prev = NULL;

    fin.close();
}


bool Person::operator==(const Person& rhs){
    // TODO: Complete this method!
    // Note: you should check first name, last name and birthday between two persons
    // refer to bool Date::operator==(const Date& rhs)
    if (f_name != rhs.f_name) return false;
    if (l_name != rhs.l_name) return false;
    return (*birthdate == *(rhs.birthdate));
}

bool Person::operator!=(const Person& rhs){ 
    // TODO: Complete this method!
    return !(*this == rhs);
}   


void Person::print_person(){
    // Already implemented for you! Do not change!
	cout << l_name <<", " << f_name << endl;
	birthdate->print_date("Month D, YYYY");
    phone->print();
    email->print();
    for (int i = 0; i < myfriends.size(); i++) {
        string code = CodeName(myfriends[i]->f_name, myfriends[i]->l_name);
        cout << code << " (" << myfriends[i]->f_name << " " << myfriends[i]->l_name << ")" << endl;
    }
}
void Person::makeFriend(Person* newFriend) { //phase 2
    myfriends.push_back(newFriend);
}
void Person::print_friends(){
    // Print this person's own name
    cout << f_name << ", " << l_name << endl;
    cout << "--------------------------------" << endl;

    vector<Person*> sorted = myfriends;

    // Sort by first two letters of each friend's code
    for (int i = 0; i < sorted.size(); i++) {
        for (int j = i + 1; j < sorted.size(); j++) {
            string ci = CodeName(sorted[i]->f_name, sorted[i]->l_name);
            string cj = CodeName(sorted[j]->f_name, sorted[j]->l_name);
            bool swap = false;
            if (ci[0] > cj[0]) {
                swap = true;
            } else if (ci[0] == cj[0] && ci[1] > cj[1]) {
                swap = true;
            }
            if (swap) {
                Person* tmp = sorted[i];
                sorted[i] = sorted[j];
                sorted[j] = tmp;
            }
        }
    }
    //Print
    for (int i = 0; i < sorted.size(); i++) {
        cout << sorted[i]->f_name << ", " << sorted[i]->l_name << endl;
    }
}