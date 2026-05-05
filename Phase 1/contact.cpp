
#include "contact.h"

Email::Email(string type, string email_addr){
    // TODO: Complete me!
    this->type = type;
    this->email_addr = email_addr;

}


void Email::set_contact(){
    // TODO: Do not change the prompts!
    cout << "Enter the type of email address: ";
    std::getline(cin, type);
    cout << "Enter email address: ";
    std::getline(cin, email_addr);
}


string Email::get_contact(string style){
    // Note: We have default argument in declaration and not in definition!
    if (style=="full")
	    return "(" + type + "): " + email_addr;
    else 
        return email_addr;
}


void Email::print(){
    // Note: get_contact is called with default argument
	cout << "Email " << get_contact() << endl;
}


Phone::Phone(string type, string num){
    // TODO: It is possible that num includes "-" or not, manage it!
    // TODO: Complete this method!
    // Note: We don't want to use C++11! stol is not valid!
    this->type = type;
    // Strip dashes and any non-digit characters
    phone_num = "";
    for (size_t i = 0; i < num.size(); i++) {
        if (isdigit(num[i]))
            phone_num += num[i];
    }
}


void Phone::set_contact(){
    // TODO: Complete this method
    // Use the same prompts as given!
	cout <<"Enter the type of phone number: ";
    std::getline(cin, type);
	cout << "Enter the phone number: ";
    string raw;
    std::getline(cin, raw);
    phone_num = "";
    for (size_t i = 0; i < raw.size(); i++) {
        if (isdigit(raw[i]))
            phone_num += raw[i];
    }
}


string Phone::get_contact(string style){
    // TODO: Complete this method, get hint from Email 
    string formatted = phone_num;
    if (phone_num.size() == 10) {
        formatted = phone_num.substr(0, 3) + "-" + phone_num.substr(3, 3) + "-" + phone_num.substr(6, 4);
    }
    if (style == "full") {
        return "(" + type + "): " + formatted;
    }
    return formatted;
}


void Phone::print(){
    // Note: get_contact is called with default argument
	cout << "Phone " << get_contact() << endl;
}
