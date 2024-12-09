#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void print_disk_map(const char *disk_map) {
    printf("%s\n", disk_map);
    printf("\n");
}
int main() {
    FILE *fp = fopen("test_inputs.txt", "r");
    if (fp == NULL) {
        perror("Error opening file");
        return 1;
    }

    char *disk_map;
    size_t len = 0;
    ssize_t read;

    read = getline(&disk_map, &len, fp);
    if (read == -1) {
        perror("Error reading file");
        free(disk_map);
        fclose(fp);
        return 1;
    }
    disk_map[strcspn(disk_map, "\n")] = '\0';
    print_disk_map(disk_map);

    int disk_len = 0;
    for (int i = 0; i<strlen(disk_map); i++) {
      disk_len += (int)disk_map[i] - '0';
    }
    printf("%d\n", disk_len);

    int disk[disk_len];
    int isFile = 1;
    int disk_idx = 0; 
    int file_id = 0;
    for (int i = 0; i<strlen(disk_map); i++) {
      int num = disk_map[i] - '0';
      if (isFile) {
        for(int j =0; j<num;j++){
          disk[disk_idx] = file_id;
          disk_idx++;
        }
        file_id++;
      }
      else {
        for(int j =0; j<num;j++){
          disk[disk_idx] = -1;
          disk_idx++;
        }
      }
      isFile = !isFile;

    }

    for (int i =0;i<disk_idx; i++) {
      printf("%d", disk[i]);
    }
    printf("\n");
    fclose(fp);
    free(disk_map);

    return 0;
}

int *
