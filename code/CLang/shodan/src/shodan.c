#include "shodan.h"
#include <stdlib.h>
#include <string.h>

static char *api_key = NULL;

void init_shodan_client(const char *key) {
    api_key = strdup(key);
    curl_global_init(CURL_GLOBAL_DEFAULT);
}

void cleanup_shodan_client() {
    free(api_key);
    curl_global_cleanup();
}

static size_t WriteMemoryCallback(void *contents, size_t size, size_t nmemb, void *userp) {
    size_t realsize = size * nmemb;
    MemoryStruct *mem = (MemoryStruct *)userp;

    char *ptr = realloc(mem->memory, mem->size + realsize + 1);
    if (ptr == NULL) {
        return 0;  // out of memory!
    }

    mem->memory = ptr;
    memcpy(&(mem->memory[mem->size]), contents, realsize);
    mem->size += realsize;
    mem->memory[mem->size] = 0;

    return realsize;
}

static char *shodan_api_request(const char *url) {
    CURL *curl_handle;
    CURLcode res;

    MemoryStruct chunk;
    chunk.memory = malloc(1);  // will be grown as needed by the realloc above
    chunk.size = 0;            // no data at this point

    curl_handle = curl_easy_init();
    if (curl_handle) {
        curl_easy_setopt(curl_handle, CURLOPT_URL, url);
        curl_easy_setopt(curl_handle, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);
        curl_easy_setopt(curl_handle, CURLOPT_WRITEDATA, (void *)&chunk);
        curl_easy_setopt(curl_handle, CURLOPT_USERAGENT, "libcurl-agent/1.0");

        res = curl_easy_perform(curl_handle);
        if (res != CURLE_OK) {
            fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
        }

        curl_easy_cleanup(curl_handle);
    }

    if (chunk.size > 0) {
        return chunk.memory;
    } else {
        free(chunk.memory);
        return NULL;
    }
}

char *shodan_search(const char *query) {
    char url[512];
    snprintf(url, sizeof(url), "https://api.shodan.io/shodan/host/search?key=%s&query=%s", api_key, query);
    return shodan_api_request(url);
}

char *shodan_host(const char *ip) {
    char url[512];
    snprintf(url, sizeof(url), "https://api.shodan.io/shodan/host/%s?key=%s", ip, api_key);
    return shodan_api_request(url);
}