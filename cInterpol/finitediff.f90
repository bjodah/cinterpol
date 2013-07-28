module fornberg
  use iso_c_binding, only c_double, c_int
  implicit none

contains

  subroutine weights (z,x,n,nd,m,c)
    ! 
    !  Input Parameters
    !    z            -  location where approximations are to be accurate,
    !    x(0:nd)      -  grid point locations, found in x(0:n)
    !    n            -  one less than total number of grid points; n must
    !                    not exceed the parameter nd below,
    !    nd           -  dimension of x- and c-arrays in calling program
    !                    x(0:nd) and c(0:nd,0:m), respectively,
    !    m            -  highest derivative for which weights are sought,
    !
    !  Output Parameter
    !    c(0:nd,0:m)  -  weights at grid locations x(0:n) for derivatives
    !                    of order 0:m, found in c(0:n,0:m)
    !
    real(c_double), intent(in) :: z
    
    implicit real*8 (a-h,o-z)
    dimension x(0:nd),c(0:nd,0:m)
    c1 = 1.0d0
    c4 = x(0)-z
    do 10 k=0,m
       do 10 j=0,n
10        c(j,k) = 0.0d0
          c(0,0) = 1.0d0
          do 50 i=1,n
             mn = min(i,m)
             c2 = 1.0d0
             c5=c4
             c4 = x(i)-z
             do 40 j=0,i-1
                c3 = x(i)-x(j)
                c2 = c2*c3
                if (j.eq.i-1) then
                   do 20 k=mn,1,-1
20                    c(i,k) = c1*(k*c(i-1,k-1)-c5*c(i-1,k))/c2
                      c(i,0) = -c1*c5*c(i-1,0)/c2
                   endif
                   do 30 k=mn,1,-1
30                    c(j,k) = (c4*c(j,k)-k*c(j,k-1))/c3
40                    c(j,0) = c4*c(j,0)/c3
50                    c1 = c2
                      return
                   end do
end module
