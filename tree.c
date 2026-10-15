/* Patricia Tree (Radix Tree) implementation for Project 2 Stage 2.
   COMP20003 Assignment 2. */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "tree.h"

/* =========================================================================
 * Module Architecture Overview:
 *   - Part 1: Parallel Helpers (Functions matching Stage 1 counterparts)
 *   - Part 2: Specialized Helpers (Stem creation, edit distance, node allocation)
 *   - Part 3: Core Tree Operations (Insert, search, and cleanup)
 * ========================================================================= */

/* =========================================================================
 * Part 1: Parallel Helpers (Stage 2 prefix comparison)
 * ========================================================================= */

/* Compare a node's prefix stem against a key bit by bit, up to prefixBits.
   Records the first mismatch bit index to decide where to branch or split.
   Parallel in Stage 1: compare_bits in dict.c. */
int compare_prefix_bits(char *prefix, unsigned int prefixBits,
                       char *key, unsigned int startBit,
                       unsigned int *mismatch_bit) {
    unsigned int i = 0;
    while (i < prefixBits) {
        if (getBit(prefix, i) != getBit(key, startBit + i)) {
            *mismatch_bit = i;
            return 0; /* Mismatch found at bit index i */
        }
        i++;
    }
    *mismatch_bit = i;
    return 1; /* All prefixBits matched */
}

/* =========================================================================
 * Part 2: Specialized Helpers (Stem creation, node allocation, edit distance)
 * ========================================================================= */

/* Step 1: Cut out a range of bits from a key to make a prefix stem.
   Reference: Specification/Tree_intro/12.png - 14.png */
char *createStem(char *oldKey, unsigned int startBit, unsigned int numBits) {
    assert(oldKey);
    int extraBytes = 0;
    if ((numBits % BITS_PER_BYTE) > 0) {
        extraBytes = 1;
    }
    int totalBytes = (numBits / BITS_PER_BYTE) + extraBytes;

    char *newStem = malloc(sizeof(char) * totalBytes);
    assert(newStem);

    /* Zero all values in stem initially, so that OR operation is well defined. */
    for (unsigned int i = 0; i < totalBytes; i++) {
        newStem[i] = 0;
    }

    /* For each bit, follow getBit logic to find the location to insert the bit
       and add the bit to the new stem. */
    for (unsigned int i = 0; i < numBits; i++) {
        unsigned int indexFromLeft = i % BITS_PER_BYTE;
        unsigned int offset = (BITS_PER_BYTE - indexFromLeft - 1) % BITS_PER_BYTE;
        unsigned int bitMaskForPosition = 1 << offset;
        unsigned int bitValueAtPosition = getBit(oldKey, startBit + i);
        unsigned int byteInNewStem = i / BITS_PER_BYTE;
        newStem[byteInNewStem] |= bitMaskForPosition * bitValueAtPosition;
    }
    return newStem;
}

/* Step 2: Make a new tree node with the stem from Step 1 and empty branches. */
TreeNode *createTreeNode(char *prefix, unsigned int prefixBits) {
    TreeNode *node = malloc(sizeof(TreeNode));
    assert(node);
    node->prefix = prefix;
    node->prefixBits = prefixBits;
    node->branchA = NULL;
    node->branchB = NULL;
    node->data = NULL;
    return node;
}

/* Step 3: Add a record to this node's data list (handles records with duplicate keys). */
void addRecordToNode(TreeNode *node, Record *record) {
    assert(node);
    assert(record);
    DataNode *newData = malloc(sizeof(DataNode));
    assert(newData);
    newData->record = record;
    newData->next = node->data;
    node->data = newData;
}

/* Helper: Return the smallest of three numbers for editDistance.
   Reference: Specification/Implement_Dt/3.c */
int min3(int a, int b, int c) {
    if (a < b) {
        if (a < c) {
            return a;
        } else {
            return c;
        }
    } else {
        if (b < c) {
            return b;
        } else {
            return c;
        }
    }
}

/* Spellcheck: Calculate edit distance between two strings using min3.
   Reference: Specification/Implement_Dt/3.c */
int editDistance(char *str1, char *str2, int n, int m) {
    assert(m >= 0 && n >= 0 && (str1 || m == 0) && (str2 || n == 0));
    int dp[n + 1][m + 1];

    for (int i = 0; i <= n; i++) {
        for (int j = 0; j <= m; j++) {
            if (i == 0) {
                dp[i][j] = j;
            } else if (j == 0) {
                dp[i][j] = i;
            } else if (str1[i - 1] == str2[j - 1]) {
                dp[i][j] = min3(1 + dp[i - 1][j], 1 + dp[i][j - 1],
                                dp[i - 1][j - 1]);
            } else {
                dp[i][j] = 1 + min3(dp[i - 1][j], dp[i][j - 1],
                                    dp[i - 1][j - 1]);
            }
        }
    }
    return dp[n][m];
}

