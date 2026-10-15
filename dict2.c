/* Stage 2 main program: reads the CSV dataset into a Patricia tree,
   then looks up each KEY read from stdin with spellchecking.
   Usage: ./dict2 2 input.csv output.txt
   COMP20003 Assignment 2, Stage 2. */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "dict.h"
#include "tree.h"

#define NUM_ARGS 4
#define ARG_STAGE 1
#define ARG_INFILE 2
#define ARG_OUTFILE 3

int main(int argc, char *argv[]) {
    if (argc < NUM_ARGS) return EXIT_FAILURE;

    FILE *in_file = fopen(argv[ARG_INFILE], "r");
    FILE *out_file = fopen(argv[ARG_OUTFILE], "w");
    assert(in_file);
    assert(out_file);

    TreeNode *root = NULL;
    char current_line[MAX_LINE_LEN];
    char current_field[MAX_FIELD_LEN];

    /* skip the header line */
    if (fgets(current_line, MAX_LINE_LEN, in_file) == NULL) {
        fclose(in_file);
        fclose(out_file);
        return EXIT_FAILURE;
    }

    /* We keep an array/list of all allocated records so we can cleanly free all records at the end */
    Node *all_records_list = NULL;

    while (fgets(current_line, MAX_LINE_LEN, in_file) != NULL) {
        int i = 0, j = 0, in_quote = 0, field_index = 0;
        Record *current_record = malloc(sizeof(Record));
        assert(current_record);

        while (current_line[i] != '\n' && current_line[i] != '\0') {
            if (current_line[i] == '"') {
                in_quote = !in_quote;
            } else if (current_line[i] == ',' && in_quote == 0) {
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

        current_field[j] = '\0';
        save_to_record(current_record, field_index, current_field);

        /* Keep record in tracking list for easy cleanup */
        all_records_list = append_node(all_records_list, current_record);

        /* Insert record into Patricia Tree */
        root = tree_insert(root, current_record);
    }
    fclose(in_file);

    /* Read queries from stdin */
    char query[MAX_LINE_LEN];
    while (fgets(query, sizeof(query), stdin) != NULL) {
        size_t len = strlen(query);
        if (len > 0 && query[len - 1] == '\n') query[len - 1] = '\0';
        search_tree_and_output(root, query, out_file);
    }

    fclose(out_file);
    free_tree(root);
    free_list(all_records_list);

    return EXIT_SUCCESS;
}

