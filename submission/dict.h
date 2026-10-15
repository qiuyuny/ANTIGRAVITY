/* =========================================================================
 * Module: dict.h (Stage 1: Linked List Dictionary Interface)
 * Responsibility: Declare data structures and routines for linear dictionary.
 * ========================================================================= */

#ifndef DICT_H
#define DICT_H

#include <stdio.h>

/* --- Dataset and Buffer Constants --- */
#define MAX_LINE_LEN 513
#define MAX_FIELD_LEN 128
#define BITS_PER_BYTE 8

/* --- Data Structures --- */

/* One row of the dataset, containing all 16 fields */
typedef struct {
    char *key;
    char *taxa;
    char *kingdom;
    char *phylum;
    char *class_name;
    char *order;
    char *family;
    char *genus;
    char *species;
    char *common_name;
    char *identifcat;
    char *data_resour;
    char *sighting_da;
    double latitude;
    double longitude;
    char *ezi_add;
} Record;

/* Linked list node storing one record */
typedef struct node {
    Record *data;
    struct node *next;
} Node;

/* --- Function Prototypes --- */

/* Part 1: Parallel Helper (Stage 1 key comparison) */
int compare_bits(char *s1, char *s2, int *b_count);

/* Part 2: Specialized Helpers (Record ingestion pipeline & bit utility) */
char *copy_field(char *field_value);
void save_to_record(Record *record, int field_index, char *field_value);
Node *append_node(Node *head, Record *new_record);
int getBit(char *s, unsigned int bitIndex);

/* Part 3: Core Linear Operations (Search and list cleanup) */
void search_and_output(Node *head, char *target, FILE *out_file);
void free_list(Node *head);

#endif
