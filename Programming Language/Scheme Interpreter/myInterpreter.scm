
(define (repl)     ;;; the read-eval-print loop.
  (display "--> ") 
  (let ((exp (read)))
    (cond ((equal? exp '(exit))      ; (exit) only allowed at top level
	   'done)
	  (else  (display (top-eval exp))
		 (newline)
		 (repl))
	  )))


(define (my-load filename)       ;; don't want to redefine the Scheme LOAD
  (load-repl (open-input-file filename)))


(define (load-repl port)
  (let ((exp (read port)))
    (cond ((eof-object? exp) 'done)
	  (else (let ((res (top-eval exp)))
		  (display res)
		  (load-repl port)))
	  )))


;; insert!, below, is a destructive update of a list L, inserting the
;; parameter val onto the front of L (so that L is actually modified).
;; insert! must only be used where absolutely necessary, e.g. when an
;; environment must be destructively updated to allow for recursion
;; (see the implementation of (define ...) below).

;; As their names imply, set-car! and set-cdr! destructively modify 
;; the car field and cdr field of a cons cell, respectively. They are
;; built-in functions (see *global-env* below).

(define (insert! val L)
  (set-cdr! L (cons (car L) (cdr L)))
  (set-car! L val)
  )


;; (define ....) is only allowed at the top level and affects only the 
;; global environment. Only the basic form of define is supported here.
 
(define (top-eval exp)
  (cond ((not (pair? exp)) (my-eval exp *global-env*))
        ((eq? (car exp) 'define)
              (cond ((pair? (cadr exp))
                    (insert! (list (car(cadr exp)) (my-eval (cons 'lambda (cons (cdr (cadr exp)) (cddr exp))) *global-env*)) *global-env*)
                    (car(cadr exp)))
                    (else (insert! (list (cadr exp) (my-eval (caddr exp) *global-env*)) *global-env*) (cadr exp))))
        (else (my-eval exp *global-env*))))

(define (lookup var env)
  (let ((item (assoc var env)))  ;; assoc returns #f if var not found in env
    (cond ((not item) (display "Error: Undefined Symbol ")
		      (display var) (newline))
	  (else (cadr item))
	  )))

(define (handle-if test then-exp else-exp env)
  (if (my-eval test env)
      (my-eval then-exp env)
      (my-eval else-exp env)))


;; still missing let, let*, letrec, the syntax for (define (f x) ...),
;; cond, begin (block).

(define (my-eval exp env)
  (cond
   ((symbol? exp) (lookup exp env))
   ((not (pair? exp)) exp)
   ((eq? (car exp) 'quote) (cadr exp))
   ((eq? (car exp) 'if)
    (handle-if (cadr exp) (caddr exp) (cadddr exp) env))
   ((eq? (car exp) 'lambda)
    (list 'closure exp env))
   ((eq? (car exp) 'let)
    (handle-let exp env))
   ((eq? (car exp) 'let*)
    (handle-let* exp env))
   ((eq? (car exp) 'cond)
    (handle-cond (cdr exp) env))
   ((eq? (car exp) 'begin)
    (handle-begin (cdr exp) env))
   ((eq? (car exp) 'letrec)
    (handle-letrec exp env))  ;; see explanation below
   (else
    (handle-call (map (lambda (sub-exp) (my-eval sub-exp env)) exp)))
   ))

(define (bind formals actuals)
  (cond ((null? formals) '())
	(else (cons (list (car formals) (car actuals))
		    (bind (cdr formals) (cdr actuals))))
	))

(define (handle-block block env)
  (cond ((null? block) (display "Error: Can't have empty block or body"))
	((null? (cdr block)) (my-eval (car block) env))
	(else (my-eval (car block) env)
	      (handle-block (cdr block) env))
	))
    

; Here's how handle-letrec should implement LETREC
; 0) The parameters are the defs,(e.g. ((f exp1) (g exp2)), and the body,
;    which is a list of expressions, e.g. ((display x) (f (g 1)))
; 1) create an association list binding the new names introducted by
;    the letrec to uninitialized values (e.g. the symbol '*uninitialized*).
;    For example, if the new names are x and y, then create 
;    ((x *uninitialized*) (y *uninitialized*))
; 2) create a new-env by appending the above association list to env.
; 3) eval the right hand side of each def using new-env
; 4) destructively modify new-env to replace the unitialized value for each
;    new name with its correspondinng value.
; 5) evaluate the body of the letrec using new-env

(define (handle-letrec exp env)
  (let ((bindings (cadr exp))  
        (body (cddr exp))) 
   (handle-block body (resolve-envrec bindings (append (create-local-envrec bindings env) env)))))

(define (create-local-envrec bindings env)
  (cond ((null? bindings) '())
		(else (cons (list (caar bindings) 'uninitialized) (create-local-envrec (cdr bindings) env)))))

(define (resolve-envrec bindings new-env)
  (cond ((null? bindings) new-env)
        (else (set-car! (cdr (assoc (caar bindings) new-env)) (my-eval (cadar bindings) new-env))
	           (resolve-envrec (cdr bindings) new-env))))

(define (handle-call evald-exps)
  (let ((fn (car evald-exps))
	(args (cdr evald-exps)))
   (cond
    ((eq? (car fn) 'closure)
     (let ((formals (cadr (cadr fn)))
	   (body (cddr (cadr fn)))
	   (env (caddr fn)))
       (handle-block body (append (bind formals args) env))))
    ((eq? (car fn) 'primitive-function)
     (apply (cadr fn) args))
    (else (display "Error: Calling non-function"))
    )))

;;--------------------------------------------------------------------

(define (handle-let exp env)
  (let ((bindings (cadr exp))
        (body (cddr exp)))
    (cond ((null? bindings) (handle-block body env))
          (else (handle-block body (append (handle-let-binding (append bindings '()) env '()) env))))))

(define (handle-let-binding exp env local)
  (cond ((null? exp) local)
        (else (handle-let-binding (cdr exp) env (cons (list (car (car exp)) (my-eval (car (cdr (car exp))) env)) local)))))

(define (handle-let* exp env)  
  (let ((bindings (cadr exp))
        (body (cddr exp))) 
    (cond ((null? bindings) (handle block body env))
          (else (handle-block body (handle-let*-binding bindings env))))))

(define (handle-let*-binding exp env)  
  ( cond ((null? exp) env)
         (else (handle-let*-binding (cdr exp) (cons (list (car (car exp)) (my-eval (car (cdr (car exp))) env)) env)))))

(define (handle-cond exp env)  
  ( let ((first-cond (car exp)))
     (if (eq? (car first-cond) 'else)
         (handle-block (cdr first-cond) env)
         (if (my-eval (car first-cond) env)
         (handle-block (cdr first-cond) env)
         (handle-cond (cdr exp) env)))))

(define (handle-begin block env)
 (cond ((null? block) (display "Error: Can't have empty block or body"))
	((null? (cdr block)) (my-eval (car block) env))
	(else (my-eval (car block) env)
	      (handle-begin (cdr block) env))))

(define (my-apply fn args)
  (cond ((eq? (car fn) 'primitive-function) (apply (cadr fn) args))
		(else (let ((formals (cadr (cadr fn)))
                       (body (cddr (cadr fn)))
			    (env (caddr fn)))	
			    (handle-block body (append (bind formals args) env))))))

;;-------------------- Here is the initial global environment --------

(define *global-env*
  (list (list 'car (list 'primitive-function car))
	(list 'cdr (list 'primitive-function cdr))
	(list 'set-car! (list 'primitive-function set-car!))
	(list 'set-cdr! (list 'primitive-function set-cdr!))
	(list 'cons (list 'primitive-function cons))
	(list 'list (list 'primitive-function list))
	(list '+ (list 'primitive-function +))
	(list '- (list 'primitive-function -))
	(list '* (list 'primitive-function *))
	(list '= (list 'primitive-function =))
	(list '< (list 'primitive-function <))
	(list '> (list 'primitive-function >))
	(list '<= (list 'primitive-function  <=))
	(list '>= (list 'primitive-function >=))
	(list 'eq? (list 'primitive-function eq?))
	(list 'pair? (list 'primitive-function pair?))
	(list 'symbol? (list 'primitive-function symbol?))
	(list 'null? (list 'primitive-function null?))
	(list 'read (list 'primitive-function read))
	(list 'display (list 'primitive-function  display))
	(list 'open-input-file (list 'primitive-function open-input-file))
	(list 'close-input-port (list 'primitive-function close-input-port))
	(list 'eof-object? (list 'primitive-function eof-object?))
	(list 'load (list 'primitive-function my-load))
   (list 'newline (list 'primitive-function newline))
   (list 'apply (list 'primitive-function my-apply));;defined above
	))

