program fput
  use utility, only : fp
  use problemSetup
  use leapfrog
  use output

  implicit none

  real(fp), allocatable :: x_prev(:), x_curr(:), x_next(:)
  real(fp) :: t
  integer :: step_num, mid_node
  
  ! 1. Setup problem
  call setup_init()
  
  ! 2. Allocate memory (0 to N+1 for ghost nodes)
  allocate(x_prev(0:nMasses+1))
  allocate(x_curr(0:nMasses+1))
  allocate(x_next(0:nMasses+1))
  
  ! 3. Set Initial Conditions
  call set_ics(x_prev, x_curr)
  
  ! Determine middle node index
  mid_node = nMasses / 2
  if (mid_node == 0) mid_node = 1
  
  ! Write initial history (t=0 and t=dt)
  call write_history(outFile, 0.0_fp, x_prev(mid_node))
  call write_history(outFile, dt, x_curr(mid_node))
  
  t = dt
  
  ! 4. Time Stepping Loop
  ! We start computing x_next for step 2 up to nSteps
  do step_num = 1, nSteps - 1
     
     call step(x_next, x_curr, x_prev, K, alpha, dt, nMasses)
     
     ! Update time and shift arrays
     t = t + dt
     x_prev = x_curr
     x_curr = x_next
     
     ! Write History
     call write_history(outFile, t, x_curr(mid_node))
     
     ! Write Snapshots at T/4, T/2, 3T/4, and T
     ! Using step counts is more robust than comparing float times
     if (step_num + 1 == nSteps / 4) then
        call write_snapshot(outFile, x_curr, nMasses, 'T4')
     else if (step_num + 1 == nSteps / 2) then
        call write_snapshot(outFile, x_curr, nMasses, 'T2')
     else if (step_num + 1 == (3 * nSteps) / 4) then
        call write_snapshot(outFile, x_curr, nMasses, '3T4')
     else if (step_num + 1 == nSteps) then
        call write_snapshot(outFile, x_curr, nMasses, 'T')
     end if
     
  end do
  
  print *, "Simulation Complete. Output saved to ", trim(outFile)
  
  deallocate(x_prev, x_curr, x_next)

end program fput