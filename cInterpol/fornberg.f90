module types
  implicit none
  private
  public dp, ivector, dvector

  integer, parameter :: dp=kind(0.d0)  ! double precision

  type ivector ! allocatable integer vector
     integer, pointer :: vec(:) => null()
  end type ivector

  type dvector ! allocatable real double precision vector
     real(dp), pointer :: vec(:) => null()
  end type dvector
  
end module


module fornberg
  use iso_c_binding, only: c_double, c_int
  use types, only: dp
  implicit none

contains

  subroutine apply_fd(nin, maxorder, xdata, ydata, xtgt, out) bind(c)
    integer(c_int), intent(in) :: nin, maxorder
    real(c_double), intent(in) :: xdata(0:nin-1), ydata(0:nin-1), xtgt
    real(c_double), intent(inout) :: out(0:maxorder)
    integer :: j,k
    real(dp), allocatable :: c(:,:)
    allocate(c(0:nin-1, 0:maxorder))
    do k=0,maxorder
      do j=0,nin-1
        c(j,k) = 0.0_dp
      end do
    end do
    call populate_weights(xtgt, xdata, nin-1, maxorder, c)
    do j=0,maxorder
      out(j) = sum(c(:, j)*ydata(:))
    end do
  end subroutine


  subroutine populate_weights (z, x, nd, m, c)
    ! 
    !  Input Parameters
    !    z            -  location where approximations are to be
    !                    accurate,
    !    x(0:nd)      -  grid point locations, found in x(0:n)
    !    nd           -  dimension of x- and c-arrays in calling
    !                    program x(0:nd) and c(0:nd,0:m), respectively,
    !    m            -  highest derivative for which weights are
    !                    sought,
    !
    !  Output Parameter
    !    c(0:nd,0:m)  -  weights at grid locations x(0:n) for
    !                    derivatives of order 0:m, found in c(0:n,0:m)
    !
    real(dp), intent(in) :: z
    integer, intent(in) :: nd, m
    real(dp), intent(in) :: x(0:nd)
    real(dp), intent(inout) :: c(0:nd, 0:m)
    
    real(dp) :: c1, c2, c3, c4, c5
    integer :: i, j, k, mn, n
    n = nd
    c1 = 1.0_dp
    c4 = x(0)-z
    c(0,0) = 1.0_dp
    do i=1,n
      mn = min(i,m)
      c2 = 1.0_dp
      c5 = c4
      c4 = x(i)-z
      do j=0,i-1
        c3 = x(i)-x(j)
        c2 = c2*c3
        if (j == i-1) then
          do k=mn,1,-1
            c(i,k) = c1*(k*c(i-1, k-1)-c5*c(i-1, k))/c2
          end do
          c(i,0) = -c1*c5*c(i-1,0)/c2
        endif
        do k=mn,1,-1
          c(j,k) = (c4*c(j,k)-k*c(j,k-1))/c3
        end do
        c(j,0) = c4*c(j,0)/c3
      end do
      c1 = c2
    end do
    return
  end subroutine
end module

module test_fornberg

  use types, only: dp
  use fornberg, only: populate_weights

  implicit none
  private
  public test_weights

contains

  subroutine test_weights()
    real(dp) :: z
    integer :: j, k, m, nd
    real(dp), allocatable :: c(:,:)
    real(dp), parameter :: x(0:2) = [-1.0_dp, 0.0_dp, 1.0_dp]
    nd = size(x)-1
    m = 2
    z = 0.0_dp
    allocate(c(0:nd, 0:m))
    do k=0,m
      do j=0,nd
        c(j,k) = 0.0_dp
      end do
    end do
    call populate_weights(z, x, nd, m, c)
    print *, c
  end subroutine

end module test_fornberg

program main
use test_fornberg, only: test_weights
call test_weights()
end program
