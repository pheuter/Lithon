(define (factorial_rec n)
  (if (= n 0)
      1
      (* n (factorial_rec (- n 1)))))
      
(define (factorial_iter n)
  (reduce (lambda (x y) (* x y)) (xrange 1 (+ 1 n))))
  
(map factorial_rec (xrange 1 11))
(map factorial_iter (xrange 11 16))