/* =========================================================================
 * Part 3: Core Tree Operations (Insert, search, and memory deallocation)
 * ========================================================================= */

/* Build tree: Insert a record into the Patricia tree.
   Walk down branches matching prefixes; break out to split when bits diverge. */
TreeNode *tree_insert(TreeNode *root, Record *record) {
    unsigned int totalBits = (strlen(record->key) + 1) * BITS_PER_BYTE;

    /* Empty tree: create the root node directly. */
    if (root == NULL) {
        char *stem = createStem(record->key, 0, totalBits);
        root = createTreeNode(stem, totalBits);
        addRecordToNode(root, record);
        return root;
    }

    /* Non-empty tree: walk down using bit_offset. */
    TreeNode *curr = root;
    unsigned int bit_offset = 0;
    unsigned int mismatch_bit = 0;

    while (curr != NULL) {
        int matched = compare_prefix_bits(curr->prefix, curr->prefixBits,
                                          record->key, bit_offset, &mismatch_bit);

        /* Prefix mismatches: bit difference found -> break to split curr. */
        if (!matched) {
            break;
        }

        /* Prefix matches: advance bit_offset across this prefix. */
        bit_offset += curr->prefixBits;

        /* Match branches: check if the key finishes here or keeps going. */
        if (bit_offset == totalBits) {
            /* Key finishes here: add duplicate record to curr. */
            addRecordToNode(curr, record);
            return root;
        }

        /* Key keeps going: follow branchA (bit 0) or branchB (bit 1). */
        int nextBit = getBit(record->key, bit_offset);
        if (nextBit == 0) {
            if (curr->branchA == NULL) {
                unsigned int remBits = totalBits - bit_offset;
                char *stem = createStem(record->key, bit_offset, remBits);
                curr->branchA = createTreeNode(stem, remBits);
                addRecordToNode(curr->branchA, record);
                return root;
            }
            curr = curr->branchA;
        } else {
            if (curr->branchB == NULL) {
                unsigned int remBits = totalBits - bit_offset;
                char *stem = createStem(record->key, bit_offset, remBits);
                curr->branchB = createTreeNode(stem, remBits);
                addRecordToNode(curr->branchB, record);
                return root;
            }
            curr = curr->branchB;
        }
    }

    /* Split on mismatch (breaks from the mismatch above):
       curr and the new key differ at mismatch_bit.
       In the new key, the difference starts at (bit_offset + mismatch_bit). */
    unsigned int oldRemainingBits = curr->prefixBits - mismatch_bit;
    char *oldStem = createStem(curr->prefix, mismatch_bit, oldRemainingBits);
    TreeNode *oldChild = createTreeNode(oldStem, oldRemainingBits);
    oldChild->branchA = curr->branchA;
    oldChild->branchB = curr->branchB;
    oldChild->data = curr->data;

    unsigned int newRemainingBits = totalBits - (bit_offset + mismatch_bit);
    char *newStem = createStem(record->key, bit_offset + mismatch_bit, newRemainingBits);
    TreeNode *newChild = createTreeNode(newStem, newRemainingBits);
    addRecordToNode(newChild, record);

    /* Truncate curr to the common prefix */
    char *commonStem = createStem(curr->prefix, 0, mismatch_bit);
    free(curr->prefix);
    curr->prefix = commonStem;
    curr->prefixBits = mismatch_bit;
    curr->data = NULL;

    /* Attach children: bit 0 to branchA, bit 1 to branchB */
    int oldBit = getBit(oldChild->prefix, 0);
    if (oldBit == 0) {
        curr->branchA = oldChild;
        curr->branchB = newChild;
    } else {
        curr->branchA = newChild;
        curr->branchB = oldChild;
    }

    return root;
}

/* Helper for search_tree_and_output: gathers all nodes with records in a subtree. */
static void collect_candidate_nodes(TreeNode *node, TreeNode ***nodes, int *count, int *capacity) {
    if (node == NULL) return;
    if (node->data != NULL) {
        if (*count >= *capacity) {
            *capacity = (*capacity == 0) ? 16 : (*capacity * 2);
            *nodes = realloc(*nodes, sizeof(TreeNode *) * (*capacity));
            assert(*nodes);
        }
        (*nodes)[(*count)++] = node;
    }
    collect_candidate_nodes(node->branchA, nodes, count, capacity);
    collect_candidate_nodes(node->branchB, nodes, count, capacity);
}

