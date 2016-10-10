#define HASH_LENGTH 256

#include "sha256/KISA_SHA256.h"
#include "lsh/include/lsh.h"
#include <stdio.h>
#include <stdlib.h>

int print_hash(const char *algorithm, unsigned int pt, unsigned char *ht,
        int xor);

int main(int argc, const char* argv[]) {
    unsigned int yyyymmdd;
    unsigned int yyyymmdd_1;
    int in;
    unsigned char h[HASH_LENGTH];

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

    SHA256_Encrpyt((BYTE *) &yyyymmdd, sizeof(yyyymmdd), h);
    print_hash("SHA256", yyyymmdd, h, 0);

    SHA256_Encrpyt((BYTE *) &yyyymmdd_1, sizeof(yyyymmdd_1), h);
    print_hash("SHA256", yyyymmdd, h, 1);

    lsh_digest(LSH_MAKE_TYPE(0, HASH_LENGTH),
            (lsh_u8 *) &yyyymmdd,
            8 * sizeof(yyyymmdd),
            h);
    print_hash("LSH", yyyymmdd, h, 0);

    lsh_digest(LSH_MAKE_TYPE(0, HASH_LENGTH),
            (lsh_u8 *) &yyyymmdd_1,
            8 * sizeof(yyyymmdd_1),
            h);
    print_hash("LSH", yyyymmdd, h, 1);

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
