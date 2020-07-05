// SmartBin_emulator.cpp : Questo file contiene la funzione 'main', in cui inizia e termina l'esecuzione del programma.
//

#define CURL_STATICLIB

#include <iostream>
#include <stdio.h>  
#include <stdlib.h> 
#include <time.h>   
#include <thread>
#include <vector>
#include <signal.h>
#include <atomic>
#include <curl/curl.h>

using namespace std;

// TODO move this to compile time - only if this fucking visual studio works!!!
#define _MY_USR "brunello"
#define _MY_PWD "SB2uyRpApwWp8znr"

const string _url_base = "http://techlabcommunity.org:6662/devices/rubbish/";


string _token = "";
const unsigned int n_bins = 10;

vector<thread> smartbin_threads_vect;
thread token_refresh_thread;

//Threads shared variables
atomic_bool _should_run = true;
atomic_bool _token_is_fresh = false;

typedef struct {
	double longitude;
	double latitude;
}long_lat;

typedef struct {
	string serial_no;
	string code;
	long_lat coord;
	string model_no;
	string brand;
	string status_code;
	double prev_weight;
	double curr_weight;
}smartbin_data;

long_lat smartbins_coord[n_bins] = {
	{11.87581,  45.40671},
	{11.87466,  45.40692},
	{11.87977,  45.41295},
	{11.88058,  45.41175},
	{11.87911,  45.41197},
	{11.87938,  45.41231},
	{11.8724,   45.40261},
	{11.87616,  45.40506},
	{11.87305,  45.40593},
	{11.887883, 45.44891},
};

smartbin_data smartbin_data_arr[n_bins] = {
	{"70940737", "SF-600707", smartbins_coord[0], "e-bin", "BBetter", "0", 0, 0},
	{"52837056", "FQ-695375", smartbins_coord[1], "e-bin", "BBetter", "0", 0, 0},
	{"38070529", "ZP-597102", smartbins_coord[2], "e-bin", "BBetter", "0", 0, 0},
	{"49834385", "TY-299937", smartbins_coord[3], "e-bin", "BBetter", "0", 0, 0},
	{"19387151", "KV-977997", smartbins_coord[4], "e-bin", "BBetter", "0", 0, 0},
	{"64747132", "ZT-921391", smartbins_coord[5], "e-bin", "BBetter", "0", 0, 0},
	{"20232019", "VB-356624", smartbins_coord[6], "e-bin", "BBetter", "0", 0, 0},
	{"19769628", "HS-179152", smartbins_coord[7], "e-bin", "BBetter", "0", 0, 0},
	{"88793385", "HY-172252", smartbins_coord[8], "e-bin", "BBetter", "0", 0, 0},
	{"64785632", "VR-387124", smartbins_coord[9], "e-bin", "BBetter", "0", 0, 0}
};


bool smartbin_token_refresh();
long smartbin_send_data(smartbin_data& sb_data);
void smartbin_weight_add(smartbin_data& sb, double weight_kg);

void smartbin_thread_fun(int ID);
void token_refresh_thread_fun();

int rand_range(int min, int max);

size_t WriteCallback(char* contents, size_t size, size_t nmemb, void* userp);

void sigint_handler(sig_atomic_t s);

int main()
{
	cout << "Smartbin Emulator start" << endl;
	signal(SIGINT, sigint_handler);


	cout << "Refreshing token... ";
	if (!smartbin_token_refresh()) {
		cout << "ERR";
		exit(1);
	}
	cout << "OK" << endl;


	//random number gen
	srand(time(NULL));


	cout << "Threads initialization... ";
	cout << endl;

	//create bin threads
	for (auto i = 0; i < n_bins; i++) {
		thread smartbin_thread = std::thread(smartbin_thread_fun, i);
		smartbin_threads_vect.push_back(move(smartbin_thread));
		cout << "    Smartbin " << smartbin_data_arr[i].code << " initialized" << endl;
	}
	cout << "DONE" << endl;

	token_refresh_thread = thread(token_refresh_thread_fun);

	while (1);

	//should never exit
}


int rand_range(int min, int max) {
	return rand() % (max - min) + min;
}

