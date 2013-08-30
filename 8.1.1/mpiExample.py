#!/usr/bin/python
# vim: set expandtab ts=4
from mpi4py import MPI
import numpy

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

data = (rank+1)**2
data = comm.gather(data, root=0)
if rank == 0:
   for i in range(size):
       assert data[i] == (i+1)**2
   print("rank="+str(rank))
   print(data)
else:
   assert data is None

