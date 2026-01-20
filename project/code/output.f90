module output
  use utility, only : fp
  implicit none
  private
  public :: write_history, write_snapshot

contains

  ! Appends time and position of the middle mass to a history file
  subroutine write_history(base_name, t, x_val)
    character(len=*), intent(in) :: base_name
    real(fp), intent(in) :: t, x_val
    integer :: u
    
    u = 20
    open(unit=u, file=trim(base_name)//'_history.dat', &
         position='append', status='unknown', action='write')
    write(u, *) t, x_val
    close(u)
  end subroutine write_history

  ! Writes the full state of the system to a snapshot file
  subroutine write_snapshot(base_name, x, N, tag)
    ! Declare N first because it is used in the dimension of x
    integer, intent(in) :: N
    
    ! Now declare the other arguments
    character(len=*), intent(in) :: base_name, tag
    real(fp), intent(in) :: x(0:N+1)
    
    integer :: u, i
    
    u = 21
    open(unit=u, file=trim(base_name)//'_snap_'//trim(tag)//'.dat', &
         status='replace', action='write')
    do i = 1, N
       write(u, *) i, x(i)
    end do
    close(u)
  end subroutine write_snapshot

end module output