#ifndef metkit_version_h
#define metkit_version_h

#define metkit_VERSION_STR "1.12.5"
#define metkit_VERSION     "1.12.5"

#define metkit_VERSION_MAJOR 1
#define metkit_VERSION_MINOR 12
#define metkit_VERSION_PATCH 5

#define metkit_GIT_SHA1 "010cf50459ac51d6e232bd8a49db66a5b534bc5d"

#ifdef __cplusplus
extern "C" {
#endif

const char * metkit_version();

unsigned int metkit_version_int();

const char * metkit_version_str();

const char * metkit_git_sha1();

#ifdef __cplusplus
}
#endif


#endif // metkit_version_h
