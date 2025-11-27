#ifndef SHODAN_CLIENT_H
#define SHODAN_CLIENT_H

#include <curl/curl.h>
#include <json-c/json.h>

typedef struct {
    char *memory;
    size_t size;
} MemoryStruct;

void init_shodan_client(const char *api_key);
void cleanup_shodan_client();
char *shodan_search(const char *query);
char *shodan_host(const char *ip);

#endif // SHODAN_CLIENT_H