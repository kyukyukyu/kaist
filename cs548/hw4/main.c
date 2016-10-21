#define HASH_LENGTH 256
#define RANDOM_BYTES_LENGTH 1000

#include "keccak/SimpleFIPS202.h"
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void check_avalanche_effect();
void confirm_timing_attack_security();

int print_hash(const char *algorithm, unsigned int pt, unsigned char *ht,
        int xor);
int print_hdist(unsigned char *ht1, unsigned char *ht2);
void generate_randbytes(unsigned char *randbytes, size_t len);
void compute_clockdiff(struct timespec *tp_a, struct timespec *tp_b,
        struct timespec *tp_diff);

int main(int argc, const char* argv[]) {
    srand48(time(NULL));
    check_avalanche_effect();
    confirm_timing_attack_security();
    return 0;
}

void check_avalanche_effect() {
    unsigned int yyyymmdd;
    unsigned int yyyymmdd_1;
    int in;
    unsigned char h1[HASH_LENGTH];
    unsigned char h2[HASH_LENGTH];

    fputs("YYYYMMDD: ", stdout);
    in = scanf("%8u", &yyyymmdd);
    if (EOF == in) {
        perror("failed to get your birth date");
    } else if (1 != in) {
        fputs("your birth date should be eight-digit unsigned integer",
                stderr);
        exit(EXIT_FAILURE);
    }

    yyyymmdd_1 = yyyymmdd ^ 0x01;

    SHA3_256(h1, (unsigned char *) &yyyymmdd, sizeof(yyyymmdd));
    print_hash("SHA3_256", yyyymmdd, h1, 0);

    SHA3_256(h2, (unsigned char *) &yyyymmdd_1, sizeof(yyyymmdd_1));
    print_hash("SHA3_256", yyyymmdd, h2, 1);

    print_hdist(h1, h2);
}

void confirm_timing_attack_security() {
    struct timespec tp_a, tp_b, tp_diff;
    int i;
    unsigned char randbytes[RANDOM_BYTES_LENGTH];
    unsigned char h[HASH_LENGTH];
    for (i = 1; i <= 100; ++i) {
        generate_randbytes(randbytes, RANDOM_BYTES_LENGTH);
        printf("Hashing the string #%d... ", i);
        clock_gettime(CLOCK_MONOTONIC, &tp_a);
        SHA3_256(h, randbytes, RANDOM_BYTES_LENGTH);
        clock_gettime(CLOCK_MONOTONIC, &tp_b);
        compute_clockdiff(&tp_a, &tp_b, &tp_diff);
        printf("done in %ld second(s) %ld nanosecond(s).\n", tp_diff.tv_sec,
                tp_diff.tv_nsec);
    }
}

int print_hash(const char *algorithm, unsigned int pt, unsigned char *ht,
        int xor) {
    static const char digits[] = "0123456789ABCDEF";
    char s[HASH_LENGTH / 4 + 1] = "";
    char *sp = s;
    const char *as = (0 == xor) ? "" : " ^ 0x01";
    int i = HASH_LENGTH / (8 * sizeof(unsigned char));

    while (i > 0) {
        *(sp++) = digits[*ht / 16];
        *(sp++) = digits[*ht % 16];
        ++ht;
        --i;
    }
    *sp = '\0';
    return printf("%s(%u%s): %s\n", algorithm, pt, as, s);
}

int print_hdist(unsigned char *ht1, unsigned char *ht2) {
    int i = HASH_LENGTH / (8 * sizeof(unsigned long long));
    int hdist = 0;
    unsigned long long *p1 = (unsigned long long *) ht1;
    unsigned long long *p2 = (unsigned long long *) ht2;
    while (i > 0) {
        // GCC builtin which calculates the Hamming distance between two
        // values.
        hdist += __builtin_popcountll(*p1 ^ *p2);
        ++p1;
        ++p2;
        --i;
    }
    return printf("Hamming distance: %d\n", hdist);
}

// This function is written with the assumption of little-endian.
void generate_randbytes(unsigned char *randbytes, size_t len) {
    unsigned char *finpoint = randbytes + len;
    unsigned int n_leftbits = 0;
    while (randbytes + sizeof(long) < finpoint) {
        *((long *) randbytes) = mrand48();
        // It is assumed that the first six bytes are written with random bits.
        randbytes += 6;     // 48 bits = 6 bytes.
    }
    n_leftbits = 8 * (finpoint - randbytes);
    if (0 < n_leftbits) {
        // Write random bits only on the left bits using bitwise operations.
        // Create a bit mask with n_leftbits 1s from the LSB so that only first
        // n_leftbits bits are written with random bits.
        long mask = (0x1 << n_leftbits) - 1;
        long randnum = mrand48();
        *((long *) randbytes) =
            (*((long *) randbytes) & ~mask) |   // Existing bits preserved.
            (randnum & mask);                   // Random bits come in.
    }
}

// Precondition: tp_b is later than tp_a.
void compute_clockdiff(struct timespec *tp_a, struct timespec *tp_b,
        struct timespec *tp_diff) {
    long nsecdiff = tp_b->tv_nsec - tp_a->tv_nsec;
    tp_diff->tv_sec = tp_b->tv_sec - tp_a->tv_sec;
    if (nsecdiff > 0) {
        tp_diff->tv_nsec = nsecdiff;
    } else if (nsecdiff < 0) {
        tp_diff->tv_sec -= 1;
        tp_diff->tv_nsec = nsecdiff + 1000000000L;
    }
}
