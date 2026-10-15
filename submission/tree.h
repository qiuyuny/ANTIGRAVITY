/* =========================================================================
 * Module: tree.h (Stage 2: Patricia Tree Interface)
 * Responsibility: Declare data structures and routines for Radix tree dictionary.
 * ========================================================================= */

#ifndef TREE_H
#define TREE_H

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include "dict.h"

/* --- Data Structures --- */

/* Linked list node for records stored at a tree node */
typedef struct dataNode {
    Record *record;
    struct dataNode *next;
} DataNode;

/* Patricia Tree node structure */
typedef struct treeNode {
    unsigned int prefixBits;       /* number of bits in the stem/prefix */
    char *prefix;                  /* bit array containing the stem */
    struct treeNode *branchA;      /* child branch for next bit = 0 */
    struct treeNode *branchB;      /* child branch for next bit = 1 */
    DataNode *data;                /* linked list of records matching this exact key */
} TreeNode;

/* --- Function Prototypes --- */

/* Part 1: Parallel Helper (Stage 2 prefix comparison) */
int compare_prefix_bits(char *prefix, unsigned int prefixBits,
                       char *key, unsigned int startBit,
                       unsigned int *mismatch_bit);

/* Part 2: Specialized Helpers (Stem creation, node allocation, edit distance) */
char *createStem(char *oldKey, unsigned int startBit, unsigned int numBits);
TreeNode *createTreeNode(char *prefix, unsigned int prefixBits);
void addRecordToNode(TreeNode *node, Record *record);
int min3(int a, int b, int c);
int editDistance(char *str1, char *str2, int n, int m);

/* Part 3: Core Tree Operations (Insert, search, and cleanup) */
TreeNode *tree_insert(TreeNode *root, Record *record);
void search_tree_and_output(TreeNode *root, char *target, FILE *out_file);
void free_tree(TreeNode *root);

#endif

