def check(k,a,b,c,x,y,z):
    assert(k >= 0)
    add_ok = (a+b+c+3*k) == (x+y+z)
    mul_ok = ((a+k)*(b+k)*(c+k)) == (x*y*z)
    print(x+y+z,x*y*z)
    assert(add_ok and mul_ok)

check(0, 7, 30, 54, 10, 18, 63)
check(1, 7, 30, 54, 10, 22, 62)
check(2, 7, 30, 54, 12, 21, 64)
check(3, 7, 30, 54, 15, 19, 66)
