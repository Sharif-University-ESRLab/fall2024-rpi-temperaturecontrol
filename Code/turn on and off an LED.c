#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>

#define GPIO_BASE 0x3F200000 // Base address for Raspberry Pi 3 Model B GPIO
#define BLOCK_SIZE 4096
#define GPIO_SET *(gpio + 7)  // GPSET0 register (offset 0x1C)
#define GPIO_CLR *(gpio + 10) // GPCLR0 register (offset 0x28)

volatile unsigned *gpio; // Pointer to GPIO memory

void setup_io() {
    int mem_fd = open("/dev/mem", O_RDWR | O_SYNC);
    if (mem_fd < 0) {
        perror("Failed to open /dev/mem");
        exit(1);
    }

    gpio = (volatile unsigned *)mmap(NULL, BLOCK_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, mem_fd, GPIO_BASE);
    if (gpio == MAP_FAILED) {
        perror("mmap failed");
        close(mem_fd);
        exit(1);
    }

    close(mem_fd);
}

void set_pin_mode_output(int pin) {
    int gpio_offset = pin / 10;
    int gpio_bit = (pin % 10) * 3;
    *(gpio + gpio_offset) &= ~(7 << gpio_bit); // Clear bits
    *(gpio + gpio_offset) |= (1 << gpio_bit); // Set bits for output mode
}

int main() {
    setup_io();

    int gpio_pin = 18; // BCM pin number

    // Set GPIO pin as output
    set_pin_mode_output(gpio_pin);

    while (1) {
        // Write HIGH to the pin
        GPIO_SET = (1 << gpio_pin);
        printf("Pin set to HIGH\n");
        sleep(1); // Wait for 1 second

        // Write LOW to the pin
        GPIO_CLR = (1 << gpio_pin);
        printf("Pin set to LOW\n");
        sleep(1); // Wait for 1 second
    }

    return 0;
}
