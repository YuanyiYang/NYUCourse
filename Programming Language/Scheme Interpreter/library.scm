(define (cadr L)
  (car (cdr L)))

(define (cddr L)
  (cdr (cdr L)))
 
(define (cdddr L)
  (cdr (cdr (cdr L))))

(define (caddr L)
  (car (cdr (cdr L))))

(define (cadddr L)
  (car (cdr (cdr (cdr L)))))

(define (caar L)
  (car (car L)))

(define (cadar L)
  (car (cdr (car L))))

(define (and x y)
	(if x y #f))

(define (or x y)
  (if x #t y))

(define (equal? x y)
  (cond ((and (not (pair? x)) (not (pair? y))) (eq? x y))
        ((and (null? x) (null? y)) #t)
        (else (if (and (pair? x) (pair? y))
                  (and (equal? (car x) (car y)) (equal? (cdr x) (cdr y)))
                  #f))))

(define (not x)
	(if x #f #t))

(define (append L1 L2)
	(cond ((null? L1) L2)   
          (else (cons (car L1) (append (cdr L1) L2)))))

(define (map fun L)
  (if (null? L)
      '()
      (cons (fun (car L)) (map fun (cdr L)))))

(define (assoc var L)
  (if (null? L)
      #f
      (if (equal? var (car (car L)))
          (car L)
          (assoc var (cdr L)))))
