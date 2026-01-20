module problemSetup

  use utility, only : fp, maxFileLen, maxStrLen, pi
  use read_initFile
  
  implicit none
  private

  integer, public :: nMasses, nSteps
  real (fp), public :: K, alpha, tFinal, dt, C
  character(len=maxStrLen), public :: runName, outFile
  character(len=maxStrLen) :: inFile

  public :: setup_init
  public :: set_ics

contains

  subroutine setup_init()
    implicit none

    ! Get name of input file from command line argument
    call get_command_argument(1,inFile)
    if (len_trim(inFile) == 0) then
       print *, "Error: Please provide an input file (e.g., ./fput_sim simulation.init)"
       stop
    end if
    print *, "Reading from ",inFile
    
    ! Fill in default values
    nMasses = 1
    tFinal = 10.0_fp * pi
    K = 1.0_fp
    alpha = 0.0_fp
    C = 1.0_fp
    
    ! Read problem settings from the input file
    nMasses = read_initFileInt(infile, 'num_masses')
    alpha = read_initFileReal(infile, 'alpha')
    C = read_initFileReal(infile, 'C')

    ! ====================== Calculate K, nSteps, and dt here ===============================
    ! K = 4(N+1)^2
    K = 4.0_fp * real((nMasses + 1)**2, fp)

    ! M = ceil(Tf * sqrt(K) / C)
    nSteps = ceiling((tFinal * sqrt(K)) / C)

    ! dt = Tf / M
    dt = tFinal / real(nSteps, fp)

    print *, "Calculated Parameters:"
    print *, "  K:      ", K
    print *, "  nSteps: ", nSteps
    print *, "  dt:     ", dt
    
    ! Set the name of the run and echo it out
    runName = read_initFileChar(infile, 'run_name')
    print *, 'Running problem: ', runName
    
    ! Set the output file, note that // does string concatenation
    outFile = 'data/' // trim(runName)
  end subroutine setup_init

  ! ============================= Add set_ics subroutine here ===============================
  subroutine set_ics(x_prev, x_curr)
    real(fp), intent(out) :: x_prev(0:nMasses+1)
    real(fp), intent(out) :: x_curr(0:nMasses+1)
    integer :: i
    real(fp) :: v_0
    
    ! Initialize all to zero (includes dummy masses at 0 and N+1)
    x_prev = 0.0_fp
    x_curr = 0.0_fp
    
    ! Set initial conditions for physical masses 1 to N
    do i = 1, nMasses
        ! x^0 = 0 for all i
        x_prev(i) = 0.0_fp
        
        ! v^0 = sin(i * pi / (N+1))
        v_0 = sin((real(i, fp) * pi) / real(nMasses + 1, fp))
        
        ! Kick-start: x^1 = x^0 + dt * v^0 (Linear extrapolation)
        x_curr(i) = x_prev(i) + dt * v_0
    end do
    
  end subroutine set_ics

end module problemSetup