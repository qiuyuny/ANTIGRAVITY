/* Implementation of the dictionary functions declared in dict.h.
   COMP20003 Assignment 2 (Retaining and adapting Stage 1). */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "dict.h"

/* =========================================================================
 * Module Architecture Overview:
 *   - Part 1: Parallel Helpers (Functions matching Stage 2 counterparts)
 *   - Part 2: Specialized Helpers (CSV parsing, record saving, node append)
 *   - Part 3: Core Linear Operations (Linear list search and cleanup)
 * ========================================================================= */

/* =========================================================================
 * Part 1: Parallel Helpers (Stage 1 key comparison)
 * ========================================================================= */

/* Compare two complete keys bit by bit to see if they match.
   Stops at the first mismatch or when the '\0' byte is reached.
   Parallel in Stage 2: compare_prefix_bits in tree.c. */
int compare_bits(char *s1, char *s2, int *b_count) {
    unsigned int bit_index = 0;
    while (1) {
        unsigned int byte_index = bit_index / BITS_PER_BYTE;
        (*b_count)++;
        if (getBit(s1, bit_index) != getBit(s2, bit_index)) return 0;
        /* bits equal so far; if we just finished the '\0' byte, done */
        if (bit_index % BITS_PER_BYTE == BITS_PER_BYTE - 1
            && s1[byte_index] == '\0') return 1;
        bit_index++;
    }
}

/* =========================================================================
 * Part 2: Specialized Helpers (Data parsing, records, and bit extraction)
 * ========================================================================= */

/* Step 1: Duplicate a field string into new memory so the record owns its data. */
char *copy_field(char *field_value) {
    char *field_copy = malloc(strlen(field_value) + 1);
    assert(field_copy);
    strcpy(field_copy, field_value);
    return field_copy;
}

/* Step 2: Store the duplicated strings into the fields of a Record. */
void save_to_record(Record *record, int field_index, char *field_value) {
    switch (field_index) {
        case 0: record->key = copy_field(field_value); break;
        case 1: record->taxa = copy_field(field_value); break;
        case 2: record->kingdom = copy_field(field_value); break;
        case 3: record->phylum = copy_field(field_value); break;
        case 4: record->class_name = copy_field(field_value); break;
        case 5: record->order = copy_field(field_value); break;
        case 6: record->family = copy_field(field_value); break;
        case 7: record->genus = copy_field(field_value); break;
        case 8: record->species = copy_field(field_value); break;
        case 9: record->common_name = copy_field(field_value); break;
        case 10: record->identifcat = copy_field(field_value); break;
        case 11: record->data_resour = copy_field(field_value); break;
        case 12: record->sighting_da = copy_field(field_value); break;
        case 13: record->latitude = atof(field_value); break;
        case 14: record->longitude = atof(field_value); break;
        case 15: record->ezi_add = copy_field(field_value); break;
    }
}

/* Step 3: Wrap the Record in a list node and append it to the end of the list. */
Node *append_node(Node *head, Record *new_record) {
    Node *new_node = malloc(sizeof(Node));
    assert(new_node);
    new_node->data = new_record;
    new_node->next = NULL;

    if (head == NULL) return new_node;

    Node *current = head;
    while (current->next != NULL) {
        current = current->next;
    }
    current->next = new_node;
    return head;
}

/* Helper: Extract a single bit (0 or 1) at bitIndex from string s.
   Provides bit-level access for compare_bits and Patricia tree traversal. */
int getBit(char *s, unsigned int bitIndex) {
    assert(s);
    unsigned int byte = bitIndex / BITS_PER_BYTE;
    unsigned int indexFromLeft = bitIndex % BITS_PER_BYTE;
    /* bits are counted from the left, so flip the index around */
    unsigned int offset = (BITS_PER_BYTE - (indexFromLeft) - 1) % BITS_PER_BYTE;
    unsigned char byteOfInterest = s[byte];
    unsigned int offsetMask = (1 << offset);
    unsigned int maskedByte = (byteOfInterest & offsetMask);
    /* move the bit down to the last position, so it becomes 0 or 1 */
    return maskedByte >> offset;
}

/* =========================================================================
 * Part 3: Core Linear Operations (Search and list deallocation)
 * ========================================================================= */

/* Search: Scan through the list and compare each key using compare_bits.
   Prints matching records to out_file and comparison counts to stdout. */
void search_and_output(Node *head, char *target, FILE *out_file) {
    Node *current = head;
    int count = 0;
    int b_count = 0, n_count = 0, s_count = 0;
    fprintf(out_file, "%s\n", target);

    while (current != NULL) {
        n_count++;
        s_count++;
        if (compare_bits(current->data->key, target, &b_count) == 1) {
            fprintf(out_file,
                    "--> KEY: %s || Taxa: %s || Kingdom: %s || Phylum: %s"
                    " || Class: %s || Order: %s || Family: %s || Genus: %s"
                    " || Species: %s || Common_Name: %s || Identifcat: %s"
                    " || Data_Resour: %s || Sighting_Da: %s"
                    " || latitude: %.5f || longitude: %.5f"
                    " || EZI_ADD: %s || \n",
                    current->data->key, current->data->taxa,
                    current->data->kingdom, current->data->phylum,
                    current->data->class_name, current->data->order,
                    current->data->family, current->data->genus,
                    current->data->species, current->data->common_name,
                    current->data->identifcat, current->data->data_resour,
                    current->data->sighting_da, current->data->latitude,
                    current->data->longitude, current->data->ezi_add);
            count++;
        }
        current = current->next;
    }

    if (count == 0) fprintf(out_file, "NOTFOUND\n");

    printf("%s --> %d records found - comparisons: b%d n%d s%d\n",
           target, count, b_count, n_count, s_count);
}

/* Cleanup: Free all nodes, records, and strings in the linked list. */
void free_list(Node *head) {
    Node *current = head;
    while (current != NULL) {
        Node *temp = current;
        current = current->next;

        free(temp->data->key);
        free(temp->data->taxa);
        free(temp->data->kingdom);
        free(temp->data->phylum);
        free(temp->data->class_name);
        free(temp->data->order);
        free(temp->data->family);
        free(temp->data->genus);
        free(temp->data->species);
        free(temp->data->common_name);
        free(temp->data->identifcat);
        free(temp->data->data_resour);
        free(temp->data->sighting_da);
        free(temp->data->ezi_add);

        free(temp->data);
        free(temp);
    }
}
