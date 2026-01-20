# Compiler
FC = gfortran

# Flags: -O3 for optimization, -Wall for warnings, -std=f2008 for standard compliance
FFLAGS = -O3 -Wall -Wextra -std=f2008

# Objects
OBJS = utility.o read_initFile.o problemSetup.o leapfrog.o output.o fput.o

# Executable name
EXEC = fput_sim

# Default target
all: $(EXEC)

# Link
$(EXEC): $(OBJS)
	$(FC) $(FFLAGS) -o $(EXEC) $(OBJS)

# Compile source files to object files
%.o: %.f90
	$(FC) $(FFLAGS) -c $<

# Module dependencies
read_initFile.o: utility.o
problemSetup.o: utility.o read_initFile.o
leapfrog.o: utility.o
output.o: utility.o
fput.o: problemSetup.o leapfrog.o output.o

# Clean up
clean:
	rm -f *.o *.mod $(EXEC)

# Create data directory if needed (optional helper)
setup_dir:
	mkdir -p data