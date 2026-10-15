# -*- coding: utf-8 -*-
import os
import urllib.request

base_raw = "https://raw.githubusercontent.com/krahets/hello-algo/main/en/docs/"

assets = {
    # 01 Linked Lists & Memory
    "01_linked_list_definition.png": "chapter_array_and_linkedlist/linked_list.assets/linked_list_definition.png",
    
    # 03 Trees & AVL
    "03_avl_rotation_cases.png": "chapter_tree/avl_tree.assets/avltree_rotation_cases.png",
    "03_avl_right_rotate.png": "chapter_tree/avl_tree.assets/avltree_right_rotate_with_grandchild.png",
    "03_bst_remove_successor.png": "chapter_tree/binary_search_tree.assets/bst_remove_case3_step2.png",
    
    # 04 Heaps & Priority Queues
    "04_binary_heap_representation.png": "chapter_heap/heap.assets/representation_of_heap.png",
    "04_heap_push_upheap.png": "chapter_heap/heap.assets/heap_push_step6.png",
    "04_heap_pop_downheap.png": "chapter_heap/heap.assets/heap_pop_step6.png",
    
    # 05 Hash Tables
    "05_hash_table_chaining.png": "chapter_hashing/hash_collision.assets/hash_table_chaining.png",
    "05_hash_table_linear_probing.png": "chapter_hashing/hash_collision.assets/hash_table_linear_probing.png",
    
    # 06 Sorting
    "06_quicksort_partition.png": "chapter_sorting/quick_sort.assets/pivot_division_step5.png",
    "06_mergesort_overview.png": "chapter_sorting/merge_sort.assets/merge_sort_overview.png",
    
    # 07 Graphs
    "07_graph_adjacency_list.png": "chapter_graph/graph.assets/adjacency_list.png",
    "07_graph_bfs_traversal.png": "chapter_graph/graph_traversal.assets/graph_bfs.png",
    "07_graph_dfs_traversal.png": "chapter_graph/graph_traversal.assets/graph_dfs.png",
}

target_dir = os.path.abspath("assets/images")
os.makedirs(target_dir, exist_ok=True)

print(f"Downloading {len(assets)} authentic visual assets to {target_dir}...")

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

for filename, rel_path in assets.items():
    dest_path = os.path.join(target_dir, filename)
    url = base_raw + rel_path
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read()
            with open(dest_path, "wb") as f:
                f.write(content)
        size_kb = len(content) / 1024
        print(f"  [OK] {filename} ({size_kb:.1f} KB)")
    except Exception as e:
        print(f"  [FAIL] {filename}: {e}")

print("Batch download complete!")
