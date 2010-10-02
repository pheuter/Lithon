(define factorial (n) 
  (return 
    (reduce mult (xrange 1 (+ 1 n)))))

(print 
  (map factorial (xrange 1 11)))