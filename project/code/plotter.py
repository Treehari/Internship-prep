import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

print("--- FINAL PLOTTER RUNNING ---")
print(f"Current Directory: {os.getcwd()}")

# 1. SMART FILE LOADER
def load_data(base_name):
    # Check if file is in current folder
    if os.path.exists(base_name):
        full_path = base_name
    # Check if file is in data/ folder
    elif os.path.exists(os.path.join("data", base_name)):
        full_path = os.path.join("data", base_name)
    else:
        print(f"  [MISSING] {base_name}")
        return None

    try:
        data = np.loadtxt(full_path)
        if data.size == 0: return None
        if len(data.shape) == 1: 
            return np.array([data[0]]), np.array([data[1]])
        return data[:, 0], data[:, 1]
    except Exception as e:
        print(f"  [ERROR] {e}")
        return None

# 2. PLOT SAVER
def save_plot(filename):
    if os.path.exists("data"):
        out = os.path.join("data", filename)
    else:
        out = filename
    plt.savefig(out)
    print(f"  [SAVED] {out}")

# 3. QUESTION A PLOTTER
def plot_a(run_name, K, Tf):
    print("\nPlotting Question (a)...")
    res = load_data(f"{run_name}_history.dat")
    if res is None: return

    t_num, x_num = res
    omega = np.sqrt(2.0 * K) 
    t_exact = np.linspace(0, Tf, 1000)
    x_exact = (1.0/omega) * np.sin(omega * t_exact)
    
    plt.figure(figsize=(10, 6))
    plt.plot(t_exact, x_exact, 'k-', label='Exact')
    plt.plot(t_num, x_num, 'r--', label='Numerical')
    plt.title("Question (a): N=1 Comparison")
    plt.legend()
    plt.grid(True)
    save_plot("plot_a_comparison.png")
    plt.close()

# 4. QUESTION D PLOTTER (Stability)
def plot_d(run_name, title, out_name):
    print(f"\nPlotting Question (d): {title}...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle(title, fontsize=16)
    
    times = ['T4', 'T2', '3T4', 'T']
    found = False
    
    # Snapshots
    for tag in times:
        res = load_data(f"{run_name}_snap_{tag}.dat")
        if res is not None:
            ax1.plot(res[0], res[1], label=tag)
            found = True
    ax1.set_title("Snapshots")
    ax1.legend()
    ax1.grid(True)
    
    # History
    res_h = load_data(f"{run_name}_history.dat")
    if res_h is not None:
        ax2.plot(res_h[0], res_h[1], 'b-')
        found = True
    ax2.set_title("History")
    ax2.grid(True)
    
    if found:
        plt.tight_layout()
        save_plot(out_name)
    else:
        print(f"  [SKIPPED] No data for {out_name}")
    plt.close()

# 5. GRID PLOTTER (For B, C, E)
def plot_grid(files, title, out_name):
    print(f"\nPlotting {title}...")
    fig, axes = plt.subplots(3, 2, figsize=(12, 14))
    fig.suptitle(title, fontsize=16)
    
    resolutions = [8, 16, 32]
    times = ['T4', 'T2', '3T4', 'T']
    found_any = False
    
    for i, N in enumerate(resolutions):
        base = files[N]
        # Snapshots
        for tag in times:
            res = load_data(f"{base}_snap_{tag}.dat")
            if res is not None:
                axes[i, 0].plot(res[0], res[1], label=tag)
                found_any = True
        axes[i, 0].set_title(f"N={N} Snapshots")
        if i==0: axes[i, 0].legend(loc='upper right', fontsize='small')

        # History
        res_h = load_data(f"{base}_history.dat")
        if res_h is not None:
            axes[i, 1].plot(res_h[0], res_h[1], 'b-')
            found_any = True
        axes[i, 1].set_title(f"N={N} History")

    if found_any:
        plt.tight_layout(rect=[0, 0.03, 1, 0.93])
        save_plot(out_name)
    else:
        print(f"  [SKIPPED] No data found for {out_name}")
    plt.close()

if __name__ == "__main__":
    # Q(a)
    plot_a('fput_n-1_alpha-0.0_C1.0', 16.0, 10*np.pi)

    # Q(b)
    files_b = {8: "fput_n-8_alpha-0.0_C1.0", 16: "fput_n-16_alpha-0.0_C1.0", 32: "fput_n-32_alpha-0.0_C1.0"}
    plot_grid(files_b, "Question (b): Linear", "plot_b_linear.png")

    # Q(c)
    files_c = {8: "fput_n-8_alpha-0.8_C0.5", 16: "fput_n-16_alpha-1.6_C0.5", 32: "fput_n-32_alpha-3.2_C0.5"}
    plot_grid(files_c, "Question (c): Nonlinear", "plot_c_nonlinear.png")

    # Q(d) - Stability Check
    # This looks for the run you just finished (C=0.9)
    plot_d("fput_n-32_alpha-3.2_C0.9", "Question (d): Stability C=0.9", "plot_d_C0.9.png")

    # Q(e)
    files_e = {8: "fput_n-8_alpha-neg0.8_C0.5", 16: "fput_n-16_alpha-neg1.6_C0.5", 32: "fput_n-32_alpha-neg3.2_C0.5"}
    plot_grid(files_e, "Question (e): Negative Alpha", "plot_e_negative.png")
