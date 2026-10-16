import matplotlib.pyplot as plt
import numpy as np

# Set clean aesthetic style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

N = [1, 2, 23, 1353]
labels = ['N=1', 'N=2', 'N=23', 'N=1353']

# Data from benchmark
dict1_nodes = [1.0, 2.0, 23.0, 1353.0]
dict2_nodes = [1.0, 2.0, 2.7, 17.4]

dict1_bits = [648.0, 884.0, 4176.0, 116489.8]
dict2_bits = [648.0, 612.0, 576.0, 525.9]

dict1_time = [93.9, 32.4, 45.5, 1001.8]
dict2_time = [79.9, 35.2, 24.6, 77.96]

# Figure 1: Node Comparisons
fig, ax = plt.subplots(figsize=(7, 4.5), dpi=300)
ax.plot(N, dict1_nodes, marker='o', color='#e74c3c', linewidth=2, label='Stage 1 (Linked List) - O(N)')
ax.plot(N, dict2_nodes, marker='s', color='#2980b9', linewidth=2, label='Stage 2 (Patricia Tree) - O(K)')
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Dataset Size N (Log Scale)', fontsize=11, fontweight='bold')
ax.set_ylabel('Average Nodes Visited (Log Scale)', fontsize=11, fontweight='bold')
ax.set_title('Figure 1: Node Comparisons vs Dataset Size', fontsize=12, fontweight='bold', pad=12)
ax.legend(frameon=True, facecolor='white', framealpha=0.9, fontsize=10)
plt.tight_layout()
plt.savefig('plot1_nodes.png')
plt.close()

# Figure 2: Bit Comparisons
fig, ax = plt.subplots(figsize=(7, 4.5), dpi=300)
ax.plot(N, dict1_bits, marker='o', color='#e74c3c', linewidth=2, label='Stage 1 (Linked List) - O(N * B)')
ax.plot(N, dict2_bits, marker='s', color='#2980b9', linewidth=2, label='Stage 2 (Patricia Tree) - O(K)')
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Dataset Size N (Log Scale)', fontsize=11, fontweight='bold')
ax.set_ylabel('Average Bit Comparisons (Log Scale)', fontsize=11, fontweight='bold')
ax.set_title('Figure 2: Bit Comparisons vs Dataset Size', fontsize=12, fontweight='bold', pad=12)
ax.legend(frameon=True, facecolor='white', framealpha=0.9, fontsize=10)
plt.tight_layout()
plt.savefig('plot2_bits.png')
plt.close()

# Figure 3: Execution Time
fig, ax = plt.subplots(figsize=(7, 4.5), dpi=300)
ax.plot(N, dict1_time, marker='o', color='#e74c3c', linewidth=2, label='Stage 1 (Linked List)')
ax.plot(N, dict2_time, marker='s', color='#27ae60', linewidth=2, label='Stage 2 (Patricia Tree)')
ax.set_xscale('log')
ax.set_xlabel('Dataset Size N (Log Scale)', fontsize=11, fontweight='bold')
ax.set_ylabel('Execution Time (ms)', fontsize=11, fontweight='bold')
ax.set_title('Figure 3: Total Execution Time vs Dataset Size (588 Queries)', fontsize=12, fontweight='bold', pad=12)
ax.legend(frameon=True, facecolor='white', framealpha=0.9, fontsize=10)
plt.tight_layout()
plt.savefig('plot3_time.png')
plt.close()

print("All 3 plots successfully generated!")

