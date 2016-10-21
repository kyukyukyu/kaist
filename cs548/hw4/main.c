#include "keccak/SimpleFIPS202.h"
#include <stdio.h>
#include <stdlib.h>

int print_hash(const char *algorithm, unsigned int pt, unsigned char *ht,
        int xor);
int print_hdist(unsigned char *ht1, unsigned char *ht2);

int main(int argc, const char* argv[]) {
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

    return 0;
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
