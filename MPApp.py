import tkinter as tk
from tkinter import messagebox


class MemoryBlock:
    def __init__(self, id, size):
        self.id = id
        self.size = size
        self.is_free = True

    def __repr__(self):
        status = "Free" if self.is_free else "Allocated"
        return f"Block {self.id}: {self.size}KB ({status})"


class WorstFitMemoryAllocator:
    def __init__(self, memory_sizes):
        self.memory_blocks = [MemoryBlock(i, size) for i, size in enumerate(memory_sizes)]
        self.original_memory = [block.size for block in self.memory_blocks]

    def reset_memory(self):
        self.memory_blocks = [MemoryBlock(i, size) for i, size in enumerate(self.original_memory)]

    def allocate(self, process_size):
        largest_block = None
        for block in self.memory_blocks:
            if block.is_free and block.size >= process_size:
                if largest_block is None or block.size > largest_block.size:
                    largest_block = block

        if largest_block:
            largest_block.is_free = False
            allocated_size = largest_block.size
            leftover_size = largest_block.size - process_size
            largest_block.size = process_size

            if leftover_size > 0:
                self.memory_blocks.append(MemoryBlock(len(self.memory_blocks), leftover_size))
            return f"Allocated {process_size}KB to Block {largest_block.id} (Remaining: {leftover_size}KB)"
        else:
            return f"Cannot allocate {process_size}KB. Not enough memory."

    def get_memory_state(self):
        return [f"Block {block.id}: {block.size}KB - {'Free' if block.is_free else 'Allocated'}" for block in self.memory_blocks]


# GUI Class
class MemoryAllocatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Worst Fit Memory Allocator")
        self.root.configure(bg="#14919B")  # Set background color

        self.memory_allocator = None

        # Widgets for Initialization
        tk.Label(root, text="Memory Blocks:", bg="#14919B", fg="black", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10, pady=5)
        self.memory_input = tk.Entry(root, width=20, bg="white", fg="black", font=("Arial", 10))
        self.memory_input.grid(row=0, column=1, padx=10, pady=5)
        tk.Button(root, text="Initialize", command=self.initialize_memory, bg="#0B6477", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=10, pady=5)

        # Memory State
        self.memory_display = tk.Text(root, height=10, width=40, state="disabled", bg="white", fg="black", font=("Arial", 10))
        self.memory_display.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

        # Widgets for Process Allocation
        tk.Label(root, text="Process Size:", bg="#14919B", fg="black", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=10, pady=5)
        self.process_size_input = tk.Entry(root, width=10, bg="#F0F0F0", fg="black", font=("Arial", 10))
        self.process_size_input.grid(row=2, column=1, padx=10, pady=5)
        tk.Button(root, text="Allocate", command=self.allocate_memory, bg="#0B6477", fg="white", font=("Arial", 10, "bold")).grid(row=2, column=2, padx=10, pady=5)

        # Reset Button
        tk.Button(root, text="Reset", command=self.reset_memory, bg="#0B6477", fg="white", font=("Arial", 10, "bold")).grid(row=3, column=0, columnspan=3, pady=10)

    def initialize_memory(self):
        memory_input = self.memory_input.get()
        try:
            memory_sizes = [int(size) for size in memory_input.split(",") if size.strip().isdigit()]
            if not memory_sizes:
                raise ValueError
            self.memory_allocator = WorstFitMemoryAllocator(memory_sizes)
            self.update_memory_display()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid memory sizes (comma-separated integers).")

    def allocate_memory(self):
        if not self.memory_allocator:
            messagebox.showerror("Error", "Memory not initialized.")
            return

        try:
            process_size = int(self.process_size_input.get())
            if process_size <= 0:
                raise ValueError
            result = self.memory_allocator.allocate(process_size)
            messagebox.showinfo("Allocation Result", result)
            self.update_memory_display()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid process size.")

    def reset_memory(self):
        if self.memory_allocator:
            self.memory_allocator.reset_memory()
            self.update_memory_display()

    def update_memory_display(self):
        if self.memory_allocator:
            self.memory_display.config(state="normal")
            self.memory_display.delete("1.0", tk.END)
            memory_state = self.memory_allocator.get_memory_state()
            for state in memory_state:
                self.memory_display.insert(tk.END, state + "\n")
            self.memory_display.config(state="disabled")


# Main Function
if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryAllocatorGUI(root)
    root.mainloop()