long smartbin_send_data(smartbin_data& sb_data) {
	CURL* curl;
	long response_code = -1;

	curl = curl_easy_init();
	if (curl) {
		curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "POST");

		string telemetry_url = _url_base + string(sb_data.code) + "/slot/plastic/telemetry";
		curl_easy_setopt(curl, CURLOPT_URL, telemetry_url.c_str());
		curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
		curl_easy_setopt(curl, CURLOPT_DEFAULT_PROTOCOL, "https");
		struct curl_slist* headers = NULL;
		string _auth_str = "Authorization: Bearer ";
		_auth_str += _token;
		headers = curl_slist_append(headers, _auth_str.c_str());
		headers = curl_slist_append(headers, "Content-Type: application/json");
		curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

		char data[500];
		sprintf_s(data, "{\n  \"actualWeight\": %f,\n  "
			"\"previousWeight\": %f,\n  "
			"\"decimalLongitude\": %f,\n  "
			"\"decimalLatitude\": %f,\n  "
			"\"hookingCode\": \"%s\",\n  "
			"\"sensorInfo\": {\n    "
			"\"serialNo\": \"%s\",\n    "
			"\"modelNo\": \"%s\",\n    "
			"\"brand\": \"%s\",\n    "
			"\"code\": \"%s\",\n    "
			"\"statusCode\": \"%s\",\n    "
			"\"note\": \"%s\"\n  }\n}",
			sb_data.curr_weight,
			sb_data.prev_weight,
			sb_data.coord.longitude,
			sb_data.coord.latitude,
			"TODO generare hooking code",
			sb_data.serial_no.c_str(),
			sb_data.model_no.c_str(),
			sb_data.brand.c_str(),
			sb_data.code.c_str(),
			sb_data.status_code.c_str(),
			"");

		curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data);

		const CURLcode res = curl_easy_perform(curl);
		if (res == CURLE_OK) {
			curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response_code);
		}
	}
	curl_easy_cleanup(curl);

	return response_code;
}


void smartbin_weight_add(smartbin_data& sb, double weight_kg) {
	double new_weight = sb.curr_weight + weight_kg;
	sb.prev_weight = sb.curr_weight;
	sb.curr_weight = new_weight;
}

void smartbin_thread_fun(int bin_index) {
	double weight_increment_kg = 0;

	while (_should_run) {
		//random weight increment
		weight_increment_kg = (double)rand_range(1, 60) / 100;
		smartbin_weight_add(smartbin_data_arr[bin_index], weight_increment_kg);
		//cout << "Adding " << weight_increment_kg << " kg" << endl;//DEBUG

		//send data to server
		if (_token_is_fresh) {
			auto ret_code = smartbin_send_data(smartbin_data_arr[bin_index]);

			switch (ret_code)
			{
			case 401:
				_token_is_fresh = false;
				//cout << "Token expired" << endl;
				break;
			case 204:
				//cout << "Success!" << endl;
				break;
			default:
				cout << "ERR - " << ret_code << endl;
				break;
			}
		}

		int rand_sleep_ms = rand_range(5000, 30000);
		//cout << "sleeping " << rand_sleep_ms << " ms" << endl;//DEBUG
		Sleep(rand_sleep_ms);
	}
}

bool smartbin_token_refresh() {
	CURL* curl;
	long response_code = 0;

	curl = curl_easy_init();
	if (curl) {
		curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "POST");
		curl_easy_setopt(curl, CURLOPT_URL, "http://techlabcommunity.org:6662/login");
		curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
		curl_easy_setopt(curl, CURLOPT_DEFAULT_PROTOCOL, "https");
		struct curl_slist* headers = NULL;
		headers = curl_slist_append(headers, "Content-Type: application/json");
		curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
		char data[100];
		sprintf_s(data, "{\n  \"username\" : \"%s\",\n  \"password\" : \"%s\"\n}", _MY_USR, _MY_PWD);

		curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
		curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data);
		std::string res_str;
		curl_easy_setopt(curl, CURLOPT_WRITEDATA, &res_str);

		const CURLcode res = curl_easy_perform(curl);

		if (res == CURLE_OK) {
			//TODO check if this function can return 0 -> initialize response_code to invalid value
			curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response_code);
			//cout << "Response code" << response_code << endl; // DEBUG

			//find token start
			size_t token_start = res_str.find("\"", 15);
			// find token end
			size_t token_end = res_str.find("\"", token_start + 1);

			_token = res_str.substr(token_start + 1, token_end - token_start - 1);
			//cout << "Token: " << _token << endl;//DEBUG

			_token_is_fresh = true;
		}
	}
	curl_easy_cleanup(curl);

	return response_code == 200;
}

void token_refresh_thread_fun() {
	if (!_token_is_fresh) {
		smartbin_token_refresh();
	}
}


size_t WriteCallback(char* contents, size_t size, size_t nmemb, void* userp)
{
	((std::string*)userp)->append((char*)contents, size * nmemb);
	return size * nmemb;
}


void sigint_handler(sig_atomic_t s) {
	cout << "Stopping threads... ";
	_should_run = false;

	//TODO better exiting routine
	for (auto& t : smartbin_threads_vect) {
		delete(&t);
	}

	cout << "DONE" << endl;
}
