/* Stage 1 main program: reads the CSV dataset into a linked list,
   then looks up each KEY read from stdin.
   Usage: ./dict1 1 input.csv output.txt
   COMP20003 Assignment 1, Stage 1. */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "dict.h"

/* program name + stage + input file + output file */
#define NUM_ARGS 4

/* positions of the arguments in argv */
#define ARG_INFILE 2
#define ARG_OUTFILE 3

int main(int argc, char *argv[]) {
    if (argc < NUM_ARGS) return EXIT_FAILURE;

    FILE *in_file = fopen(argv[ARG_INFILE], "r");
    FILE *out_file = fopen(argv[ARG_OUTFILE], "w");
    assert(in_file);
    assert(out_file);

    Node *head = NULL;
    char current_line[MAX_LINE_LEN];
    char current_field[MAX_FIELD_LEN];

    /* skip the header line */
    fgets(current_line, MAX_LINE_LEN, in_file);

    while (fgets(current_line, MAX_LINE_LEN, in_file) != NULL) {
        int i = 0, j = 0, in_quote = 0, field_index = 0;
        Record *current_record = malloc(sizeof(Record));
        assert(current_record);

        while (current_line[i] != '\n' && current_line[i] != '\0') {
            if (current_line[i] == '"') {
                /* commas between quotes are text, not separators,
                   and the quotes themselves are not stored */
                in_quote = !in_quote;
            } else if (current_line[i] == ',' && in_quote == 0) {
                /* a comma outside quotes ends the field */
                current_field[j] = '\0';
                save_to_record(current_record, field_index, current_field);
                field_index++;
                j = 0;
            } else {
                current_field[j] = current_line[i];
                j++;
            }
            i++;
        }

        /* the last field ends at the end of the line, not a comma */
        current_field[j] = '\0';
        save_to_record(current_record, field_index, current_field);
        head = append_node(head, current_record);
    }
    fclose(in_file);

    /* each line of stdin is one query; a query ends at the newline,
       so an empty line is still a valid query (an empty address) */
    char query[MAX_LINE_LEN];
    while (fgets(query, sizeof(query), stdin) != NULL) {
        size_t len = strlen(query);
        if (len > 0 && query[len-1] == '\n') query[len-1] = '\0';
        search_and_output(head, query, out_file);
    }

    fclose(out_file);
    free_list(head);
    return EXIT_SUCCESS;
}
