convolution *must* be an operation. but what is it an operation of?

say it was a FunctionNode in a DAG. what would its input and output be?
its input might be a vector, or if there were unsubstituted variables, it might also be an analytic function

if its an analytic function, thats easy to handle. its just continuous convolution
but theres no easy way to acquire a vector from - i dont think theres any easy way to acquire a vector for convolution input *in the middle of an expression tree*

would the DAG have to implement vectors? so far, all the number sets have been scalar
