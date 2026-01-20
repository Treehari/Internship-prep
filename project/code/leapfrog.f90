module leapfrog
  use utility, only : fp
  implicit none
  private
  public :: step

contains

  subroutine step(x_next, x_curr, x_prev, K, alpha, dt, N)
    ! Declare N first because it is used in the dimensions of the arrays below
    integer, intent(in)   :: N
    
    ! Now we can use N in the array dimensions
    real(fp), intent(out) :: x_next(0:N+1)
    real(fp), intent(in)  :: x_curr(0:N+1), x_prev(0:N+1)
    
    ! Declare other inputs
    real(fp), intent(in)  :: K, alpha, dt
    
    integer :: i
    real(fp) :: linear_term, nonlinear_term
    
    ! Boundary conditions: Dummy masses remain at 0
    x_next(0) = 0.0_fp
    x_next(N+1) = 0.0_fp
    
    ! Loop over internal masses
    do i = 1, N
       ! Term: (x_{i+1} - 2x_i + x_{i-1})
       linear_term = x_curr(i+1) - 2.0_fp*x_curr(i) + x_curr(i-1)
       
       ! Term: (1 + alpha * (x_{i+1} - x_{i-1}))
       nonlinear_term = 1.0_fp + alpha * (x_curr(i+1) - x_curr(i-1))
       
       ! Leapfrog update: x^{n+1} = 2x^n - x^{n-1} + K * dt^2 * Force
       x_next(i) = 2.0_fp*x_curr(i) - x_prev(i) + &
                   (K * dt**2 * linear_term * nonlinear_term)
    end do

  end subroutine step

end module leapfrog