
#include "network.h"
#include <limits>
#include "misc.h"
#include <fstream>
#include <dirent.h>

Network::Network(){
    head = NULL;
    tail = NULL;
    count = 0;
}


Network::Network(string fileName){
    // TODO: complete this method!
    // Implement it in one single line!
    // You may need to implement the load method before this!
    head = NULL; tail = NULL; count = 0; loadDB(fileName);
}

Network::~Network(){ 
    Person* ptr = head;
    while (ptr != NULL) {
        Person* nxt = ptr->next;
        delete ptr;
        ptr = nxt;
    }
    
}

Person* Network::search(Person* searchEntry){
    // Searches the Network for searchEntry
    // if found, returns a pointer to it, else returns NULL
    // TODO: Complete this method
    Person* ptr = head;
    while (ptr != NULL) {
        if (*ptr == *searchEntry) return ptr;
        ptr = ptr->next;
    }
    return NULL;
}


Person* Network::search(string fname, string lname){
    // New == for Person, only based on fname and lname
    // if found, returns a pointer to it, else returns NULL
    // TODO: Complete this method
    // Note: two ways to implement this, 1st making a new Person with fname and lname and and using search(Person*), 2nd using fname and lname directly. 
    Person* ptr = head;
    while (ptr != NULL) {
        if (ptr->f_name == fname && ptr->l_name == lname)
            return ptr;
        ptr = ptr->next;
    }
    return NULL;
}




void Network::loadDB(string filename){
    // TODO: Complete this method
    ifstream fin(filename.c_str());
    if (!fin.is_open()) return;
    Person* ptr = head;
    while (ptr != NULL) {
        Person* nxt = ptr->next;
        delete ptr;
        ptr = nxt;
    }
    head = NULL;
    tail = NULL;
    count = 0;

    string line;
    while (std::getline(fin, line)) {
        if (line.empty()) continue;
        bool isSep = true;
        for (size_t i = 0; i < line.size(); i++)
            if (line[i] != '-') { isSep = false; break; }
        if (isSep) continue;

        string fname = line;
        string lname, bdate, line4, line5;
        if (!std::getline(fin, lname)) break;
        if (!std::getline(fin, bdate)) break;
        if (!std::getline(fin, line4)) break;
        if (!std::getline(fin, line5)) break;

        string emailLine, phoneLine;
        if (line4.find('@') != string::npos) {
            emailLine = line4; phoneLine = line5;
        } else {
            phoneLine = line4; emailLine = line5;
        }

        Person* p = new Person(fname, lname, bdate, emailLine, phoneLine);
        push_back(p);
    }
    fin.close();
}

void Network::saveDB(string filename){
    // TODO: Complete this method
    ofstream fout(filename.c_str());
    if (!fout.is_open()) return;

    Person* ptr = head;
    while (ptr != NULL) {
        fout << ptr->f_name << "\n";
        fout << ptr->l_name << "\n";
        fout << ptr->birthdate->to_string() << "\n";
        fout << ptr->email->get_contact() << "\n"; 
        fout << ptr->phone->get_contact() << "\n";   
        fout << "--------------------\n";
        ptr = ptr->next;
    }
    fout.close();
}


void Network::printDB(){
    // Leave me alone! I know how to print! 
    // Note: Notice that we don't need to update this even after adding to Personattributes
    // This is a feature of OOP, classes are supposed to take care of themselves!
    cout << "Number of people: " << count << endl;
    cout << "------------------------------" << endl;
    Person* ptr = head;
    while(ptr != NULL){
        ptr->print_person();
        cout << "------------------------------" << endl;
        ptr = ptr->next;
    }
}



void Network::push_front(Person* newEntry){
    newEntry->prev = NULL;
    newEntry->next = head;

    if (head != NULL)
        head->prev = newEntry;
    else
        tail = newEntry;
    
    head = newEntry;
    count++;
}


void Network::push_back(Person* newEntry){
    // Adds a new Person (newEntry) to the back of LL
    // TODO: Complete this method
    newEntry->next = NULL;
    newEntry->prev = tail;
    if (tail != NULL) tail->next = newEntry;
    else head = newEntry;
    tail = newEntry;
    count++;
}


bool Network::remove(string fname, string lname){
    // TODO: Complete this method
    Person* found = search(fname, lname);
    if (found == NULL) return false;

    if (found->prev != NULL) found->prev->next = found->next;
    else head = found->next;

    if (found->next != NULL) found->next->prev = found->prev;
    else tail = found->prev;

    delete found;
    count--;
    return true;
}


