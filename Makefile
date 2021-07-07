step:
	echo ""; python3 tema1.py < step.in > step.out

accept:
	echo ""; python3 tema1.py < accept.in > accept.out

k_accept:
	echo ""; python3 tema1.py < k_accept.in > k_accept.out
	
list_step:	 
	echo ""; cat step.out; echo ""

list_accept:	 
	echo ""; cat accept.out; echo ""

list_k_accept:	 
	echo ""; cat k_accept.out; echo ""

verify_step:
	diff step.ref step.out > /dev/null

verify_accept:
	diff accept.ref accept.out > /dev/null

verify_k_accept:
	diff k_accept.ref k_accept.out > /dev/null

clean:
	rm step.out accept.out k_accept.out