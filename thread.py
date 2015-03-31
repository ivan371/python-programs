import threading
import os

def writer(fin_name, fout_name, n, k, event_for_wait, event_for_set):
	event_for_wait.wait()
	event_for_wait.clear()
	fd_in = os.open(fin_name, os.O_RDONLY)
	if fd_in == -1:
		print ("ERROR IN OPEN FIN")
		os._exit(-1)

	fd_out = os.open(fout_name, os.O_WRONLY)
	if fd_out == -1:
		print ("ERROR IN OPEN FOUT")
		os.close(fd_in)
		os._exit(-1)

	size = os.path.getsize(fin_name)
	os.lseek(fd_in, (size + 1) / n * k, 0)
	os.lseek(fd_out, (size + 1)/ n * k, 0)
	tmp = os.read(fd_in, (size + 1) / n + 1)
	if tmp == -1:
		print ("READ ERROR")
		os.close(fd_in)
		os.close(fd_out)
		os._exit(-1)

	os.write(fd_out, tmp)
	os.close(fd_in)
	os.close(fd_out)
	event_for_set.set()

print ("scan num of threads")
n = input()
print ("name_fin")
fin_name = input()
print ("name_fout")
fout_name = input()
e = []
t = []
for i in range (n):
	e.append(threading.Event())
for i in range (n - 1):
	t.append(threading.Thread(target=writer, args=(fin_name, fout_name, n, i, e[i], e[i + 1])))
t.append(threading.Thread(target = writer, args=(fin_name, fout_name, n, n - 1, e[n - 1], e[0])))
for i in range (n):
	t[i].start()
e[0].set()
for i in range (n):
	t[i].join()
