#include <cstdio>
#include <cstring>
#include <iostream>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

int CreateDir(const char *sPathName) {
  char DirName[256];
  strcpy(DirName, sPathName);
  int i, len = strlen(DirName);
  if (DirName[len - 1] != '/')
    strcat(DirName, "/");

  len = strlen(DirName);

  for (i = 1; i < len; i++) {
    if (DirName[i] == '/') {
      DirName[i] = 0;
      if (access(DirName, NULL) != 0) {
        if (mkdir(DirName, 0755) == -1) {
          perror("mkdir   error");
          return -1;
        }
      }
      DirName[i] = '/';
    }
  }

  return 0;
}

int main() {
  char *path = "/log_output/mpa_log";
  int ret = CreateDir(path);
  return 0;
}