/* Core Search: Looks up target in the Patricia tree with spellchecking fallback.
   Prints matching records to out_file and prints operation counts to stdout. */
void search_tree_and_output(TreeNode *root, char *target, FILE *out_file) {
    int b_count = 0, n_count = 0, s_count = 0;
    fprintf(out_file, "%s\n", target);

    if (root == NULL) {
        fprintf(out_file, "NOTFOUND\n");
        printf("%s --> NOTFOUND\n", target);
        return;
    }

    unsigned int totalBits = (strlen(target) + 1) * BITS_PER_BYTE;
    TreeNode *curr = root;
    unsigned int bit_offset = 0;
    TreeNode *target_node = NULL;

    while (curr != NULL) {
        n_count++;
        unsigned int mismatch_bit = 0;
        int matched = compare_prefix_bits(curr->prefix, curr->prefixBits,
                                          target, bit_offset, &mismatch_bit);

        if (!matched) {
            /* Mismatched bits count: bits up to and including the diverging bit */
            b_count += mismatch_bit + 1;
            break;
        }

        /* All bits in prefix matched */
        b_count += curr->prefixBits;
        bit_offset += curr->prefixBits;

        if (bit_offset == totalBits) {
            if (curr->data != NULL) {
                target_node = curr;
                s_count++;
            }
            break;
        }

        /* Check next bit to choose branch */
        int nextBit = getBit(target, bit_offset);
        if (nextBit == 0) {
            if (curr->branchA == NULL) {
                b_count++;
                break;
            }
            curr = curr->branchA;
        } else {
            if (curr->branchB == NULL) {
                b_count++;
                break;
            }
            curr = curr->branchB;
        }
    }

    /* If exact match was not found, perform spellchecking on subtree at curr */
    if (target_node == NULL && curr != NULL) {
        TreeNode **candidates = NULL;
        int cand_count = 0, cand_capacity = 0;
        collect_candidate_nodes(curr, &candidates, &cand_count, &cand_capacity);

        int min_dist = -1;
        int target_len = strlen(target);

        for (int k = 0; k < cand_count; k++) {
            char *cand_key = candidates[k]->data->record->key;
            s_count++;
            int dist = editDistance(target, cand_key, target_len, strlen(cand_key));
            if (min_dist == -1 || dist < min_dist) {
                min_dist = dist;
                target_node = candidates[k];
            } else if (dist == min_dist) {
                if (strcmp(cand_key, target_node->data->record->key) < 0) {
                    target_node = candidates[k];
                }
            }
        }
        if (candidates) free(candidates);
    }

    /* Output results */
    int record_count = 0;
    if (target_node != NULL && target_node->data != NULL) {
        DataNode *curr_data = target_node->data;
        while (curr_data != NULL) {
            Record *r = curr_data->record;
            fprintf(out_file,
                    "--> KEY: %s || Taxa: %s || Kingdom: %s || Phylum: %s"
                    " || Class: %s || Order: %s || Family: %s || Genus: %s"
                    " || Species: %s || Common_Name: %s || Identificat: %s"
                    " || Data_Resour: %s || Sighting_Da: %s"
                    " || latitude: %.5f || longitude: %.5f"
                    " || EZI_ADD: %s || \n",
                    r->key, r->taxa, r->kingdom, r->phylum,
                    r->class_name, r->order, r->family, r->genus,
                    r->species, r->common_name, r->identifcat,
                    r->data_resour, r->sighting_da, r->latitude,
                    r->longitude, r->ezi_add);
            record_count++;
            curr_data = curr_data->next;
        }
    } else {
        fprintf(out_file, "NOTFOUND\n");
    }

    printf("%s --> %d records found - comparisons: b%d n%d s%d\n",
           target, record_count, b_count, n_count, s_count);
}

/* Cleanup: Free all nodes, stems, and data records in the tree. */
void free_tree(TreeNode *root) {
    if (!root) return;
    free_tree(root->branchA);
    free_tree(root->branchB);

    if (root->prefix) {
        free(root->prefix);
    }

    DataNode *curr = root->data;
    while (curr) {
        DataNode *temp = curr;
        curr = curr->next;
        free(temp);
    }
    free(root);
}
