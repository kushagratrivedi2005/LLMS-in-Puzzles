#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cstdlib>
#include <ctime>
#include <unordered_map>
#include <nlohmann/json.hpp>

using json = nlohmann::json;
using namespace std;

// Function to generate a random string of given length
string generate_random_string(int length) {
    string characters = "abcdef";
    string result;
    for (int i = 0; i < length; ++i) {
        result += characters[rand() % characters.size()];
    }
    return result;
}

// Function to apply a transition to a given string
string apply_transition(const string &current, const string &src, const string &tgt) {
    size_t src_pos = current.find(src);
    size_t tgt_pos = current.find(tgt);

    // If src is found but tgt is also found before src, reject transition
    if (src_pos != string::npos && tgt_pos != string::npos && tgt_pos < src_pos) {
        return current; // Transition is invalid, return unchanged string
    }

    // Apply transition normally
    if (src_pos != string::npos) {
        return current.substr(0, src_pos) + tgt + current.substr(src_pos + src.length());
    }
    return current;
}


// Function to generate transitions while ensuring uniqueness
vector<pair<string, string>> generate_transitions(
    string &initial_string, int num_transitions, int num_unique_transitions, 
    int min_src_length, int max_src_length, int min_tgt_length, int max_tgt_length, 
    int max_usage_per_transition, int max_empty_transitions, vector<int> &solution,
    bool allow_non_empty_to_empty) 
{
    vector<pair<string, string>> transitions;
    unordered_map<string, int> transition_map; // Map src->tgt to index
    unordered_map<string, int> transition_usage; // Tracks usage count
    string current = "";

    for (int i = 0; i < num_transitions; ++i) {
        int src_len = min_src_length + (rand() % (max_src_length - min_src_length + 1));
        int tgt_len = min_tgt_length + (rand() % (max_tgt_length - min_tgt_length + 1));

        string src;
        if (current.empty()) {
            src = generate_random_string(src_len);
        } else {
            if (src_len > current.size()) {
                src_len = current.size();  // Prevent overflow
            }
            size_t pos = rand() % (current.size() - src_len + 1);  // Ensure valid range
            src = current.substr(pos, src_len);
        }
        // Randomly decide if this should be a transition to an empty string
        string tgt;
        bool is_empty_tgt = false;
        if (allow_non_empty_to_empty && max_empty_transitions > 0 && (rand() % 100) < 20) { 
            // 20% probability of making tgt = ""
            tgt = "";
            is_empty_tgt = true;
        } else {
            tgt = generate_random_string(tgt_len);
        }

        if (current.empty()) {
            current = src;
            transitions.emplace_back(src, "");
            transition_map[src + "->"] = transitions.size() - 1; // Store index
            transition_usage[src + "->"] = 1;
            max_empty_transitions--;
            solution.push_back(transitions.size() - 1);
            cout<<"transitions1"<<" "<<transitions.size()-1<<endl;
            cout<<" "<<" "<<src<<" "<<current<<endl;
        } else {
            string key = src + "->" + tgt;

            if (transition_map.find(key) != transition_map.end()) {
                // If transition already exists, reuse index
                if(transition_usage[key]>=max_usage_per_transition){
                   continue;
                }
                solution.push_back(transition_map[key]);
                cout<<"transitions2"<<" "<<transition_map[key]<<endl;
                transition_usage[key]++;
                cout<<src<<" "<<tgt;
            } else {
                if(src==" " && max_empty_transitions<=0){
                    continue;
                }
                if(src==" "){
                    max_empty_transitions--;
                }
                // If it's a new transition, add it (ensuring unique transitions)
                if (transitions.size() < num_unique_transitions) {
                    if(transition_usage[key]>=max_usage_per_transition){
                        continue;
                    }
                    transitions.emplace_back(tgt, src);
                    transition_map[key] = transitions.size() - 1;
                    transition_usage[key] = 1;
                    solution.push_back(transitions.size() - 1);
                    cout<<"transitions3"<<" "<<transitions.size()-1<<endl;
                    cout<<src<<" "<<tgt;
                } else {
                vector<int> valid_indices;
                
                // Find all valid transitions (where 'src' exists in 'current')
                for (int j = 0; j < transitions.size(); ++j) {
                    if (current.find(transitions[j].second) != string::npos) { 
                        valid_indices.push_back(j);
                    }
                }
                // Only reuse a transition if a valid one exists
                if (!valid_indices.empty()) {
                    int existing_index = valid_indices[rand() % valid_indices.size()];
                    if(transition_usage[transitions[existing_index].second + "->" + transitions[existing_index].first]>=max_usage_per_transition){
                        continue;
                    }
                    solution.push_back(existing_index);
                    cout<<"transitions4"<<" "<<existing_index<<endl;
                    transition_usage[transitions[existing_index].second + "->" + transitions[existing_index].first]++;
                   string new_current = apply_transition(current, transitions[existing_index].second, transitions[existing_index].first);
                    string reversed_back = apply_transition(new_current, transitions[existing_index].first, transitions[existing_index].second); // Reverse the transition
                    if (new_current == current || reversed_back != current) {
                        // If the transition didn't change anything or is not reversible, remove last solution step
                        if (!solution.empty()) {
                            transition_usage[transitions[existing_index].second + "->" + transitions[existing_index].first]--;
                            cout << solution.back() << endl;
                            solution.pop_back();
                        }
                        continue; // Skip adding this transition
                    }
                    current = new_current;                   
                    cout<<transitions[existing_index].second<<" "<<transitions[existing_index].first<<" "<<current<<endl;
                    continue;
                } 
            }
            }
            string new_current = apply_transition(current, src, tgt);
            string reversed_back = apply_transition(new_current, tgt, src); // Try to reverse the transition
            if (new_current == current || reversed_back != current) {
                // Transition was invalid or non-reversible, remove the last added solution step
                if (!solution.empty()) {
                    transition_usage[src + "->" + tgt]--;
                    cout << solution.back() << endl;
                    solution.pop_back();
                }
                continue; // Skip adding this transition
            }
            current = new_current;
            cout<<" "<<current<<endl;
        }
    }

    initial_string = current;
    return transitions;
}

