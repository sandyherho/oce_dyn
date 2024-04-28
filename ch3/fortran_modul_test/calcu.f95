MODULE calcu
USE decla
CONTAINS
!+++++++++++++++++++++++++++++++++++++++++++
SUBROUTINE init
x = 2.0
y = 1.0
RETURN
END SUBROUTINE init
!+++++++++++++++++++++++++++++++++++++++++++
SUBROUTINE squaresum
real :: sum ! declaration of local variable
sum = x+y
z = sum * sum
RETURN
END SUBROUTINE squaresum
END MODULE calcu