void Network::showMenu(){
    // TODO: Complete this method!
    // All the prompts are given to you, 
    // You should add code before, between and after prompts!

    int opt;
    while(1){
        cout << "\033[2J\033[1;1H";
        printMe("banner"); // from misc library

        cout << "Select from below: \n";
        cout << "1. Save network database \n";
        cout << "2. Load network database \n";
        cout << "3. Add a new person \n";
        cout << "4. Remove a person \n";
        cout << "5. Print people with last name  \n";
        cout << "6. Connect \n"; //phase 2
        cout << "7. Wise Search \n";
        cout << "\nSelect an option ... ";
        
        if (cin >> opt) {
            cin.clear();
            cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        } else {
            cin.clear();
            cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            cout << "Wrong option! " << endl;
            return;
        }
        
        // You may need these variables! Add more if you want!
        string fname, lname, fileName, bdate;
        cout << "\033[2J\033[1;1H";

        if (opt==1){
            // TODO: Complete me!
            cout << "Saving network database \n";
            cout << "Enter the name of the save file: ";
            std::getline(cin, fileName);
            saveDB(fileName);
            // Save the network database into the file with the given name,
            // with each person saved in the format the save as printing out the person info,
            // and people are delimited similar to "networkDB.txt" format
            cout << "Network saved in " << fileName << endl;
        }
        else if (opt==2){
            // TODO: Complete me!
            cout << "Loading network database \n";
            // TODO: print all the files in this same directory that have "networkDB.txt" format
            // print format: one filename one line.
            // This step just shows all the available .txt file to load.
            DIR* dir = opendir(".");
            if (dir != NULL) {
                struct dirent* entry;
                while ((entry = readdir(dir)) != NULL) {
                    string name = entry->d_name;
                    if (name.size() > 4 && name.substr(name.size() - 4) == ".txt")
                        cout << name << endl;
                }
                closedir(dir);
            }
            cout << "Enter the name of the load file: "; 
            std::getline(cin, fileName);
            ifstream test(fileName.c_str());
            if (!test.is_open()) {
                // If file with name FILENAME does not exist: 
                cout << "File " << fileName << " does not exist!" << endl;
            } else {
                test.close();
                loadDB(fileName);
                // If file is loaded successfully, also print the count of people in it: 
                cout << "Network loaded from " << fileName << " with " << count << " people \n";
            }
        }
        else if (opt == 3){
            // TODO: Complete me!
            // TODO: use push_front, and not push_back 
            // Add a new Person ONLY if it does not exists!
            cout << "Adding a new person \n";
            Person* p = new Person();
            if (search(p) == NULL) {
                push_front(p);
                cout << "Person added! \n";
            } else {
                cout << "Person already exists! \n";
                delete p;
            }
        }
        else if (opt == 4){
            // TODO: Complete me!
            // if found, cout << "Remove Successful! \n";
            // if not found: cout << "Person not found! \n";
            cout << "Removing a person \n";
            cout << "First name: ";
            std::getline(cin, fname);
            cout << "Last name: ";
            std::getline(cin, lname);
            if (remove(fname, lname))
                cout << "Remove Successful! \n";
            else
                cout << "Person not found! \n";
        }
        else if (opt==5){
            // TODO: Complete me!
            // print the people with the given last name
            // if not found: cout << "Person not found! \n";
            cout << "Print people with last name \n";
            cout << "Last name: ";
            std::getline(cin, lname);
            Person* ptr = head;
            bool any = false;
            while (ptr != NULL) {
                if (ptr->l_name == lname) {
                    ptr->print_person();
                    cout << "------------------------------" << endl;
                    any = true;
                }
                ptr = ptr->next;
            }
            if (!any) cout << "Person not found! \n";
        }
        else if (opt == 6){
            cout << "Make friends \n";
            cout << "Person 1\n";
            cout << "First Name: ";
            std::getline(cin, fname);
            cout << "Last Name: ";
            std::getline(cin, lname);
            Person* p1 = search(fname, lname);
            if (p1 == NULL) {
                cout << "Person not found \n";
            } else {
                string fname2, lname2;
                cout << "Person 2\n";
                cout << "First Name: ";
                std::getline(cin, fname2);
                cout << "Last Name: ";
                std::getline(cin, lname2);
                Person* p2 = search(fname2, lname2);
                if (p2 == NULL) {
                    cout << "Person not found \n";
                } else {
                    cout << "\n";
                    p1->print_person();
                    cout << "\n";
                    p2->print_person();
                    p1->makeFriend(p2);
                    p2->makeFriend(p1);
                }
    }
}
        else if (opt == 7){
            cout << "Wise Search \n";
            cout << "Search By: \n";
            string query;
            std::getline(cin, query);

            bool found = false;
            Person* ptr = head;
            while (ptr != NULL) {
                bool match = false;
                if (ptr->phone->get_contact().find(query) != string::npos) // check phone
                    match = true;
                if (ptr->email->get_contact().find(query) != string::npos)  // check email
                    match = true;
                if (ptr->birthdate->to_string().find(query) != string::npos) // check birthdate
                    match = true;
                if (ptr->f_name.find(query) != string::npos)
                    match = true;
                if (ptr->l_name.find(query) != string::npos)
                    match = true;

                if (match) {
                    ptr->print_person();
                    cout << "------------------------------" << endl;
                    found = true;
                }
                ptr = ptr->next;
            }
            if (!found)
                cout << "Person not found \n";
        }
        else
            cout << "Nothing matched!\n";
        
        cin.clear();
        cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        cout << "\n\nPress Enter key to go back to main menu ... ";
        string temp;
        std::getline (std::cin, temp);
        cout << "\033[2J\033[1;1H";
    }
}