// Function to write JSON to a file
void write_json_to_file(const string &filename, const json &j) {
    ofstream file(filename);
    if (file.is_open()) {
        file << j.dump(4);
        file.close();
        cout << "Test case written to " << filename << "\n";
    } else {
        cerr << "Failed to open file for writing." << endl;
    }
}

int main() {
    srand(time(0));
    
    json test_case;
    test_case["problem_id"] = "100";
    
    string problem_id = test_case["problem_id"];  // Extract problem ID
    string initial_string;
    vector<int> solution;

    // Define min/max lengths and transition limits
    int min_src_length = 1; //min length of src string
    int max_src_length = 3; //max length of src string
    int min_tgt_length = 2; //min length of tgt string
    int max_tgt_length = 4; //max length of tgt string
    int num_transitions = 18; // Total steps
    int num_unique_transitions =11; // Unique transition rules allowed
    int max_usage_per_transition = 2;  // Each transition can be applied at most 3 times.
    int max_empty_transitions = 1; // Maximum number of empty transitions allowed.
    bool empty_to_non_empty = false; // Allow transitions from empty to non-empty strings

    if(max_usage_per_transition*num_unique_transitions<num_transitions){
        cout<<"Not possible";
        return 0;
    }
    vector<pair<string, string>> transitions = generate_transitions(
        initial_string, num_transitions, num_unique_transitions, 
        min_src_length, max_src_length, min_tgt_length, max_tgt_length, 
        max_usage_per_transition,max_empty_transitions, solution, empty_to_non_empty);
    
    test_case["initial_string"] = initial_string;
    for (const auto &t : transitions) {
        test_case["transitions"].push_back({{"src", t.first}, {"tgt", t.second}});
    }
    
    reverse(solution.begin(), solution.end());
   // Use problem_id for filenames
    write_json_to_file("../sample-data/puzzles/" + problem_id + ".json", test_case);

    json solution_file;
    solution_file["problem_id"] = problem_id;
    solution_file["solution"] = solution;
    write_json_to_file("../sample-data/solutions/" + problem_id + ".json", solution_file);
    
    return 0;
}
