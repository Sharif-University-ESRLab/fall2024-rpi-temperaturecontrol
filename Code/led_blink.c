#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

#define GPIO_PIN "18"

void export_gpio(const char *pin) {
    int fd = open("/sys/class/gpio/export", O_WRONLY);
    if (fd == -1) {
        perror("Unable to open /sys/class/gpio/export");
        exit(1);
    }
    write(fd, pin, sizeof(GPIO_PIN));
    close(fd);
}

void set_direction(const char *pin, const char *direction) {
    char path[35];
    snprintf(path, sizeof(path), "/sys/class/gpio/gpio%s/direction", pin);
    int fd = open(path, O_WRONLY);
    if (fd == -1) {
        perror("Unable to set GPIO direction");
        exit(1);
    }
    write(fd, direction, strlen(direction));
    close(fd);
}

void write_gpio(const char *pin, const char *value) {
    char path[35];
    snprintf(path, sizeof(path), "/sys/class/gpio/gpio%s/value", pin);
    int fd = open(path, O_WRONLY);
    if (fd == -1) {
        perror("Unable to write to GPIO value");
        exit(1);
    }
    write(fd, value, 1);
    close(fd);
}

int main() {
    export_gpio(GPIO_PIN);
    set_direction(GPIO_PIN, "out");

    while (1) {
        write_gpio(GPIO_PIN, "1");
        sleep(1);
        write_gpio(GPIO_PIN, "0");
        sleep(1);
    }

    return 0;
}
