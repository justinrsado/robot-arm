armControl_arduino:
	Expects a byte string of the format "<theta1,theta2,theta3>" over serial, where theta1, theta2, and theta3 correspond to the base-Z, base-X, 	and elbow rotations, respectively
armControl_mouse:
	Serial transmission of motor angles is commented out for demo purposes
	run this for mouse-controlled IK environment
	control the end-effector by clicking and dragging your mouse
cv_sender:
	Calculates and sends movement values over localhost TCP socket
	run this at the same time and with the same port as armControl_cv 
armControl_cv:
	Serial transmission is commented out for demo purposes
	receives CV-obtained movement values asynchronously over localhost TCP socket, and uses them to control simulated inverse kinematics environment
	run this at the same time and with the same port as cv_sender for hand-controlled IK environment
	control the end-effector by holding left click on the PyGame window whilst moving your hand
	 
*Note: ending armControl_cv while the IK environment is open results in a crash
*Note: the PyGame process in armControl_cv takes a second to detach -- if you see an "Address in use" error, try changing ports