#include <iostream>
#include <fstream>
#include <string>
#include <vector>
using namespace std;

/* Input file format:
 * The name of the movie is followed with the name of the cast
 * Each entry is in separate lines
 * Movies are separated from each other by dashed lines
 */

int main(){
    ifstream infile;
    infile.open("sample.txt");
    string buff;

    vector <string> movie;
    vector < vector<string> > cast;
    vector <string> temp;

    while (getline(infile, buff)){
        temp.clear();
        movie.push_back(buff);
        getline(infile, buff);

        while(buff.compare(0, 5, "-----") != 0){
            temp.push_back(buff);
            getline(infile, buff);
        }
        
        cast.push_back(temp);
    }
    for (int i=0; i<movie.size(); i++){
        cout << "Movie Name: " << movie[i] << endl;
        for (int j=0; j<cast[i].size(); j++)
            cout << "--- " << cast[i][j] << endl;
    }

    return 0;
}